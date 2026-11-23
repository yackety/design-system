import { Directive, ElementRef, EnvironmentInjector, Injectable, Input, OnDestroy, OnInit, afterNextRender, inject } from '@angular/core';
import { CanDeactivateFn, NavigationCancel, NavigationEnd, NavigationError, NavigationStart, Route, Router, Routes } from '@angular/router';
import { Subscription } from 'rxjs';
import { HalvoService } from '@halvo/angular';

/** Links whose order defines "forward" and "back" between pages. */
const NAV_LINKS = '.snav a[href], .tabbar a[href], .side a[href], nav a[href]';
/** Longest a page may wait for its exit animation before the navigation goes on anyway. */
const MAX_WAIT_MS = 400;

/**
 * Runs Halvo's page swap between routes: the old page's cards sink and the page slides out,
 * then the new page slides in from the side it comes from and its cards rise.
 * Set up with `HalvoRouteTransitionDirective` on the element around `<router-outlet>`, and
 * `withHalvoTransitions(routes)` in `provideRouter` for the exit half.
 */
@Injectable({ providedIn: 'root' })
export class HalvoRouteTransitions {
  private readonly halvo = inject(HalvoService);
  private readonly router = inject(Router);
  private readonly injector = inject(EnvironmentInjector);
  private container: HTMLElement | null = null;
  private depth = 1;
  private cards = true;
  private sub?: Subscription;
  private direction: 1 | -1 = 1;
  private from = '';
  private leaving: { url: string; done: Promise<boolean> } | null = null;

  /** Called by the directive. */
  attach(el: HTMLElement, depth: number, cards: boolean): void {
    this.container = el;
    this.depth = Math.max(1, depth);
    this.cards = cards;
    if (this.sub || !this.halvo.isBrowser) return;
    this.sub = this.router.events.subscribe((e) => {
      if (e instanceof NavigationStart) {
        this.from = this.router.url;
        this.direction = this.dirBetween(this.from, e.url, e.navigationTrigger === 'popstate');
      } else if (e instanceof NavigationEnd) {
        const changed = this.key(this.from) !== this.key(e.urlAfterRedirects);
        const left = this.leaving !== null;
        this.leaving = null;
        if (changed || left) this.enterAfterRender();
      } else if (e instanceof NavigationCancel || e instanceof NavigationError) {
        if (this.leaving && this.container) {
          const c = this.container;
          this.halvo.run((h) => h.motion.pageReset(c));
        }
        this.leaving = null;
      }
    });
  }

  /** Called by the directive. */
  detach(el: HTMLElement): void {
    if (this.container === el) this.container = null;
  }

  /**
   * Plays the exit animation when the page (the first `transitionDepth` URL segments) changes.
   * Used by `halvoLeaveGuard`; resolves true when it's done (at most 400ms).
   */
  leave(fromUrl: string, toUrl: string): Promise<boolean> | boolean {
    const c = this.container;
    if (!c || !this.halvo.motion || this.key(fromUrl) === this.key(toUrl)) return true;
    if (this.leaving?.url === toUrl) return this.leaving.done;
    const dir = this.direction;
    const run = this.halvo.run((h) => h.motion.pageOut(c, { direction: dir })) ?? Promise.resolve();
    const done = Promise.race([run, new Promise<void>((r) => setTimeout(r, MAX_WAIT_MS))]).then(() => true);
    this.leaving = { url: toUrl, done };
    return done;
  }

  private enterAfterRender(): void {
    const c = this.container;
    if (!c) return;
    const dir = this.direction;
    const cards = this.cards;
    afterNextRender(() => this.halvo.run((h) => h.motion.pageIn(c, { direction: dir, cards })), { injector: this.injector });
  }

  /** The page a URL belongs to: its first `depth` path segments. */
  private key(url: string): string {
    return url.split(/[?#(]/)[0].split('/').filter(Boolean).slice(0, this.depth).join('/');
  }

  private dirBetween(from: string, to: string, popstate: boolean): 1 | -1 {
    const keys: string[] = [];
    document.querySelectorAll<HTMLAnchorElement>(NAV_LINKS).forEach((a) => {
      const k = this.key(new URL(a.href, document.baseURI).pathname.replace(new URL(document.baseURI).pathname, '/'));
      if (!keys.includes(k)) keys.push(k);
    });
    const a = keys.indexOf(this.key(from));
    const b = keys.indexOf(this.key(to));
    if (a > -1 && b > -1 && a !== b) return b > a ? 1 : -1;
    return popstate ? -1 : 1;
  }
}

/**
 * Marks the element that holds `<router-outlet>` as the page container for Halvo's page swap.
 * The new page always slides in and its cards rise; add `withHalvoTransitions(routes)` for the exit half.
 *
 *   <main halvoRouteTransition><router-outlet /></main>
 */
@Directive({
  selector: '[halvoRouteTransition]',
  standalone: true,
})
export class HalvoRouteTransitionDirective implements OnInit, OnDestroy {
  /** How many URL segments name a page (default 1: /rooms/living → /rooms/kitchen is not a page change). */
  @Input() transitionDepth = 1;
  /** Let the transition rise the new page's cards (set false if pages run halvoMotion themselves). */
  @Input() transitionCards = true;

  private readonly el = inject<ElementRef<HTMLElement>>(ElementRef);
  private readonly transitions = inject(HalvoRouteTransitions);

  ngOnInit(): void {
    this.transitions.attach(this.el.nativeElement, this.transitionDepth, this.transitionCards);
  }

  ngOnDestroy(): void {
    this.transitions.detach(this.el.nativeElement);
  }
}

/** Holds a route's page on screen while Halvo plays its exit animation (≤ 400ms). */
export const halvoLeaveGuard: CanDeactivateFn<unknown> = (_component, _route, current, next) =>
  inject(HalvoRouteTransitions).leave(current.url, next.url);

/**
 * Adds `halvoLeaveGuard` to every route that renders a component, recursively.
 *
 *   provideRouter(withHalvoTransitions(routes))
 *
 * Wrap lazily loaded child route arrays (`loadChildren`) the same way.
 */
export function withHalvoTransitions(routes: Routes): Routes {
  return routes.map((r) => {
    const out: Route = { ...r };
    if (r.component || r.loadComponent) out.canDeactivate = [...(r.canDeactivate ?? []), halvoLeaveGuard];
    if (r.children) out.children = withHalvoTransitions(r.children);
    return out;
  });
}
