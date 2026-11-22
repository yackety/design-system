import { AfterViewInit, Directive, ElementRef, NgZone, OnDestroy, inject } from '@angular/core';
import { NgControl } from '@angular/forms';
import { Subscription } from 'rxjs';
import type { SelectHandle } from './halvo-api';
import { HalvoService } from './halvo.service';

/**
 * Turns a native `<select>` into Halvo's glass listbox.
 *
 *   <select halvoSelect formControlName="room">
 *     @for (r of rooms; track r.id) { <option [value]="r.id">{{ r.name }}</option> }
 *   </select>
 *
 * Works with formControl / formControlName / ngModel (Angular's own select accessor keeps
 * handling the value), re-reads options when they change, follows `disabled`, and removes
 * the listbox when the element is destroyed. Add class `select--sm` for the 34px size.
 */
@Directive({
  selector: 'select[halvoSelect]',
  standalone: true,
  exportAs: 'halvoSelect',
})
export class HalvoSelectDirective implements AfterViewInit, OnDestroy {
  private readonly el = inject<ElementRef<HTMLSelectElement>>(ElementRef);
  private readonly halvo = inject(HalvoService);
  private readonly zone = inject(NgZone);
  private readonly control = inject(NgControl, { optional: true, self: true });
  private handle: SelectHandle | null = null;
  private observer?: MutationObserver;
  private readonly subs = new Subscription();
  private queued = false;

  ngAfterViewInit(): void {
    const ui = this.halvo.ui;
    if (!ui) return;
    const select = this.el.nativeElement;
    select.classList.add('input');
    this.handle = ui.select(select);
    this.zone.runOutsideAngular(() => {
      this.observer = new MutationObserver(() => this.refreshSoon());
      this.observer.observe(select, {
        childList: true,
        subtree: true,
        characterData: true,
        attributes: true,
        attributeFilter: ['disabled', 'label', 'value', 'hidden'],
      });
    });
    if (this.control?.valueChanges) this.subs.add(this.control.valueChanges.subscribe(() => this.refreshSoon()));
    if (this.control?.statusChanges) this.subs.add(this.control.statusChanges.subscribe(() => this.refreshSoon()));
    this.refreshSoon(); // ngModel writes its first value a tick after init
  }

  /** Re-reads options, value and disabled state. Call it after changing them outside Angular. */
  refresh(): void {
    this.handle?.refresh();
  }

  open(): void {
    this.handle?.open();
  }

  close(): void {
    this.handle?.close();
  }

  private refreshSoon(): void {
    if (this.queued) return;
    this.queued = true;
    queueMicrotask(() => {
      this.queued = false;
      this.handle?.refresh();
    });
  }

  ngOnDestroy(): void {
    this.observer?.disconnect();
    this.subs.unsubscribe();
    const handle = this.handle;
    if (!handle) return;
    handle.close();
    const wrap = handle.wrap;
    const select = this.el.nativeElement;
    // put the <select> back where Angular left it, or drop the listbox if Angular already removed it
    if (wrap.isConnected) {
      if (wrap.contains(select)) wrap.replaceWith(select);
      else wrap.remove();
    }
    this.handle = null;
  }
}
