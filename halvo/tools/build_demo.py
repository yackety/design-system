"""Build a local demo of the Halvo design system.

Usage (from the halvo folder):  python tools/build_demo.py .
Then open demo/index.html in a browser (double-click works; no server needed).

It compiles tokens.json into demo/tokens.css, wraps every components/<Name>/preview.html
into demo/<Name>.html (loading tokens.css, components/bundle.css and components/bundle.js),
and writes demo/index.html: a gallery of every component with a light/dark switch.
"""
import glob
import html
import json
import os
import re
import sys

root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
out = os.path.join(root, 'demo')
os.makedirs(out, exist_ok=True)

# ---- tokens.json -> tokens.css (same layout the design-system page generates)
t = json.load(open(os.path.join(root, 'tokens.json'), encoding='utf-8'))
themes = [x['id'] for x in t['color']['themes']]
first = themes[0]


def val(v, theme):
    return v if isinstance(v, str) else v.get(theme, v.get(first))


css = ['/* Halvo — generated from tokens.json by tools/build_demo.py */']
for i, theme in enumerate(themes):
    sel = ':root, [data-theme="%s"]' % theme if i == 0 else '[data-theme="%s"]' % theme
    rows = ['  --%s: %s;' % (c['name'], val(c['value'], theme)) for c in t['color']['tokens'] + t.get('shadow', {}).get('tokens', [])]
    css.append(sel + ' {\n' + '\n'.join(rows) + '\n}')
rows = []
for fam, body in t.items():
    if fam in ('name', 'version', 'meta', 'color', 'type', 'shadow') or not isinstance(body, dict) or 'tokens' not in body:
        continue
    rows += ['  --%s: %s;' % (c['name'], c['value']) for c in body['tokens']]
rows += ['  --font-%s: %s;' % (k, v) for k, v in t['type']['families'].items()]
css.append(':root {\n' + '\n'.join(rows) + '\n}')
open(os.path.join(out, 'tokens.css'), 'w', encoding='utf-8').write('\n'.join(css) + '\n')

# ---- component order and groups (bundle header, then folders)
bundle = open(os.path.join(root, 'components', 'bundle.js'), encoding='utf-8').read()
m = re.search(r'@ds-bundle: (\{.*?\}) \*/', bundle)
order = [c['name'] for c in json.loads(m.group(1))['components']] if m else []
folders = sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(root, 'components', '*', 'preview.html')))
names = [n for n in ['Cover'] + order if n in folders] + [n for n in folders if n not in order and n != 'Cover']

HEAD = ('<meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="tokens.css"><link rel="stylesheet" href="../components/bundle.css">'
        '<script src="../components/bundle.js"></script>'
        '<script>try{var t=new URLSearchParams(location.search).get("theme")||localStorage.getItem("halvo-demo-theme");if(t)document.documentElement.dataset.theme=t}catch(e){}</script>')
cards = []
for n in names:
    src = open(os.path.join(root, 'components', n, 'preview.html'), encoding='utf-8').read()
    marker = re.match(r'<!-- @dsCard([^>]*)-->', src)
    attrs = dict(re.findall(r'(\w+)=("[^"]*"|\S+)', marker.group(1))) if marker else {}
    height = int(attrs.get('height', '200').strip('"'))
    group = attrs.get('group', '"Overview"' if n == 'Cover' else '"Other"').strip('"')
    page = src.replace('<html>', '<html data-theme="%s">' % first, 1)
    page = page.replace('</title>', '</title>' + HEAD, 1) if '</title>' in page else page.replace('<head>', '<head>' + HEAD, 1)
    open(os.path.join(out, n + '.html'), 'w', encoding='utf-8').write(page)
    readme = os.path.join(root, 'components', n, 'README.md')
    summary = ''
    if os.path.exists(readme):
        lines = [l for l in open(readme, encoding='utf-8').read().splitlines() if l.strip() and not l.startswith('#')]
        summary = lines[0] if lines else ''
    cards.append((n, group, height, summary))

# ---- gallery
nav, body, last = [], [], None
for n, group, height, summary in cards:
    if group != last:
        body.append('<h2 class="g">%s</h2>' % html.escape(group))
        nav.append('<span class="nav-g">%s</span>' % html.escape(group))
        last = group
    nav.append('<a href="#%s">%s</a>' % (n, n))
    body.append('<section class="item" id="%s"><header><h3>%s</h3><p>%s</p><a class="open" href="%s.html" target="_blank">Open ↗</a></header>'
                '<iframe src="%s.html" style="height:%dpx" loading="lazy" title="%s"></iframe></section>'
                % (n, n, html.escape(re.sub(r'[`*]', '', summary)), n, n, height, n))

index = """<!doctype html>
<html data-theme="%(first)s">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Halvo design system — demo</title>
<link rel="stylesheet" href="tokens.css"><link rel="stylesheet" href="../components/bundle.css">
<style>
  body { margin: 0; display: grid; grid-template-columns: 220px minmax(0, 1fr); min-height: 100vh; }
  aside { position: sticky; top: 0; height: 100vh; overflow-y: auto; padding: 20px 14px; border-right: 1px solid var(--line); box-sizing: border-box; }
  aside b { display: block; font-size: 21px; letter-spacing: -.02em; margin: 0 0 4px 6px; }
  aside small { display: block; color: var(--muted); margin: 0 0 14px 6px; font-weight: 600; }
  aside a { display: block; padding: 6px 8px; border-radius: 10px; color: var(--ink-2); text-decoration: none; font-weight: 600; font-size: 13.5px; }
  aside a:hover { background: var(--glass-2); color: var(--ink); }
  .nav-g { display: block; margin: 14px 0 4px 8px; font-size: 11px; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); font-weight: 700; }
  main { padding: 24px 28px 80px; max-width: 1060px; }
  .top { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
  .top h1 { flex: 1; font-size: 30px; font-weight: 600; letter-spacing: -.025em; }
  .g { margin: 36px 0 10px; font-size: 11px; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); font-weight: 700; }
  .item { margin-bottom: 18px; }
  .item header { display: flex; align-items: baseline; gap: 12px; margin-bottom: 8px; }
  .item h3 { font-size: 15px; font-weight: 600; }
  .item p { flex: 1; color: var(--muted); font-size: 12.5px; font-weight: 600; }
  .open { color: var(--accent-text); font-size: 12.5px; font-weight: 600; text-decoration: none; }
  iframe { display: block; width: 100%%; border: 0; border-radius: 22px; background: var(--bg); box-shadow: inset 0 0 0 1px var(--line); }
</style></head>
<body>
<aside><b>Halvo</b><small>The smart home, under glass.</small>%(nav)s</aside>
<main>
  <div class="top"><h1>Design system demo</h1><button class="btn btn--sm" id="theme">Switch to light</button></div>
  <p class="muted" style="font-weight:600">Every component preview, live. Rebuild with <code>python tools/build_demo.py .</code> after editing.</p>
  %(body)s
</main>
<script>
  var root = document.documentElement, btn = document.getElementById('theme');
  function apply(t) {
    root.dataset.theme = t; btn.textContent = t === 'dark' ? 'Switch to light' : 'Switch to dark';
    try { localStorage.setItem('halvo-demo-theme', t); } catch (e) {}
    document.querySelectorAll('iframe').forEach(function (f) { try { f.contentDocument.documentElement.dataset.theme = t; } catch (e) { f.src = f.src.split('?')[0] + '?theme=' + t; } });
  }
  var saved = null; try { saved = localStorage.getItem('halvo-demo-theme'); } catch (e) {}
  if (saved) apply(saved);
  btn.onclick = function () { apply(root.dataset.theme === 'dark' ? 'light' : 'dark'); };
</script>
</body>
</html>
""" % {'first': first, 'nav': '\n'.join(nav), 'body': '\n  '.join(body)}
open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(index)
print('demo/: %d component pages + index.html + tokens.css' % len(cards))
