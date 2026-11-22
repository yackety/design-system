# Finder

The ⌘K command palette: one large search field over grouped results for pages, rooms, devices and actions.

**Provide** `.finder` > `.finder__in` (search icon + `input`), `.finder__list` with `.finder__group` labels and `.finder__item` rows (`.finder__ico` 36px tile + `.cell__text` + optional trailing hint), `.finder__foot` with key hints. Selection is `aria-selected="true"`, moved with ↑ ↓, run with ↵.

- 620px wide at 12vh from the top, radius 24, overlay glass. Input `fs-xl` 500, 62px row.
- Items radius 13, padding 8 10; selected `glass-3` (dark 10% white). Group labels 11px uppercase 0.06em.
- Motion: panel drops in from −18px at 0.97 (0.45s `back.out(1.6)`), the first 8 results `slide` 6px with 20ms stagger, again on each new query; out −10px in 0.18s `power2.in`.
