# Versioning

Halvo uses semantic versioning, `MAJOR.MINOR.PATCH`, applied to what projects depend on: token names, CSS class names and the markup each component expects, and the functions on `window.Halvo`.

## What goes in which version

| Change | Version | Examples |
| --- | --- | --- |
| Something a project uses stops working or looks broken | **major** | remove or rename a token, class or function; change a component's required markup; change a function's arguments; change a token's meaning (e.g. `muted` becomes a background) |
| Something new, or a deliberate visual change | **minor** | add a token, component, modifier class, option or function; retune a colour, radius, font or timing; deprecate a name |
| A fix that keeps every name and contract | **patch** | fix a contrast bug, a layout glitch, a JS error, a typo in a guideline |

When unsure between two, choose the larger one.

## How breaking changes are avoided

1. **Deprecate before removing.** A name being replaced stays as an alias for at least one minor release and is listed under *Deprecated* in the changelog with its replacement. Old CSS class: keep it as an extra selector on the new rule. Old token: keep it as an alias (`"value": "{new-token}"`). Old function: keep it and log a one-time `console.warn` pointing to the new one.
2. **Remove only in a major**, and list every removal under *Breaking* with the one-line fix ("rename `.foo` to `.bar`").
3. **The release tool enforces it.** `tools/release.py` records the public surface (`api-surface.json`: every token, class, CSS custom property and `Halvo.*` function) at each release. A `minor` or `patch` that removes anything from it is refused; a `patch` that adds anything is refused.
4. **Markup and behaviour are reviewed by hand**, because the tool can't see them: if a component's README "Provide" section changes, it is at least a minor, and a major if old markup no longer renders correctly.

## Releasing

```
# 1. make the change, then describe it in CHANGELOG.md under "## [Unreleased]"
python tools/release.py check          # what changed in the public surface?
python tools/release.py minor          # or patch / major: bumps, builds dist/, snapshots, commits, tags vX.Y.Z
```

Then publish the design-system artifact so the brand book matches.

## Using a version in a project

- **Pin an exact version** (a git tag such as `v1.2.0`, or a copied `dist/` folder named with its version). Never track `main`.
- **Upgrading within the same major** (1.2 → 1.5) is safe: read the changelog for visual changes and deprecations, then fix deprecation warnings before the next major.
- **Upgrading across a major** (1.x → 2.0): read every *Breaking* entry; each one says what to change.
- Check what you are running: `Halvo.version` in the browser console, or the banner at the top of each `dist/` file.
