#!/bin/sh

# Create an isolated Python environment and install this project with dev tools.
set -eu

PROJECT_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$PROJECT_ROOT"

PYTHON=${PYTHON:-python3}

if ! command -v "$PYTHON" >/dev/null 2>&1; then
    echo "Python command '$PYTHON' was not found. Set PYTHON to a Python 3.10+ command." >&2
    exit 1
fi

"$PYTHON" -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'

echo "Setup complete. Run 'make check' to inspect this environment."
