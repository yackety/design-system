import { AfterViewInit, Directive, ElementRef, Input, OnChanges, SimpleChanges, inject } from '@angular/core';
import { HalvoService } from './halvo.service';

export type HalvoMotionName = 'rise' | 'slide' | 'deal' | 'pop' | 'grow' | 'grow-x' | 'draw' | 'split' | 'grid';

/**
 * Plays one of Halvo's entrance moves once, after the element first renders.
 * List moves (rise, slide, deal, pop, grow, grid) stagger the element's children;
 * `split` animates a heading's letters; `draw` traces the SVG strokes inside.
 *
 *   <div class="kpis" halvoMotion="rise">…cards…</div>
 *   <h1 halvoMotion="split">Good evening, Amara</h1>
 *   <div class="heat" halvoMotion="grid" motionTargets=".heat__cell i" [motionCols]="12"></div>
 */
@Directive({
  selector: '[halvoMotion]',
  standalone: true,
})
export class HalvoMotionDirective implements AfterViewInit {
  @Input({ required: true }) halvoMotion!: HalvoMotionName;
  /** CSS selector of what to animate inside the element (default: its children, or the element itself for split/draw). */
  @Input() motionTargets?: string;
  /** Seconds before the move starts. */
  @Input() motionDelay = 0;
  /** Seconds between items (each move has its own default). */
  @Input() motionStagger?: number;
  /** Columns, for `grid`. */
  @Input() motionCols = 1;

  private readonly el = inject<ElementRef<HTMLElement>>(ElementRef);
  private readonly halvo = inject(HalvoService);

  ngAfterViewInit(): void {
    this.play();
  }

  /** Plays the move again. */
  play(): void {
    this.halvo.run(({ motion }) => {
      const host = this.el.nativeElement;
      const pick = (fallback: Element[]) => (this.motionTargets ? Array.from(host.querySelectorAll(this.motionTargets)) : fallback);
      const kids = pick(Array.from(host.children));
      const opts = { delay: this.motionDelay, ...(this.motionStagger !== undefined ? { stagger: this.motionStagger } : {}) };
      switch (this.halvoMotion) {
        case 'rise': return motion.rise(kids, opts);
        case 'slide': return motion.slide(kids, opts);
        case 'deal': return motion.deal(kids, opts);
        case 'pop': return motion.pop(kids, opts);
        case 'grow': return motion.grow(kids, opts);
        case 'grow-x': return motion.grow(kids, { ...opts, axis: 'x' });
        case 'grid': return motion.gridPop(kids, this.motionCols, { delay: this.motionDelay });
        case 'split': return motion.splitText(this.motionTargets ? (host.querySelector(this.motionTargets) as Element) : host, { delay: this.motionDelay });
        case 'draw': return motion.draw(pick(host instanceof SVGGeometryElement ? [host] : Array.from(host.querySelectorAll('path, line, polyline, circle'))), { delay: this.motionDelay });
      }
    });
  }
}

/**
 * Counts a number up to its value (1.2s) and again from the old value whenever it changes.
 *
 *   <span [halvoCount]="watts" [countFormat]="formatWatts" countFlash></span>
 */
@Directive({
  selector: '[halvoCount]',
  standalone: true,
})
export class HalvoCountDirective implements OnChanges {
  @Input({ required: true }) halvoCount!: number;
  /** Formats the running value (default: rounded, with thousands separators). */
  @Input() countFormat?: (v: number) => string;
  /** Seconds (default 1.2). */
  @Input() countDuration?: number;
  /** Start value for the first count (default 0). */
  @Input() countFrom = 0;
  /** Flash the value in accent when it changes after the first count. */
  @Input() countFlash: boolean | '' = false;

  private readonly el = inject<ElementRef<HTMLElement>>(ElementRef);
  private readonly halvo = inject(HalvoService);
  private first = true;

  ngOnChanges(changes: SimpleChanges): void {
    if (!changes['halvoCount']) return;
    const value = Number(this.halvoCount);
    const el = this.el.nativeElement;
    const format = this.countFormat;
    const ran = this.halvo.run(({ motion }) => {
      const opts = { duration: this.countDuration, ...(this.first ? { from: this.countFrom } : {}) };
      void motion.countTo(el, value, format, opts);
      if (!this.first && this.countFlash !== false) void motion.flash(el);
    });
    if (ran === undefined) el.textContent = format ? format(value) : String(value); // server render
    this.first = false;
  }
}

/** Makes the element follow the pointer a little (use on the one primary action). */
@Directive({
  selector: '[halvoMagnetic]',
  standalone: true,
  host: { class: 'magnetic' },
})
export class HalvoMagneticDirective implements AfterViewInit {
  private readonly el = inject<ElementRef<HTMLElement>>(ElementRef);
  private readonly halvo = inject(HalvoService);

  ngAfterViewInit(): void {
    this.halvo.run(({ motion }) => motion.magnetic(this.el.nativeElement.parentElement ?? undefined));
  }
}

/** Lifts a tile 4px on hover. */
@Directive({
  selector: '[halvoLift]',
  standalone: true,
  host: { 'data-lift': '' },
})
export class HalvoLiftDirective implements AfterViewInit {
  private readonly el = inject<ElementRef<HTMLElement>>(ElementRef);
  private readonly halvo = inject(HalvoService);

  ngAfterViewInit(): void {
    this.halvo.run(({ motion }) => motion.lift(this.el.nativeElement.parentElement ?? undefined));
  }
}
