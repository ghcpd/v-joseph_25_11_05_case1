#!/usr/bin/env bash
set -euo pipefail
# Create virtual environment
python -m venv .venv
if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
elif [ -f .venv/Scripts/activate ]; then
  # For Git Bash on Windows
  source .venv/Scripts/activate
fi
pip install -r requirements.txt
