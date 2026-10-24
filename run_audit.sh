#!/usr/bin/env bash
# Setup + run script for audit_project.py
# Usage: ./run_audit.sh /path/to/MAKSIMAR_PLATFORM

set -e

if [ -z "$1" ]; then
    echo "Usage: ./run_audit.sh /path/to/your/repo"
    exit 1
fi

# Resolve the directory this script itself lives in, so it works
# no matter which directory you run it from.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing analysis tools (vulture, pydeps)..."
pip install vulture pydeps --break-system-packages --quiet || \
    pip install vulture pydeps --quiet

echo "Running audit on $1 ..."
python3 "$SCRIPT_DIR/audit_project.py" "$1"

echo ""
echo "Done. Open audit_report/SUMMARY.md first, then duplicates.md,"
echo "then dependency_graph.svg (open in a browser or image viewer)."
