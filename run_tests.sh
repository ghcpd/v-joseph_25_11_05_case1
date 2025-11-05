#!/usr/bin/env bash
set -e

LOG_DIR=logs
mkdir -p "$LOG_DIR"

# Activate virtualenv if available
if [ -f ".venv/bin/activate" ]; then
  echo "Activating venv..."
  source .venv/bin/activate
fi

echo "Running test_script.py..."
python test_script.py > "$LOG_DIR/test_script_output.txt" 2>&1 || true

# If pytest is installed, run tests
if command -v pytest >/dev/null 2>&1; then
  echo "Running pytest..."
  pytest -q > "$LOG_DIR/pytest_output.txt" 2>&1 || true
fi

# Summarize logs into defects.txt
cat "$LOG_DIR/test_script_output.txt" > defects.txt
if [ -f "$LOG_DIR/pytest_output.txt" ]; then
  echo "\n--- pytest output ---\n" >> defects.txt
  cat "$LOG_DIR/pytest_output.txt" >> defects.txt
fi

echo "Logs saved to $LOG_DIR and defects.txt"
