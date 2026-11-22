# SideNav

The floating glass sidebar: app mark, grouped page links with a sliding highlight, and a home switcher at the foot.

**Provide** `.side` (glass) > `.brand` (`.mark` + `.brand__text`) and `.snav` holding `<span class="snav__pill">` then `.snav__sec` groups (`.snav__group` label + `.snav__item` links with a 20px icon, `.snav__label`, optional `.snav__count`). Current item: `aria-current="page"`. Move the highlight with `Halvo.motion.pill(pill, item, {radius: 14})`.

- Panel: fixed at `inset` from the edges, width `side` (256px) or `side-rail` (84px, labels hidden, counts become 8px dots), radius `r-xl`, padding 16 12 12.
- Item: 42px, radius 14, padding-left 20, `fs-md` 600 `ink-2`; icon `muted`, current icon `accent-text`. Highlight: `glass-3` + rim (dark 13% white).
- Counts: `warn` on `warn-soft`, 20px pill.
- Mark: 40px tile, radius 13, gradient 160° `accent-hi` → `accent`, `accent-ink` glyph, `glow` shadow.
- Motion (boot): panel slides in from x −40 (0.9s `expo.out`), then the brand, groups and items from x −12 with 25ms stagger (0.5s `power3.out`), the highlight scales in from 0.4 on x.
