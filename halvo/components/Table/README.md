# Table

Plain data rows inside a flush card: small muted headers, 600-weight cells, hairline dividers, a soft hover on clickable rows.

**Provide** `.card.card--flush` > `.chead` + `.table-wrap` > `table.table`. Put an icon tile + `.cell__text` (`b` + `small`) in the first column with `.cell`; numbers right-aligned with `.r`; status as a `.pill`. Clickable rows get `tr.is-click`. Add `table--stack` so that on phones each row becomes a two-line card using `m-main`, `m-end`, `m-sub`, `m-tag` cells.

- Head: `fs-xs` 600 `muted`, padding 10 14. Cells: `fs-md` 600 (secondary cells `td.muted` at 500), padding 12 14, `line` dividers, none under the last row.
- Hover: `glass-2` behind the whole row.
- Motion: rows `slide` in (12px, 40ms stagger) when the table first shows or its filter changes.
