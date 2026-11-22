# Modal

A centred glass dialog for short, focused tasks; it grows out of the control that opened it.

**Provide** a `.scrim` and a `.modal` (`role="dialog" aria-modal="true"` with a label) holding `.modal__head` (h2 `fs-2xl` 700 + `p` `muted`, close `ibtn--flat`), `.modal__body`, `.modal__foot` (ghost cancel + primary). `modal--wide` is 760px. Trap focus; Escape closes.

- `glass-strong` + `blur-overlay` + rims + `shadow-lg`, radius `r-xl`, width ≤520. Scrim: light `#14120e47`, dark `#00000080`.
- On phones it becomes a bottom sheet (radius 26 26 0 0, ≤92dvh) with a grip.
- Motion: scrim fades 0.3s; dialog `modalIn` from 0.86 with transform-origin at the trigger, 0.5s `back.out(1.5)`; out to 0.94 in 0.2s `power2.in`. Sheets use `sheetIn/Out`.
