# SignIn

The sign-in card over the home photo: large app mark, greeting, two fields, one button.

**Provide** `.signin` (fills the screen, centres its child) > `.signin__card` with `.mark.mark--lg`, `h1`, `p`, `.signin__fields` (`.field`s) and a `btn--primary btn--lg btn--block`.

- Card: overlay glass (`glass-strong`, `blur-overlay`, rims, `shadow-lg`), radius `r-xl`, padding 32, width ≤420. Mark 56px, radius 18. Title 30px 600 −0.025em; lead `muted`.
- Copy: "Welcome home" / "Sign in to Larch House." Errors say what to fix, under the field.
- Motion: the card's children rise 18px with 60ms stagger (0.6s `expo.out`). A wrong password shakes the fields; success scales the card to 0.96 and fades it (0.3s `power2.in`), then a toast greets the person by first name.
