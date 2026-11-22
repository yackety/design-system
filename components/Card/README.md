# Card

The frosted glass panel every Halvo screen is built from: `glass` fill, backdrop `blur`, two rim insets and `shadow`.

**Provide** `<section class="card">` with a `.chead` (title `h2/h3` in `fs-lg` 600, optional `p` subtitle in `fs-sm` `muted`, trailing action) and any body. `card--flush` drops the padding for tables and media. Inside a card, recessed groups use `.well` (`glass-2`, radius `r-md`).

- Radius `r-lg` (22px), padding 18 / 20 / 20; 20px radius and 16px padding at ≤760px.
- The recipe is `background: var(--glass); backdrop-filter: var(--blur); box-shadow: inset 0 1px 0 var(--rim), inset 0 0 0 1px var(--rim-2), var(--shadow)`. Without backdrop-filter support it falls back to `glass-strong`.
- Glass needs something behind it: the room photo with `veil` over it. Never put glass on flat `bg` in a product screen.
- Motion: cards enter with `rise` (staggered 60ms) and leave a route with `pageLeave`. Tiles that open something carry `data-lift`.
- Section labels inside cards: `.section-label`, 11px uppercase 0.08em `muted`.
