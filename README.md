# Design systems

One repository, one folder per design system. Each system is versioned and released on its own.

| System | Folder | Current | What it is |
| --- | --- | --- | --- |
| Halvo | [halvo/](halvo/) | see [halvo/CHANGELOG.md](halvo/CHANGELOG.md) | Glass smart-home UI: tokens, CSS components, motion kit, Tailwind presets; Angular package in `halvo/angular/` |

## Layout

```
design-system/
├─ releases/              installable packages, one per release: <package>-<version>.tgz
├─ halvo/
│  ├─ package.json        name + version of this system (the single source of its version)
│  ├─ CHANGELOG.md        every release; write changes under "Unreleased"
│  ├─ VERSIONING.md       what counts as major / minor / patch
│  ├─ api-surface.json    public names at the last release (guards against breaking changes)
│  ├─ tokens.json, components/, icons/, tailwind/
│  ├─ dist/               built files projects load
│  └─ tools/              release.py, build_demo.py, build_tailwind.py, gen.py
└─ <next-system>/         same shape
```

## Versions and tags

- Tags are per system: `halvo@1.0.0`, `halvo@1.1.0`, `<next-system>@0.1.0` … so systems never collide.
- Release from inside a system's folder: `python tools/release.py check`, then `python tools/release.py minor` (or `patch` / `major`). It bumps that system's version, builds `dist/`, packs `releases/<package>-<version>.tgz`, and commits **only that folder** plus the package, then tags.

## Using a system in a project

Install the released package, pinned to an exact version:

```
npm i D:/workspace/design-system/releases/halvo-design-system-1.1.0.tgz
# Angular projects also:
npm i D:/workspace/design-system/releases/halvo-angular-1.1.0.tgz
```

(npm cannot install a sub-folder of a git repository, so projects install the packed `.tgz`. When this repo moves to a shared host, publish the same package to a private registry — GitHub Packages, GitLab, Verdaccio — and install `@halvo/design-system@1.0.0` instead.)

To upgrade, read the system's CHANGELOG, then install the newer `.tgz`.

## Adding a new design system

1. Create `<name>/` with `package.json` (`"name": "@<name>/design-system"`, `"version": "0.1.0"`), `tokens.json`, `components/`, `CHANGELOG.md` (with an empty `## [Unreleased]`) and `VERSIONING.md`.
2. Copy `halvo/tools/` and adjust the generators; `release.py` takes its tag prefix from the folder name.
3. Run `python tools/release.py snapshot` once, commit, and tag `<name>@0.1.0`. Stay on `0.x` until the system is ready for projects; release `1.0.0` when its names are stable.
4. Add a row to the table above.
