# -*- coding: utf-8 -*-
REPLAY = '<button class="btn btn--sm btn--ghost" data-replay>@@play|ico ico--sm@@Replay</button>'

# ---------------------------------------------------------------- Field (custom select)
C['Field'] = ("""
# Field

Label, glass input and helper text, stacked with a 7px gap.

**Provide** `<label class="field"><span>Label</span><input class="input"><small>Help</small></label>`. Dropdowns are a `<select class="input" data-hv-select>` in the same slot, enhanced by `Halvo.ui.selects()` into the glass **Select**; `.textarea` works the same way. Wrap with `.inwrap` + a leading `.ico` for search. Mark errors with `input.is-bad` and `small.bad`. Lay fields out in `.formgrid` (2 columns, 14px gap, `span2` for full width; 1 column ≤999px).

- Input: 44px, radius 13, padding 0 14, `glass-2`, 1px inset `line-2`, `fs-base` 500. Placeholder `muted` at 85%.
- Focus: inset 1.5px `accent` + 4px `accent-soft` halo. Error: inset 1.5px `bad`.
- Motion: a rejected submit shakes the field (`shake`, 0.42s) — once, with the message in words.
- Inputs are 16px on phones to stop zoom. Never ship a bare native `<select>`: always enhance it.
""", doc('Inputs', 480, 'Field', """
<div class="hv-stage" style="min-height:460px"><form class="card" id="f" style="display:grid;grid-template-columns:1fr 1fr;gap:14px" novalidate>
  <label class="field" style="grid-column:1/-1"><span>Search devices</span><span class="inwrap">@@search@@<input class="input" placeholder="Lamp, plug, camera…"></span></label>
  <label class="field"><span>Device name</span><input class="input" value="Arc floor lamp"><small>Shown on tiles and in scenes.</small></label>
  <label class="field"><span>Room</span><select class="input" data-hv-select name="room">
    <optgroup label="Ground floor"><option selected>Living room</option><option>Kitchen</option><option>Media room</option></optgroup>
    <optgroup label="First floor"><option>Studio</option><option>Garden lounge</option></optgroup>
  </select><small>Moves it to that room's tiles.</small></label>
  <label class="field"><span>Door code</span><input class="input" id="pin" placeholder="4–8 digits"><small id="msg">Guests get their own code.</small></label>
  <div style="display:flex;align-items:flex-end;justify-content:flex-end;gap:8px"><button type="button" class="btn btn--ghost">Cancel</button><button class="btn btn--primary">Save</button></div>
</form></div>""", """
var M = Halvo.motion, pin = document.getElementById('pin'), msg = document.getElementById('msg');
Halvo.ui.selects();
document.getElementById('f').onsubmit = function (e) {
  e.preventDefault();
  var ok = /^\\d{4,8}$/.test(pin.value);
  pin.classList.toggle('is-bad', !ok); msg.className = ok ? '' : 'bad';
  msg.textContent = ok ? 'Saved.' : 'Use 4 to 8 digits.';
  if (!ok) M.shake(pin.closest('.field'));
};
"""))

# ---------------------------------------------------------------- Select
C['Select'] = ("""
# Select

A glass dropdown: the trigger looks like an input, the options open in a frosted listbox with a tick on the chosen one.

**Provide** an ordinary `<select class="input" data-hv-select>` (with `<optgroup>`s if useful; `data-hint` on an `<option>` adds a second line; an empty-value first option acts as a placeholder) and call `Halvo.ui.selects(root)` once, or `Halvo.ui.select(el)` for one. Add `select--sm` for the 34px toolbar size. The native element stays in the form, hidden, so `value`, `name`, `required` and `change` events keep working; call `.refresh()` on the returned object after changing its options.

- Trigger: the `.input` recipe plus a 16px chevron in `muted`; open = `glass-3` with the accent focus ring, chevron turned 180° (0.3s `power3.out`). Placeholder text is `muted`.
- List: `.pop` glass (`glass-strong`, `blur-overlay`, `shadow-lg`, radius 18, padding 6), 6px from the trigger, at least as wide, max 288px tall then scrolls. It flips above the trigger when there is no room below.
- Options: `menu__item` rows (40px, radius 11, `fs-md` 600). Active row `glass-3` (dark 10% white); selected row in `ink` with an `accent-text` tick. Group labels are 11px uppercase `muted`.
- Keyboard: ↓ ↑ Enter / Space open; arrows, Home, End move; Enter / Space choose; Esc closes and returns focus; typing jumps to a match.
- Motion: list `popIn` (0.92 → 1, −6px, 0.4s `back.out(2)`), first 8 options `slide` 6px with 20ms stagger; close 0.15s `power2.in`; the new value rolls into the trigger (`roll`, 0.35s `back.out(2)`).

**Intentional addition:** Halvo itself styles the native `<select>` (a CSS chevron on `select.input`, still used as the no-JS fallback). The custom listbox was added so open menus match the glass system.
""", doc('Inputs', 440, 'Select', """
<div class="hv-stage" style="min-height:410px"><div class="card" style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;align-items:start">
  <label class="field"><span>Heating mode</span><select class="input" data-hv-select>
    <option value="heat" data-hint="Hold the set point" selected>Heat</option>
    <option value="eco" data-hint="Drift 1° when nobody is in">Eco</option>
    <option value="cool" data-hint="Air conditioning on">Cool</option>
    <option value="auto" data-hint="Follow the heating plan">Auto</option>
    <option value="off" disabled>Off (locked by schedule)</option>
  </select></label>
  <label class="field"><span>Room</span><select class="input" data-hv-select>
    <option value="" selected>Choose a room</option>
    <optgroup label="Ground floor"><option>Living room</option><option>Kitchen</option><option>Media room</option></optgroup>
    <optgroup label="First floor"><option>Studio</option><option>Garden lounge</option></optgroup>
  </select><small id="out">Nothing chosen yet.</small></label>
  <div class="field"><span>Sort</span><select class="input select--sm" data-hv-select aria-label="Sort devices">
    <option>Most used</option><option>Name A–Z</option><option>Room</option><option>Power draw</option>
  </select></div>
</div></div>""", """
Halvo.ui.selects();
document.querySelectorAll('select')[1].addEventListener('change', function (e) { document.getElementById('out').textContent = 'Moves to ' + e.target.value + '.'; });
"""))

# ---------------------------------------------------------------- Dial
C['Dial'] = ("""
# Dial

The thermostat: a 270° ring of 81 ticks that light from cool to warm up to the set point, a white knob you drag, and the set point in big type.

**Provide** an empty `<div class="dial">` (add `dial--md` for the 250px card size) and call `Halvo.ui.dial(el, {value, indoor, min: 10, max: 30, step: 0.5, mode: 'heat' | 'cool' | 'eco' | 'auto', on, onChange})`. It returns `{value, set(v), setIndoor(v), setMode(m), setOn(b), replay()}`. Pair it with a `.seg` for the mode.

- Geometry (300 viewBox): face r 110 (`glass-2`, dark 18% black), ticks at r 134, every 8th tick major (20px, 2.8px stroke) else 13px / 2.2px. Lit ticks mix `cool` → `warm` along the ring (`--t`) with a 3px glow; off = all `line-2`.
- Indoor reading: a small `ink` triangle on the ring. Knob: white 22px disc with an `accent` dot and drop shadow.
- Read-out: mode in 12px uppercase `accent-text`, figure `dial-figure` (64px, −0.04em) with `°C` in `fs-xl` `muted`, then "Indoors 21° · warming" in `fs-sm` `muted`.
- Input: drag on the ring (the centre 30% is a dead zone), arrow keys, or the round − / + buttons, in 0.5° steps. It is a `role="slider"` with a spoken value.
- Motion: on mount the ticks fade in one after another (0.5s, 9ms stagger), the knob sweeps from 10° to the set point and the figure counts up with it (1.5s `expo.out`). Dragging follows in 0.12s `power2.out`; buttons and keys swing the knob with 0.7s `back.out(1.6)` and count the figure in 0.5s.
""", doc('Inputs', 420, 'Dial', """
<div class="hv-stage"><section class="card" style="display:grid;grid-template-columns:1fr 300px;gap:20px;align-items:center">
  <div class="hv-col">
    <div class="chead" style="margin:0"><div class="chead__text"><h3>Climate</h3><p>Whole house · outside 9.5°</p></div></div>
    <div class="seg seg--accent" id="mode"><span class="seg__thumb"></span>
      <button aria-pressed="true" data-m="heat">@@flame@@Heat</button><button aria-pressed="false" data-m="eco">@@leaf@@Eco</button><button aria-pressed="false" data-m="cool">@@snow@@Cool</button><button aria-pressed="false" data-m="auto">@@auto@@Auto</button>
    </div>
    <div class="row-set" style="padding:6px 0;border:0"><div class="row-set__text"><b>Heating</b><small>Turn the dial or use − / +</small></div><button class="switch" role="switch" aria-checked="true" aria-label="Heating" id="on"><i></i></button></div>
    <div>""" + REPLAY + """</div>
  </div>
  <div class="dial" id="dial"></div>
</section></div>""", """
var M = Halvo.motion, d = Halvo.ui.dial(document.getElementById('dial'), { value: 21.5, indoor: 21, mode: 'heat' });
var seg = document.getElementById('mode'), th = seg.querySelector('.seg__thumb');
seg.querySelectorAll('button').forEach(function (b) { b.onclick = function () { seg.querySelector('[aria-pressed="true"]').setAttribute('aria-pressed', 'false'); b.setAttribute('aria-pressed', 'true'); M.pill(th, b, { radius: 10 }); d.setMode(b.dataset.m); }; });
requestAnimationFrame(function () { M.pill(th, seg.querySelector('[aria-pressed="true"]'), { radius: 10, animate: false }); });
var sw = document.getElementById('on'); sw.onclick = function () { var on = sw.getAttribute('aria-checked') !== 'true'; sw.setAttribute('aria-checked', on); M.switchKnob(sw); d.setOn(on); };
document.querySelector('[data-replay]').onclick = function () { d.replay(); };
"""))

# ---------------------------------------------------------------- Table
C['Table'] = ("""
# Table

Plain data rows inside a flush card: small muted headers, 600-weight cells, hairline dividers, a soft hover on clickable rows.

**Provide** `.card.card--flush` > `.chead` + `.table-wrap` > `table.table`. Put an icon tile + `.cell__text` (`b` + `small`) in the first column with `.cell`; numbers right-aligned with `.r`; status as a `.pill`. Clickable rows get `tr.is-click`. Add `table--stack` so that on phones each row becomes a two-line card using `m-main`, `m-end`, `m-sub`, `m-tag` cells.

- Head: `fs-xs` 600 `muted`, padding 10 14. Cells: `fs-md` 600 (secondary cells `td.muted` at 500), padding 12 14, `line` dividers, none under the last row.
- Hover: `glass-2` behind the whole row.
- Motion: rows `slide` in (12px, 40ms stagger) when the table first shows or its filter changes.
""", doc('Data', 330, 'Table', """
<div class="hv-stage"><section class="card card--flush">
  <div class="chead"><div class="chead__text"><h3>Plugs &amp; power</h3><p>5 devices · 312 W now</p></div><select class="input select--sm" data-hv-select aria-label="Sort" style="width:150px"><option>Most power</option><option>Name A–Z</option><option>Room</option></select></div>
  <div class="table-wrap"><table class="table">
    <thead><tr><th>Device</th><th>Room</th><th class="r">Now</th><th class="r">Today</th><th>Status</th></tr></thead>
    <tbody id="rows">
      <tr class="is-click"><td><div class="cell"><span class="feed__ico tone--accent">@@plug|ico ico--sm@@</span><div class="cell__text"><b>Dishwasher</b><small>Bosch · eco 50°</small></div></div></td><td class="muted">Kitchen</td><td class="r">186 W</td><td class="r">0.82 kWh</td><td><span class="pill pill--accent">Running</span></td></tr>
      <tr class="is-click"><td><div class="cell"><span class="feed__ico tone--plain">@@tv|ico ico--sm@@</span><div class="cell__text"><b>Media wall</b><small>TV + soundbar</small></div></div></td><td class="muted">Media room</td><td class="r">74 W</td><td class="r">0.41 kWh</td><td><span class="pill pill--good">On</span></td></tr>
      <tr class="is-click"><td><div class="cell"><span class="feed__ico tone--plain">@@plug|ico ico--sm@@</span><div class="cell__text"><b>Desk strip</b><small>Studio</small></div></div></td><td class="muted">Studio</td><td class="r">52 W</td><td class="r">0.33 kWh</td><td><span class="pill pill--good">On</span></td></tr>
      <tr class="is-click"><td><div class="cell"><span class="feed__ico tone--plain">@@fan|ico ico--sm@@</span><div class="cell__text"><b>Air purifier</b><small>Filter 12%</small></div></div></td><td class="muted">Living room</td><td class="r">0 W</td><td class="r">0.09 kWh</td><td><span class="pill pill--warn">Filter due</span></td></tr>
    </tbody>
  </table></div>
</section></div>""", """
Halvo.ui.selects();
Halvo.motion.slide(document.querySelectorAll('#rows tr'));
"""))

# ---------------------------------------------------------------- Empty
C['Empty'] = ("""
# Empty

What a card shows when there is nothing yet: a quiet icon tile, one line saying what's missing, one line saying what to do, and at most one button.

**Provide** `.empty` > `.empty__icon` (54px tile, radius 17, `glass-2` + `line`, 20–26px icon in `ink-2`), `b` title, `p` help, optional `.btn`.

- Centred, padding 40 20, gap 8. Title `fs-lg` 600 `ink`; help `fs-sm` `muted`, max 36ch.
- Write it as a fact and a next step: "No cameras yet" / "Add one and its live view shows up here." Never "Oops" or blame.
- Motion: the tile `pop`s in and the text `slide`s after it.
""", doc('Status', 270, 'Empty', """
<div class="hv-stage"><section class="card"><div class="empty" id="e">
  <span class="empty__icon">@@video@@</span>
  <b>No cameras yet</b>
  <p>Add one and its live view and motion alerts show up here.</p>
  <button class="btn btn--primary btn--sm">@@plus@@Add a camera</button>
</div><div style="text-align:center">""" + REPLAY + """</div></section></div>""", """
var M = Halvo.motion, e = document.getElementById('e');
function play() { M.pop(e.querySelector('.empty__icon')); M.slide(e.querySelectorAll('b, p, .btn'), { delay: .15 }); }
document.querySelector('[data-replay]').onclick = play; play();
"""))

# ---------------------------------------------------------------- Heatmap
C['Heatmap'] = ("""
# Heatmap

A day × hour grid of rounded cells whose teal deepens with the value, for when-is-it-busy questions (energy by hour, motion by hour).

**Provide** `.heat` with `grid-template-columns: auto repeat(<cols>, minmax(0, 1fr))`: an empty corner, `.heat__col` labels, then per row a `.heat__row` label and `.heat__cell`s each holding an `<i>` whose background is `color-mix(in oklab, var(--data) <14 + v·86>%, var(--glass-3))`. Mark the peak `is-peak`. Show a `.charttip` on hover.

- Cells: aspect 1.5, radius 6, 4px gaps. Peak ring: 2px `bg` gap + 2px `data`.
- Labels `fs-2xs` / `fs-xs` 600 `muted`. Always state the scale in a legend or caption.
- Motion: cells pop from 0 as a wave from the top-left cell (0.6s `back.out(2.2)`, 12ms per cell of distance) — `Halvo.motion.gridPop(cells, cols)`.
""", doc('Data', 330, 'Heatmap', """
<div class="hv-stage"><section class="card">
  <div class="chead"><div class="chead__text"><h3>When the house uses power</h3><p>Average kWh by weekday and hour · peak Sunday 19:00</p></div>""" + REPLAY + """</div>
  <div class="heat" id="heat"></div>
</section></div>""", """
var heat = document.getElementById('heat'), days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], hours = ['00', '02', '04', '06', '08', '10', '12', '14', '16', '18', '20', '22'];
heat.style.gridTemplateColumns = 'auto repeat(' + hours.length + ', minmax(0, 1fr))';
var html = '<span></span>' + hours.map(function (h) { return '<span class="heat__col">' + h + '</span>'; }).join('');
var cells = [];
days.forEach(function (d, r) {
  html += '<span class="heat__row">' + d + '</span>';
  hours.forEach(function (h, c) {
    var base = [.12, .08, .06, .22, .48, .3, .34, .28, .36, .72, .62, .3][c], v = Math.min(1, base + (r > 4 ? .18 : 0) * (c > 3 && c < 10 ? 1 : .4) + ((r * 7 + c * 3) % 5) * .02);
    var peak = r === 6 && c === 9; if (peak) v = 1;
    html += '<span class="heat__cell' + (peak ? ' is-peak' : '') + '" data-tip="' + (v * 1.6).toFixed(2) + ' kWh|' + d + ' · ' + h + ':00"><i style="background:color-mix(in oklab, var(--data) ' + Math.round(14 + v * 86) + '%, var(--glass-3))"></i></span>';
  });
});
heat.innerHTML = html;
heat.querySelectorAll('.heat__cell').forEach(function (c) {
  c.onpointerenter = function () { var t = c.dataset.tip.split('|'), tip = document.createElement('span'); tip.className = 'charttip'; tip.innerHTML = '<b></b><small></small>'; tip.querySelector('b').textContent = t[0]; tip.querySelector('small').textContent = t[1]; c.appendChild(tip); };
  c.onpointerleave = function () { var t = c.querySelector('.charttip'); if (t) t.remove(); };
});
function play() { Halvo.motion.gridPop(heat.querySelectorAll('.heat__cell i'), hours.length); }
document.querySelector('[data-replay]').onclick = play; play();
"""))

# ---------------------------------------------------------------- Feed
C['Feed'] = ("""
# Feed

A chronological activity log: tinted icon tile, what happened, and when / who in muted text.

**Provide** `.feed` > `.feed__row` > `.feed__ico.tone--*` (34px, radius 11, 17px icon) + `.feed__text` (`b`, `small`) + optional trailing time or `.pill`. Tones: `tone--good` (locked, arrived), `tone--warn` (left open), `tone--bad` (alarm, offline), `tone--info` (updates), `tone--accent` (scenes and automations), `tone--plain` (everything else).

- Rows padding 10 0 with `line` dividers. Title `fs-md` 600, detail `fs-xs` `muted`.
- Write entries as past-tense facts with the actor: "Front door locked · by Amara", "Motion at the side gate".
- Motion: rows `slide` in 12px with 40ms stagger; a new entry arriving live slides in at the top and its icon `pop`s.
""", doc('Data', 330, 'Feed', """
<div class="hv-stage"><section class="card">
  <div class="chead"><div class="chead__text"><h3>Activity</h3><p>Today</p></div><button class="btn btn--sm" id="add">Simulate event</button></div>
  <div class="feed" id="feed">
    <div class="feed__row"><span class="feed__ico tone--good">@@lock@@</span><div class="feed__text"><b>Front door locked</b><small>by Amara · 19:38</small></div></div>
    <div class="feed__row"><span class="feed__ico tone--accent">@@auto@@</span><div class="feed__text"><b>Evening scene ran</b><small>Automation · 19:30</small></div></div>
    <div class="feed__row"><span class="feed__ico tone--warn">@@door@@</span><div class="feed__text"><b>Back door left open 5 min</b><small>Kitchen · 18:52</small></div></div>
    <div class="feed__row"><span class="feed__ico tone--plain">@@users@@</span><div class="feed__text"><b>Theo arrived home</b><small>18:20</small></div></div>
  </div>
</section></div>""", """
var M = Halvo.motion, feed = document.getElementById('feed');
M.slide(feed.children);
document.getElementById('add').onclick = function () {
  var r = document.createElement('div'); r.className = 'feed__row';
  r.innerHTML = '<span class="feed__ico tone--bad">@@alert@@</span><div class="feed__text"><b>Motion at the side gate</b><small>Camera · just now</small></div>';
  feed.insertBefore(r, feed.firstChild); if (feed.children.length > 5) feed.lastChild.remove();
  M.slide(r, { y: -12 }); M.pop(r.querySelector('.feed__ico'), { delay: .1 });
};
"""))

# ---------------------------------------------------------------- Notices
C['Notices'] = ("""
# Notices

The notifications popover under the bell: a short list of what needs attention, unread ones marked with a glowing teal dot.

**Provide** `.pop.notices` > `.notices__head` (`b` "Notifications" + a `.linkbtn` "Mark all read") and `.notices__list` of `button.notice` (`.notice__ico.tone--*` 36px + `.notice__text` with `b`, `p`, `small` time). Add `is-unread`. Anchor it under the bell `.ibtn` and update its `.ibtn__badge`.

- Width ≤380, overlay glass, radius 18, list max 420px tall. Rows radius 13, padding 10, hover `glass-2`.
- Unread dot: 7px `accent` with an 8px `glow`, after the title.
- Motion: opens with `popIn` from the bell; rows rise 8px with 40ms stagger after 80ms (0.45s `power3.out`). A new notice rings the bell (`ring`) and pops the badge. "Mark all read" removes the dots and the badge pops away.
""", doc('Overlays', 420, 'Notices', """
<div class="hv-stage" style="min-height:400px;display:flex;flex-direction:column;align-items:flex-end;gap:8px">
  <button class="ibtn" aria-label="Notifications" id="bell">@@bell@@<span class="ibtn__badge" id="badge">2</span></button>
  <div class="pop notices" id="pop">
    <div class="notices__head"><b>Notifications</b><button class="linkbtn" id="read">Mark all read</button></div>
    <div class="notices__list" id="list">
      <button class="notice is-unread"><span class="notice__ico tone--warn">@@fan@@</span><span class="notice__text"><b>Purifier filter at 12%</b><p>Order a new one before it stops cleaning.</p><small>12 min ago</small></span></button>
      <button class="notice is-unread"><span class="notice__ico tone--bad">@@video@@</span><span class="notice__text"><b>Side gate camera offline</b><p>Last seen 14:02. Check its power.</p><small>5 h ago</small></span></button>
      <button class="notice"><span class="notice__ico tone--good">@@sun@@</span><span class="notice__text"><b>Roof covered 74% of today</b><p>Battery is at 64% going into the evening.</p><small>Today</small></span></button>
    </div>
  </div>
</div>""", """
var M = Halvo.motion, pop = document.getElementById('pop'), bell = document.getElementById('bell'), badge = document.getElementById('badge');
function open() { pop.hidden = false; M.popIn(pop, '92% 0%'); M.fromTo(pop.querySelectorAll('.notice'), { opacity: 0, y: 8 }, null, { duration: .45, ease: 'power3.out', stagger: .04, delay: .08 }); }
bell.onclick = function () { if (pop.hidden) open(); else pop.hidden = true; };
document.getElementById('read').onclick = function () { pop.querySelectorAll('.is-unread').forEach(function (n) { n.classList.remove('is-unread'); }); M.fromTo(badge, { scale: 1 }, { scale: 0 }, { duration: .25, ease: 'power2.in', keep: true }); };
open(); setTimeout(function () { M.ring(bell.querySelector('svg'), badge); }, 700);
"""))

# ---------------------------------------------------------------- TabBar
C['TabBar'] = ("""
# TabBar

The phone navigation (≤760px): a floating glass bar of five destinations at the bottom, the current one on a solid teal pill that slides.

**Provide** `nav.tabbar.glass` > `<span class="tabbar__pill">` + five links (icon + 11px label), the current with `aria-current="page"`. Halvo's CSS fixes it 10px from the sides and bottom (plus the safe-area inset) below 761px and hides it above; put `tabbar-space` on the page container so the last content clears it. Call `Halvo.motion.pill(pill, current, {radius: 18})`, again without animation on resize. The fifth slot is "More" and opens the all-pages sheet.

- Bar: radius 26, padding 6, five equal columns. Items 54px (44 in landscape), radius 18, `fs-2xs` 600 `muted`; current `accent-ink` on `accent`.
- It replaces the sidebar below 761px (`.side` hides itself there); the top bar keeps search and the profile.
- Motion: on load it slides up 90px (0.7s `expo.out`); the pill moves like the tabs pill.
""", doc('Navigation', 150, 'TabBar', """
<div class="hv-stage hv-demo" style="display:flex;justify-content:center">
  <nav class="tabbar glass" id="tb" aria-label="Quick" style="width:390px">
    <span class="tabbar__pill"></span>
    <a href="#" aria-current="page">@@grid@@Home</a>
    <a href="#">@@home@@Rooms</a>
    <a href="#">@@thermo@@Climate</a>
    <a href="#">@@shield@@Security</a>
    <a href="#">@@gear@@More</a>
  </nav>
</div>""", """
var M = Halvo.motion, tb = document.getElementById('tb'), pill = tb.querySelector('.tabbar__pill');
tb.querySelectorAll('a').forEach(function (a) { a.onclick = function (e) { e.preventDefault(); tb.querySelector('[aria-current]').removeAttribute('aria-current'); a.setAttribute('aria-current', 'page'); M.pill(pill, a, { radius: 18 }); M.nudge(a); }; });
requestAnimationFrame(function () { M.pill(pill, tb.querySelector('[aria-current]'), { radius: 18, animate: false }); M.fromTo(tb, { y: 90 }, null, { duration: .7, ease: 'expo.out' }); });
"""))

# ---------------------------------------------------------------- SignIn
C['SignIn'] = ("""
# SignIn

The sign-in card over the home photo: large app mark, greeting, two fields, one button.

**Provide** `.signin` (fills the screen, centres its child) > `.signin__card` with `.mark.mark--lg`, `h1`, `p`, `.signin__fields` (`.field`s) and a `btn--primary btn--lg btn--block`.

- Card: overlay glass (`glass-strong`, `blur-overlay`, rims, `shadow-lg`), radius `r-xl`, padding 32, width ≤420. Mark 56px, radius 18. Title 30px 600 −0.025em; lead `muted`.
- Copy: "Welcome home" / "Sign in to Larch House." Errors say what to fix, under the field.
- Motion: the card's children rise 18px with 60ms stagger (0.6s `expo.out`). A wrong password shakes the fields; success scales the card to 0.96 and fades it (0.3s `power2.in`), then a toast greets the person by first name.
""", doc('Overlays', 500, 'SignIn', """
<div class="hv-stage" style="min-height:480px;display:grid">
  <div class="signin"><form class="signin__card" id="card" novalidate>
    <span class="mark mark--lg">@@home@@</span>
    <h1>Welcome home</h1>
    <p>Sign in to Larch House.</p>
    <div class="signin__fields" id="fields">
      <label class="field"><span>Email</span><input class="input" type="email" value="amara@larch.house" autocomplete="off"></label>
      <label class="field"><span>Password</span><input class="input" type="password" id="pw" placeholder="Try anything, then “halvo”"><small id="msg"></small></label>
    </div>
    <button class="btn btn--primary btn--lg btn--block">Sign in</button>
  </form></div>
</div>""", """
var M = Halvo.motion, card = document.getElementById('card'), pw = document.getElementById('pw'), msg = document.getElementById('msg');
function enter() { card.style.opacity = ''; card.getAnimations().forEach(function (a) { a.cancel(); }); M.fromTo(card.children, { opacity: 0, y: 18 }, null, { duration: .6, ease: 'expo.out', stagger: .06 }); }
card.onsubmit = function (e) {
  e.preventDefault();
  if (pw.value !== 'halvo') { pw.classList.add('is-bad'); msg.className = 'bad'; msg.textContent = 'That password doesn’t match. Try again.'; M.shake(document.getElementById('fields')); return; }
  pw.classList.remove('is-bad'); msg.textContent = '';
  M.fromTo(card, { scale: 1, opacity: 1 }, { scale: .96, opacity: 0 }, { duration: .3, ease: 'power2.in', keep: true }).then(function () { setTimeout(function () { pw.value = ''; enter(); }, 700); });
};
enter();
"""))
