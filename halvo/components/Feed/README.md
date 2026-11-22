# Feed

A chronological activity log: tinted icon tile, what happened, and when / who in muted text.

**Provide** `.feed` > `.feed__row` > `.feed__ico.tone--*` (34px, radius 11, 17px icon) + `.feed__text` (`b`, `small`) + optional trailing time or `.pill`. Tones: `tone--good` (locked, arrived), `tone--warn` (left open), `tone--bad` (alarm, offline), `tone--info` (updates), `tone--accent` (scenes and automations), `tone--plain` (everything else).

- Rows padding 10 0 with `line` dividers. Title `fs-md` 600, detail `fs-xs` `muted`.
- Write entries as past-tense facts with the actor: "Front door locked · by Amara", "Motion at the side gate".
- Motion: rows `slide` in 12px with 40ms stagger; a new entry arriving live slides in at the top and its icon `pop`s.
