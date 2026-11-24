# -*- coding: utf-8 -*-
REPLAY = '<button class="btn btn--sm btn--ghost" data-replay>@@play|ico ico--sm@@Replay</button>'

# ---------------------------------------------------------------- Motion
C['Motion'] = ("""
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
""", doc('Foundations', 560, 'Motion', """
<div class="hv-stage">
  <div class="hv-row" style="justify-content:space-between;margin-bottom:14px">
    <h1 id="t" style="font-size:34px;font-weight:600;letter-spacing:-.025em;line-height:1.04">Under glass, in motion</h1>
    <button class="btn btn--primary magnetic" id="all">@@play@@Play all</button>
  </div>
  <div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px">
    <div class="card" data-lift><div class="chead"><div class="chead__text"><h3>rise</h3><p>expo.out · 0.8s</p></div><button class="ibtn ibtn--sm" data-run="rise">@@play|ico ico--sm@@</button></div>
      <div class="hv-col" id="rise" style="gap:6px"><div class="well" style="height:22px"></div><div class="well" style="height:22px"></div><div class="well" style="height:22px"></div></div></div>
    <div class="card" data-lift><div class="chead"><div class="chead__text"><h3>deal</h3><p>back.out(1.4) · 0.85s</p></div><button class="ibtn ibtn--sm" data-run="deal">@@play|ico ico--sm@@</button></div>
      <div class="hv-row" id="deal" style="gap:6px;flex-wrap:nowrap"><div class="well" style="flex:1;height:76px"></div><div class="well" style="flex:1;height:76px"></div><div class="well" style="flex:1;height:76px"></div></div></div>
    <div class="card" data-lift><div class="chead"><div class="chead__text"><h3>grow</h3><p>expo.out · 0.9s</p></div><button class="ibtn ibtn--sm" data-run="grow">@@play|ico ico--sm@@</button></div>
      <div id="grow" style="display:flex;align-items:flex-end;gap:7px;height:76px"></div></div>
    <div class="card" data-lift><div class="chead"><div class="chead__text"><h3>draw</h3><p>power2.inOut · 1.1s</p></div><button class="ibtn ibtn--sm" data-run="draw">@@play|ico ico--sm@@</button></div>
      <svg viewBox="0 0 200 76" style="width:100%;height:76px;overflow:visible"><path id="draw" class="area__line" d="M2 60 C 30 58, 40 30, 64 36 S 100 64, 124 40 S 160 8, 198 14"/></svg></div>
    <div class="card" data-lift><div class="chead"><div class="chead__text"><h3>countTo</h3><p>power3.out · 1.2s</p></div><button class="ibtn ibtn--sm" data-run="count">@@play|ico ico--sm@@</button></div>
      <div class="kpi__value" style="font-size:34px;margin:0"><span id="count">1,478</span><small>W</small></div></div>
    <div class="card" data-lift><div class="chead"><div class="chead__text"><h3>flash</h3><p>back.out(2.4) · 0.55s</p></div><button class="ibtn ibtn--sm" data-run="flash">@@play|ico ico--sm@@</button></div>
      <div class="kpi__value" style="font-size:34px;margin:0;display:inline-block" id="flash">21.5°</div></div>
    <div class="card" data-lift><div class="chead"><div class="chead__text"><h3>pop · ring</h3><p>back.out(3) · 0.6s</p></div><button class="ibtn ibtn--sm" data-run="pop">@@play|ico ico--sm@@</button></div>
      <div class="hv-row"><span class="ibtn" id="bell">@@bell@@<span class="ibtn__badge" id="badge">3</span></span><span class="pill pill--good" data-pop>Fresh</span><span class="pill pill--accent" data-pop>Live</span></div></div>
    <div class="card" data-lift><div class="chead"><div class="chead__text"><h3>shake</h3><p>power2.out · 0.42s</p></div><button class="ibtn ibtn--sm" data-run="shake">@@play|ico ico--sm@@</button></div>
      <input class="input is-bad" id="shake" value="0000" aria-label="PIN"></div>
  </div>
  <div class="hv-row" style="margin-top:12px;justify-content:space-between">
    <nav class="tabs" id="tabs"><span class="tabs__line"></span><button aria-current="page">Living room</button><button>Kitchen</button><button>Media room</button><button>Studio</button></nav>
    <span class="muted" style="font-size:12.5px;font-weight:600">pill — click a tab · <span class="live"></span>breathe · <span class="eq"><i></i><i></i><i></i><i></i></span> eq</span>
  </div>
</div>""", """
var M = Halvo.motion, $ = function (s) { return document.querySelector(s); };
var g = $('#grow'); [40, 62, 30, 80, 55, 92, 48, 70].forEach(function (h, i) { var b = document.createElement('i'); b.style.cssText = 'flex:1;height:' + h + '%;border-radius:99px;transform-origin:50% 100%;background:' + (i === 5 ? 'var(--data);box-shadow:0 0 18px -2px var(--glow)' : 'color-mix(in oklab,var(--data) 50%,transparent)'); g.appendChild(b); });
var runs = {
  rise: function () { return M.rise($('#rise').children); },
  deal: function () { return M.deal($('#deal').children); },
  grow: function () { return M.grow(g.children); },
  draw: function () { return M.draw($('#draw')); },
  count: function () { return M.countTo($('#count'), 1478, null, { from: 0 }); },
  flash: function () { return M.flash($('#flash')); },
  pop: function () { M.ring($('#bell svg'), $('#badge')); return M.pop(document.querySelectorAll('[data-pop]'), { delay: .1 }); },
  shake: function () { return M.shake($('#shake')); }
};
document.querySelectorAll('[data-run]').forEach(function (b) { b.onclick = function () { M.nudge(b); runs[b.dataset.run](); }; });
var tabs = $('#tabs'), line = tabs.querySelector('.tabs__line');
tabs.querySelectorAll('button').forEach(function (b) { b.onclick = function () { tabs.querySelector('[aria-current]').removeAttribute('aria-current'); b.setAttribute('aria-current', 'page'); M.pill(line, b, { radius: 12 }); }; });
M.pill(line, tabs.querySelector('[aria-current]'), { radius: 12, animate: false });
function all() { M.splitText($('#t')); M.rise(document.querySelectorAll('.card'), { delay: .1 }); setTimeout(function () { Object.keys(runs).forEach(function (k) { if (k !== 'shake') runs[k](); }); }, 350); }
$('#all').onclick = all; M.magnetic(); M.lift(); all();
"""))

# ---------------------------------------------------------------- Button
C['Button'] = ("""
# Button

A 42px glass button; the teal `btn--primary` is reserved for the one action a view exists for.

**Provide** a `<button class="btn">` with a label in sentence case, verb first ("Add device", "All on"); an 18px stroke icon may lead. Modifiers: `btn--primary`, `btn--ghost` (no fill, for toolbars), `btn--danger` (text in `bad`), `btn--sm` (34px, radius 11), `btn--lg` (52px, radius 16), `btn--block`.

- Default: `glass-2` fill, `rim-2` top highlight, `line-2` outline, radius 13, `fs-md` 600. Hover → `glass-3`.
- Primary: gradient 160° `accent-hi` → `accent`, text `accent-ink`, `glow` shadow `0 10px 24px -12px`. Hover → flat `accent-hi`.
- Disabled: 45% opacity, `not-allowed`.
- Motion: the top-bar primary carries `.magnetic` (pointer follow, `Halvo.motion.magnetic`). Icons acknowledge a press with `nudge` (0.7 → 1, `back.out(3)`).

Don't put two primaries side by side, and don't use white text on teal.
""", doc('Actions', 140, 'Button', """
<div class="hv-stage hv-col">
  <div class="hv-row">
    <button class="btn btn--primary magnetic">@@plus@@New</button>
    <button class="btn">@@bulb@@All on</button>
    <button class="btn">@@moon@@All off</button>
    <button class="btn btn--ghost">Cancel</button>
    <button class="btn btn--danger">@@trash@@Remove</button>
    <button class="btn" disabled>Disabled</button>
  </div>
  <div class="hv-row">
    <button class="btn btn--primary btn--lg">Add a device</button>
    <button class="btn btn--lg">Plan</button>
    <button class="btn btn--primary btn--sm">@@plus@@Scene</button>
    <button class="btn btn--sm">Thermostat</button>
    <a class="linkbtn" href="#" onclick="return false">All rooms</a>
  </div>
</div>""", """
var M = Halvo.motion; M.magnetic();
document.querySelectorAll('.btn').forEach(function (b) { b.addEventListener('click', function () { M.nudge(b); }); });
"""))

# ---------------------------------------------------------------- IconButton
C['IconButton'] = ("""
# IconButton

A 44px square glass button holding one 20px icon, with an optional count badge.

**Provide** `<button class="ibtn" aria-label="…">` + icon. Variants: `ibtn--sm` (34px, radius 11), `ibtn--flat` (no fill), `ibtn--round` (40px circle, used for the dial's − / +). Badge: `<span class="ibtn__badge">3</span>` — `accent` fill, `accent-ink` text, `glow` halo.

- Radius 14, `glass-2` fill, 1px `line` outline; hover `glass-3`. Always set `aria-label`.
- Motion: the bell rings (`Halvo.motion.ring`) and its badge pops when a notice arrives; the theme button swaps themes with a circle wipe from its centre (`themeSwap`, 450ms `power2.inOut`).
- `.kbd` shows shortcuts beside search: 24px, radius 7, `fs-2xs` 700 `muted`.
""", doc('Actions', 100, 'IconButton', """
<div class="hv-stage hv-row">
  <button class="ibtn" aria-label="Search">@@search@@</button>
  <button class="ibtn" aria-label="Switch theme" id="theme">@@sun@@</button>
  <button class="ibtn" aria-label="Notifications" id="bell">@@bell@@<span class="ibtn__badge">3</span></button>
  <button class="ibtn ibtn--sm" aria-label="Edit">@@edit|ico ico--sm@@</button>
  <button class="ibtn ibtn--flat" aria-label="Close">@@x@@</button>
  <button class="ibtn ibtn--round" aria-label="Lower">@@minus@@</button>
  <button class="ibtn ibtn--round" aria-label="Raise">@@plus@@</button>
  <span class="kbd">⌘</span><span class="kbd">K</span>
</div>""", """
var M = Halvo.motion, root = document.documentElement;
document.getElementById('bell').onclick = function () { M.ring(this.querySelector('svg'), this.querySelector('.ibtn__badge')); };
document.getElementById('theme').onclick = function () { var b = this; M.themeSwap(b, function () { root.dataset.theme = root.dataset.theme === 'light' ? 'dark' : 'light'; }); };
document.querySelectorAll('.ibtn').forEach(function (b) { if (!b.id) b.onclick = function () { M.nudge(b); }; });
"""))

# ---------------------------------------------------------------- Chip
C['Chip'] = ("""
# Chip

A 34px toggle used for filters and quick picks; pressed chips turn solid teal.

**Provide** `<button class="chip" aria-pressed="false">Label <span class="badge">4</span></button>` inside `.chips`. Toggle `aria-pressed`.

- Idle: `glass-2`, `line` outline, `ink-2` text `fs-sm` 600, radius 11. Hover → `glass-3`, `ink`.
- Pressed: `accent` fill, `accent-ink` text, `glow` shadow `0 6px 16px -10px`; its badge drops to 8% black.
- On touch screens chips grow to 44px tall.
""", doc('Actions', 96, 'Chip', """
<div class="hv-stage"><div class="chips">
  <button class="chip" aria-pressed="true">All devices <span class="badge">24</span></button>
  <button class="chip" aria-pressed="false">@@bulb|ico ico--sm@@Lighting <span class="badge">9</span></button>
  <button class="chip" aria-pressed="false">@@plug|ico ico--sm@@Plugs &amp; power <span class="badge">5</span></button>
  <button class="chip" aria-pressed="false">@@speaker|ico ico--sm@@Audio &amp; screens</button>
  <button class="chip" aria-pressed="false">@@shield|ico ico--sm@@Safety</button>
</div></div>""", """
document.querySelectorAll('.chip').forEach(function (c) { c.onclick = function () { c.setAttribute('aria-pressed', c.getAttribute('aria-pressed') !== 'true'); Halvo.motion.nudge(c); }; });
"""))

# ---------------------------------------------------------------- Card
C['Card'] = ("""
# Card

The frosted glass panel every Halvo screen is built from: `glass` fill, backdrop `blur`, two rim insets and `shadow`.

**Provide** `<section class="card">` with a `.chead` (title `h2/h3` in `fs-lg` 600, optional `p` subtitle in `fs-sm` `muted`, trailing action) and any body. `card--flush` drops the padding for tables and media. Inside a card, recessed groups use `.well` (`glass-2`, radius `r-md`).

- Radius `r-lg` (22px), padding 18 / 20 / 20; 20px radius and 16px padding at ≤760px.
- The recipe is `background: var(--glass); backdrop-filter: var(--blur); box-shadow: inset 0 1px 0 var(--rim), inset 0 0 0 1px var(--rim-2), var(--shadow)`. Without backdrop-filter support it falls back to `glass-strong`.
- Glass needs something behind it: the room photo with `veil` over it. Never put glass on flat `bg` in a product screen.
- Motion: cards enter with `rise` (staggered 60ms) and leave a route with `pageLeave`. Tiles that open something carry `data-lift`.
- Section labels inside cards: `.section-label`, 11px uppercase 0.08em `muted`.
""", doc('Surfaces', 300, 'Card', """
<div class="hv-stage" style="display:grid;grid-template-columns:1.3fr 1fr;gap:12px">
  <section class="card">
    <div class="chead"><div class="chead__text"><h3>Lights</h3><p>2 on · drag to dim, pick a colour</p></div><span class="switch" role="switch" aria-checked="true"><i></i></span></div>
    <div class="well" style="padding:12px 14px;display:flex;align-items:center;gap:12px"><span class="dev__ico" style="background:var(--accent);color:var(--accent-ink);box-shadow:0 0 22px -4px var(--glow)">@@bulb@@</span><div class="cell__text"><b>Arc floor lamp</b><small>72% · 2700 K · 9 W</small></div></div>
    <div class="section-label">Scenes</div>
    <div class="hv-row"><span class="chip">Slow morning</span><span class="chip">Film night</span><span class="chip">Lights out</span></div>
  </section>
  <section class="card" data-lift>
    <div class="chead"><div class="chead__text"><h3>Climate</h3><p>House set to 21.5° · heat</p></div><button class="btn btn--sm">Thermostat</button></div>
    <div class="kpi__value" style="font-size:34px;margin:0">21°<small>0.3° under</small></div>
    <p class="muted" style="font-size:12.5px;font-weight:600;margin-top:6px">Warming toward it now</p>
    <div style="margin-top:14px">""" + REPLAY + """</div>
  </section>
</div>""", """
var M = Halvo.motion; M.lift();
function play() { M.rise(document.querySelectorAll('.card')); }
document.querySelector('[data-replay]').onclick = play; play();
"""))

# ---------------------------------------------------------------- Kpi
C['Kpi'] = ("""
# Kpi

A glass stat tile: label with icon, a big figure with a small unit, and a footer with a delta or sparkline.

**Provide** `.kpi` with `.kpi__label` (17px icon + text), `.kpi__value` (figure + `<small>` unit), `.kpi__foot` (delta/`live` dot + `.spark` svg). Set `--k` on the tile to tint the corner glow, label icon and spark (`--k: var(--warm)` for energy, `var(--cool)` for usage, `var(--s3)` for solar).

- 124px min height, padding 16 / 18 / 14, `r-lg`. Corner glow: 150px radial of `--k` at 22%, top −50 / right −40.
- Figure `fs-3xl` (22px) 600, unit `fs-md` `muted`. 18px at ≤760px, where the spark hides.
- Delta pills: `delta--up` (`good` on `good-soft`) and `delta--down` (`bad` on `bad-soft`), always with an arrow.
- Motion: figures count up (`countTo`, 1.2s `power3.out`) and sparks draw (`draw`); a live value that changes gets `flash`.
""", doc('Surfaces', 300, 'Kpi', """
<div class="hv-stage">
  <div class="kpis">
    <div class="kpi" style="--k:var(--warm)"><div class="kpi__label">@@bolt@@Drawing now</div><div class="kpi__value"><span data-n="1478">1,478</span><small>W</small></div>
      <div class="kpi__foot"><span><span class="live"></span>live</span><svg class="spark" viewBox="0 0 88 28"><path class="spark__area" d="M0 24 L14 22 L28 23 L42 18 L56 19 L70 10 L88 8 L88 28 L0 28Z"/><path d="M0 24 L14 22 L28 23 L42 18 L56 19 L70 10 L88 8"/></svg></div></div>
    <div class="kpi" style="--k:var(--cool)"><div class="kpi__label">@@trend@@Used today</div><div class="kpi__value"><span data-n="15.8" data-d="1">15.8</span><small>kWh</small></div>
      <div class="kpi__foot"><span class="delta delta--down">↑ 25%</span> vs yesterday<svg class="spark" viewBox="0 0 88 28"><path d="M0 22 L10 20 L18 12 L26 16 L36 14 L46 17 L56 9 L66 12 L76 7 L88 6"/></svg></div></div>
    <div class="kpi" style="--k:var(--s3)"><div class="kpi__label">@@sun@@Solar today</div><div class="kpi__value"><span data-n="11.7" data-d="1">11.7</span><small>kWh</small></div>
      <div class="kpi__foot">Battery 64%<svg class="spark" viewBox="0 0 88 28"><path class="spark__area" d="M0 26 C 20 26, 30 4, 44 4 S 68 26, 88 26 L88 28 L0 28Z"/><path d="M0 26 C 20 26, 30 4, 44 4 S 68 26, 88 26"/></svg></div></div>
    <div class="kpi"><div class="kpi__label">@@drop@@Humidity</div><div class="kpi__value"><span data-n="46">46</span><small>%</small></div>
      <div class="kpi__foot"><span class="delta delta--up">↓ 2%</span> Comfort band 40–55%</div></div>
  </div>
  <div style="margin-top:10px">""" + REPLAY + """</div>
</div>""", """
var M = Halvo.motion;
function play() {
  M.rise(document.querySelectorAll('.kpi'));
  document.querySelectorAll('[data-n]').forEach(function (el, i) { var d = +(el.dataset.d || 0); M.countTo(el, +el.dataset.n, function (v) { return v.toLocaleString('en-GB', { minimumFractionDigits: d, maximumFractionDigits: d }); }, { from: 0, delay: .15 + i * .06 }); });
  M.draw(document.querySelectorAll('.spark path:not(.spark__area)'), { delay: .3 });
}
document.querySelector('[data-replay]').onclick = play; play();
"""))

# ---------------------------------------------------------------- PageHead
C['PageHead'] = ("""
# PageHead

The glass banner at the top of each page: eyebrow, greeting-style title, one plain sentence of status, then facts and actions.

**Provide** `.phead` > `.phead__text` (`.phead__eyebrow`, `h1`, `p`) + `.phead__actions`. Facts sit as `.pill`s; people as an `.avstack`.

- Title: `page-title` style — clamp(28px, 2.6vw, 38px), 600, −0.025em, line-height 1.04, with a soft text shadow (dark `#0000002e`, light `#fff9`) so it reads over the photo.
- Lead: `fs-base` in `ink-2`, max 70ch. Write it as a sentence about the home, not a list.
- Motion: the title enters with `splitText` (letters rise from a clipped word box, 0.85s `power4.out`, 22ms per letter); pills follow with `slide`.
""", doc('Surfaces', 230, 'PageHead', """
<div class="hv-stage">
  <header class="phead">
    <div class="phead__text">
      <div class="phead__eyebrow">Larch House · Wednesday evening</div>
      <h1 id="t">Good evening, Amara</h1>
      <p>Heating holds 21.5° until 22:30, then eases to 17° for the night. The dishwasher finishes at 20:20, and the roof covered 74% of today.</p>
      <div class="hv-row" style="margin-top:12px;gap:6px" id="facts">
        <span class="pill pill--plain">@@users|ico ico--sm@@2 of 3 home</span>
        <span class="pill pill--plain">@@bulb|ico ico--sm@@9 devices on</span>
        <span class="pill pill--plain">@@bolt|ico ico--sm@@1.48 kW now</span>
        <span class="pill pill--good">Every door locked</span>
      </div>
    </div>
    <div class="phead__actions"><div class="avstack"><span class="av" style="--h:var(--h1)">AL</span><span class="av" style="--h:var(--h2)">TO</span></div>""" + REPLAY + """</div>
  </header>
</div>""", """
var M = Halvo.motion;
function play() { M.splitText(document.getElementById('t')); M.slide(document.querySelectorAll('#facts > *'), { delay: .35 }); }
document.querySelector('[data-replay]').onclick = play; play();
"""))

# ---------------------------------------------------------------- Tabs
C['Tabs'] = ("""
# Tabs

Page-level sub-navigation in a glass strip; the current tab sits on a solid teal pill that slides between tabs.

**Provide** `<nav class="tabs">` holding `<span class="tabs__line"></span>` then links/buttons; mark the current one `aria-current="page"`. After layout and on every change call `Halvo.motion.pill(line, current, {radius: 12})` (first call with `animate: false`).

- Strip: glass recipe, radius 16, padding 5, gap 2, scrolls sideways without a scrollbar.
- Tab: 38px (40 on mobile), padding 0 14, radius 12, `fs-md` 600 `muted`; current tab text `accent-ink`; badges inside drop to 14% black.
- Motion: the pill is a full-size layer clipped with `inset(… round 12px)`. The edge in the direction of travel leaves first (0.36s `power3.out`), the far edge catches up (0.55s `power3.inOut`), so it stretches and then settles.
""", doc('Navigation', 110, 'Tabs', """
<div class="hv-stage">
  <nav class="tabs" id="tabs"><span class="tabs__line"></span>
    <button aria-current="page">Living room <span class="badge">2</span></button>
    <button>Kitchen <span class="badge">1</span></button>
    <button>Media room <span class="badge">1</span></button>
    <button>Studio <span class="badge">1</span></button>
    <button>Garden lounge</button>
  </nav>
</div>""", """
var M = Halvo.motion, tabs = document.getElementById('tabs'), line = tabs.querySelector('.tabs__line');
tabs.querySelectorAll('button').forEach(function (b) { b.onclick = function () { tabs.querySelector('[aria-current]').removeAttribute('aria-current'); b.setAttribute('aria-current', 'page'); M.pill(line, b, { radius: 12 }); }; });
requestAnimationFrame(function () { M.pill(line, tabs.querySelector('[aria-current]'), { radius: 12, animate: false }); });
"""))

# ---------------------------------------------------------------- Segmented
C['Segmented'] = ("""
# Segmented

A recessed switch between 2–5 modes inside a card; the thumb slides like the tab pill.

**Provide** `<div class="seg">` with `<span class="seg__thumb"></span>` and `<button aria-pressed>`s (optional 16px icon). `seg--accent` paints the thumb teal for the primary mode switch (heating mode, chart range). Call `Halvo.motion.pill(thumb, pressed, {radius: 10})`.

- Track: `well`, 1px `line`, radius 14, padding 4. Buttons 32px (40 on touch), radius 10, `fs-sm` 600 `muted`; pressed `ink` (or `accent-ink` on `seg--accent`).
- Thumb: `glass-3` with a `rim` highlight (dark: 16% white).
- On mobile a segmented control in a card head wraps to its own full-width row.
""", doc('Navigation', 120, 'Segmented', """
<div class="hv-stage hv-col">
  <div class="seg" data-seg><span class="seg__thumb"></span>
    <button aria-pressed="true">@@flame@@Heat</button><button aria-pressed="false">@@leaf@@Eco</button><button aria-pressed="false">@@snow@@Cool</button><button aria-pressed="false">@@auto@@Auto</button>
  </div>
  <div class="seg seg--accent" data-seg><span class="seg__thumb"></span>
    <button aria-pressed="false">Day</button><button aria-pressed="true">Week</button><button aria-pressed="false">Month</button><button aria-pressed="false">Year</button>
  </div>
</div>""", """
var M = Halvo.motion;
document.querySelectorAll('[data-seg]').forEach(function (s) {
  var th = s.querySelector('.seg__thumb');
  s.querySelectorAll('button').forEach(function (b) { b.onclick = function () { s.querySelector('[aria-pressed="true"]').setAttribute('aria-pressed', 'false'); b.setAttribute('aria-pressed', 'true'); M.pill(th, b, { radius: 10 }); }; });
  requestAnimationFrame(function () { M.pill(th, s.querySelector('[aria-pressed="true"]'), { radius: 10, animate: false }); });
});
"""))

# ---------------------------------------------------------------- SideNav
C['SideNav'] = ("""
# SideNav

The floating glass sidebar: app mark, grouped page links with a sliding highlight, and a home switcher at the foot.

**Provide** `.side` (glass) > `.brand` (`.mark` + `.brand__text`) and `.snav` holding `<span class="snav__pill">` then `.snav__sec` groups (`.snav__group` label + `.snav__item` links with a 20px icon, `.snav__label`, optional `.snav__count`). Current item: `aria-current="page"`. Move the highlight with `Halvo.motion.pill(pill, item, {radius: 14})`.

- Panel: sticks at `inset` from the top and is at most the viewport height minus 2 × `inset`; width `side` (256px) or `side-rail` (84px, labels hidden, counts become 8px dots), radius `r-xl`, padding 16 12 12. Hidden below 761px, where the TabBar takes over.
- A long menu scrolls inside `.snav` (no visible scrollbar); the highlight moves with the items and covers the whole scroll area.
- Item: 42px, radius 14, padding-left 20, `fs-md` 600 `ink-2`; icon `muted`, current icon `accent-text`. Highlight: `glass-3` + rim (dark 13% white).
- Counts: `warn` on `warn-soft`, 20px pill.
- Mark: 40px tile, radius 13, gradient 160° `accent-hi` → `accent`, `accent-ink` glyph, `glow` shadow.
- Motion (boot): panel slides in from x −40 (0.9s `expo.out`), then the brand, groups and items from x −12 with 25ms stagger (0.5s `power3.out`), the highlight scales in from 0.4 on x.
""", doc('Navigation', 470, 'SideNav', """
<div class="hv-stage hv-demo" style="display:flex;gap:16px;align-items:flex-start">
  <aside class="side glass" id="side" style="max-height:440px">
    <div class="brand"><span class="mark">@@home@@</span><span class="brand__text"><b>Halvo</b><small>Larch House</small></span></div>
    <nav class="snav" id="snav"><span class="snav__pill"></span>
      <div class="snav__sec"><span class="snav__group">Home</span>
        <button class="snav__item" aria-current="page">@@grid@@<span class="snav__label">Overview</span></button>
        <button class="snav__item">@@home@@<span class="snav__label">Rooms</span></button>
        <button class="snav__item">@@bulb@@<span class="snav__label">Devices</span><span class="snav__count">2</span></button></div>
      <div class="snav__sec"><span class="snav__group">Systems</span>
        <button class="snav__item">@@thermo@@<span class="snav__label">Climate</span></button>
        <button class="snav__item">@@bolt@@<span class="snav__label">Energy</span></button>
        <button class="snav__item">@@shield@@<span class="snav__label">Security</span></button>
        <button class="snav__item">@@music@@<span class="snav__label">Media</span></button></div>
      <div class="snav__sec"><span class="snav__group">More</span>
        <button class="snav__item">@@auto@@<span class="snav__label">Automations</span></button>
        <button class="snav__item">@@users@@<span class="snav__label">Family</span></button>
        <button class="snav__item">@@gear@@<span class="snav__label">Settings</span></button></div>
    </nav>
  </aside>
  <div>""" + REPLAY + """</div>
</div>""", """
var M = Halvo.motion, nav = document.getElementById('snav'), pill = nav.querySelector('.snav__pill');
nav.querySelectorAll('.snav__item').forEach(function (b) { b.onclick = function () { nav.querySelector('[aria-current]').removeAttribute('aria-current'); b.setAttribute('aria-current', 'page'); M.pill(pill, b, { radius: 14 }); }; });
function boot() {
  M.fromTo(document.getElementById('side'), { x: -40, opacity: 0 }, null, { duration: .9, ease: 'expo.out' });
  M.fromTo(document.querySelectorAll('.side .brand, .snav__group, .snav__item'), { opacity: 0, x: -12 }, null, { duration: .5, ease: 'power3.out', stagger: .025, delay: .3 });
  M.fromTo(pill, { opacity: 0, scaleX: .4 }, null, { duration: .6, ease: 'expo.out', delay: .55, origin: '0 50%' });
}
requestAnimationFrame(function () { M.pill(pill, nav.querySelector('[aria-current]'), { radius: 14, animate: false }); boot(); });
document.querySelector('[data-replay]').onclick = boot;
"""))

# ---------------------------------------------------------------- Field
C['Field'] = ("""
# Field

Label, glass input and helper text, stacked with a 7px gap.

**Provide** `<label class="field"><span>Label</span><input class="input"><small>Help</small></label>`. Use `.select` / `select.input` and `.textarea` the same way; wrap with `.inwrap` + a leading `.ico` for search. Mark errors with `input.is-bad` and `small.bad`. Lay fields out in `.formgrid` (2 columns, 14px gap, `span2` for full width; 1 column ≤999px).

- Input: 44px, radius 13, padding 0 14, `glass-2`, 1px inset `line-2`, `fs-base` 500. Placeholder `muted` at 85%.
- Focus: inset 1.5px `accent` + 4px `accent-soft` halo. Error: inset 1.5px `bad`.
- Motion: a rejected submit shakes the field (`shake`, 0.42s) — once, with the message in words.
- Inputs are 16px on phones to stop zoom.
""", doc('Inputs', 270, 'Field', """
<div class="hv-stage"><form class="card" id="f" style="display:grid;grid-template-columns:1fr 1fr;gap:14px" novalidate>
  <label class="field" style="grid-column:1/-1"><span>Search devices</span><span class="inwrap">@@search@@<input class="input" placeholder="Lamp, plug, camera…"></span></label>
  <label class="field"><span>Device name</span><input class="input" value="Arc floor lamp"><small>Shown on tiles and in scenes.</small></label>
  <label class="field"><span>Room</span><select class="input select"><option>Living room</option><option>Kitchen</option><option>Studio</option></select></label>
  <label class="field"><span>Door code</span><input class="input" id="pin" placeholder="4–8 digits"><small id="msg">Guests get their own code.</small></label>
  <div style="display:flex;align-items:flex-end;justify-content:flex-end;gap:8px"><button type="button" class="btn btn--ghost">Cancel</button><button class="btn btn--primary">Save</button></div>
</form></div>""", """
var M = Halvo.motion, pin = document.getElementById('pin'), msg = document.getElementById('msg');
document.getElementById('f').onsubmit = function (e) {
  e.preventDefault();
  var ok = /^\\d{4,8}$/.test(pin.value);
  pin.classList.toggle('is-bad', !ok); msg.className = ok ? '' : 'bad';
  msg.textContent = ok ? 'Saved.' : 'Use 4 to 8 digits.';
  if (!ok) M.shake(pin.closest('.field'));
};
"""))

# ---------------------------------------------------------------- Switch
C['Switch'] = ("""
# Switch

A 44×26 on/off toggle; on is solid teal with a glow, the white knob springs 18px.

**Provide** `<button class="switch" role="switch" aria-checked="false"><i></i></button>` with an accessible name (usually the `.row-set` text beside it). Toggle `aria-checked`, then call `Halvo.motion.switchKnob(el)`.

- Off: `well` track, inset 1px `line-2`. On: `accent` track, `0 0 14px -2px var(--glow)`.
- Knob: 20px white, 3px inset, `0 2px 5px #0000004d`.
- Motion: knob travel 0.45s `back.out(2.2)` — a little overshoot, then rest.
- Settings lists use `.row-set`: title `b` 600, `small` `muted` `fs-sm`, 14px padding, `line` dividers.
- Group related rows in a `.row-group`: a `glass-2` frame (radius `r-md`, padding 2px 16px, `line` outline) that gives the rows their side padding; stack groups `gap` apart, each under a `.section-label`. (Intentional addition: the source only has bare `.row-set` lists.)
""", doc('Inputs', 330, 'Switch', """
<div class="hv-stage"><div class="card">
  <div class="section-label">Arrival</div>
  <div class="row-group">
  <div class="row-set"><div class="row-set__text"><b>Arrival lights</b><small>Hall and porch come on when someone gets home after dark.</small></div><button class="switch" role="switch" aria-checked="true" aria-label="Arrival lights"><i></i></button></div>
  <div class="row-set"><div class="row-set__text"><b>Quiet hours</b><small>No chimes or speaker alerts 22:00–07:00.</small></div><button class="switch" role="switch" aria-checked="false" aria-label="Quiet hours"><i></i></button></div>
  </div>
  <div class="section-label">Comfort</div>
  <div class="row-group">
  <div class="row-set"><div class="row-set__text"><b>Eco heating</b><small>Lets rooms drift 1° when nobody is in.</small></div><button class="switch" role="switch" aria-checked="true" aria-label="Eco heating"><i></i></button></div>
  </div>
</div></div>""", """
document.querySelectorAll('.switch').forEach(function (s) { s.onclick = function () { s.setAttribute('aria-checked', s.getAttribute('aria-checked') !== 'true'); Halvo.motion.switchKnob(s); }; });
"""))

# ---------------------------------------------------------------- Check
C['Check'] = ("""
# Check

A 20px rounded-square checkbox; checked fills `accent` with an `accent-ink` tick.

**Provide** `<button class="check" role="checkbox" aria-checked="false">` + check icon (stroke 2.4) next to its label. Toggle `aria-checked`.

- Unchecked: inset 1.5px `line-2`, radius 6. Checked: `accent` fill, no outline, tick opacity 1.
- Motion: the tick `nudge`s in (0.7 → 1, `back.out(3)`).
""", doc('Inputs', 140, 'Check', """
<div class="hv-stage"><div class="card hv-col" style="gap:10px">
  <label class="hv-row" style="gap:10px"><button class="check" role="checkbox" aria-checked="true" aria-label="Lock all doors">@@check@@</button><span>Lock all doors</span></label>
  <label class="hv-row" style="gap:10px"><button class="check" role="checkbox" aria-checked="true" aria-label="Lights off">@@check@@</button><span>Turn every light off</span></label>
  <label class="hv-row" style="gap:10px"><button class="check" role="checkbox" aria-checked="false" aria-label="Heating">@@check@@</button><span>Drop heating to 16°</span></label>
</div></div>""", """
document.querySelectorAll('.check').forEach(function (c) { c.onclick = function (e) { e.preventDefault(); var on = c.getAttribute('aria-checked') !== 'true'; c.setAttribute('aria-checked', on); if (on) Halvo.motion.nudge(c); }; });
"""))

# ---------------------------------------------------------------- Range
C['Range'] = ("""
# Range

A 10px track with a glowing teal fill and a white 22px knob, value read out on the right.

**Provide** `.range` > `.range__track` (`.range__fill` + `.range__knob`) + a transparent `<input type="range">` laid over it + `<output>`. Drive the fill with `transform: scaleX(v)` and the knob with `translateX(v * 100%)`. `range--compact` drops the output.

- Track `well`, radius 10, inset 1px `line`. Fill: gradient 90° `accent` at 55% → `accent`, `0 0 14px -3px var(--glow)`.
- Knob: white, `0 2px 8px #00000059`, 4px `accent-soft` ring (solid `accent` on keyboard focus).
- Motion: fill and knob follow with `power3.out` (0.3s while dragging, longer when set by a scene).
""", doc('Inputs', 130, 'Range', """
<div class="hv-stage"><div class="card hv-col" style="gap:4px">
  <div class="cell__text"><b>Arc floor lamp</b><small>Brightness</small></div>
  <div class="range" id="r"><span class="range__track"><span class="range__fill"></span><span class="range__knob"></span></span><input type="range" min="0" max="100" value="72" aria-label="Brightness"><output>72%</output></div>
  <div class="hv-row" style="gap:6px"><button class="chip" data-v="20">Dim</button><button class="chip" data-v="60">Evening</button><button class="chip" data-v="100">Bright</button></div>
</div></div>""", """
var M = Halvo.motion, r = document.getElementById('r'), inp = r.querySelector('input'), fill = r.querySelector('.range__fill'), knob = r.querySelector('.range__knob'), out = r.querySelector('output');
var cur = { v: 72 };
function set(v, d) {
  var from = cur.v; cur.v = v;
  M.tweenValue(from, v, { duration: d, ease: 'power3.out' }, function (x) { fill.style.transform = 'scaleX(' + x / 100 + ')'; knob.style.transform = 'translateX(' + x + '%)'; out.textContent = Math.round(x) + '%'; });
}
set(72, 0);
inp.oninput = function () { set(+inp.value, .3); };
document.querySelectorAll('[data-v]').forEach(function (b) { b.onclick = function () { inp.value = b.dataset.v; set(+b.dataset.v, .8); }; });
"""))

# ---------------------------------------------------------------- Stepper
C['Stepper'] = ("""
# Stepper

A compact − value + control for small counts and set points.

**Provide** `.stepper` > `button` (minus), `<output>`, `button.is-add` (plus, teal). Call `Halvo.motion.roll(valueEl, up)` after each change.

- Track `well`, radius 12, padding 3; buttons 30px (38 on touch), radius 9, hover `glass-3`; the plus is `accent` / `accent-ink`.
- Value `fs-md` 700, min width 34.
- Motion: the new value rolls in from the side it came from (±60% y, 0.35s `back.out(2)`).
""", doc('Inputs', 100, 'Stepper', """
<div class="hv-stage hv-row" style="gap:18px">
  <div class="cell__text" style="flex:none"><b>Guests tonight</b><small>Adds codes and lights the porch</small></div>
  <div class="stepper"><button aria-label="Fewer" data-d="-1">@@minus@@</button><output><span id="v">2</span></output><button class="is-add" aria-label="More" data-d="1">@@plus@@</button></div>
</div>""", """
var v = document.getElementById('v'), n = 2;
document.querySelectorAll('[data-d]').forEach(function (b) { b.onclick = function () { var d = +b.dataset.d; if (n + d < 0 || n + d > 12) { Halvo.motion.shake(b.parentElement); return; } n += d; v.textContent = n; Halvo.motion.roll(v, d > 0); }; });
"""))

# ---------------------------------------------------------------- Pill
C['Pill'] = ("""
# Pill

Status and fact labels: `.pill` (24px with a dot), `.badge` (20px count), `.delta` (change), `.live` (breathing dot).

**Provide** `<span class="pill pill--good">Fresh</span>`; tones `--good --warn --bad --info --accent`, or `pill--plain` (no dot) for neutral facts with an icon. Counts: `<span class="badge">3</span>`. Changes: `delta--up` / `delta--down` with an arrow.

- Pill: radius 99, padding 0 9, `fs-xs` 600; neutral = `glass-2` + `line`; toned = `*-soft` fill, `*` text, no outline. The 6px dot is `currentColor`.
- Status is never colour alone: every pill says its state in words.
- `.live`: 8px `good` dot with a 2s `breathe` halo (opacity .08 ↔ .4). `.eq`: four 3px bars on the 1.1s `eq` loop, for what's playing.
""", doc('Status', 120, 'Pill', """
<div class="hv-stage hv-col" style="gap:10px">
  <div class="hv-row" style="gap:6px"><span class="pill pill--good">Fresh</span><span class="pill pill--warn">Filter due</span><span class="pill pill--bad">Offline</span><span class="pill pill--info">Updating</span><span class="pill pill--accent">Scene on</span><span class="pill">Idle</span><span class="pill pill--plain">@@lock|ico ico--sm@@Every door locked</span></div>
  <div class="hv-row" style="gap:10px"><span class="badge">2</span><span class="delta delta--up">↑ 4%</span><span class="delta delta--down">↑ 25%</span><span style="font-size:12px;font-weight:600"><span class="live"></span>live</span><span class="eq"><i></i><i></i><i></i><i></i></span><span class="muted" style="font-size:12px;font-weight:600">Playing in Media room</span></div>
</div>""", """
Halvo.motion.pop(document.querySelectorAll('.pill'), { stagger: .04 });
"""))

# ---------------------------------------------------------------- Avatar
C['Avatar'] = ("""
# Avatar

A round initials badge on a pastel hue, with an optional presence dot; photos fill the same circle.

**Provide** `<span class="av" style="--h:var(--h2)">TO</span>`, sizes `av--sm` 26 / default 34 / `av--lg` 48 / `av--xl` 72. Presence: `<i class="av__dot"></i>` (`good`, ringed in `bg`). Groups: `.avstack` overlaps by 8px with a 2px `bg` ring.

- Initials 700 in `mono-ink` on `h1`–`h6` (same in both themes, so contrast holds).
- Give each person one hue and keep it everywhere.
""", doc('Status', 100, 'Avatar', """
<div class="hv-stage hv-row" style="gap:14px">
  <span class="av av--xl" style="--h:var(--h1)">AL</span>
  <span class="av av--lg" style="--h:var(--h2)">TO<i class="av__dot"></i></span>
  <span class="av" style="--h:var(--h3)">MK<i class="av__dot"></i></span>
  <span class="av av--sm" style="--h:var(--h4)">JB</span>
  <span class="avstack"><span class="av" style="--h:var(--h1)">AL</span><span class="av" style="--h:var(--h2)">TO</span><span class="av" style="--h:var(--h5)">+1</span></span>
</div>""", """
Halvo.motion.pop(document.querySelectorAll('.hv-stage > .av, .avstack .av'), { stagger: .05 });
"""))

# ---------------------------------------------------------------- Meter
C['Meter'] = ("""
# Meter

A thin read-only bar for levels: battery, filter life, air quality, device load.

**Provide** `<span class="meter" role="meter" aria-valuenow="64" aria-valuemin="0" aria-valuemax="100" aria-label="Battery"><i></i></span>` and set the fill with `Halvo.motion.fill(i, 0.64)`. Tones: `is-warn`, `is-bad`.

- 8px tall (5px inside device tiles), radius 8, `well` track, `accent` fill scaled on x from the left.
- Motion: fills to its value in 1s `expo.out` after 0.15s; later changes animate from the old value.
""", doc('Status', 150, 'Meter', """
<div class="hv-stage"><div class="card" style="display:grid;grid-template-columns:auto 1fr auto;gap:12px 14px;align-items:center">
  <span class="muted" style="font-size:12.5px;font-weight:600">Battery</span><span class="meter" role="meter" aria-label="Battery"><i data-v=".64"></i></span><b>64%</b>
  <span class="muted" style="font-size:12.5px;font-weight:600">CO₂</span><span class="meter is-warn" role="meter" aria-label="CO2"><i data-v=".76"></i></span><b>905</b>
  <span class="muted" style="font-size:12.5px;font-weight:600">Filter</span><span class="meter is-bad" role="meter" aria-label="Filter"><i data-v=".12"></i></span><b>12%</b>
  <span></span><span>""" + REPLAY + """</span><span></span>
</div></div>""", """
function play() { document.querySelectorAll('.meter i').forEach(function (i, k) { i.__f = 0; Halvo.motion.fill(i, +i.dataset.v, { delay: .15 + k * .08 }); }); }
document.querySelector('[data-replay]').onclick = play; play();
"""))

# ---------------------------------------------------------------- Toast
C['Toast'] = ("""
# Toast

A dark smoked-glass confirmation that rises at the bottom centre, says what happened, and offers Undo.

**Provide** `.toast` > icon, `<span>` message, optional `<button>Undo</button>`; `is-warn` for cautions. Stack them in a fixed `.toasts` column (bottom 22px, width ≤440px, 8px gap; above the tab bar on phones).

- Always dark in both themes: `#16181cdb` with blur 20px, text `#f1efea`, icon teal `#5fd8c4` (warn `#ffb27e`), radius 16, `shadow-lg`.
- Message: past tense, the thing first — "Film night is on", "Front door locked".
- Motion: in 30px up from 0.94, 0.5s `back.out(1.8)`; out 16px down, 0.25s `power2.in`. Lives 3.2s, 5.5s when it has Undo.
""", doc('Feedback', 210, 'Toast', """
<div class="hv-stage" style="min-height:170px;display:flex;flex-direction:column;align-items:center;gap:12px">
  <div class="hv-row"><button class="btn btn--primary" id="go">Run Film night</button><button class="btn" id="warn">Unlock back door</button></div>
  <div id="stack" style="display:flex;flex-direction:column;gap:8px;align-items:center;width:100%;margin-top:auto"></div>
</div>""", """
var M = Halvo.motion, stack = document.getElementById('stack');
var ICON = { ok: '@@check@@', warn: '@@alert@@' };
function toast(text, warn) {
  var t = document.createElement('div'); t.className = 'toast' + (warn ? ' is-warn' : '');
  t.innerHTML = ICON[warn ? 'warn' : 'ok'] + '<span></span><button>Undo</button>'; t.querySelector('span').textContent = text;
  stack.appendChild(t); while (stack.children.length > 2) stack.firstChild.remove();
  M.toastIn(t);
  var close = function () { M.toastOut(t).then(function () { t.remove(); }); };
  t.querySelector('button').onclick = close; setTimeout(close, 5500);
}
document.getElementById('go').onclick = function () { toast('Film night is on'); };
document.getElementById('warn').onclick = function () { toast('Back door unlocked for 10 minutes', true); };
toast('Front door locked');
"""))

# ---------------------------------------------------------------- Menu
C['Menu'] = ("""
# Menu

A small glass popover of actions anchored under the control that opened it.

**Provide** `.pop` positioned under its anchor, holding `.menu__label`, `.menu__item` buttons (18px `muted` icon + label + optional `.kbd`), `.menu__sep`, and `menu__item--danger` last. Close on Escape, outside click and choice; return focus to the anchor.

- `glass-strong` with `blur-overlay`, rims and `shadow-lg`, radius 18, padding 6, min width 230.
- Item 40px (46 on touch), radius 11, `fs-md` 600; hover/focus `glass-3` (dark 10% white).
- Motion: `popIn` — from 0.92 and −6px, origin at the anchor's centre edge, 0.4s `back.out(2)`; it flips above the anchor when there's no room below.
""", doc('Overlays', 300, 'Menu', """
<div class="hv-stage" style="min-height:270px">
  <div style="position:relative;display:inline-block">
    <button class="btn btn--primary" id="open" aria-haspopup="menu" aria-expanded="false">@@plus@@New</button>
    <div class="pop" id="menu" role="menu" style="position:absolute;top:50px;left:0" hidden>
      <div class="menu__label">Create</div>
      <button class="menu__item" role="menuitem">@@auto@@Scene<span class="kbd">S</span></button>
      <button class="menu__item" role="menuitem">@@sunrise@@Routine<span class="kbd">R</span></button>
      <button class="menu__item" role="menuitem">@@plug@@Device<span class="kbd">D</span></button>
      <div class="menu__sep"></div>
      <button class="menu__item" role="menuitem">@@users@@Invite a guest</button>
      <button class="menu__item menu__item--danger" role="menuitem">@@trash@@Clear history</button>
    </div>
  </div>
</div>""", """
var M = Halvo.motion, b = document.getElementById('open'), m = document.getElementById('menu');
function show() { m.hidden = false; b.setAttribute('aria-expanded', 'true'); M.popIn(m, '40px 0%'); M.slide(m.querySelectorAll('.menu__item'), { y: 6, stagger: .02 }); }
function hide() { m.hidden = true; b.setAttribute('aria-expanded', 'false'); }
b.onclick = function (e) { e.stopPropagation(); m.hidden ? show() : hide(); };
m.onclick = function (e) { e.stopPropagation(); if (e.target.closest('.menu__item')) hide(); };
document.addEventListener('click', hide); document.addEventListener('keydown', function (e) { if (e.key === 'Escape') hide(); });
show();
"""))

# ---------------------------------------------------------------- Modal
C['Modal'] = ("""
# Modal

A centred glass dialog for short, focused tasks; it grows out of the control that opened it.

**Provide** a `.scrim` and a `.modal-wrap` (the fixed layer that centres it) holding the `.modal` (`role="dialog" aria-modal="true"` with a label, a `.sheet__grip` first for phones) holding `.modal__head` (h2 `fs-2xl` 700 + `p` `muted`, close `ibtn--flat`), `.modal__body`, `.modal__foot` (ghost cancel + primary). `modal--wide` is 760px. Trap focus; Escape closes.

- `glass-strong` + `blur-overlay` + rims + `shadow-lg`, radius `r-xl`, width ≤520. Scrim: light `#14120e47`, dark `#00000080`.
- On phones (≤760px) `.modal-wrap` drops it to the bottom as a sheet (radius 26 26 0 0, ≤92dvh) with the grip, and `modalIn` / `modalOut` play the sheet motion.
- Motion: scrim fades 0.3s; dialog `modalIn` from 0.86 with transform-origin at the trigger, 0.5s `back.out(1.5)`; out to 0.94 in 0.2s `power2.in`. Sheets use `sheetIn/Out`.
""", doc('Overlays', 400, 'Modal', """
<div class="hv-stage hv-demo" style="min-height:370px">
  <button class="btn btn--primary" id="open" style="position:absolute;top:20px;left:20px">@@plus@@Add a device</button>
  <div class="scrim" id="scrim" hidden></div>
  <div class="modal-wrap"><div class="modal" id="dlg" role="dialog" aria-modal="true" aria-labelledby="mt" hidden>
    <div class="sheet__grip"><i></i></div>
    <div class="modal__head"><div style="flex:1"><h2 id="mt">Add a device</h2><p>Put it in pairing mode, then pick it below.</p></div><button class="ibtn ibtn--flat ibtn--sm" aria-label="Close" data-close>@@x|ico ico--sm@@</button></div>
    <div class="modal__body"><div class="hv-col" style="gap:6px">
      <div class="well" style="padding:10px 12px;display:flex;gap:12px;align-items:center"><span class="finder__ico">@@bulb@@</span><div class="cell__text"><b>Lumvik bulb E27</b><small>Found 2 seconds ago · strong signal</small></div><span class="pill pill--accent">New</span></div>
      <div class="well" style="padding:10px 12px;display:flex;gap:12px;align-items:center"><span class="finder__ico">@@plug@@</span><div class="cell__text"><b>Smart plug mini</b><small>Found 6 seconds ago</small></div></div>
    </div></div>
    <div class="modal__foot"><button class="btn btn--ghost" data-close>Cancel</button><button class="btn btn--primary" data-close>Add 2 devices</button></div>
  </div></div>
</div>""", """
var M = Halvo.motion, s = document.getElementById('scrim'), d = document.getElementById('dlg'), o = document.getElementById('open');
function open() {
  s.hidden = d.hidden = false;
  var a = o.getBoundingClientRect(), r = d.getBoundingClientRect();
  M.scrimIn(s); M.modalIn(d, (a.left + a.width / 2 - r.left) + 'px ' + (a.top + a.height / 2 - r.top) + 'px');
  M.slide(d.querySelectorAll('.well'), { delay: .15 });
}
function close() { M.scrimOut(s); M.modalOut(d).then(function () { s.hidden = d.hidden = true; d.getAnimations().forEach(function (x) { x.cancel(); }); s.getAnimations().forEach(function (x) { x.cancel(); }); }); }
o.onclick = open; s.onclick = close; d.querySelectorAll('[data-close]').forEach(function (b) { b.onclick = close; });
open();
"""))

# ---------------------------------------------------------------- Drawer
C['Drawer'] = ("""
# Drawer

A tall glass panel that slides in from the right for detail and editing (a device, a person, an event).

**Provide** `.scrim` + `.drawer` (`role="dialog"`) with `.drawer__head` (h2 `fs-3xl` 700, `p` `muted`, close), `.drawer__body` (scrolls), `.drawer__foot`. Inside, device facts use `.facts` tiles and controls use `.row-set`.

- Fixed 12px from the top, right and bottom of the viewport; width ≤460; radius `r-xl`; overlay glass recipe. Head and foot separated by `line`.
- On phones (≤760px) Halvo's CSS turns it into a bottom sheet (full width, ≤92dvh, radius 26 26 0 0); put a `<div class="sheet__grip"><i></i></div>` first inside it (hidden on larger screens).
- Motion: `drawerIn` — x 104% → 0 in 0.6s `expo.out`, scrim 0.3s, body rows `slide` in after; out 0.32s `power3.in`. On phones `drawerIn` / `drawerOut` play the sheet motion (up from the bottom) by themselves.
""", doc('Overlays', 520, 'Drawer', """
<div class="hv-stage hv-demo" style="min-height:490px">
  <button class="btn" id="open">@@bulb@@Arc floor lamp</button>
  <div class="scrim" id="scrim" hidden></div>
  <aside class="drawer" id="dr" role="dialog" aria-modal="true" aria-labelledby="dt" hidden>
    <div class="sheet__grip"><i></i></div>
    <div class="drawer__head"><div style="flex:1"><h2 id="dt">Arc floor lamp</h2><p>Living room · Lumvik · on for 3 h 24 min</p></div><button class="ibtn ibtn--flat ibtn--sm" aria-label="Close" data-close>@@x|ico ico--sm@@</button></div>
    <div class="drawer__body">
      <div class="row-set" data-row><div class="row-set__text"><b>Power</b><small>9 W now</small></div><button class="switch" role="switch" aria-checked="true" aria-label="Power"><i></i></button></div>
      <div class="row-set" data-row><div class="row-set__text"><b>Brightness</b><small>72%</small></div><span class="meter" style="width:120px"><i style="transform:scaleX(.72)"></i></span></div>
      <div class="row-set" data-row><div class="row-set__text"><b>Colour</b><small>2700 K warm white</small></div><span class="chip">Warm</span></div>
      <div class="row-set" data-row><div class="row-set__text"><b>In scenes</b><small>Slow morning, Film night</small></div></div>
    </div>
    <div class="drawer__foot"><button class="btn btn--danger btn--ghost">Remove</button><button class="btn btn--primary" data-close>Done</button></div>
  </aside>
</div>""", """
var M = Halvo.motion, s = document.getElementById('scrim'), d = document.getElementById('dr');
function open() { s.hidden = d.hidden = false; M.scrimIn(s); M.drawerIn(d); M.slide(d.querySelectorAll('[data-row]'), { delay: .12 }); }
function close() { M.scrimOut(s); M.drawerOut(d).then(function () { s.hidden = d.hidden = true; [s, d].forEach(function (e) { e.getAnimations().forEach(function (x) { x.cancel(); }); }); }); }
document.getElementById('open').onclick = open; s.onclick = close; d.querySelectorAll('[data-close]').forEach(function (b) { b.onclick = close; });
d.querySelector('.switch').onclick = function () { this.setAttribute('aria-checked', this.getAttribute('aria-checked') !== 'true'); M.switchKnob(this); };
open();
"""))

# ---------------------------------------------------------------- Finder
C['Finder'] = ("""
# Finder

The ⌘K command palette: one large search field over grouped results for pages, rooms, devices and actions.

**Provide** `.finder` > `.finder__in` (search icon + `input`), `.finder__list` with `.finder__group` labels and `.finder__item` rows (`.finder__ico` 36px tile + `.cell__text` + optional trailing hint), `.finder__foot` with key hints. Selection is `aria-selected="true"`, moved with ↑ ↓, run with ↵.

- 620px wide at 12vh from the top, radius 24, overlay glass. Input `fs-xl` 500, 62px row.
- Items radius 13, padding 8 10; selected `glass-3` (dark 10% white). Group labels 11px uppercase 0.06em.
- Motion: panel drops in from −18px at 0.97 (0.45s `back.out(1.6)`), the first 8 results `slide` 6px with 20ms stagger, again on each new query; out −10px in 0.18s `power2.in`.
""", doc('Overlays', 440, 'Finder', """
<div class="hv-stage" style="min-height:410px;display:flex;justify-content:center;align-items:flex-start">
  <div class="finder" id="fd" role="dialog" aria-label="Search Halvo">
    <div class="finder__in">@@search@@<input id="q" placeholder="Search rooms, devices, scenes…" value="li" aria-label="Search"><span class="kbd">esc</span></div>
    <div class="finder__list" id="list" role="listbox"></div>
    <div class="finder__foot"><span><span class="kbd">↑</span> <span class="kbd">↓</span> move</span><span><span class="kbd">↵</span> open</span></div>
  </div>
</div>""", """
var M = Halvo.motion, list = document.getElementById('list'), q = document.getElementById('q');
var DATA = [['Rooms', 'Living room', 'Ground floor · 2 lights on', 'home'], ['Rooms', 'Garden lounge', 'First floor', 'home'], ['Devices', 'Arc floor lamp', 'Living room · 72%', 'bulb'], ['Devices', 'Beam pendants', 'Living room · off', 'bulb'], ['Devices', 'Living speaker', 'Playing', 'music'], ['Scenes', 'Lights out', 'All lights off, doors locked', 'moon'], ['Scenes', 'Slow morning', 'Blinds up, pendants warm', 'sun']];
var ICO = { home: '@@home@@', bulb: '@@bulb@@', music: '@@music@@', moon: '@@moon@@', sun: '@@sun@@' };
var sel = 0;
function render() {
  var t = q.value.toLowerCase(), rows = DATA.filter(function (d) { return (d[1] + d[2]).toLowerCase().indexOf(t) > -1; }), html = '', g = '';
  rows.forEach(function (d, i) { if (d[0] !== g) { g = d[0]; html += '<div class="finder__group">' + g + '</div>'; } html += '<button class="finder__item" role="option" aria-selected="' + (i === sel) + '"><span class="finder__ico">' + ICO[d[3]] + '</span><span class="cell__text"><b></b><small></small></span></button>'; });
  list.innerHTML = html || '<p class="muted" style="padding:20px;text-align:center">Nothing matches.</p>';
  list.querySelectorAll('.finder__item').forEach(function (el, i) { el.querySelector('b').textContent = rows[i][1]; el.querySelector('small').textContent = rows[i][2]; el.onmouseenter = function () { sel = i; mark(); }; });
  M.slide(Array.prototype.slice.call(list.querySelectorAll('.finder__item'), 0, 8), { y: 6, stagger: .02 });
}
function mark() { list.querySelectorAll('.finder__item').forEach(function (el, i) { el.setAttribute('aria-selected', i === sel); }); }
q.oninput = function () { sel = 0; render(); };
q.onkeydown = function (e) { var n = list.querySelectorAll('.finder__item').length; if (e.key === 'ArrowDown') { sel = (sel + 1) % n; mark(); e.preventDefault(); } if (e.key === 'ArrowUp') { sel = (sel - 1 + n) % n; mark(); e.preventDefault(); } };
render(); M.fromTo(document.getElementById('fd'), { y: -18, scale: .97, opacity: 0 }, null, { duration: .45, ease: 'back.out(1.6)' });
"""))

# ---------------------------------------------------------------- Bars
C['Bars'] = ("""
# Bars

Rounded-capsule column chart for hourly or daily totals; the highlighted column glows.

**Provide** `.bars` > `.bars__grid` (dashed `line-2` rules with `fs-2xs` labels, solid base) and `.bars__cols` of `.bars__col` > `.bars__track` (`.bars__ghost` full height + `.bars__bar` at its value) + `.bars__label`. Mark the current/peak column `is-hi`. `bars--compact` drops the y labels.

- Bars are capsules inset 22% each side (max 46px track), `data` at 50%; `is-hi` is full `data` with `0 0 18px -2px var(--glow)` and an `accent-text` label.
- Ghosts (`well`) show the scale behind every bar.
- Motion: bars `grow` from the base, 0.9s `expo.out`, 30ms stagger. Hover shows a dark `.charttip`.
""", doc('Data', 270, 'Bars', """
<div class="hv-stage"><section class="card">
  <div class="chead"><div class="chead__text"><h3>Energy by hour</h3><p>Today · peak at 19:00</p></div>""" + REPLAY + """</div>
  <div class="bars" style="height:170px">
    <div class="bars__grid"><div><span>2 kW</span></div><div><span>1 kW</span></div><div><span>0</span></div></div>
    <div class="bars__cols" id="cols"></div>
  </div>
</section></div>""", """
var M = Halvo.motion, cols = document.getElementById('cols');
[['07', .35], ['09', .5], ['11', .3], ['13', .42], ['15', .28], ['17', .6], ['19', .92], ['21', .7], ['23', .38]].forEach(function (d) {
  var c = document.createElement('div'); c.className = 'bars__col' + (d[0] === '19' ? ' is-hi' : '');
  c.innerHTML = '<div class="bars__track"><i class="bars__ghost"></i><i class="bars__bar" style="height:' + d[1] * 100 + '%"></i></div><span class="bars__label">' + d[0] + '</span>';
  cols.appendChild(c);
});
function play() { M.grow(cols.querySelectorAll('.bars__bar')); }
document.querySelector('[data-replay]').onclick = play; play();
"""))

# ---------------------------------------------------------------- Area
C['Area'] = ("""
# Area

A smooth line chart with a faint fill, a glowing `data` stroke and an optional dashed comparison line.

**Provide** an `svg.area__svg` with `.area__grid` lines, `path.area__fill`, `path.area__cmp` (comparison, `warm` dashed 4 5), `path.area__line`, and `circle.area__dot` for the hovered point. Add a `.legend` (`i` squares; `i.is-dash` for the comparison).

- Line 2.4px round, `drop-shadow(0 4px 8px var(--glow))`; fill `data` at 14%; grid dashed `line-2`; dot `bg` filled with a 2.5px `data` ring.
- Motion: the line `draw`s itself in 1.1s `power2.inOut`; the fill and dot fade in after.
""", doc('Data', 260, 'Area', """
<div class="hv-stage"><section class="card">
  <div class="chead"><div class="chead__text"><h3>Indoor temperature</h3><p>Last 24 hours</p></div><div class="legend"><span><i></i>Today</span><span><i class="is-dash"></i>Yesterday</span></div>""" + REPLAY + """</div>
  <div class="area"><svg class="area__svg" viewBox="0 0 600 150" preserveAspectRatio="none" style="height:150px">
    <g class="area__grid"><line x1="0" x2="600" y1="10" y2="10"/><line x1="0" x2="600" y1="75" y2="75"/><line x1="0" x2="600" y1="140" y2="140" style="stroke-dasharray:none"/></g>
    <path class="area__fill" id="fill" d="M0 110 C 60 108, 90 120, 150 112 S 240 60, 300 58 S 400 80, 450 70 S 540 30, 600 34 L600 140 L0 140Z"/>
    <path class="area__cmp" d="M0 118 C 70 116, 110 124, 170 118 S 260 84, 320 82 S 420 96, 470 90 S 550 64, 600 66"/>
    <path class="area__line" id="line" d="M0 110 C 60 108, 90 120, 150 112 S 240 60, 300 58 S 400 80, 450 70 S 540 30, 600 34"/>
    <circle class="area__dot" id="dot" cx="450" cy="70" r="5"/>
  </svg></div>
</section></div>""", """
var M = Halvo.motion;
function play() { M.draw(document.getElementById('line')); M.fromTo(document.getElementById('fill'), { opacity: 0 }, null, { duration: .8, delay: .6, ease: 'power2.out' }); M.pop(document.getElementById('dot'), { delay: 1 }); }
document.querySelector('[data-replay]').onclick = play; play();
"""))

# ---------------------------------------------------------------- Ring
C['Ring'] = ("""
# Ring

A round progress gauge with a figure in the middle, for shares of a whole (solar cover, battery, goals).

**Provide** `.ring` sized by width/height with an `svg` (`circle.ring__track` + `circle.ring__arc`, rotated −90° so it starts at 12 o'clock) and `.ring__in` holding the figure and caption.

- Track `well`, arc `data` with round caps; stroke width about 10% of the diameter.
- Figure in `ink` 600, caption `fs-2xs` `muted`.
- Motion: the arc draws to its value (stroke offset, 1.2s `power3.out`) while the figure counts up.
""", doc('Data', 170, 'Ring', """
<div class="hv-stage hv-row" style="gap:28px">
  <div class="ring" style="width:118px;height:118px"><svg viewBox="0 0 120 120"><circle class="ring__track" cx="60" cy="60" r="52" stroke-width="11"/><circle class="ring__arc" data-v=".74" cx="60" cy="60" r="52" stroke-width="11" transform="rotate(-90 60 60)"/></svg><div class="ring__in"><b style="font-size:22px;font-weight:600" data-n="74">74</b><b style="font-size:13px">%</b><br><small class="muted" style="font-size:11px;font-weight:600">roof cover</small></div></div>
  <div class="ring" style="width:92px;height:92px"><svg viewBox="0 0 120 120"><circle class="ring__track" cx="60" cy="60" r="50" stroke-width="13"/><circle class="ring__arc" data-v=".64" style="stroke:var(--s3)" cx="60" cy="60" r="50" stroke-width="13" transform="rotate(-90 60 60)"/></svg><div class="ring__in"><b style="font-size:17px;font-weight:600" data-n="64">64</b><b style="font-size:12px">%</b><br><small class="muted" style="font-size:11px;font-weight:600">battery</small></div></div>
  """ + REPLAY + """
</div>""", """
var M = Halvo.motion;
function play() {
  document.querySelectorAll('.ring__arc').forEach(function (c, i) {
    var len = 2 * Math.PI * c.r.baseVal.value, v = +c.dataset.v; c.style.strokeDasharray = len;
    M.tweenValue(0, v, { duration: 1.2, delay: i * .1, ease: 'power3.out' }, function (x) { c.style.strokeDashoffset = len * (1 - x); });
  });
  document.querySelectorAll('[data-n]').forEach(function (el, i) { M.countTo(el, +el.dataset.n, null, { from: 0, delay: i * .1 }); });
}
document.querySelector('[data-replay]').onclick = play; play();
"""))

# ---------------------------------------------------------------- Device
C['Device'] = ("""
# Device

A glass tile per device: icon, room and name, live state; when on, the icon turns teal and a soft teal light spills from the top-left corner.

**Provide** `<button class="dev card" data-lift>` (or `.glass`) > `.dev__top` (`.dev__ico` + a `.switch` or `.pill`), `.dev__name` (`small` room, `b` name), `.dev__state` (state text + optional 5px `.meter`). Add `is-on` when running and `is-off-line` when unreachable. Grid: `.devs` (auto-fill, min 200px; 2 columns on phones).

- Tile: `r-lg`, padding 16, min height 164. On: corner radial of `accent-soft`, fill `#302c2694` (dark) / `#ffffffbd` (light); icon `accent` / `accent-ink` with a 22px `glow`.
- Offline: 72% opacity, icon in `bad`, state says "Offline".
- Motion: tiles `deal` in (y 40, ±2.5°, 0.85s `back.out(1.4)`, 70ms stagger), `lift` on hover, and the icon `nudge`s when toggled.
""", doc('Data', 250, 'Device', """
<div class="hv-stage"><div class="devs" style="grid-template-columns:repeat(4,minmax(0,1fr))">
  <button class="dev glass is-on" data-lift><div class="dev__top"><span class="dev__ico">@@bulb@@</span><span class="switch" role="switch" aria-checked="true"><i></i></span></div><div class="dev__name"><small>Living room</small><b>Arc floor lamp</b></div><div class="dev__state"><span>72%</span><span class="meter"><i style="transform:scaleX(.72)"></i></span></div></button>
  <button class="dev glass" data-lift><div class="dev__top"><span class="dev__ico">@@bulb@@</span><span class="switch" role="switch" aria-checked="false"><i></i></span></div><div class="dev__name"><small>Living room</small><b>Beam pendants</b></div><div class="dev__state"><span>Off</span></div></button>
  <button class="dev glass is-on" data-lift><div class="dev__top"><span class="dev__ico">@@speaker@@</span><span class="eq"><i></i><i></i><i></i><i></i></span></div><div class="dev__name"><small>Media room</small><b>Living speaker</b></div><div class="dev__state"><span>Playing · 38%</span></div></button>
  <button class="dev glass is-off-line" data-lift><div class="dev__top"><span class="dev__ico">@@video@@</span><span class="pill pill--bad">Offline</span></div><div class="dev__name"><small>Garden</small><b>Side gate camera</b></div><div class="dev__state"><span>Last seen 14:02</span></div></button>
</div></div>""", """
var M = Halvo.motion; M.lift();
document.querySelectorAll('.dev').forEach(function (d) { var sw = d.querySelector('.switch'); if (!sw) return; d.onclick = function () { var on = !d.classList.contains('is-on'); d.classList.toggle('is-on', on); sw.setAttribute('aria-checked', on); M.switchKnob(sw); M.nudge(d.querySelector('.dev__ico')); d.querySelector('.dev__state span').textContent = on ? '100%' : 'Off'; }; });
M.deal(document.querySelectorAll('.dev'));
"""))
