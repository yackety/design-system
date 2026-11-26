// Color helpers: hex <-> OKLCH, WCAG contrast, and brand-color derivation.
// No dependencies. Formulas: OKLab by Björn Ottosson; contrast per WCAG 2.x.

const clamp01 = (x) => Math.min(1, Math.max(0, x));

export function parseHex(hex) {
  const m = /^#([0-9a-f]{3}|[0-9a-f]{4}|[0-9a-f]{6}|[0-9a-f]{8})$/i.exec(String(hex).trim());
  if (!m) return null;
  let h = m[1];
  if (h.length <= 4) h = [...h].map((c) => c + c).join('');
  const n = (i) => parseInt(h.slice(i, i + 2), 16) / 255;
  return { r: n(0), g: n(2), b: n(4), a: h.length === 8 ? n(6) : 1 };
}

export function toHex({ r, g, b, a = 1 }) {
  const c = (x) => Math.round(clamp01(x) * 255).toString(16).padStart(2, '0');
  return '#' + c(r) + c(g) + c(b) + (a < 1 ? c(a) : '');
}

const toLinear = (c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
const toGamma = (c) => (c <= 0.0031308 ? 12.92 * c : 1.055 * c ** (1 / 2.4) - 0.055);

export function hexToOklch(hex) {
  const { r, g, b } = parseHex(hex);
  const [lr, lg, lb] = [r, g, b].map(toLinear);
  const l = Math.cbrt(0.4122214708 * lr + 0.5363325363 * lg + 0.0514459929 * lb);
  const m = Math.cbrt(0.2119034982 * lr + 0.6806995451 * lg + 0.1073969566 * lb);
  const s = Math.cbrt(0.0883024619 * lr + 0.2817188376 * lg + 0.6299787005 * lb);
  const L = 0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s;
  const A = 1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s;
  const B = 0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s;
  const C = Math.hypot(A, B);
  let H = (Math.atan2(B, A) * 180) / Math.PI;
  if (H < 0) H += 360;
  return { L, C, H };
}

function oklchToLinear(L, C, H) {
  const hr = (H * Math.PI) / 180;
  const A = C * Math.cos(hr);
  const B = C * Math.sin(hr);
  const l = (L + 0.3963377774 * A + 0.2158037573 * B) ** 3;
  const m = (L - 0.1055613458 * A - 0.0638541728 * B) ** 3;
  const s = (L - 0.0894841775 * A - 1.291485548 * B) ** 3;
  return [
    4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
    -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
    -0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s,
  ];
}

// Converts OKLCH to hex, lowering chroma until the colour fits in sRGB.
export function oklchToHex(L, C, H) {
  L = clamp01(L);
  let c = Math.max(0, C);
  for (let i = 0; i < 60; i++) {
    const lin = oklchToLinear(L, c, H);
    if (lin.every((v) => v >= -1e-4 && v <= 1 + 1e-4)) {
      const [r, g, b] = lin.map((v) => toGamma(clamp01(v)));
      return toHex({ r, g, b });
    }
    c *= 0.94;
  }
  const [r, g, b] = oklchToLinear(L, 0, H).map((v) => toGamma(clamp01(v)));
  return toHex({ r, g, b });
}

export function luminance(hex) {
  const { r, g, b } = parseHex(hex);
  const [R, G, B] = [r, g, b].map(toLinear);
  return 0.2126 * R + 0.7152 * G + 0.0722 * B;
}

// Composites a colour that may have alpha over an opaque background.
export function over(fgHex, bgHex) {
  const f = parseHex(fgHex);
  const b = parseHex(bgHex);
  if (f.a >= 1) return toHex(f);
  return toHex({ r: f.r * f.a + b.r * (1 - f.a), g: f.g * f.a + b.g * (1 - f.a), b: f.b * f.a + b.b * (1 - f.a) });
}

export function contrast(aHex, bHex) {
  const la = luminance(aHex);
  const lb = luminance(bHex);
  const [hi, lo] = la > lb ? [la, lb] : [lb, la];
  return (hi + 0.05) / (lo + 0.05);
}

const minContrast = (hex, backgrounds) => Math.min(...backgrounds.map((b) => contrast(hex, b)));

// Moves lightness in `dir` (-1 darker, +1 lighter) until `ok(hex)` holds.
function walk(L, C, H, dir, ok) {
  for (let i = 0; i <= 100; i++) {
    const hex = oklchToHex(L, C, H);
    if (ok(hex)) return hex;
    L = clamp01(L + dir * 0.01);
  }
  return oklchToHex(L, C, H);
}

const WHITE = '#ffffff';

/**
 * Derives the brand-related tokens of one mode from a single brand colour.
 * `ctx` holds the mode's already-resolved neutrals (bg, surface, surface-2).
 * Target: every pair in the contract passes with a small margin.
 */
export function deriveBrand(primaryHex, mode, ctx, target = 4.6) {
  const { L, C, H } = hexToOklch(primaryHex);
  const neutrals = [ctx.bg, ctx.surface, ctx['surface-2']];
  const out = {};

  if (mode === 'light') {
    let primary;
    let fg;
    const ink = oklchToHex(0.2, Math.min(C, 0.05), H);
    if (contrast(WHITE, primaryHex) >= target) {
      primary = primaryHex;
      fg = WHITE;
    } else if (contrast(ink, primaryHex) >= target && minContrast(primaryHex, neutrals) >= 3) {
      primary = primaryHex; // light brand colours that still stand out from the surface keep a dark label
      fg = ink;
    } else {
      // too light to stand out (yellow, lime, sky): darken until a white label passes.
      // Projects that want the bright colour on screen should give it as brand.accent instead.
      primary = walk(L, C, H, -1, (hex) => contrast(WHITE, hex) >= target);
      fg = WHITE;
    }
    const p = hexToOklch(primary);
    const hover = fg === WHITE
      ? walk(p.L - 0.06, p.C, p.H, -1, (hex) => contrast(fg, hex) >= target)
      : walk(p.L - 0.05, p.C, p.H, +1, (hex) => contrast(fg, hex) >= target);
    const soft = oklchToHex(0.955, Math.min(p.C, 0.035), p.H);
    const text = walk(Math.min(p.L, 0.55), p.C, p.H, -1, (hex) => minContrast(hex, [...neutrals, soft]) >= target);
    Object.assign(out, { primary, 'primary-hover': hover, 'primary-fg': fg, 'primary-soft': soft, 'primary-text': text, focus: text, 'chart-1': primary });
  } else {
    const fg = oklchToHex(0.2, Math.min(C, 0.06), H);
    const primary = walk(Math.max(L, 0.72), C, H, +1, (hex) => contrast(fg, hex) >= target && minContrast(hex, neutrals) >= 3);
    const p = hexToOklch(primary);
    const hover = walk(p.L + 0.05, p.C, p.H, +1, (hex) => contrast(fg, hex) >= target);
    const soft = oklchToHex(0.3, Math.min(p.C * 0.5, 0.06), p.H);
    const text = walk(Math.max(p.L, 0.78), p.C, p.H, +1, (hex) => minContrast(hex, [...neutrals, soft]) >= target);
    Object.assign(out, { primary, 'primary-hover': hover, 'primary-fg': fg, 'primary-soft': soft, 'primary-text': text, focus: text, 'chart-1': primary });
  }
  return out;
}

/** Derives `accent` and `accent-fg` for one mode from a brand accent colour. */
export function deriveAccent(accentHex, mode, target = 4.6) {
  const { L, C, H } = hexToOklch(accentHex);
  if (mode === 'light') {
    if (contrast(WHITE, accentHex) >= target) return { accent: accentHex, 'accent-fg': WHITE };
    return { accent: walk(L, C, H, -1, (hex) => contrast(WHITE, hex) >= target), 'accent-fg': WHITE };
  }
  const fg = oklchToHex(0.2, Math.min(C, 0.06), H);
  return { accent: walk(Math.max(L, 0.72), C, H, +1, (hex) => contrast(fg, hex) >= target), 'accent-fg': fg };
}
