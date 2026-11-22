import { Injectable, NgZone, PLATFORM_ID, inject } from '@angular/core';
import { DOCUMENT, isPlatformBrowser } from '@angular/common';
import type { MotionProps, UiProps } from './halvo-api';

/** The shape of `window.Halvo`, defined by `@halvo/design-system/dist/halvo.js`. */
export interface HalvoGlobal {
  motion: MotionProps;
  ui: UiProps;
  version: string;
}

export type HalvoTheme = 'dark' | 'light';

/**
 * Typed, SSR-safe access to `window.Halvo`.
 * Load `node_modules/@halvo/design-system/dist/halvo.js` through `"scripts"` in angular.json.
 */
@Injectable({ providedIn: 'root' })
export class HalvoService {
  private readonly zone = inject(NgZone);
  private readonly document = inject(DOCUMENT);
  /** False during server-side rendering: every Halvo call is skipped there. */
  readonly isBrowser = isPlatformBrowser(inject(PLATFORM_ID));
  private warned = false;

  /** `window.Halvo`, or null on the server or when halvo.js is not loaded. */
  get halvo(): HalvoGlobal | null {
    if (!this.isBrowser) return null;
    const h = (globalThis as unknown as { Halvo?: HalvoGlobal }).Halvo ?? null;
    if (!h && !this.warned) {
      this.warned = true;
      console.warn('[halvo] window.Halvo is missing. Add "node_modules/@halvo/design-system/dist/halvo.js" to "scripts" in angular.json.');
    }
    return h;
  }

  get motion(): MotionProps | null {
    return this.halvo?.motion ?? null;
  }

  get ui(): UiProps | null {
    return this.halvo?.ui ?? null;
  }

  /** The design-system version the page is running, e.g. "1.1.0". */
  get version(): string | null {
    return this.halvo?.version ?? null;
  }

  /**
   * Runs Halvo work outside Angular's zone, so animation frames don't trigger change detection.
   * Returns undefined on the server or when halvo.js is missing.
   */
  run<T>(fn: (halvo: HalvoGlobal) => T): T | undefined {
    const h = this.halvo;
    return h ? this.zone.runOutsideAngular(() => fn(h)) : undefined;
  }

  /** The current theme, read from `<html data-theme>`. */
  get theme(): HalvoTheme {
    return this.document.documentElement.dataset['theme'] === 'light' ? 'light' : 'dark';
  }

  /** Switches theme with Halvo's circle wipe from `from` (e.g. the theme button). */
  setTheme(theme: HalvoTheme, from?: Element | null): Promise<void> {
    const apply = () => {
      this.document.documentElement.dataset['theme'] = theme;
    };
    const p = this.run((h) => h.motion.themeSwap(from ?? null, apply));
    if (p) return p;
    apply();
    return Promise.resolve();
  }

  toggleTheme(from?: Element | null): Promise<void> {
    return this.setTheme(this.theme === 'dark' ? 'light' : 'dark', from);
  }
}
