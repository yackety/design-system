# Button

A 42px glass button; the teal `btn--primary` is reserved for the one action a view exists for.

**Provide** a `<button class="btn">` with a label in sentence case, verb first ("Add device", "All on"); an 18px stroke icon may lead. Modifiers: `btn--primary`, `btn--ghost` (no fill, for toolbars), `btn--danger` (text in `bad`), `btn--sm` (34px, radius 11), `btn--lg` (52px, radius 16), `btn--block`.

- Default: `glass-2` fill, `rim-2` top highlight, `line-2` outline, radius 13, `fs-md` 600. Hover → `glass-3`.
- Primary: gradient 160° `accent-hi` → `accent`, text `accent-ink`, `glow` shadow `0 10px 24px -12px`. Hover → flat `accent-hi`.
- Disabled: 45% opacity, `not-allowed`.
- Motion: the top-bar primary carries `.magnetic` (pointer follow, `Halvo.motion.magnetic`). Icons acknowledge a press with `nudge` (0.7 → 1, `back.out(3)`).

Don't put two primaries side by side, and don't use white text on teal.
