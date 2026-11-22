"""Generate Tailwind theme files from tokens.json, so Tailwind utilities speak Halvo.

Usage (from the halvo folder):  python tools/build_tailwind.py .
Writes:
  tailwind/halvo.css        Tailwind v4: @import after "tailwindcss" (see header comment inside)
  tailwind/halvo.preset.js  Tailwind v3: presets: [require('./halvo/tailwind/halvo.preset.js')]
Colours point at Halvo's CSS variables, so they follow data-theme (dark / light) automatically.
"""
import json
import os
import sys

root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
t = json.load(open(os.path.join(root, 'tokens.json'), encoding='utf-8'))
out = os.path.join(root, 'tailwind')
os.makedirs(out, exist_ok=True)

colors = [c['name'] for c in t['color']['tokens']]
radius = {c['name'].replace('r-', '', 1): c['name'] for c in t['radius']['tokens']}
radius_extra = {'control': '13px', 'small': '11px'}  # component radii the README names (buttons/inputs, chips/small)
spacing = {c['name']: c['name'] for c in t['spacing']['tokens'] if c['name'] != 'max'}
max_width = next((c['value'] for c in t['spacing']['tokens'] if c['name'] == 'max'), '1480px')
shadows = {'surface': 'shadow', 'overlay': 'shadow-lg'}  # not 'glass': it would clash with the glass colour (shadow-<colour>)
font_sans = t['type']['families']['sans']
text = []
for g in t['type']['groups']:
    for s in g['styles']:
        name = s['name'][3:] if s['name'].startswith('fs-') else s['name']
        text.append((name, s['fontSize'], s.get('lineHeight'), s.get('letterSpacing'), s.get('fontWeight')))
eases = []
for c in t['ease']['tokens']:
    name = 'halvo' if c['name'] == 'ease' else c['name'].replace('ease-', '', 1)
    eases.append((name, c['value']))
durations = [(c['name'].replace('dur-', '', 1), c['value']) for c in t['duration']['tokens']]

# ---------------------------------------------------------------- v4
v4 = ['/* Halvo for Tailwind CSS v4 — generated from tokens.json by tools/build_tailwind.py. Do not edit by hand.',
      '',
      '   app.css:',
      '     @import url("https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap");  (must come first:',
      '        bundle.css imports the font too, but an @import inside a layer is ignored by browsers)',
      '     @import "tailwindcss" prefix(tw);              (prefix avoids the .ring / .table name clash with Halvo)',
      '     @import "../halvo/demo/tokens.css" layer(base);  (or your copy of tokens.css)',
      '     @import "../halvo/components/bundle.css" layer(components);',
      '     @import "../halvo/tailwind/halvo.css";',
      '',
      '   Then: tw:bg-glass tw:text-muted tw:rounded-lg tw:p-gap tw:shadow-surface tw:ease-expo-out tw:dark:bg-well',
      '   Tailwind\'s default palette is removed on purpose: colours come only from Halvo. */',
      '',
      '@custom-variant dark (&:where([data-theme=dark], [data-theme=dark] *));',
      '@custom-variant light (&:where([data-theme=light], [data-theme=light] *));',
      '',
      '@theme inline {',
      '  --color-*: initial;',
      '  --color-white: #fff;',
      '  --color-black: #000;']
v4 += ['  --color-%s: var(--%s);' % (n, n) for n in colors]
v4 += ['', '  --font-sans: %s;' % font_sans, '  --font-halvo: %s;' % font_sans, '']
for name, size, lh, ls, fw in text:
    v4.append('  --text-%s: %s;' % (name, size))
    if lh is not None:
        v4.append('  --text-%s--line-height: %s;' % (name, lh))
    if ls:
        v4.append('  --text-%s--letter-spacing: %s;' % (name, ls))
    if fw:
        v4.append('  --text-%s--font-weight: %s;' % (name, str(fw).split()[0]))
v4.append('')
v4 += ['  --radius-%s: var(--%s);' % (k, v) for k, v in radius.items()]
v4 += ['  --radius-%s: %s;' % (k, v) for k, v in radius_extra.items()]
v4.append('')
v4 += ['  --spacing-%s: var(--%s);' % (k, v) for k, v in spacing.items()]
v4 += ['  --container-content: %s;' % max_width, '']
v4 += ['  --shadow-%s: var(--%s);' % (k, v) for k, v in shadows.items()]
v4.append('')
v4 += ['  --ease-%s: %s;' % (k, v) for k, v in eases]
v4 += ['}', '',
       '/* Durations have no theme namespace in v4; these utilities mirror the duration tokens. */']
for name, v in durations:
    v4 += ['@utility duration-%s {' % name, '  transition-duration: %s;' % v, '  animation-duration: %s;' % v, '}']
open(os.path.join(out, 'halvo.css'), 'w', encoding='utf-8').write('\n'.join(v4) + '\n')

# ---------------------------------------------------------------- v3
def js(obj, ind=4):
    return json.dumps(obj, indent=2).replace('\n', '\n' + ' ' * ind)


fonts = [f.strip().strip('"') for f in font_sans.split(',')]
font_size = {}
for name, size, lh, ls, fw in text:
    opts = {}
    if lh is not None:
        opts['lineHeight'] = str(lh)
    if ls:
        opts['letterSpacing'] = ls
    if fw:
        opts['fontWeight'] = str(fw).split()[0]
    font_size[name] = [size, opts]
preset = {
    'darkMode': ['selector', '[data-theme="dark"]'],
    'theme': {'extend': {
        'colors': {n: 'var(--%s)' % n for n in colors},
        'fontFamily': {'sans': fonts, 'halvo': fonts},
        'fontSize': font_size,
        'borderRadius': dict({k: 'var(--%s)' % v for k, v in radius.items()}, **radius_extra),
        'spacing': {k: 'var(--%s)' % v for k, v in spacing.items()},
        'maxWidth': {'content': max_width},
        'boxShadow': {k: 'var(--%s)' % v for k, v in shadows.items()},
        'transitionTimingFunction': dict(eases),
        'transitionDuration': {k: v for k, v in durations},
    }},
}
v3 = ['/* Halvo preset for Tailwind CSS v3 — generated from tokens.json by tools/build_tailwind.py. Do not edit by hand.',
      ' *',
      ' * tailwind.config.js:',
      " *   module.exports = { presets: [require('./halvo/tailwind/halvo.preset.js')], prefix: 'tw-', content: [...] }",
      ' * Load tokens.css and components/bundle.css after @tailwind base and @tailwind components, before @tailwind utilities.',
      ' * Put the Be Vietnam Pro @import url(https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap) first in your CSS.',
      ' * Colours are CSS variables, so opacity modifiers (bg-accent/50) do not work in v3; use the *-soft tokens instead.',
      ' */',
      'module.exports = ' + js(preset, 0) + ';']
open(os.path.join(out, 'halvo.preset.js'), 'w', encoding='utf-8').write('\n'.join(v3) + '\n')
print('tailwind/halvo.css + tailwind/halvo.preset.js: %d colours, %d text sizes, %d eases' % (len(colors), len(text), len(eases)))
