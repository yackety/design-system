# Device

A glass tile per device: icon, room and name, live state; when on, the icon turns teal and a soft teal light spills from the top-left corner.

**Provide** `<button class="dev card" data-lift>` (or `.glass`) > `.dev__top` (`.dev__ico` + a `.switch` or `.pill`), `.dev__name` (`small` room, `b` name), `.dev__state` (state text + optional 5px `.meter`). Add `is-on` when running and `is-off-line` when unreachable. Grid: `.devs` (auto-fill, min 200px; 2 columns on phones).

- Tile: `r-lg`, padding 16, min height 164. On: corner radial of `accent-soft`, fill `#302c2694` (dark) / `#ffffffbd` (light); icon `accent` / `accent-ink` with a 22px `glow`.
- Offline: 72% opacity, icon in `bad`, state says "Offline".
- Motion: tiles `deal` in (y 40, ±2.5°, 0.85s `back.out(1.4)`, 70ms stagger), `lift` on hover, and the icon `nudge`s when toggled.
