import os
import pathlib
import re

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
import django

django.setup()

from django.urls import get_resolver

resolver = get_resolver()
pattern_names = set(name for name in resolver.reverse_dict.keys() if isinstance(name, str))
url_re = re.compile(r"\{\%\s*url\s+'([^']+)'(?:\s+[^\%]+)?\s*\%\}")
template_names = set()
for p in pathlib.Path('.').rglob('*.html'):
    text = p.read_text(encoding='utf-8', errors='ignore')
    names = [m.group(1) for m in url_re.finditer(text)]
    if names:
        print('FILE', p)
        print(names)
        template_names.update(names)

print('total', len(template_names))
print(sorted(template_names))
print('missing', sorted(template_names - pattern_names))
print('patterns loaded', len(pattern_names))
