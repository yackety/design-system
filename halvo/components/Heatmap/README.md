# Heatmap

A day × hour grid of rounded cells whose teal deepens with the value, for when-is-it-busy questions (energy by hour, motion by hour).

**Provide** `.heat` with `grid-template-columns: auto repeat(<cols>, minmax(0, 1fr))`: an empty corner, `.heat__col` labels, then per row a `.heat__row` label and `.heat__cell`s each holding an `<i>` whose background is `color-mix(in oklab, var(--data) <14 + v·86>%, var(--glass-3))`. Mark the peak `is-peak`. Show a `.charttip` on hover.

- Cells: aspect 1.5, radius 6, 4px gaps. Peak ring: 2px `bg` gap + 2px `data`.
- Labels `fs-2xs` / `fs-xs` 600 `muted`. Always state the scale in a legend or caption.
- Motion: cells pop from 0 as a wave from the top-left cell (0.6s `back.out(2.2)`, 12ms per cell of distance) — `Halvo.motion.gridPop(cells, cols)`.
