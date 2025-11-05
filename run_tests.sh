#!/usr/bin/env bash
set -e
if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
elif [ -f .venv/Scripts/activate ]; then
  source .venv/Scripts/activate
fi
python test_script.py > defects.txt 2>&1 || true
