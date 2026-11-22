# Notices

The notifications popover under the bell: a short list of what needs attention, unread ones marked with a glowing teal dot.

**Provide** `.pop.notices` > `.notices__head` (`b` "Notifications" + a `.linkbtn` "Mark all read") and `.notices__list` of `button.notice` (`.notice__ico.tone--*` 36px + `.notice__text` with `b`, `p`, `small` time). Add `is-unread`. Anchor it under the bell `.ibtn` and update its `.ibtn__badge`.

- Width ≤380, overlay glass, radius 18, list max 420px tall. Rows radius 13, padding 10, hover `glass-2`.
- Unread dot: 7px `accent` with an 8px `glow`, after the title.
- Motion: opens with `popIn` from the bell; rows rise 8px with 40ms stagger after 80ms (0.45s `power3.out`). A new notice rings the bell (`ring`) and pops the badge. "Mark all read" removes the dots and the badge pops away.
