# Project rules: Angular app on the Halvo design system

This app's UI is built with **Halvo**: `@halvo/design-system` (tokens, CSS components, motion kit) and
`@halvo/angular` (directives + `HalvoService`). Both packages are installed from `.tgz` files in
`D:\workspace\design-system\releases` and always share one version. Their docs ship inside the packages.

**Pinned Halvo major: 1.x** (1.1.1 at the time of writing). Never move to a new major unless asked.

## 1. Bootstrap (only if this folder has no `angular.json` yet)

Do these steps in order and stop to report if one fails.

1. Scaffold the app **into this folder** (this CLAUDE.md is kept):
   ```
   npx --yes @angular/cli@20.3.0 new <app-name> --directory . --defaults --style=css --ssr=false --skip-tests
   ```
   Halvo is client-rendered only: never answer yes to SSR, never add `@angular/ssr`.
2. Choose the Halvo version: list `D:\workspace\design-system\releases` and take the highest
   `halvo-design-system-X.Y.Z.tgz` whose major is the pinned major. Install **both** packages of **that same version**:
   ```
   npm i D:/workspace/design-system/releases/halvo-design-system-X.Y.Z.tgz D:/workspace/design-system/releases/halvo-angular-X.Y.Z.tgz
   ```
   Check: `node -e "console.log(require('@halvo/design-system/package.json').version, require('@halvo/angular/package.json').version)"` prints the same version twice.
3. `angular.json` → `projects.<app-name>.architect.build.options` (and `architect.test.options` if it exists):
   ```json
   "styles": ["node_modules/@halvo/design-system/dist/halvo.css", "src/styles.css"],
   "scripts": ["node_modules/@halvo/design-system/dist/halvo.js"]
   ```
   Never `import` halvo.js in TypeScript; it is loaded only through `"scripts"`.
4. `src/index.html`: `<html lang="vi" data-theme="dark">` (theme `light` is the other option).
5. Replace the starter template in `src/app/app.html` (and empty `src/app/app.css`) with the page shell below, and set the
   root component's `imports` to `[RouterOutlet, RouterLink, RouterLinkActive, ...HALVO_DIRECTIVES]`
   (`import { HALVO_DIRECTIVES } from '@halvo/angular';`).
6. Verify: `npx ng build` finishes without errors, then run `npx ng serve` and open the page: Be Vietnam Pro font,
   dark glass surfaces, the tabs pill slides when clicked. Report what you checked.

## 2. Read before building any UI

- `node_modules/@halvo/design-system/README.md`: the brand book (voice, colour, type, shape, motion, icons, don'ts).
- `node_modules/@halvo/design-system/components/<Name>/README.md` for every component you use (markup to provide, states, motion).
- `node_modules/@halvo/angular/README.md`: the directives and `HalvoService`.
- `node_modules/@halvo/design-system/tokens.json`: token names and their usage notes.

## 3. Rules

- Build UI only from Halvo's CSS classes and tokens (`var(--accent)`, `var(--glass)`, `var(--r-lg)`…). No hard-coded colours,
  sizes or shadows; no other UI kit (Angular Material, PrimeNG, daisyUI, Bootstrap…).
- Don't restyle Halvo classes in component styles (they are global; no `::ng-deep`). Component CSS is for layout only.
- Use the directives from `HALVO_DIRECTIVES`:
  - `halvoSelect` on **every** `<select>` (never a bare native dropdown); it works with `formControlName` / `ngModel`.
  - `halvoPill` on `.tabs`, `.seg`, `.snav`, `.tabbar`; mark the active item with `aria-current="page"` (router: `routerLinkActive ariaCurrentWhenActive="page"`).
  - `halvoDial` for temperatures, `halvoMotion` for entrances, `halvoCount` for changing numbers, `halvoLift` on clickable tiles,
    `halvoMagnetic` on the one primary action.
- Any Halvo call you write yourself goes through `HalvoService` (`inject(HalvoService)`, then `halvo.run(h => h.motion.rise(...))`).
- Icons: Lucide line icons as inline SVG with `class="ico"` (`ico--sm` for 16px). 40 are shipped in
  `node_modules/@halvo/design-system/icons/`; for others use the `lucide-angular` package with `class="ico"`. No emoji, no icon fonts.
- Copy: Vietnamese, sentence case, numbers with smaller units (`1.478 W`, `21,5°`), facts joined by ` · `, status in words.
- Glass needs a backdrop: a room photo with the veil, or `class="hv-stage"` on the page wrapper when there is no photo.
- Never edit files in `node_modules`. If Halvo lacks something, build it from tokens in the app and tell the user it could
  become a Halvo component.

## 4. Page shell (starting template)

```html
<div class="hv-stage" style="min-height:100vh;display:grid;grid-template-columns:auto 1fr;gap:var(--gap)">
  <aside class="side glass">
    <div class="brand"><span class="mark"><!-- Lucide house svg, class="ico" --></span>
      <span class="brand__text"><b>App name</b><small>Subtitle</small></span></div>
    <nav class="snav" halvoPill>
      <span class="snav__pill"></span>
      <a class="snav__item" routerLink="/" routerLinkActive [routerLinkActiveOptions]="{ exact: true }" ariaCurrentWhenActive="page">
        <span class="snav__label">Tổng quan</span></a>
    </nav>
  </aside>
  <main style="min-width:0;display:flex;flex-direction:column;gap:var(--gap)">
    <header class="phead">
      <div class="phead__text"><h1 halvoMotion="split">Chào buổi tối</h1><p>Một câu tóm tắt tình trạng.</p></div>
    </header>
    <div class="kpis" halvoMotion="rise"><!-- .kpi tiles --></div>
    <router-outlet />
  </main>
</div>
```

## 5. Upgrading Halvo

- Read `D:\workspace\design-system\halvo\CHANGELOG.md` (or the CHANGELOG inside the newer package).
- Install the newer **pair** of `.tgz` files with the same version; same major only unless the user asks.
- Fix every *Deprecated* warning; for a new major, apply each *Breaking* entry. Run `npx ng build` afterwards.

This session needs read access to `D:\workspace\design-system\releases` (npm reads the `.tgz` files there): ask the user to allow it if prompted.
