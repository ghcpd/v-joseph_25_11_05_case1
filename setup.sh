#!/usr/bin/env bash
# Setup script (POSIX). On Windows use the corresponding PowerShell commands.
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
