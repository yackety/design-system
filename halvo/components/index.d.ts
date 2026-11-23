// Halvo — window.Halvo. Components are CSS classes (see each component's README);
// the bundle adds the motion kit. Every function resolves when the motion ends and
// jumps to the end state under prefers-reduced-motion.

type Targets = Element | ArrayLike<Element> | string | null | undefined;
type EaseName =
  | 'none' | 'power1.in' | 'power1.out' | 'power2.in' | 'power2.out' | 'power2.inOut'
  | 'power3.in' | 'power3.out' | 'power3.inOut' | 'power4.out' | 'expo.out' | `back.out(${number})`;

interface TweenProps {
  x?: number; y?: number; xPercent?: number; yPercent?: number; rotation?: number;
  scale?: number; scaleX?: number; scaleY?: number; opacity?: number;
  clipPath?: string; strokeDashoffset?: number; color?: string; filter?: string;
}
interface TweenOptions {
  duration?: number; delay?: number; ease?: EaseName;
  stagger?: number | { amount: number };
  /** keep the end state (for exits); otherwise the element returns to its CSS state */
  keep?: boolean; origin?: string;
}

export interface MotionProps {
  /** CSS easing string for a GSAP ease name (back.out(n) → linear()) */
  ease(name: EaseName): string;
  fromTo(targets: Targets, from: TweenProps | ((i: number, el: Element) => TweenProps), to: TweenProps | null, opts?: TweenOptions): Promise<void>;
  tweenValue(from: number, to: number, opts: { duration: number; delay?: number; ease?: EaseName }, onUpdate: (v: number) => void): Promise<void>;

  splitText(el: Element, opts?: { delay?: number }): Promise<void>;
  rise(els: Targets, opts?: { y?: number; stagger?: number; delay?: number }): Promise<void>;
  slide(els: Targets, opts?: { x?: number; y?: number; stagger?: number; delay?: number }): Promise<void>;
  deal(els: Targets, opts?: { stagger?: number; delay?: number }): Promise<void>;
  grow(els: Targets, opts?: { axis?: 'x' | 'y'; duration?: number; stagger?: number; delay?: number }): Promise<void>;
  draw(paths: Targets, opts?: { duration?: number; delay?: number }): Promise<void>;
  pop(els: Targets, opts?: { from?: number; stagger?: number; delay?: number }): Promise<void>;
  flash(el: Element): Promise<void>;
  countTo(el: Element, to: number, format?: (v: number) => string, opts?: { from?: number; duration?: number; delay?: number }): Promise<void>;
  nudge(el: Element): Promise<void>;
  shake(el: Element): Promise<void>;
  ring(bell: Element, badge?: Element): Promise<void>;
  roll(el: Element, up: boolean): Promise<void>;
  switchKnob(switchEl: Element): Promise<void>;
  fill(el: HTMLElement, value: number, opts?: { duration?: number; delay?: number; ease?: EaseName }): Promise<void>;
  magnetic(root?: ParentNode): void;
  lift(root?: ParentNode, y?: number): void;
  pill(indicator: HTMLElement, target: HTMLElement, opts?: { radius?: number; animate?: boolean }): Promise<void> | void;

  scrimIn(el: Element): Promise<void>; scrimOut(el: Element): Promise<void>;
  modalIn(el: Element, origin?: string): Promise<void>; modalOut(el: Element): Promise<void>;
  drawerIn(el: Element): Promise<void>; drawerOut(el: Element): Promise<void>;
  sheetIn(el: Element): Promise<void>; sheetOut(el: Element): Promise<void>;
  popIn(el: Element, origin?: string): Promise<void>;
  finderIn(el: Element, items: Targets): Promise<void>; finderOut(el: Element): Promise<void>;
  toastIn(el: Element): Promise<void>; toastOut(el: Element): Promise<void>;
  pageLeave(cards: Targets): Promise<void>;
  /** Page swap out: cards sink, page head/tabs fade, container slides 16px against `direction`. Held until pageIn/pageReset. */
  pageOut(container: Element, opts?: { direction?: 1 | -1 }): Promise<void>;
  /** Page swap in: container slides from 26px, page head/tabs fade in, top-level cards rise (unless cards: false). */
  pageIn(container: Element, opts?: { direction?: 1 | -1; cards?: boolean }): Promise<void>;
  /** Cancels a pageOut that won't be followed by a new page. */
  pageReset(container: Element): void;
  themeSwap(button: Element | null, apply: () => void): Promise<void>;

  gridPop(cells: Targets, cols: number, opts?: { each?: number; delay?: number }): Promise<void>;
}

export interface SelectHandle { wrap: HTMLElement; select: HTMLSelectElement; open(): void; close(focus?: boolean): void; refresh(): void }
export interface DialOptions { value?: number; indoor?: number; min?: number; max?: number; step?: number; mode?: 'heat' | 'cool' | 'eco' | 'auto'; on?: boolean; controls?: boolean; label?: string; onChange?: (v: number) => void }
export interface DialHandle { readonly value: number; set(v: number): void; setIndoor(v: number): void; setMode(m: DialOptions['mode']): void; setOn(on: boolean): void; replay(): void }
export interface UiProps {
  /** Enhance one native <select> into the glass listbox. */
  select(el: HTMLSelectElement): SelectHandle;
  /** Enhance every select[data-hv-select] under root. */
  selects(root?: ParentNode): SelectHandle[];
  /** Build the thermostat inside an empty element. */
  dial(el: HTMLElement, opts?: DialOptions): DialHandle;
}

declare global {
  interface Window { Halvo: { motion: MotionProps; ui: UiProps; version: string } }
}
