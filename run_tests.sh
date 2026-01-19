#!/usr/bin/env bash
# DataSync Pro v2.0 - Test Execution Script
# Runs test_script.py and collects all output to defects.txt

set -e

echo "=========================================="
echo "DataSync Pro v2.0 - Test Execution"
echo "=========================================="
echo

# Detect OS for virtual environment activation
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    VENV_ACTIVATE=".venv\\Scripts\\activate"
else
    VENV_ACTIVATE=".venv/bin/activate"
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Running setup.sh..."
    bash setup.sh
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_ACTIVATE"

# Run tests and capture all output
echo "Running tests..."
echo

# Create defects.txt with test execution header
{
    echo "================================================================================"
    echo "DATASYNC PRO v2.0 - TEST EXECUTION REPORT"
    echo "================================================================================"
    echo "Test Execution Date: $(date)"
    echo "================================================================================"
    echo
    echo "TEST EXECUTION LOG:"
    echo "================================================================================"
    echo
    python test_script.py
    TEST_EXIT_CODE=$?
    echo
    echo "================================================================================"
    echo "TEST EXECUTION COMPLETED"
    echo "Exit Code: $TEST_EXIT_CODE"
    echo "================================================================================"
} | tee defects.txt

# Extract just the exit code for script exit
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo
    echo "✓ All tests passed!"
    exit 0
else
    echo
    echo "✗ Some tests failed. Check defects.txt for details."
    exit 1
fi
