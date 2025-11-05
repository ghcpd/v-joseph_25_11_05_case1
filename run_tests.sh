#!/usr/bin/env bash
set -e
source .venv/bin/activate
python test_script.py > defects.txt 2>&1 || true
