import os
import re
from pathlib import Path

root = Path('.')
ignore_dirs = {'venv', '.git', '__pycache__'}

py_files = [p for p in root.rglob('*.py') if not any(part in ignore_dirs for part in p.parts)]
missing = []
references = []
for py in py_files:
    text = py.read_text(encoding='utf-8', errors='ignore')
    for m in re.finditer(r"render\(request,\s*['\"]([^'\"]+)['\"]", text):
        tpl = m.group(1)
        references.append((py, tpl))
        # Search for the template file in the project tree.
        found = any(p.match(f'**/{tpl}') or str(p).endswith(tpl.replace('/', os.sep)) for p in root.rglob('*.html'))
        if not found:
            missing.append((py, tpl))
print(f'Template references found: {len(references)}')
for py, tpl in references:
    print(f'{py} -> {tpl}')
print(f'Missing template files: {len(missing)}')
for py, tpl in missing:
    print(f'{py} -> {tpl}')
