# Toast

A dark smoked-glass confirmation that rises at the bottom centre, says what happened, and offers Undo.

**Provide** `.toast` > icon, `<span>` message, optional `<button>Undo</button>`; `is-warn` for cautions. Stack them in a fixed `.toasts` column (bottom 22px, width ≤440px, 8px gap; above the tab bar on phones).

- Always dark in both themes: `#16181cdb` with blur 20px, text `#f1efea`, icon teal `#5fd8c4` (warn `#ffb27e`), radius 16, `shadow-lg`.
- Message: past tense, the thing first — "Film night is on", "Front door locked".
- Motion: in 30px up from 0.94, 0.5s `back.out(1.8)`; out 16px down, 0.25s `power2.in`. Lives 3.2s, 5.5s when it has Undo.
