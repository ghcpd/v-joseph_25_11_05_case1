#!/usr/bin/env bash
set -euo pipefail
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Windows PowerShell instructions (executable on PowerShell):
# python -m venv .venv
# .\.venv\Scripts\Activate.ps1
# python -m pip install --upgrade pip
# pip install -r requirements.txt

# Note: if datasync_pro is a local package in this repository and you want to import
# it as a package, either run tests from the repository root (PYTHONPATH includes it)
# or install it in editable mode if packaging is added (not present in this simple repo).