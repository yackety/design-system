# Halvo for Angular

`@halvo/angular` wraps the Halvo design system for Angular 17.3 and newer (tested on Angular 20): a typed `HalvoService` and standalone directives for the parts that need JavaScript. Everything else in Halvo is plain CSS classes you use straight in templates.

> **Server-side rendering (SSR) is not supported.** Use Halvo in client-rendered Angular apps (`ng new --ssr=false`). Apps with `@angular/ssr`, prerendering or hydration are untested and may break.

It is released together with `@halvo/design-system`, at the same version.

## Starting a new project with Claude

Copy `angular/CLAUDE.template.md` (in the design-system repo) into an empty folder as `CLAUDE.md` and start a Claude session there: it scaffolds the Angular app, installs the latest 1.x pair of Halvo packages, wires `angular.json` and builds a first page shell.

## Install

```
npm i D:/workspace/design-system/releases/halvo-design-system-1.2.0.tgz D:/workspace/design-system/releases/halvo-angular-1.2.0.tgz
```

In `angular.json` → `projects › <app> › architect › build › options`:

```json
"styles": ["node_modules/@halvo/design-system/dist/halvo.css", "src/styles.css"],
"scripts": ["node_modules/@halvo/design-system/dist/halvo.js"]
```

Set the theme on `<html data-theme="dark">` (or `light`) in `index.html`, and `lang="vi"` for Vietnamese pages.

## Use

```ts
import { HALVO_DIRECTIVES, HalvoService } from '@halvo/angular';

@Component({
  standalone: true,
  imports: [ReactiveFormsModule, ...HALVO_DIRECTIVES],
  templateUrl: './rooms.html',
})
export class RoomsComponent {
  readonly halvo = inject(HalvoService);
}
```

| Directive | Put it on | What it does |
| --- | --- | --- |
| `halvoSelect` | `<select>` | The glass dropdown. Works with `formControlName`, `formControl` and `ngModel`, follows option changes from `@for`, `disabled` and values set from code, and cleans up on destroy. Add `class="select--sm"` for 34px. |
| `halvoPill` | `.tabs`, `.seg`, `.tabbar`, `.snav` | Slides the selection pill to the item with `aria-current` / `aria-pressed` / `aria-selected`. With the router: `routerLinkActive ariaCurrentWhenActive="page"`. |
| `halvoDial` | an empty `<div>` | The thermostat. `[(value)]` or a form control; `[indoor]`, `[mode]`, `[on]`; `min`, `max`, `step`, `controls` are read once. |
| `halvoMotion="rise"` | any container | Plays an entrance once: `rise`, `slide`, `deal`, `pop`, `grow`, `grow-x` stagger the children; `split` animates a heading's letters; `draw` traces SVG strokes; `grid` (+ `[motionCols]`) is the heatmap wave. `motionTargets`, `motionDelay`, `motionStagger` tune it. |
| `[halvoCount]="value"` | a number's element | Counts up, and from the old value on every change; `[countFormat]`, `countFlash`. |
| `halvoMagnetic` | the one primary button | Pointer-follow. |
| `halvoLift` | a tile | Lifts 4px on hover. |

```html
<nav class="tabs" halvoPill>
  <span class="tabs__line"></span>
  <a routerLink="living" routerLinkActive ariaCurrentWhenActive="page">Phòng khách</a>
  <a routerLink="kitchen" routerLinkActive ariaCurrentWhenActive="page">Bếp</a>
</nav>

<div class="kpis" halvoMotion="rise">
  <div class="kpi" halvoLift>
    <div class="kpi__value"><span [halvoCount]="watts" countFlash></span><small>W</small></div>
  </div>
</div>

<label class="field"><span>Phòng</span>
  <select halvoSelect formControlName="room">
    @for (r of rooms(); track r.id) { <option [value]="r.id">{{ r.name }}</option> }
  </select>
</label>

<div halvoDial formControlName="target" [indoor]="indoor()" [mode]="mode()" class="dial--md"></div>
```

### Page transitions (router)

Halvo's page swap between routes lives in the secondary entry `@halvo/angular/router` (only apps that use `@angular/router` import it):

1. On leaving, the visible cards sink and fade, the page head and tabs fade up, and the page slides 16px against the direction of travel (≈0.18s; the route waits for it, at most 400ms).
2. The new page slides in from 26px on the side it comes from (0.7s), its page head and tabs fade in, and its cards rise one after another.

Direction comes from the order of the links in your side nav / tab bar: going down the menu slides left, going up slides right; the browser's back button slides right.

```ts
// app.routes.ts
import { withHalvoTransitions } from '@halvo/angular/router';
export const routes: Routes = withHalvoTransitions([
  { path: '', component: OverviewPage },
  { path: 'rooms', component: RoomsPage },
]);
```

```html
<!-- app.html: the element that holds the outlet -->
<main halvoRouteTransition><router-outlet /></main>
```

```ts
// root component
imports: [RouterOutlet, RouterLink, RouterLinkActive, ...HALVO_DIRECTIVES, HalvoRouteTransitionDirective]
```

- `transitionDepth` (default 1): how many URL segments name a page. `/rooms/living → /rooms/kitchen` stays on the same page and doesn't swap.
- `transitionCards` (default true): the transition rises the new page's `.card`, `.kpi`, `.tile` and `[data-lift]` elements. Don't also put `halvoMotion="rise"` on those grids, or set `[transitionCards]="false"` and keep your own.
- Without `withHalvoTransitions` you still get the entrance, just not the exit. Wrap lazily loaded child routes (`loadChildren`) with it too.
- Cards that appear later (after data loads) aren't part of the swap: give them `halvoMotion="rise"` inside the `@if` that renders them.

### HalvoService

- `motion`, `ui`, `version`: typed `window.Halvo` (null if `halvo.js` is not loaded).
- `run(h => …)`: runs Halvo work outside Angular's zone, so animation frames don't trigger change detection. Use it for any `motion.*` call you make yourself.
- `theme`, `setTheme('light', buttonEl)`, `toggleTheme(buttonEl)`: theme switch with the circle wipe.

## Notes

- **SSR is not supported** (see the top of this page). Load `halvo.js` only through `"scripts"` in angular.json, never `import` it in code.
- **Zoneless apps** work the same; `run()` simply calls the function.
- Don't redefine Halvo's classes in component styles; they are global and need no `::ng-deep`.
- Tailwind and Lucide: see the design system README (`lucide-angular` icons take `class="ico"`).
