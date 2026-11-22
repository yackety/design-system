# Dial

The thermostat: a 270° ring of 81 ticks that light from cool to warm up to the set point, a white knob you drag, and the set point in big type.

**Provide** an empty `<div class="dial">` (add `dial--md` for the 250px card size) and call `Halvo.ui.dial(el, {value, indoor, min: 10, max: 30, step: 0.5, mode: 'heat' | 'cool' | 'eco' | 'auto', on, onChange})`. It returns `{value, set(v), setIndoor(v), setMode(m), setOn(b), replay()}`. Pair it with a `.seg` for the mode.

- Geometry (300 viewBox): face r 110 (`glass-2`, dark 18% black), ticks at r 134, every 8th tick major (20px, 2.8px stroke) else 13px / 2.2px. Lit ticks mix `cool` → `warm` along the ring (`--t`) with a 3px glow; off = all `line-2`.
- Indoor reading: a small `ink` triangle on the ring. Knob: white 22px disc with an `accent` dot and drop shadow.
- Read-out: mode in 12px uppercase `accent-text`, figure `dial-figure` (64px, −0.04em) with `°C` in `fs-xl` `muted`, then "Indoors 21° · warming" in `fs-sm` `muted`.
- Input: drag on the ring (the centre 30% is a dead zone), arrow keys, or the round − / + buttons, in 0.5° steps. It is a `role="slider"` with a spoken value.
- Motion: on mount the ticks fade in one after another (0.5s, 9ms stagger), the knob sweeps from 10° to the set point and the figure counts up with it (1.5s `expo.out`). Dragging follows in 0.12s `power2.out`; buttons and keys swing the knob with 0.7s `back.out(1.6)` and count the figure in 0.5s.
