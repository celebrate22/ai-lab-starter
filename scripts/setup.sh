#!/bin/sh

# Prepare this project on Linux or macOS: create its private Python environment
# and install the package plus the optional tools used for development.
set -eu

# Find this project's folder from this script's location, not the terminal's
# current folder. CDPATH is cleared so shell settings do not add extra output.
PROJECT_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$PROJECT_ROOT"

# Allow a different Python command, for example: make setup PYTHON=python3.12.
PYTHON=${PYTHON:-python3}

if ! command -v "$PYTHON" >/dev/null 2>&1; then
    echo "Python command '$PYTHON' was not found. Set PYTHON to a Python 3.10+ command." >&2
    exit 1
fi

# Create an isolated environment, then use its Python to install this project.
"$PYTHON" -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'

echo "Setup complete. Run 'make check' to inspect this environment."
