#!/usr/bin/env bash
set -euo pipefail

# Activate virtual environment if present
if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

LOGFILE=test_output.log
# Run pytest to execute tests
python -m pytest -q --disable-warnings --maxfail=1 | tee "$LOGFILE"

# Append pytest output to defects.txt so manual notes are preserved.
cat "$LOGFILE" >> defects.txt

# Exit with pytest status
exit ${PIPESTATUS[0]:-$?}
