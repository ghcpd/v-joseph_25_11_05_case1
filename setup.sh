#!/usr/bin/env bash
set -e
# Creates a virtual environment and installs test dependencies
# POSIX: ./setup.sh
# Windows (PowerShell): .\setup.sh (run within a PowerShell session)

PY=python
if command -v python3 >/dev/null 2>&1; then
  PY=python3
fi

$PY -m venv .venv

# POSIX activation
if [ -f ".venv/bin/activate" ]; then
  echo "Activating POSIX venv"
  source .venv/bin/activate
else
  echo "POSIX venv not found; if you're on Windows, activate with: .\\.venv\\Scripts\\Activate.ps1"
fi

pip install --upgrade pip
pip install -r requirements.txt

echo "Setup finished. Activate the virtual environment and run tests with ./run_tests.sh or python test_script.py"
