#!/usr/bin/env python3
"""
Gopang Build Script
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).parent

def read(path, label):
    p = ROOT / path
    if not p.exists():
        print(f"ERROR - File not found: {p}")
        sys.exit(1)
    content = p.read_text(encoding='utf-8')
    print(f"OK {label}: {len(content):,} chars")
    return content

klaw_prompt = read('klaw/prompts/system_prompt.txt', 'K-Law prompt')
iddm_prompt = read('klaw/iddm/IDDM_full.txt', 'IDDM prompt')
template    = read('src/index_template.html', 'HTML template')

ver_m   = re.search(r'v(\d+\.\d+)', klaw_prompt)
version = ver_m.group(0) if ver_m else 'v14.3'
print(f"OK K-Law version: {version}")

output = template
output = output.replace('{{KLAW_PROMPT}}', json.dumps(klaw_prompt, ensure_ascii=False))
output = output.replace('{{IDDM_PROMPT}}', json.dumps(iddm_prompt, ensure_ascii=False))
output = output.replace('{{VERSION}}', version)

for marker in ['{{KLAW_PROMPT}}', '{{IDDM_PROMPT}}', '{{VERSION}}']:
    if marker in output:
        print(f"ERROR - Replace failed: {marker}")
        sys.exit(1)

out_path = ROOT / 'index.html'
out_path.write_text(output, encoding='utf-8')
print(f"\nOK Build complete: index.html ({len(output):,} chars)")
print(f"   K-Law {version} prompt embedded")