# Area

A smooth line chart with a faint fill, a glowing `data` stroke and an optional dashed comparison line.

**Provide** an `svg.area__svg` with `.area__grid` lines, `path.area__fill`, `path.area__cmp` (comparison, `warm` dashed 4 5), `path.area__line`, and `circle.area__dot` for the hovered point. Add a `.legend` (`i` squares; `i.is-dash` for the comparison).

- Line 2.4px round, `drop-shadow(0 4px 8px var(--glow))`; fill `data` at 14%; grid dashed `line-2`; dot `bg` filled with a 2.5px `data` ring.
- Motion: the line `draw`s itself in 1.1s `power2.inOut`; the fill and dot fade in after.
