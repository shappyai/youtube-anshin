$ErrorActionPreference = "Stop"
if (!(Test-Path .git)) { git init }
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt
python scripts\doctor.py
Write-Host "Setup complete. Next: codex" -ForegroundColor Green
