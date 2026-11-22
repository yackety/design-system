# Chip

A 34px toggle used for filters and quick picks; pressed chips turn solid teal.

**Provide** `<button class="chip" aria-pressed="false">Label <span class="badge">4</span></button>` inside `.chips`. Toggle `aria-pressed`.

- Idle: `glass-2`, `line` outline, `ink-2` text `fs-sm` 600, radius 11. Hover → `glass-3`, `ink`.
- Pressed: `accent` fill, `accent-ink` text, `glow` shadow `0 6px 16px -10px`; its badge drops to 8% black.
- On touch screens chips grow to 44px tall.
