# Switch

A 44×26 on/off toggle; on is solid teal with a glow, the white knob springs 18px.

**Provide** `<button class="switch" role="switch" aria-checked="false"><i></i></button>` with an accessible name (usually the `.row-set` text beside it). Toggle `aria-checked`, then call `Halvo.motion.switchKnob(el)`.

- Off: `well` track, inset 1px `line-2`. On: `accent` track, `0 0 14px -2px var(--glow)`.
- Knob: 20px white, 3px inset, `0 2px 5px #0000004d`.
- Motion: knob travel 0.45s `back.out(2.2)` — a little overshoot, then rest.
- Settings lists use `.row-set`: title `b` 600, `small` `muted` `fs-sm`, 14px padding, `line` dividers.
- Group related rows in a `.row-group`: a `glass-2` frame (radius `r-md`, padding 2px 16px, `line` outline) that gives the rows their side padding; stack groups `gap` apart, each under a `.section-label`. (Intentional addition: the source only has bare `.row-set` lists.)
