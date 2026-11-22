# PageHead

The glass banner at the top of each page: eyebrow, greeting-style title, one plain sentence of status, then facts and actions.

**Provide** `.phead` > `.phead__text` (`.phead__eyebrow`, `h1`, `p`) + `.phead__actions`. Facts sit as `.pill`s; people as an `.avstack`.

- Title: `page-title` style — clamp(28px, 2.6vw, 38px), 600, −0.025em, line-height 1.04, with a soft text shadow (dark `#0000002e`, light `#fff9`) so it reads over the photo.
- Lead: `fs-base` in `ink-2`, max 70ch. Write it as a sentence about the home, not a list.
- Motion: the title enters with `splitText` (letters rise from a clipped word box, 0.85s `power4.out`, 22ms per letter); pills follow with `slide`.
