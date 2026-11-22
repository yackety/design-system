# Stepper

A compact − value + control for small counts and set points.

**Provide** `.stepper` > `button` (minus), `<output>`, `button.is-add` (plus, teal). Call `Halvo.motion.roll(valueEl, up)` after each change.

- Track `well`, radius 12, padding 3; buttons 30px (38 on touch), radius 9, hover `glass-3`; the plus is `accent` / `accent-ink`.
- Value `fs-md` 700, min width 34.
- Motion: the new value rolls in from the side it came from (±60% y, 0.35s `back.out(2)`).
