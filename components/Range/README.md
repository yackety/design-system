# Range

A 10px track with a glowing teal fill and a white 22px knob, value read out on the right.

**Provide** `.range` > `.range__track` (`.range__fill` + `.range__knob`) + a transparent `<input type="range">` laid over it + `<output>`. Drive the fill with `transform: scaleX(v)` and the knob with `translateX(v * 100%)`. `range--compact` drops the output.

- Track `well`, radius 10, inset 1px `line`. Fill: gradient 90° `accent` at 55% → `accent`, `0 0 14px -3px var(--glow)`.
- Knob: white, `0 2px 8px #00000059`, 4px `accent-soft` ring (solid `accent` on keyboard focus).
- Motion: fill and knob follow with `power3.out` (0.3s while dragging, longer when set by a scene).
