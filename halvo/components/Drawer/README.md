# Drawer

A tall glass panel that slides in from the right for detail and editing (a device, a person, an event).

**Provide** `.scrim` + `.drawer` (`role="dialog"`) with `.drawer__head` (h2 `fs-3xl` 700, `p` `muted`, close), `.drawer__body` (scrolls), `.drawer__foot`. Inside, device facts use `.facts` tiles and controls use `.row-set`.

- Floats 12px from the top, right and bottom; width ≤460; radius `r-xl`; overlay glass recipe. Head and foot separated by `line`.
- On phones it becomes a bottom sheet (full width, ≤92dvh, radius 26 26 0 0).
- Motion: `drawerIn` — x 104% → 0 in 0.6s `expo.out`, scrim 0.3s, body rows `slide` in after; out 0.32s `power3.in`.
