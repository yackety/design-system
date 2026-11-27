#!/usr/bin/env node
// Suite design system build.
//   node tools/build.mjs                      validate every theme and build dist/
//   node tools/build.mjs new-theme --id acme --name "Acme" --primary "#0b6e4f"
//        [--accent "#b45309"] [--radius 13] [--font "Inter"] [--density compact]
//        [--extends default|classic] [--style glass|flat] [--mode dark|light]
// Exit code 1 when a theme is incomplete or fails a contrast pair.

import { readFileSync, writeFileSync, readdirSync, mkdirSync, existsSync, rmSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseHex, over, contrast, deriveBrand, deriveAccent, shiftLightness, withAlpha } from './color.mjs';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const readJson = (p) => JSON.parse(readFileSync(join(root, p), 'utf8'));
const pkg = readJson('package.json');
const contract = readJson('tokens/contract.json');
const base = readJson('tokens/base.json');

const COLOR_NAMES = contract.color.map((t) => t.name);
const ALPHA_ALLOWED = new Set(contract.color.filter((t) => t.alpha).map((t) => t.name));
const PAINT_NAMES = contract.paint.map((t) => t.name);
const MODE_NAMES = [...COLOR_NAMES, ...PAINT_NAMES, ...contract.modeTokens.map((t) => t.name)];
const THEME_NAMES = contract.themeTokens.map((t) => t.name);
const COMPONENT_NAMES = contract.componentTokens.map((t) => t.name);
const STYLES = Object.fromEntries(Object.entries(base.styles).filter(([k]) => !k.startsWith('$')));
const COMPONENT_FILES = ['base', 'button', 'form', 'card', 'badge', 'alert', 'tabs', 'table', 'dialog', 'toast', 'shell', 'auth', 'misc', 'listbox', 'list', 'calendar', 'upload', 'stepper', 'filter', 'extra', 'motion'];

// ---------- colour helpers bound to one mode ----------

const isOpaque = (hex) => (parseHex(hex)?.a ?? 1) >= 1;

/** Colours (#rrggbb or #rrggbbaa) found in a backdrop paint, composited over bg: the grounds glass can sit on. */
function backdropSamples(m) {
  const found = String(m.backdrop ?? '').match(/#[0-9a-f]{8}\b|#[0-9a-f]{6}\b/gi) ?? [];
  return [...new Set([m.bg, ...found.map((c) => over(c, m.bg))])];
}

/** Resolves a token to an opaque colour by compositing it over its ground (contract.grounds). */
function opaque(m, name, sample) {
  if (name === 'bg') return m.bg;
  const value = m[name];
  if (isOpaque(value)) return value;
  const ground = contract.grounds[name] ?? contract.grounds['*'];
  const under = ground === 'backdrop' ? (sample ?? m.bg) : opaque(m, ground, sample);
  return over(value, under);
}

// ---------- themes ----------

const themeFiles = () => readdirSync(join(root, 'themes')).filter((f) => f.endsWith('.json')).sort();

function loadRaw(id) {
  const p = join(root, 'themes', `${id}.json`);
  if (!existsSync(p)) throw new Error(`Theme "${id}" not found (themes/${id}.json)`);
  return JSON.parse(readFileSync(p, 'utf8'));
}

function resolve(id, seen = []) {
  if (seen.includes(id)) throw new Error(`Theme inheritance cycle: ${[...seen, id].join(' → ')}`);
  const raw = loadRaw(id);
  const parent = raw.extends ? resolve(raw.extends, [...seen, id]) : null;
  const style = raw.style ?? parent?.style ?? 'flat';
  const t = {
    id: raw.id ?? id,
    name: raw.name ?? id,
    description: raw.description ?? '',
    extends: raw.extends ?? null,
    style,
    defaultMode: raw.defaultMode ?? parent?.defaultMode ?? 'light',
    density: raw.density ?? parent?.density ?? 'comfortable',
    brand: { ...(parent?.brand ?? {}), ...(raw.brand ?? {}) },
    theme: { ...(parent?.theme ?? {}), ...(raw.theme ?? {}) },
    componentOverrides: { ...(parent?.componentOverrides ?? {}), ...(raw.components ?? {}) },
    modes: {},
    derived: {},
  };
  t.components = { ...(STYLES[style] ?? {}), ...t.componentOverrides };

  for (const mode of contract.modes) {
    const explicit = raw.modes?.[mode] ?? {};
    const merged = { ...(parent?.modes[mode] ?? {}), ...explicit };
    const derived = {};
    if (raw.brand?.primary) {
      const ground = { bg: merged.bg, surface: opaque(merged, 'surface'), 'surface-2': opaque(merged, 'surface-2') };
      Object.assign(derived, deriveBrand(raw.brand.primary, mode, ground));
      // Gradient top stop: as light as possible (up to +0.08 L) while the label still passes 4.6:1.
      let hi = derived.primary;
      if (style === 'glass') {
        for (let dL = 0.08; dL > 0; dL -= 0.01) {
          const candidate = shiftLightness(derived.primary, dL);
          if (contrast(derived['primary-fg'], candidate) >= 4.6) { hi = candidate; break; }
        }
      }
      derived['primary-hi'] = hi;
      derived.glow = style === 'glass' ? withAlpha(derived.primary, mode === 'dark' ? 0.45 : 0.5) : '#00000000';
      if (style === 'glass') derived['primary-soft'] = withAlpha(derived.primary, mode === 'dark' ? 0.16 : 0.18);
    }
    if (raw.brand?.accent) Object.assign(derived, deriveAccent(raw.brand.accent, mode));
    const m = { ...merged, ...derived, ...explicit }; // explicit values always win
    if (!explicit['primary-fill'] && (derived.primary || !m['primary-fill'])) {
      m['primary-fill'] = style === 'glass' ? `linear-gradient(160deg, ${m['primary-hi']}, ${m.primary})` : m.primary;
      derived['primary-fill'] = m['primary-fill'];
    }
    t.modes[mode] = m;
    t.derived[mode] = Object.keys(derived).filter((k) => !(k in explicit));
  }
  return t;
}

// ---------- validation ----------

function validate(t) {
  const errors = [];
  const warnings = [];
  if (!STYLES[t.style]) errors.push(`style "${t.style}" is not one of ${Object.keys(STYLES).join(', ')}`);
  if (!contract.modes.includes(t.defaultMode)) errors.push(`defaultMode "${t.defaultMode}" is not one of ${contract.modes.join(', ')}`);
  if (!base.density[t.density]) errors.push(`density "${t.density}" is not one of ${Object.keys(base.density).join(', ')}`);
  for (const name of THEME_NAMES) if (!t.theme[name]) errors.push(`missing theme token "${name}"`);
  for (const k of Object.keys(t.theme)) if (!THEME_NAMES.includes(k)) errors.push(`unknown theme token "${k}"`);
  for (const name of COMPONENT_NAMES) if (t.components[name] == null) errors.push(`style "${t.style}" has no value for component token "${name}"`);
  for (const k of Object.keys(t.components)) if (!COMPONENT_NAMES.includes(k)) errors.push(`unknown component token "${k}"`);
  const firstFont = (t.theme['font-sans'] ?? '').split(',')[0].replace(/["']/g, '').trim();
  if (firstFont && !base.fontWhitelist.some((f) => f.family === firstFont)) {
    warnings.push(`font "${firstFont}" is not in tokens/base.json fontWhitelist (Vietnamese support unchecked)`);
  }

  const results = [];
  for (const mode of contract.modes) {
    const m = t.modes[mode];
    const before = errors.length;
    for (const name of MODE_NAMES) if (m[name] == null || m[name] === '') errors.push(`${mode}: missing token "${name}"`);
    for (const k of Object.keys(m)) if (!MODE_NAMES.includes(k)) errors.push(`${mode}: unknown token "${k}"`);
    for (const name of COLOR_NAMES) {
      if (m[name] == null) continue;
      const c = parseHex(m[name]);
      if (!c) errors.push(`${mode}: "${name}" must be a hex colour, got ${m[name]}`);
      else if (c.a < 1 && !ALPHA_ALLOWED.has(name)) errors.push(`${mode}: "${name}" must be opaque (alpha is allowed on ${[...ALPHA_ALLOWED].join(', ')})`);
    }
    if (errors.length > before) continue;

    const samples = backdropSamples(m);
    for (const pair of contract.contrast) {
      const onGlass = pair.bg === 'surface-glass';
      let worst = Infinity;
      for (const sample of onGlass ? samples : [undefined]) {
        const bg = opaque(m, pair.bg, sample);
        const fg = isOpaque(m[pair.fg]) ? m[pair.fg] : over(m[pair.fg], bg);
        worst = Math.min(worst, contrast(fg, bg));
      }
      const ok = worst >= pair.min;
      results.push({ mode, fg: pair.fg, bg: pair.bg, min: pair.min, ratio: Math.round(worst * 100) / 100, ok });
      if (!ok) errors.push(`${mode}: contrast ${pair.fg} on ${pair.bg}${onGlass ? ' (worst backdrop sample)' : ''} is ${worst.toFixed(2)}:1, needs ${pair.min}:1`);
    }
  }
  return { errors, warnings, results };
}

// ---------- CSS output ----------

const banner = (what) => `/*! Suite design system v${pkg.version} — ${what}. Generated by tools/build.mjs; edit tokens/, themes/ or components/, not this file. */\n`;
const decls = (obj, indent = '  ') => Object.entries(obj).map(([k, v]) => `${indent}--${k}: ${v};`).join('\n');

function baseCss() {
  const products = ['crm', 'erp', 'hrm', 'dms', 'bi', 'wf'];
  return banner('base tokens') + [
    `:root {\n${decls(base.tokens)}\n  --product: var(--primary);\n}`,
    ...Object.entries(base.density).map(([id, v]) => `[data-density="${id}"] {\n${decls(v)}\n}`),
    products.map((p) => `[data-product="${p}"] { --product: var(--product-${p}); --product-strip: var(--product-${p}); }`).join('\n'),
    `@media (prefers-reduced-motion: reduce) {\n  :root { --dur-fast: 0ms; --dur-base: 0ms; --dur-slow: 0ms; --dur-reveal: 0ms; --stagger: 0ms; }\n}`,
  ].join('\n\n') + '\n';
}

/**
 * One theme as CSS. Without data-theme the theme's defaultMode applies (no OS media query:
 * the app's ThemeService resolves "system" to an explicit data-theme).
 */
function themeCss(t, scope) {
  const sel = scope ? `:root[data-brand="${t.id}"]` : ':root';
  const pick = (mode) => Object.fromEntries(MODE_NAMES.map((n) => [n, t.modes[mode][n]]));
  const other = contract.modes.find((m) => m !== t.defaultMode);
  return [
    `/* Theme "${t.id}": ${t.name}${t.extends ? ` (extends ${t.extends})` : ''} · style ${t.style} · default ${t.defaultMode} */`,
    `${sel} {\n${decls(t.theme)}\n${decls(t.components)}\n${decls(pick(t.defaultMode))}\n  color-scheme: ${t.defaultMode};\n}`,
    `${sel}:not([data-density]) {\n${decls(base.density[t.density])}\n}`,
    `${sel}[data-theme="${other}"] {\n${decls(pick(other))}\n  color-scheme: ${other};\n}`,
    `@media (prefers-reduced-transparency: reduce) {\n  ${sel} { --blur: none; --blur-overlay: none; --surface-glass: var(--surface); --surface-raised: var(--surface); }\n}`,
  ].join('\n\n') + '\n';
}

function tailwindCss() {
  const colors = [...COLOR_NAMES, 'product'];
  return banner('Tailwind v4 theme') +
    `/* Import after "tailwindcss". Removes Tailwind's palette so only Suite colours exist.\n` +
    `   Radius (rounded-sm|md|lg|xl) and fonts (font-sans|mono) need no mapping: Suite's unlayered tokens\n` +
    `   override Tailwind's defaults of the same name. Density: h-(--control-h), px-(--control-px). */\n` +
    `@theme {\n  --color-*: initial;\n}\n@theme inline {\n` +
    `  --color-transparent: transparent;\n  --color-current: currentColor;\n` +
    colors.map((n) => `  --color-${n}: var(--${n});`).join('\n') + '\n}\n';
}

function build() {
  const ids = themeFiles().map((f) => f.replace(/\.json$/, ''));
  const themes = [];
  let failed = false;
  for (const id of ids) {
    const t = resolve(id);
    const v = validate(t);
    themes.push({ t, v });
    const passed = v.results.filter((r) => r.ok).length;
    console.log(`${v.errors.length ? '✗' : '✓'} ${id.padEnd(12)} ${t.style.padEnd(5)} ${t.defaultMode.padEnd(5)} ${passed}/${v.results.length} contrast pairs${t.derived.light.length ? `, derived: ${t.derived.light.join(', ')}` : ''}`);
    for (const w of v.warnings) console.log(`    warning: ${w}`);
    for (const e of v.errors) console.log(`    error: ${e}`);
    if (v.errors.length) failed = true;
  }
  if (!themes.some(({ t }) => t.id === 'default')) { console.log('error: themes/default.json is required'); failed = true; }
  if (failed) { console.log('\nBuild stopped: fix the errors above.'); process.exit(1); }

  const dist = join(root, 'dist');
  rmSync(dist, { recursive: true, force: true });
  mkdirSync(join(dist, 'themes'), { recursive: true });

  const components = banner('components') + COMPONENT_FILES.map((f) => readFileSync(join(root, 'components', `${f}.css`), 'utf8')).join('\n');
  const baseOut = baseCss();
  writeFileSync(join(dist, 'base.css'), baseOut);
  writeFileSync(join(dist, 'components.css'), components);
  writeFileSync(join(dist, 'tailwind.css'), tailwindCss());
  const motion = readFileSync(join(root, 'components', 'motion.mjs'), 'utf8').replace('/*! Suite motion helpers.', `/*! Suite design system v${pkg.version} — motion helpers.`);
  writeFileSync(join(dist, 'motion.mjs'), motion);
  writeFileSync(join(dist, 'motion.js'), motion); // same ES module; some static servers serve .mjs as text/plain
  for (const { t } of themes) writeFileSync(join(dist, 'themes', `${t.id}.css`), banner(`theme ${t.id}`) + themeCss(t, false));
  writeFileSync(join(dist, 'themes.all.css'), banner('all themes, scoped by data-brand (previews, console)') + themes.map(({ t }) => themeCss(t, true)).join('\n'));
  const defaultTheme = themes.find(({ t }) => t.id === 'default').t;
  writeFileSync(join(dist, 'suite.css'), banner('base + default theme + components') + baseOut + '\n' + themeCss(defaultTheme, false) + '\n' + components);

  const index = themes.map(({ t, v }) => ({
    id: t.id, name: t.name, description: t.description, extends: t.extends, style: t.style, defaultMode: t.defaultMode,
    density: t.density, brand: t.brand, theme: t.theme, components: t.components, modes: t.modes, derived: t.derived, contrast: v.results,
  }));
  writeFileSync(join(dist, 'tokens.json'), JSON.stringify({ version: pkg.version, base, themes: index }, null, 2));
  writeFileSync(join(dist, 'themes.index.js'), `/* generated */\nwindow.SuiteThemes = ${JSON.stringify({ version: pkg.version, contract, themes: index })};\n`);
  console.log(`\nBuilt dist/ for ${themes.length} themes (v${pkg.version}).`);
}

// ---------- new-theme ----------

function newTheme(args) {
  const opt = {};
  for (let i = 0; i < args.length; i += 2) opt[args[i].replace(/^--/, '')] = args[i + 1];
  if (!opt.id || !/^[a-z][a-z0-9-]{1,30}$/.test(opt.id)) throw new Error('--id is required: lowercase letters, digits and dashes');
  if (!opt.primary || !parseHex(opt.primary)) throw new Error('--primary is required: a hex colour such as "#0b6e4f"');
  if (opt.style && !STYLES[opt.style]) throw new Error(`--style must be one of ${Object.keys(STYLES).join(', ')}`);
  const file = join(root, 'themes', `${opt.id}.json`);
  if (existsSync(file)) throw new Error(`themes/${opt.id}.json already exists`);
  const theme = {
    id: opt.id,
    name: opt.name ?? opt.id,
    description: opt.description ?? `Theme của khách hàng ${opt.name ?? opt.id}.`,
    extends: opt.extends ?? (opt.style === 'flat' ? 'classic' : 'default'),
    ...(opt.style ? { style: opt.style } : {}),
    ...(opt.mode ? { defaultMode: opt.mode } : {}),
    ...(opt.density ? { density: opt.density } : {}),
    brand: { primary: opt.primary, ...(opt.accent ? { accent: opt.accent } : {}) },
    theme: {},
  };
  if (opt.font) theme.theme['font-sans'] = `"${opt.font}", "Be Vietnam Pro", system-ui, sans-serif`;
  if (opt.radius) {
    const r = Number(opt.radius);
    theme.theme['radius-sm'] = `${Math.max(0, Math.round(r * 0.6))}px`;
    theme.theme['radius-md'] = `${r}px`;
    theme.theme['radius-lg'] = `${Math.round(r * 1.7)}px`;
    theme.theme['radius-xl'] = `${Math.round(r * 2.15)}px`;
  }
  writeFileSync(file, JSON.stringify(theme, null, 2) + '\n');
  console.log(`Created themes/${opt.id}.json\n`);
  build();
}

const [cmd, ...rest] = process.argv.slice(2);
try {
  if (!cmd || cmd === 'build') build();
  else if (cmd === 'new-theme') newTheme(rest);
  else { console.log('Usage: node tools/build.mjs [build | new-theme --id <id> --primary <hex> ...]'); process.exit(2); }
} catch (e) {
  console.error(`error: ${e.message}`);
  process.exit(1);
}
