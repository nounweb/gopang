#!/usr/bin/env python3
"""
고팡(Gopang) 빌드 스크립트
------------------------------
역할:
  klaw/prompts/system_prompt.txt (K-Law 프롬프트)
  klaw/iddm/IDDM_full.txt        (IDDM 프롬프트)
  src/index_template.html        (HTML 템플릿)
→ index.html 생성 (프롬프트가 내장된 완성본)

실행:
  python3 build.py

GitHub Actions에서 자동 실행:
  klaw/prompts/system_prompt.txt 변경 후 push → 자동 빌드 → Pages 배포
"""

import json, re, sys
from pathlib import Path

ROOT = Path(__file__).parent

# ── 1. 파일 읽기 ──────────────────────────────────────────────
def read(path, label):
    p = ROOT / path
    if not p.exists():
        print(f"❌ 파일 없음: {p}")
        sys.exit(1)
    content = p.read_text(encoding='utf-8')
    print(f"✅ {label}: {len(content):,}자")
    return content

klaw_prompt = read('klaw/prompts/system_prompt.txt', 'K-Law 프롬프트')
iddm_prompt  = read('klaw/iddm/IDDM_full.txt',        'IDDM 프롬프트')
template     = read('src/index_template.html',          'HTML 템플릿')

# ── 2. 버전 자동 추출 ─────────────────────────────────────────
ver_m   = re.search(r'v(\d+\.\d+)', klaw_prompt)
version = ver_m.group(0) if ver_m else 'v14.3'
print(f"✅ 감지된 K-Law 버전: {version}")

# ── 3. 플레이스홀더 교체 ──────────────────────────────────────
# 템플릿에서 {{KLAW_PROMPT}}, {{IDDM_PROMPT}}, {{VERSION}} 치환
output = template
output = output.replace('{{KLAW_PROMPT}}', json.dumps(klaw_prompt, ensure_ascii=False))
output = output.replace('{{IDDM_PROMPT}}',  json.dumps(iddm_prompt,  ensure_ascii=False))
output = output.replace('{{VERSION}}',      version)

# 치환 확인
for marker in ['{{KLAW_PROMPT}}', '{{IDDM_PROMPT}}', '{{VERSION}}']:
    if marker in output:
        print(f"❌ 치환 실패: {marker}")
        sys.exit(1)

# ── 4. 출력 ───────────────────────────────────────────────────
out_path = ROOT / 'index.html'
out_path.write_text(output, encoding='utf-8')
print(f"\n✅ 빌드 완료: index.html ({len(output):,}자)")
print(f"   K-Law {version} 프롬프트 내장됨")
