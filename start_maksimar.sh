#!/usr/bin/env bash
set -euo pipefail

ROOT="$HOME/MAKSIMAR_PLATFORM"
LOGDIR="$ROOT/logs"
SYSLOG="$LOGDIR/system.log"

mkdir -p "$LOGDIR"
touch "$SYSLOG"

cd "$ROOT"

echo "[START] $(date -Is) Starting MAKSIMAR" | tee -a "$SYSLOG"

# 1) Secure bootstrap (genesis + core integrity)
python3 BOOT/system_bootstrap.py 2>&1 | tee -a "$SYSLOG"

# 2) Start dashboard (will also start Control Plane)
"$ROOT/tools/dashboard.sh"
