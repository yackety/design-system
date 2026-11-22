# Check

A 20px rounded-square checkbox; checked fills `accent` with an `accent-ink` tick.

**Provide** `<button class="check" role="checkbox" aria-checked="false">` + check icon (stroke 2.4) next to its label. Toggle `aria-checked`.

- Unchecked: inset 1.5px `line-2`, radius 6. Checked: `accent` fill, no outline, tick opacity 1.
- Motion: the tick `nudge`s in (0.7 → 1, `back.out(3)`).
