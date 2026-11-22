import os, re, sys

ROOT = sys.argv[1]  # .../ds/project
P = {
 'plus': '<path d="M12 5v14M5 12h14"/>',
 'minus': '<path d="M5 12h14"/>',
 'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 'x': '<path d="M6 6l12 12M18 6L6 18"/>',
 'search': '<circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.2-4.2"/>',
 'bulb': '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/>',
 'home': '<path d="M4 11l8-7 8 7M6 9.5V20h12V9.5M10 20v-5h4v5"/>',
 'bolt': '<path d="M13 3L5 13.5h6L10 21l8-10.5h-6z"/>',
 'thermo': '<path d="M10 14.5V5a2 2 0 1 1 4 0v9.5a4 4 0 1 1-4 0z"/><path d="M12 15V9"/>',
 'bell': '<path d="M6 16v-5a6 6 0 0 1 12 0v5l1.5 2h-15zM10 20.5a2 2 0 0 0 4 0"/>',
 'moon': '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
 'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M5.3 18.7l1.4-1.4M17.3 6.7l1.4-1.4"/>',
 'plug': '<path d="M9 3v5M15 3v5M7 8h10v3a5 5 0 0 1-10 0zM12 16v5"/>',
 'drop': '<path d="M12 3.5s6 6.4 6 10.5a6 6 0 0 1-12 0c0-4.1 6-10.5 6-10.5z"/>',
 'leaf': '<path d="M5 19c0-8 5-13 14-14 0 9-5 14-13 14M5 19l7-7"/>',
 'snow': '<path d="M12 3v18M4.2 7.5l15.6 9M4.2 16.5l15.6-9"/>',
 'flame': '<path d="M12 21a6 6 0 0 1-6-6c0-3.5 3-5.5 3.5-9 2.5 1.5 4 3.5 4 5.5 1-1 1.5-2 1.5-3 1.8 1.6 3 3.8 3 6.5a6 6 0 0 1-6 6z"/>',
 'auto': '<path d="M12 4v2M12 18v2M4 12h2M18 12h2M6.3 6.3l1.4 1.4M16.3 16.3l1.4 1.4M6.3 17.7l1.4-1.4M16.3 7.7l1.4-1.4"/><circle cx="12" cy="12" r="3"/>',
 'fan': '<circle cx="12" cy="12" r="1.5"/><path d="M12 10.5c0-4 1-7 3.5-7s2.5 3-1 5.5M13.5 12c4 0 7 1 7 3.5s-3 2.5-5.5-1M12 13.5c0 4-1 7-3.5 7s-2.5-3 1-5.5M10.5 12c-4 0-7-1-7-3.5s3-2.5 5.5 1"/>',
 'shield': '<path d="M12 3l7 3v5c0 5-3 8.5-7 10-4-1.5-7-5-7-10V6z"/>',
 'lock': '<rect x="5" y="11" width="14" height="10" rx="2.5"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
 'music': '<path d="M9 18V6l10-2v12"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="16.5" cy="16" r="2.5"/>',
 'grid': '<rect x="4" y="4" width="6.5" height="6.5" rx="2"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="2"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="2"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="2"/>',
 'users': '<circle cx="9" cy="8" r="3.5"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6M16 4.5a3.5 3.5 0 0 1 0 7M18 14c2 .7 3 2.8 3 6"/>',
 'gear': '<circle cx="12" cy="12" r="3"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M5.3 18.7l2.1-2.1M16.6 7.4l2.1-2.1"/>',
 'chev': '<path d="M9 6l6 6-6 6"/>',
 'tv': '<rect x="3" y="5" width="18" height="12" rx="2.5"/><path d="M8 21h8"/>',
 'speaker': '<rect x="6" y="3" width="12" height="18" rx="3"/><circle cx="12" cy="14" r="3"/><circle cx="12" cy="7.5" r=".8"/>',
 'video': '<rect x="3" y="6" width="13" height="12" rx="2.5"/><path d="M16 10.5l5-3v9l-5-3"/>',
 'trend': '<path d="M3 17l6-6 4 4 8-8M15 7h6v6"/>',
 'sunrise': '<path d="M4 18h16M7 18a5 5 0 0 1 10 0M12 6v4M5.6 11.6l1.4 1.4M18.4 11.6L17 13"/>',
 'focus': '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r=".8"/>',
 'film': '<rect x="4" y="4" width="16" height="16" rx="2.5"/><path d="M8 4v16M16 4v16M4 9h4M4 15h4M16 9h4M16 15h4"/>',
 'door': '<path d="M6 21V4.5A1.5 1.5 0 0 1 7.5 3h9A1.5 1.5 0 0 1 18 4.5V21M4 21h16M14.5 12.5v.01"/>',
 'edit': '<path d="M4 20h4L19 9l-4-4L4 16zM13.5 6.5l4 4"/>',
 'trash': '<path d="M5 7h14M10 7V4.5h4V7M7 7l1 13h8l1-13"/>',
 'copy': '<rect x="8" y="8" width="12" height="12" rx="2.5"/><path d="M16 8V5.5A1.5 1.5 0 0 0 14.5 4h-9A1.5 1.5 0 0 0 4 5.5v9A1.5 1.5 0 0 0 5.5 16H8"/>',
 'play': '<path d="M8 5.5v13l10-6.5z"/>',
}

# ---- Lucide icons (icons/*.svg, ISC) replace the stand-ins above
LUCIDE = {'plus': 'plus', 'minus': 'minus', 'check': 'check', 'x': 'x', 'search': 'search', 'bulb': 'lightbulb',
  'home': 'house', 'bolt': 'zap', 'thermo': 'thermometer', 'bell': 'bell', 'moon': 'moon', 'sun': 'sun', 'plug': 'plug',
  'drop': 'droplet', 'leaf': 'leaf', 'snow': 'snowflake', 'flame': 'flame', 'auto': 'sparkles', 'fan': 'fan',
  'shield': 'shield', 'lock': 'lock', 'music': 'music', 'grid': 'layout-grid', 'users': 'users', 'gear': 'settings',
  'chev': 'chevron-right', 'chevdown': 'chevron-down', 'tv': 'tv', 'speaker': 'speaker', 'video': 'video',
  'trend': 'trending-up', 'sunrise': 'sunrise', 'focus': 'target', 'film': 'film', 'door': 'door-open',
  'edit': 'pencil', 'trash': 'trash-2', 'copy': 'copy', 'play': 'play', 'alert': 'triangle-alert'}
def _lucide(name):
    s = open(os.path.join(ROOT, 'icons', name + '.svg'), encoding='utf-8').read()
    body = re.search(r'<svg[^>]*>(.*)</svg>', s, re.S).group(1)
    return re.sub(r'\s*/>', '/>', re.sub(r'\s+', ' ', body)).strip()
for _k, _v in LUCIDE.items():
    if os.path.exists(os.path.join(ROOT, 'icons', _v + '.svg')):
        P[_k] = _lucide(_v)

def ico(m):
    name, cls = (m.group(1).split('|') + ['ico'])[:2]
    return '<svg class="%s" viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % (cls, P[name])

def doc(group, height, title, body, script, subtitle=''):
    sub = (' subtitle="%s"' % subtitle) if subtitle else ''
    group_attr = (' group="%s"' % group) if group else ''
    html = ('<!-- @dsCard%s height=%d%s -->\n<!doctype html>\n<html>\n<head><meta charset="utf-8"><title>%s</title></head>\n<body>\n%s\n<script>\n%s\n</script>\n</body>\n</html>\n'
            % (group_attr, height, sub, title, body.strip(), script.strip()))
    return re.sub(r'@@([a-z| -]+)@@', ico, html)

def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)

C = {}  # name -> (readme, preview)
exec(open(os.path.join(os.path.dirname(__file__), 'components.py'), encoding='utf-8').read())
exec(open(os.path.join(os.path.dirname(__file__), 'components2.py'), encoding='utf-8').read())
for name, (readme, prev) in C.items():
    write('components/%s/README.md' % name, readme.strip() + '\n')
    write('components/%s/preview.html' % name, prev)
print(len(C), 'components written')
