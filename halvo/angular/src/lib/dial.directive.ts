import {
  AfterViewInit,
  Directive,
  ElementRef,
  EventEmitter,
  Input,
  NgZone,
  OnChanges,
  OnDestroy,
  Output,
  SimpleChanges,
  forwardRef,
  inject,
} from '@angular/core';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';
import type { DialHandle } from './halvo-api';
import { HalvoService } from './halvo.service';

export type HalvoDialMode = 'heat' | 'cool' | 'eco' | 'auto';

/**
 * Halvo's thermostat dial on an empty element. Two-way bind the set point with [(value)],
 * or use it as a form control (formControlName / ngModel).
 *
 *   <div halvoDial [(value)]="target" [indoor]="21" [mode]="mode" [on]="heating"></div>
 *   <div halvoDial formControlName="target" class="dial--md"></div>
 */
@Directive({
  selector: '[halvoDial]',
  standalone: true,
  exportAs: 'halvoDial',
  providers: [{ provide: NG_VALUE_ACCESSOR, useExisting: forwardRef(() => HalvoDialDirective), multi: true }],
})
export class HalvoDialDirective implements AfterViewInit, OnChanges, OnDestroy, ControlValueAccessor {
  /** The set point (°C). */
  @Input() value = 21.5;
  /** The measured indoor temperature, shown as a marker on the ring. */
  @Input() indoor = 21;
  @Input() mode: HalvoDialMode = 'heat';
  /** Off greys the ticks and shows "Off". */
  @Input() on = true;
  /** Range and step are read once, when the dial is created. */
  @Input() min = 10;
  @Input() max = 30;
  @Input() step = 0.5;
  /** Show the round − / + buttons. Read once. */
  @Input() controls = true;
  @Input() label = 'Set temperature';
  /** Emits the new set point whenever the person turns the dial or presses − / +. */
  @Output() readonly valueChange = new EventEmitter<number>();

  private readonly el = inject<ElementRef<HTMLElement>>(ElementRef);
  private readonly halvo = inject(HalvoService);
  private readonly zone = inject(NgZone);
  private handle?: DialHandle;
  private applying = false;
  private onChange: (v: number) => void = () => {};
  private onTouched: () => void = () => {};

  ngAfterViewInit(): void {
    this.handle = this.halvo.run((h) =>
      h.ui.dial(this.el.nativeElement, {
        value: this.value,
        indoor: this.indoor,
        mode: this.mode,
        on: this.on,
        min: this.min,
        max: this.max,
        step: this.step,
        controls: this.controls,
        label: this.label,
        onChange: (v) => {
          if (this.applying) return;
          this.zone.run(() => {
            this.value = v;
            this.valueChange.emit(v);
            this.onChange(v);
            this.onTouched();
          });
        },
      }),
    );
  }

  ngOnChanges(changes: SimpleChanges): void {
    const h = this.handle;
    if (!h) return;
    this.zone.runOutsideAngular(() => {
      if (changes['indoor']) h.setIndoor(this.indoor);
      if (changes['mode']) h.setMode(this.mode);
      if (changes['on']) h.setOn(this.on);
    });
    if (changes['value'] && h.value !== this.value) this.apply(this.value);
  }

  /** Replays the intro sweep. */
  replay(): void {
    this.zone.runOutsideAngular(() => this.handle?.replay());
  }

  writeValue(v: unknown): void {
    if (v === null || v === undefined || v === '' || isNaN(Number(v))) return;
    this.value = Number(v);
    if (this.handle && this.handle.value !== this.value) this.apply(this.value);
  }

  registerOnChange(fn: (v: number) => void): void {
    this.onChange = fn;
  }

  registerOnTouched(fn: () => void): void {
    this.onTouched = fn;
  }

  setDisabledState(disabled: boolean): void {
    const el = this.el.nativeElement;
    el.classList.toggle('is-disabled', disabled);
    el.style.pointerEvents = disabled ? 'none' : '';
    el.style.opacity = disabled ? '0.45' : '';
  }

  private apply(v: number): void {
    const h = this.handle;
    if (!h) return;
    this.applying = true;
    try {
      this.zone.runOutsideAngular(() => h.set(v));
    } finally {
      this.applying = false;
    }
  }

  ngOnDestroy(): void {
    this.handle = undefined;
  }
}
