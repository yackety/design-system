# Ring

A round progress gauge with a figure in the middle, for shares of a whole (solar cover, battery, goals).

**Provide** `.ring` sized by width/height with an `svg` (`circle.ring__track` + `circle.ring__arc`, rotated −90° so it starts at 12 o'clock) and `.ring__in` holding the figure and caption.

- Track `well`, arc `data` with round caps; stroke width about 10% of the diameter.
- Figure in `ink` 600, caption `fs-2xs` `muted`.
- Motion: the arc draws to its value (stroke offset, 1.2s `power3.out`) while the figure counts up.
