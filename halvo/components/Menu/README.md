# Menu

A small glass popover of actions anchored under the control that opened it.

**Provide** `.pop` positioned under its anchor, holding `.menu__label`, `.menu__item` buttons (18px `muted` icon + label + optional `.kbd`), `.menu__sep`, and `menu__item--danger` last. Close on Escape, outside click and choice; return focus to the anchor.

- `glass-strong` with `blur-overlay`, rims and `shadow-lg`, radius 18, padding 6, min width 230.
- Item 40px (46 on touch), radius 11, `fs-md` 600; hover/focus `glass-3` (dark 10% white).
- Motion: `popIn` — from 0.92 and −6px, origin at the anchor's centre edge, 0.4s `back.out(2)`; it flips above the anchor when there's no room below.
