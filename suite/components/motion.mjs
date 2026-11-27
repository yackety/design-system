/*! Suite motion helpers. Framework-free ES module; Angular (@suite/ui) wraps them as directives.
 *  pill(track, options)        sliding highlight for .s-tabs, .s-seg, .s-nav, .s-bottom-nav
 *  countTo(el, value, options) number counts up from its last value
 *  replay(el)                  re-run the CSS entrance (.s-motion-rise / -slide / -fade) of an element
 *  reducedMotion()             true when the user asked for less motion
 */

const ACTIVE = '[aria-current="page"], [aria-selected="true"], [aria-pressed="true"]';

export const reducedMotion = () =>
  typeof matchMedia === 'function' && matchMedia('(prefers-reduced-motion: reduce)').matches;

/**
 * Draws the sliding pill behind the active item of `track`.
 * Call it again whenever the active item changes; it also follows resizes and font loading.
 * Returns { update, destroy }.
 */
export function pill(track, options = {}) {
  if (!track) return { update() {}, destroy() {} };
  track.classList.add('s-pill-track');
  let ind = track.querySelector(':scope > .s-pill');
  if (!ind) {
    ind = document.createElement('span');
    ind.className = 's-pill';
    ind.setAttribute('aria-hidden', 'true');
    track.prepend(ind);
  }
  let last = null;

  const place = (animate) => {
    const target = options.target ? options.target() : track.querySelector(ACTIVE);
    if (!target || !target.offsetWidth) { track.classList.remove('is-pill'); last = null; return; }
    const W = Math.max(track.scrollWidth, track.offsetWidth);
    const H = Math.max(track.scrollHeight, track.offsetHeight);
    const box = target.getBoundingClientRect();
    const host = track.getBoundingClientRect();
    const left = box.left - host.left + track.scrollLeft;
    const top = box.top - host.top + track.scrollTop;
    const edges = { t: top, l: left, r: W - (left + box.width), b: H - (top + box.height) };
    ind.style.width = W + 'px';
    ind.style.height = H + 'px';

    if (last && ['t', 'r', 'b', 'l'].every((k) => Math.abs(edges[k] - last[k]) < 0.5)) return; // nothing moved
    const moving = animate && last && !reducedMotion();
    if (moving) {
      const vertical = Math.abs(edges.t - last.t) > Math.abs(edges.l - last.l);
      ind.dataset.axis = vertical ? 'y' : 'x';
      ind.dataset.dir = (vertical ? edges.t > last.t : edges.l > last.l) ? 'fwd' : 'back';
      ind.classList.add('is-moving');
    } else {
      ind.classList.remove('is-moving');
    }
    for (const k of ['t', 'r', 'b', 'l']) ind.style.setProperty(`--pill-${k}`, edges[k] + 'px');
    track.classList.add('is-pill');
    last = edges;
  };

  place(false);
  const ro = typeof ResizeObserver === 'function' ? new ResizeObserver(() => place(false)) : null;
  ro?.observe(track);
  document.fonts?.ready?.then(() => place(false));

  return {
    update: () => place(true),
    destroy() { ro?.disconnect(); ind.remove(); track.classList.remove('is-pill', 's-pill-track'); },
  };
}

const easeOutCubic = (t) => 1 - Math.pow(1 - t, 3);

/**
 * Counts the number in `el` from its last value (or `from`) to `to`.
 * `format` turns a number into text, e.g. (v) => new Intl.NumberFormat('vi-VN').format(Math.round(v)).
 */
export function countTo(el, to, { from, duration = 900, format = (v) => String(Math.round(v)), flash = false } = {}) {
  if (!el) return Promise.resolve();
  const start = from ?? el.__suiteValue ?? 0;
  if (reducedMotion() || start === to) {
    el.__suiteValue = to;
    el.textContent = format(to);
    return Promise.resolve();
  }
  cancelAnimationFrame(el.__suiteFrame);
  return new Promise((done) => {
    const t0 = performance.now();
    const step = (now) => {
      const t = Math.min(1, (now - t0) / duration);
      const v = start + (to - start) * easeOutCubic(t);
      el.__suiteValue = v;
      el.textContent = format(v);
      if (t < 1) el.__suiteFrame = requestAnimationFrame(step);
      else {
        el.__suiteValue = to;
        el.textContent = format(to);
        if (flash) { el.classList.remove('s-flash'); void el.offsetWidth; el.classList.add('s-flash'); }
        done();
      }
    };
    el.__suiteFrame = requestAnimationFrame(step);
  });
}

/** Re-runs the CSS entrance animation of `el` (and its children for the stagger classes). */
export function replay(el) {
  if (!el || reducedMotion()) return;
  const cls = ['s-motion-rise', 's-motion-slide', 's-motion-fade'].filter((c) => el.classList.contains(c));
  el.classList.remove(...cls);
  void el.offsetWidth;
  el.classList.add(...cls);
}
