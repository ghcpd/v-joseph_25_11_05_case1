#!/usr/bin/env bash
# DataSync Pro v2.0 - Environment Setup Script
# Compatible with Linux, macOS, and Windows (Git Bash/WSL)

set -euo pipefail

echo "=========================================="
echo "DataSync Pro v2.0 - Environment Setup"
echo "=========================================="
echo

# Detect OS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    VENV_ACTIVATE=".venv\\Scripts\\activate"
    PYTHON_CMD="python"
else
    VENV_ACTIVATE=".venv/bin/activate"
    PYTHON_CMD="python3"
fi

# Create virtual environment
echo "Creating virtual environment..."
$PYTHON_CMD -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_ACTIVATE"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo
echo "=========================================="
echo "Setup complete! Virtual environment ready."
echo "=========================================="
echo
echo "To activate the environment, run:"
echo "  source $VENV_ACTIVATE"
echo
