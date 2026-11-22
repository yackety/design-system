# Tabs

Page-level sub-navigation in a glass strip; the current tab sits on a solid teal pill that slides between tabs.

**Provide** `<nav class="tabs">` holding `<span class="tabs__line"></span>` then links/buttons; mark the current one `aria-current="page"`. After layout and on every change call `Halvo.motion.pill(line, current, {radius: 12})` (first call with `animate: false`).

- Strip: glass recipe, radius 16, padding 5, gap 2, scrolls sideways without a scrollbar.
- Tab: 38px (40 on mobile), padding 0 14, radius 12, `fs-md` 600 `muted`; current tab text `accent-ink`; badges inside drop to 14% black.
- Motion: the pill is a full-size layer clipped with `inset(… round 12px)`. The edge in the direction of travel leaves first (0.36s `power3.out`), the far edge catches up (0.55s `power3.inOut`), so it stretches and then settles.
