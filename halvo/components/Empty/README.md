# Empty

What a card shows when there is nothing yet: a quiet icon tile, one line saying what's missing, one line saying what to do, and at most one button.

**Provide** `.empty` > `.empty__icon` (54px tile, radius 17, `glass-2` + `line`, 20–26px icon in `ink-2`), `b` title, `p` help, optional `.btn`.

- Centred, padding 40 20, gap 8. Title `fs-lg` 600 `ink`; help `fs-sm` `muted`, max 36ch.
- Write it as a fact and a next step: "No cameras yet" / "Add one and its live view shows up here." Never "Oops" or blame.
- Motion: the tile `pop`s in and the text `slide`s after it.
