# Changelog

Every release of Halvo, newest first. Versions follow [VERSIONING.md](VERSIONING.md): **major** breaks something (a removed or renamed token, class, markup contract or function), **minor** adds or visibly changes something, **patch** fixes without changing the public surface. Pin an exact version in projects and read this file before upgrading.

Write changes under **Unreleased** as you make them, grouped as *Breaking*, *Added*, *Changed*, *Deprecated*, *Fixed*. `python tools/release.py minor` (or `patch` / `major`) turns that section into the next version.

## [Unreleased]

## [1.4.0] — 2026-11-24

### Added
- `.hv-shell`: the app frame (side nav + main column, `gap` apart; one column on phones). Use it instead of a hand-written grid.

### Fixed
- Uneven side margins on phones: with the side nav hidden, the 1.3.0 page shell (an inline `auto 1fr` grid) left an empty column and gap on the right (20px left vs 38px right at 375px). A compatibility rule now collapses such shells to one column; new pages should use `.hv-shell`.
- `angular/CLAUDE.template.md` uses `.hv-shell` and includes the mobile tab bar and `tabbar-space` in the page shell.

## [1.3.0] — 2026-11-24

### Added
- **Mobile layout (≤760px)** in the CSS: `.tabbar` is fixed at the bottom (hidden on larger screens) and `.side` hides; `.drawer` and modals become bottom sheets with a `.sheet__grip`; `.toasts` sit above the tab bar. New helpers: `.tabbar-space` (bottom padding so content clears the tab bar), `.modal-wrap` (the fixed layer that centres a modal, or drops it to the bottom on phones), `.modal--wide`, `.toasts` (toast stack).
- `.row-group`: a framed group of `.row-set` settings rows with its own padding (intentional addition).
- `.hv-demo`: keeps overlays and the tab bar inside a preview frame (for docs and previews, not apps).

### Changed
- `.hv-stage` uses `overflow: clip` instead of `hidden`, so `position: sticky` works inside it.
- `.side` is sticky at `--inset` and never taller than the viewport; `.snav` scrolls when the menu is long (no visible scrollbar).
- `.drawer` and `.scrim` are `position: fixed` (as in the original Halvo) instead of `absolute`. If you placed a drawer inside a positioned container on purpose, give it `position: absolute` yourself.
- `Halvo.motion.drawerIn/drawerOut` and `modalIn/modalOut` play the bottom-sheet motion on phones.

### Fixed
- The sliding pill (`Halvo.motion.pill`, `halvoPill`) now covers the whole scroll area of a scrolling container, so the side-nav highlight stays on the right item after scrolling.

## [1.2.0] — 2026-11-23

### Added
- **Page transitions between routes**, as in the original Halvo: the old page's cards sink and the page slides out, then the new page slides in from the side it comes from and its cards rise.
  - Core: `Halvo.motion.pageOut(container, {direction})`, `pageIn(container, {direction, cards})`, `pageReset(container)` (framework-free).
  - Angular: new entry point `@halvo/angular/router` with `HalvoRouteTransitionDirective` (`halvoRouteTransition` on the element around `<router-outlet>`), `withHalvoTransitions(routes)`, `halvoLeaveGuard` and `HalvoRouteTransitions`. `@angular/router` is an optional peer dependency, needed only for this entry point.

## [1.1.1] — 2026-11-22

### Fixed
- Links used as nav items, tabs, buttons, chips or rows (`a.snav__item`, `.tabs a`, `.tabbar a`, `a.btn` …) no longer show the browser's underline and link colour.

### Added
- `angular/CLAUDE.template.md`: a CLAUDE.md for new Angular projects, so a Claude session can scaffold the app, install Halvo and follow its rules.

## [1.1.0] — 2026-11-22

### Added
- **`@halvo/angular`**: a new package, released with the design system at the same version. Typed `HalvoService` (motion, ui, version, `run()` outside the zone, `setTheme` / `toggleTheme`) and standalone directives: `halvoSelect` (works with reactive forms and `ngModel`, follows option and value changes, cleans up), `halvoPill`, `halvoDial` (`[(value)]` and form control), `halvoMotion`, `halvoCount`, `halvoMagnetic`, `halvoLift`. Supports Angular 17.3+ (tested on 20.3), client-rendered apps only: **server-side rendering (SSR) is not supported**. See `angular/README.md`.
- TypeScript declarations for `window.Halvo` ship in the package: `dist/halvo.d.ts` (`"types"` in package.json).

## [1.0.0] — 2026-11-22

First versioned release: the baseline every project upgrades from.

### Contents
- Tokens for dark (default) and light themes: 44 colours, 13 type styles, spacing, radius, shadows, backdrop blur, 10 eases, 7 durations.
- Typeface **Be Vietnam Pro** 400–700 (full Vietnamese support).
- 36 components with guidelines and live previews: Motion, Button, IconButton, Chip, Card, Kpi, PageHead, Tabs, Segmented, SideNav, TabBar, Field, Select, Switch, Check, Range, Stepper, Dial, Pill, Avatar, Meter, Empty, Toast, Menu, Notices, Modal, Drawer, Finder, SignIn, Bars, Area, Heatmap, Ring, Table, Feed, Device.
- `window.Halvo.motion`: the motion kit (rise, slide, deal, grow, draw, pop, flash, countTo, shake, ring, magnetic, lift, pill, gridPop, overlays, themeSwap …).
- `window.Halvo.ui`: `select`, `selects` (glass dropdown replacing the native one), `dial` (thermostat).
- Lucide icons (ISC) in `icons/`.
- Tailwind v4 theme (`dist/tailwind/halvo.css`) and v3 preset (`dist/tailwind/halvo.preset.js`).
- Distribution files in `dist/`: `halvo.css`, `tokens.css`, `components.css`, `halvo.js`.
