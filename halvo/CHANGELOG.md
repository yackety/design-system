# Changelog

Every release of Halvo, newest first. Versions follow [VERSIONING.md](VERSIONING.md): **major** breaks something (a removed or renamed token, class, markup contract or function), **minor** adds or visibly changes something, **patch** fixes without changing the public surface. Pin an exact version in projects and read this file before upgrading.

Write changes under **Unreleased** as you make them, grouped as *Breaking*, *Added*, *Changed*, *Deprecated*, *Fixed*. `python tools/release.py minor` (or `patch` / `major`) turns that section into the next version.

## [Unreleased]

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
