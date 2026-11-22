# Kpi

A glass stat tile: label with icon, a big figure with a small unit, and a footer with a delta or sparkline.

**Provide** `.kpi` with `.kpi__label` (17px icon + text), `.kpi__value` (figure + `<small>` unit), `.kpi__foot` (delta/`live` dot + `.spark` svg). Set `--k` on the tile to tint the corner glow, label icon and spark (`--k: var(--warm)` for energy, `var(--cool)` for usage, `var(--s3)` for solar).

- 124px min height, padding 16 / 18 / 14, `r-lg`. Corner glow: 150px radial of `--k` at 22%, top −50 / right −40.
- Figure `fs-3xl` (22px) 600, unit `fs-md` `muted`. 18px at ≤760px, where the spark hides.
- Delta pills: `delta--up` (`good` on `good-soft`) and `delta--down` (`bad` on `bad-soft`), always with an arrow.
- Motion: figures count up (`countTo`, 1.2s `power3.out`) and sparks draw (`draw`); a live value that changes gets `flash`.
