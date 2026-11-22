# Pill

Status and fact labels: `.pill` (24px with a dot), `.badge` (20px count), `.delta` (change), `.live` (breathing dot).

**Provide** `<span class="pill pill--good">Fresh</span>`; tones `--good --warn --bad --info --accent`, or `pill--plain` (no dot) for neutral facts with an icon. Counts: `<span class="badge">3</span>`. Changes: `delta--up` / `delta--down` with an arrow.

- Pill: radius 99, padding 0 9, `fs-xs` 600; neutral = `glass-2` + `line`; toned = `*-soft` fill, `*` text, no outline. The 6px dot is `currentColor`.
- Status is never colour alone: every pill says its state in words.
- `.live`: 8px `good` dot with a 2s `breathe` halo (opacity .08 ↔ .4). `.eq`: four 3px bars on the 1.1s `eq` loop, for what's playing.
