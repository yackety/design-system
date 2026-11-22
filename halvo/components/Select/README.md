# Select

A glass dropdown: the trigger looks like an input, the options open in a frosted listbox with a tick on the chosen one.

**Provide** an ordinary `<select class="input" data-hv-select>` (with `<optgroup>`s if useful; `data-hint` on an `<option>` adds a second line; an empty-value first option acts as a placeholder) and call `Halvo.ui.selects(root)` once, or `Halvo.ui.select(el)` for one. Add `select--sm` for the 34px toolbar size. The native element stays in the form, hidden, so `value`, `name`, `required` and `change` events keep working; call `.refresh()` on the returned object after changing its options.

- Trigger: the `.input` recipe plus a 16px chevron in `muted`; open = `glass-3` with the accent focus ring, chevron turned 180° (0.3s `power3.out`). Placeholder text is `muted`.
- List: `.pop` glass (`glass-strong`, `blur-overlay`, `shadow-lg`, radius 18, padding 6), 6px from the trigger, at least as wide, max 288px tall then scrolls. It flips above the trigger when there is no room below.
- Options: `menu__item` rows (40px, radius 11, `fs-md` 600). Active row `glass-3` (dark 10% white); selected row in `ink` with an `accent-text` tick. Group labels are 11px uppercase `muted`.
- Keyboard: ↓ ↑ Enter / Space open; arrows, Home, End move; Enter / Space choose; Esc closes and returns focus; typing jumps to a match.
- Motion: list `popIn` (0.92 → 1, −6px, 0.4s `back.out(2)`), first 8 options `slide` 6px with 20ms stagger; close 0.15s `power2.in`; the new value rolls into the trigger (`roll`, 0.35s `back.out(2)`).

**Intentional addition:** Halvo itself styles the native `<select>` (a CSS chevron on `select.input`, still used as the no-JS fallback). The custom listbox was added so open menus match the glass system.
