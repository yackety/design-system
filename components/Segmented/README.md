# Segmented

A recessed switch between 2–5 modes inside a card; the thumb slides like the tab pill.

**Provide** `<div class="seg">` with `<span class="seg__thumb"></span>` and `<button aria-pressed>`s (optional 16px icon). `seg--accent` paints the thumb teal for the primary mode switch (heating mode, chart range). Call `Halvo.motion.pill(thumb, pressed, {radius: 10})`.

- Track: `well`, 1px `line`, radius 14, padding 4. Buttons 32px (40 on touch), radius 10, `fs-sm` 600 `muted`; pressed `ink` (or `accent-ink` on `seg--accent`).
- Thumb: `glass-3` with a `rim` highlight (dark: 16% white).
- On mobile a segmented control in a card head wraps to its own full-width row.
