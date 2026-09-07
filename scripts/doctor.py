from __future__ import annotations
import shutil, sys, os
from pathlib import Path
from _common import ROOT, find_font

checks = []
for name in ['git','ffmpeg','ffprobe','codex']:
    p = shutil.which(name)
    checks.append((name, bool(p), p or 'not found'))
checks.append(('python>=3.11', sys.version_info >= (3,11), sys.version.split()[0]))
checks.append(('Japanese font', bool(find_font()), find_font() or 'not found; thumbnail may need --font'))

print(f'Project: {ROOT}')
for name, ok, detail in checks:
    print(f"[{'OK' if ok else 'NG'}] {name}: {detail}")

required = [ROOT/'AGENTS.md', ROOT/'config/channel.yaml', ROOT/'config/production.yaml']
for p in required:
    print(f"[{'OK' if p.exists() else 'NG'}] file: {p.relative_to(ROOT)}")

api = bool(os.getenv('OPENAI_API_KEY'))
print(f"[{'OK' if api else '--'}] OPENAI_API_KEY: {'set' if api else 'not set (TTS is optional until needed)'}")

critical = [ok for name,ok,_ in checks if name in ('ffmpeg','ffprobe','python>=3.11')]
raise SystemExit(0 if all(critical) else 1)
