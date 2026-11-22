# Field

Label, glass input and helper text, stacked with a 7px gap.

**Provide** `<label class="field"><span>Label</span><input class="input"><small>Help</small></label>`. Dropdowns are a `<select class="input" data-hv-select>` in the same slot, enhanced by `Halvo.ui.selects()` into the glass **Select**; `.textarea` works the same way. Wrap with `.inwrap` + a leading `.ico` for search. Mark errors with `input.is-bad` and `small.bad`. Lay fields out in `.formgrid` (2 columns, 14px gap, `span2` for full width; 1 column ≤999px).

- Input: 44px, radius 13, padding 0 14, `glass-2`, 1px inset `line-2`, `fs-base` 500. Placeholder `muted` at 85%.
- Focus: inset 1.5px `accent` + 4px `accent-soft` halo. Error: inset 1.5px `bad`.
- Motion: a rejected submit shakes the field (`shake`, 0.42s) — once, with the message in words.
- Inputs are 16px on phones to stop zoom. Never ship a bare native `<select>`: always enhance it.
