# Bars

Rounded-capsule column chart for hourly or daily totals; the highlighted column glows.

**Provide** `.bars` > `.bars__grid` (dashed `line-2` rules with `fs-2xs` labels, solid base) and `.bars__cols` of `.bars__col` > `.bars__track` (`.bars__ghost` full height + `.bars__bar` at its value) + `.bars__label`. Mark the current/peak column `is-hi`. `bars--compact` drops the y labels.

- Bars are capsules inset 22% each side (max 46px track), `data` at 50%; `is-hi` is full `data` with `0 0 18px -2px var(--glow)` and an `accent-text` label.
- Ghosts (`well`) show the scale behind every bar.
- Motion: bars `grow` from the base, 0.9s `expo.out`, 30ms stagger. Hover shows a dark `.charttip`.
