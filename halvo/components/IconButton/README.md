# IconButton

A 44px square glass button holding one 20px icon, with an optional count badge.

**Provide** `<button class="ibtn" aria-label="…">` + icon. Variants: `ibtn--sm` (34px, radius 11), `ibtn--flat` (no fill), `ibtn--round` (40px circle, used for the dial's − / +). Badge: `<span class="ibtn__badge">3</span>` — `accent` fill, `accent-ink` text, `glow` halo.

- Radius 14, `glass-2` fill, 1px `line` outline; hover `glass-3`. Always set `aria-label`.
- Motion: the bell rings (`Halvo.motion.ring`) and its badge pops when a notice arrives; the theme button swaps themes with a circle wipe from its centre (`themeSwap`, 450ms `power2.inOut`).
- `.kbd` shows shortcuts beside search: 24px, radius 7, `fs-2xs` 700 `muted`.
