# Meter

A thin read-only bar for levels: battery, filter life, air quality, device load.

**Provide** `<span class="meter" role="meter" aria-valuenow="64" aria-valuemin="0" aria-valuemax="100" aria-label="Battery"><i></i></span>` and set the fill with `Halvo.motion.fill(i, 0.64)`. Tones: `is-warn`, `is-bad`.

- 8px tall (5px inside device tiles), radius 8, `well` track, `accent` fill scaled on x from the left.
- Motion: fills to its value in 1s `expo.out` after 0.15s; later changes animate from the old value.
