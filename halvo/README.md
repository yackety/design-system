Halvo is a smart-home dashboard "under glass": frosted panels float over a full-bleed photo of the room you're looking at, with one teal accent for whatever is on, live or yours to press. It is calm, warm and numeric. Motion is part of the system, not decoration: every surface arrives, every number counts, every selection slides.

## Using this system

- **Use a released version.** Each release is a git tag `halvo@X.Y.Z` and a package `releases/halvo-design-system-X.Y.Z.tgz` (in the repository root) with ready files in `dist/`: `halvo.css` (font + tokens + components in one), `halvo.js` (`window.Halvo`), plus `tokens.css` / `components.css` for layered setups and `tailwind/` for Tailwind. Pin the exact version and read `CHANGELOG.md` before upgrading; `VERSIONING.md` says what counts as breaking. `Halvo.version` reports what a page is running.
- Load `tokens.css`, then `components/bundle.css`, then `components/bundle.js` (or just `dist/halvo.css` + `dist/halvo.js`). It defines `window.Halvo.motion` (the motion kit) and `window.Halvo.ui` (`select`, `selects`, `dial`). No framework or animation library is needed.
- Write dropdowns as `<select class="input" data-hv-select>` and call `Halvo.ui.selects()` once: they become the glass **Select**. Never ship a bare native dropdown.
- Set `data-theme="dark"` (the default) or `data-theme="light"` on `<html>`.
- Build screens from the component classes as their guidelines describe; never restyle glass by hand.
- Typeface: **Be Vietnam Pro** 400 / 500 / 600 / 700 from Google Fonts (bundle.css imports it); it covers Latin, Latin Extended and every Vietnamese tone mark. Turn on tabular numerals everywhere (`font-variant-numeric: tabular-nums`).

### With Angular

Install `@halvo/angular` next to the design system: directives for the Select, the sliding pill, the dial and the motion moves, plus a typed `HalvoService`. See `angular/README.md`. Both packages share one version number. Client-rendered apps only: server-side rendering (SSR) is not supported.

### With TypeScript

`dist/halvo.d.ts` types `window.Halvo` (`MotionProps`, `UiProps`, `SelectHandle`, `DialHandle`). Add `"types": ["@halvo/design-system"]` to tsconfig, or `import type { MotionProps } from '@halvo/design-system'`.

### With Tailwind

Tailwind is optional: use it for layout (grid, flex, spacing, breakpoints) and let Halvo's classes paint the surfaces. `tailwind/halvo.css` (v4) and `tailwind/halvo.preset.js` (v3) map the tokens into Tailwind's theme, so `bg-glass`, `text-muted`, `border-line`, `rounded-lg` (22px), `p-gap`, `shadow-surface`, `ease-expo-out`, `duration-base` and `dark:` (on `data-theme`) all resolve to Halvo values. They are generated from `tokens.json` by `python tools/build_tailwind.py .`.

- Always set a prefix (`@import "tailwindcss" prefix(tw)` / `prefix: 'tw-'`): Tailwind's `ring` and `table` utilities share names with Halvo's `.ring` and `.table`.
- v4: import Halvo into layers (`tokens.css` in `base`, `bundle.css` in `components`) so utilities can override component styles, and put the Be Vietnam Pro `@import url(…)` first in the stylesheet.
- Tailwind's own palette is removed in v4 (kept in v3 but don't use it). Use Halvo colour names only; for tints use the `*-soft` tokens (v4 also allows `bg-accent/50`).
- Don't use daisyUI or other component plugins with Halvo: they ship `.btn`, `.card`, `.badge`, `.modal`, `.drawer`.

## Content

Halvo talks like a thoughtful housemate: plain, specific, in full sentences about the home.

- **Greet, then report.** "Good evening, Amara" followed by one sentence of what matters: "Heating holds 21.5° until 22:30, then eases to 17° for the night. The dishwasher finishes at 20:20, and the roof covered 74% of today."
- **Numbers carry units, and the unit is smaller.** `1,478 W`, `15.8 kWh`, `21.5°`, `46 %`. Use thin facts joined by a middle dot: "Ground floor · 2 of 2 lights on · 8 devices drawing 55 W".
- **Sentence case** for everything: titles, buttons, tabs ("Living room", "Add a device", "All on"). Uppercase only for 11px section labels (`SCENES`).
- **Name things like people do.** Rooms by name, devices by what they are ("Arc floor lamp", "Side gate camera"), people by first name.
- **Status in words.** "Every door locked", "Offline", "Fresh", "Filter due". Never colour alone.
- **Confirm in the past tense**, thing first: "Film night is on", "Front door locked". Offer Undo instead of asking "Are you sure?".
- No emoji, no exclamation marks, no "Oops".

## Visual foundations

**Glass over a photo.** Every screen has a backdrop: the current room's photo, covered by `veil` (dark theme: a radial veil from `#090b0e70` to `#090b0eb3`). Surfaces on top are glass: `glass` + backdrop `blur` + `inset 0 1px 0 var(--rim)` + `inset 0 0 0 1px var(--rim-2)` + `shadow`. Overlays use `glass-strong` with `blur-overlay` and `shadow-lg`. Controls on glass step up through `glass-2` (rest) and `glass-3` (hover / selected). Recessed tracks use `well`.

**Colour.**
- Text: `ink` for primary, `ink-2` for labels and secondary copy, `muted` for captions, units and idle icons. All three hold 4.5:1 on `bg` in both themes; on glass they rely on the veil, so never drop the veil.
- `accent` (teal) marks what is on, current or primary: the primary button, the current tab pill, a switch that's on, a device that's running, the focus ring. Text on accent is always `accent-ink`. Accent-coloured text on glass is `accent-text`.
- `glow` sits under lit things (primary button `0 10px 24px -12px`, switch on `0 0 14px -2px`, device icon `0 0 22px -4px`).
- Temperature has two ends: `cool` and `warm`. Thermostat ticks blend between them; heating copy and the comparison line use `warm`.
- Status: `good`, `warn`, `bad`, `info`, each with a `*-soft` fill. They are for status only.
- Charts use `data` (teal) for the main series and `s1`–`s6` for categories. People get a pastel `h1`–`h6` with `mono-ink` initials.

**Type.** Be Vietnam Pro throughout, weight 500 for body, 600 for UI and headings, 700 for small labels, badges and dialog titles. The scale is small and tight: `fs-base` 14px body, `fs-md` 13.5px controls, `fs-sm` 12.5px captions, `fs-lg` 15px card titles, `fs-3xl` 22px stats, `page-title` up to 38px, `dial-figure` up to 64px. Big type gets negative tracking (−0.025em to −0.04em); uppercase labels get +0.06–0.08em. (The source uses Urbanist, which has no Vietnamese tone-mark glyphs; Be Vietnam Pro replaces it so Vietnamese copy never falls back letter by letter. It sets a touch wider, so keep long labels short.)

**Shape.** Soft and nested. `r-xl` 28px for the sidebar and dialogs, `r-lg` 22px for cards, 16px for strips and toasts, 13–14px for buttons, inputs and nav items, 11px for small controls and chips, 99px for pills, badges and switches. A child's radius is always smaller than its parent's.

**Space.** Cards sit `gap` (12px) apart in a grid; the sidebar and top bar float `inset` (10px) from the viewport. Card padding 18 / 20 / 20, KPI padding 16 / 18 / 14. Content stops at `max` (1480px). Sidebar `side` 256px, rail `side-rail` 84px.

**Focus and states.** Focus is a 2px solid `accent` outline, 2px offset. Inputs focus with an inset 1.5px `accent` ring plus a 4px `accent-soft` halo. Disabled is 45% opacity. Touch targets grow to 44px on coarse pointers.

**Layout.** Floating sidebar + sticky glass top bar + a page head + a 12px-gap grid of cards. At ≤760px the sidebar is replaced by a floating five-item tab bar with a sliding teal pill, dialogs become bottom sheets with a grip, and tables stack.

## Motion

Read the **Motion** component before animating anything. In short:

- **Arrive with ease-out, leave with ease-in, faster.** Entrances use `expo.out` (`ease-expo-out`) or `power3.out` (`ease-power3-out`); exits use `power2.in` at about a third of the time.
- **Pages:** the title letters rise (`splitText`), cards `rise` 26px with a 60ms stagger, figures `countTo`, sparklines `draw`, bars `grow`, heatmap cells `gridPop` as a wave. Leaving a page, visible cards sink 8px in 0.135s.
- **Selection slides.** Tabs, segmented controls, the side nav and the tab bar share one moving pill (`pill`): leading edge first, trailing edge catches up.
- **Small things spring.** Badges, pills, knobs, menus and stepper values use `back.out` (`ease-back-2`, `ease-back-3`). Page-sized surfaces never overshoot.
- **Overlays:** modal grows from its trigger (0.86 → 1, `back.out(1.5)`), drawer slides 104% from the right (0.6s `expo.out`), menus drop 6px from their anchor, toasts rise 30px. Theme changes wipe in a circle from the theme button.
- **Ambient loops are quiet and CSS-only:** `breathe` on live dots, `eq` on what's playing, `airspin` on running fans.
- Respect `prefers-reduced-motion`: every helper jumps to its end state, CSS durations collapse.

## Iconography

Line icons on a 24px grid, 1.7px stroke, round caps and joins, `currentColor`, no fill. 20px by default (`.ico`), 16px small (`ico--sm`), 26px large. Idle icons are `muted`; current or active icons are `accent-text`, or `accent-ink` on teal tiles. Icons sit in 36–40px rounded tiles (radius 11–13) when they label a row or device. No emoji, no icon fonts, no filled icon sets (Font Awesome solid and the like clash with the hairline glass).

Use **Lucide** (ISC licence) as inline SVG: paste the icon's `<path>`s inside `<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">`. The `.ico` class overrides Lucide's 2px stroke with Halvo's 1.7px and sizes it, and `currentColor` lets it take the state colour. Common picks: `house` (home), `lightbulb` (lights), `thermometer`, `zap` (energy), `shield` / `lock` (security), `sparkles` (scenes, auto), `music`, `fan`, `droplet`, `flame` / `snowflake` / `leaf` (heat / cool / eco), `bell`, `search`, `settings`. The source's own icon set was not copied.

## Don't

- Don't put glass on a flat colour in a product screen: it needs the photo and veil behind it.
- Don't use teal for decoration or more than one primary action per view.
- Don't use white on teal, or status colours for anything but status.
- Don't leave a native `<select>` unenhanced; its open menu ignores the glass system.
- Don't animate blur, layout or colour. Animate transform, opacity, clip-path and stroke only.
- Don't add gradients beyond the two the system has (the 160° accent fill, the KPI corner glow).
