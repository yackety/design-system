# Motion

Halvo's motion kit: fourteen named moves with fixed durations and eases, exposed as `Halvo.motion`.

The source animates with GSAP; `bundle.js` ports every move to the Web Animations API with the same numbers, so a page needs no animation library. Each helper returns a Promise and collapses to the end state under `prefers-reduced-motion`.

| Move | Use it for | Spec |
| --- | --- | --- |
| `splitText(el)` | Page titles | letters `yPercent 115 → 0`, `rotate 6° → 0`, 0.85s `power4.out`, 22ms stagger, clipped by `.word` |
| `rise(els)` | Cards and sections entering | `opacity 0, y 26, scale .985`, 0.8s `expo.out`, 60ms stagger |
| `slide(els)` | List rows, menu and finder items | `opacity 0, y 12`, 0.55s `power3.out`, 40ms stagger |
| `deal(els)` | Tiles (devices, scenes) | `y 40, ±2.5°, scale .95`, 0.85s `back.out(1.4)`, 70ms stagger |
| `grow(els, {axis})` | Bars, meters | `scaleY/scaleX 0 → 1`, 0.9s `expo.out`, 30ms stagger |
| `draw(paths)` | Sparklines, area lines, rings | stroke dash offset, 1.1s `power2.inOut` |
| `pop(els)` | Dots, badges, small marks | `scale .6 → 1`, 0.6s `back.out(3)` |
| `countTo(el, n)` | Every figure that changes | count from last value, 1.2s `power3.out` |
| `flash(el)` | A value that just changed | hop `y -4, scale 1.08`, 0.55s `back.out(2.4)` + 1s accent colour flash |
| `shake(el)` | Rejected input | `x 0,-8,7,-5,3,0`, 0.42s |
| `ring(bell, badge)` | New notification | rotate `0,16,-14,10,-6,0` from 50% 10%, 0.8s; badge `scale .4 → 1` |
| `magnetic(root)` | The one primary action in the top bar (`.magnetic`) | follows the pointer 20% x / 28% y, 0.5s `power3.out` |
| `lift(root)` | `[data-lift]` tiles | `y -4` on hover, 0.45s in / 0.5s out |
| `pageOut(container, {direction})` / `pageIn(container, {direction, cards})` | Switching pages | out: visible cards sink 8px (0.135s), page head/tabs lift 6px, the page slides 16px against the direction (0.18s `power2.in`); in: the page slides from 26px (0.7s `expo.out`), page head/tabs fade in, cards rise 50ms apart. `pageReset` undoes an out |
| `pill(indicator, target)` | Tabs, segmented, side nav, tab bar | clip-path inset morph: leading edge 0.36s `power3.out`, trailing 0.55s `power3.inOut`, cross axis 0.45s; re-measures on resize |
| `gridPop(cells, cols)` | Heatmap cells | `scale 0 → 1`, 0.6s `back.out(2.2)`, 12ms per cell of distance from the top-left |

The thermostat's sweep and the Select's open / close live in `Halvo.ui.dial` and `Halvo.ui.select`. Overlay moves (`modalIn/Out`, `drawerIn/Out`, `sheetIn/Out`, `popIn`, `finderIn/Out`, `toastIn/Out`, `scrimIn/Out`), `pageLeave`, `roll`, `switchKnob`, `fill` and `themeSwap` are documented on the components that use them.

**Rules**
- Things arrive with `expo.out` or `power3.out` and leave with `power2.in`, about a third as long.
- Springy `back.out` is for small things only: pills, badges, knobs, menus. Never for page-sized surfaces.
- Stagger lists; never animate more than ~12 items one by one (use `stagger: {amount}` beyond that).
- Animate `transform`, `opacity`, `clip-path` and stroke offsets only. Glass blur never animates.
- Ambient loops are CSS: `breathe` (live dot, 2s), `eq` (music bars, 1.1s), `airspin` (fans, `--spin`), `flash` (1s).
