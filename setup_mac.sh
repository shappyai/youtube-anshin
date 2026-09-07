#!/usr/bin/env bash
set -euo pipefail
[ -d .git ] || git init
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r requirements.txt
python scripts/doctor.py
echo "Setup complete. Next: codex"
