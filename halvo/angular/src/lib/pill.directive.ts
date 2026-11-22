import { AfterViewInit, Directive, ElementRef, Input, OnDestroy, inject } from '@angular/core';
import { HalvoService } from './halvo.service';

const INDICATORS = '.tabs__line, .seg__thumb, .tabbar__pill, .snav__pill';
const RADII: Record<string, number> = { tabs__line: 12, seg__thumb: 10, tabbar__pill: 18, snav__pill: 14 };
const ACTIVE = '[aria-current="page"], [aria-current="true"], [aria-pressed="true"], [aria-selected="true"]';

/**
 * Slides Halvo's selection pill (tabs, segmented control, side nav, tab bar) to the active item.
 * Put it on the container that holds the indicator; mark the active item with aria-current /
 * aria-pressed / aria-selected (routerLinkActive: `ariaCurrentWhenActive="page"`).
 *
 *   <nav class="tabs" halvoPill>
 *     <span class="tabs__line"></span>
 *     <a routerLink="living" routerLinkActive ariaCurrentWhenActive="page">Living room</a>
 *   </nav>
 */
@Directive({
  selector: '[halvoPill]',
  standalone: true,
  exportAs: 'halvoPill',
})
export class HalvoPillDirective implements AfterViewInit, OnDestroy {
  /** Optional CSS selector for the active item (defaults to the aria-current/pressed/selected item). */
  @Input() halvoPill: string | '' = '';
  /** Optional CSS selector for the indicator (defaults to the Halvo indicator classes). */
  @Input() pillIndicator?: string;
  /** Corner radius in px (defaults per component: tabs 12, segmented 10, tab bar 18, side nav 14). */
  @Input() pillRadius?: number;

  private readonly el = inject<ElementRef<HTMLElement>>(ElementRef);
  private readonly halvo = inject(HalvoService);
  private observer?: MutationObserver;
  private indicator: HTMLElement | null = null;
  private frame = 0;

  ngAfterViewInit(): void {
    this.halvo.run(() => {
      const host = this.el.nativeElement;
      this.indicator = host.querySelector<HTMLElement>(this.pillIndicator || INDICATORS);
      if (!this.indicator) {
        console.warn('[halvo] halvoPill: no indicator element (.tabs__line, .seg__thumb, .tabbar__pill or .snav__pill) inside', host);
        return;
      }
      this.frame = requestAnimationFrame(() => this.move(false));
      this.observer = new MutationObserver(() => this.move(true));
      this.observer.observe(host, {
        subtree: true,
        childList: true,
        attributes: true,
        attributeFilter: ['aria-current', 'aria-pressed', 'aria-selected'],
      });
    });
  }

  /** Re-measures and moves the pill (e.g. after the container was hidden). */
  update(animate = true): void {
    this.halvo.run(() => this.move(animate));
  }

  private move(animate: boolean): void {
    const ind = this.indicator;
    const motion = this.halvo.motion;
    if (!ind || !motion) return;
    const target = Array.from(this.el.nativeElement.querySelectorAll<HTMLElement>(this.halvoPill || ACTIVE)).find((n) => n !== ind) ?? null;
    if (!target) {
      ind.style.opacity = '0';
      return;
    }
    const cls = Object.keys(RADII).find((c) => ind.classList.contains(c));
    void motion.pill(ind, target, { radius: this.pillRadius ?? (cls ? RADII[cls] : 13), animate });
  }

  ngOnDestroy(): void {
    cancelAnimationFrame(this.frame);
    this.observer?.disconnect();
    const ro = (this.indicator as (HTMLElement & { __ro?: ResizeObserver }) | null)?.__ro;
    ro?.disconnect();
  }
}
