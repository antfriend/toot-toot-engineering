#!/usr/bin/env bash
set -euo pipefail

DRY_RUN=0
VERIFY=0
PORT=${K10_SERIAL:-/dev/ttyACM0}
K10_ID=${K10_ID:-hw:k10}

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --verify) VERIFY=1 ;;
    --port=*) PORT="${arg#*=}" ;;
  esac
done

step() {
  echo "[step] $1"
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "[dry-run] $2"
  else
    eval "$2"
  fi
}

step "Activate venv" "source .venv/bin/activate"
step "Run K10 gateway" "PYTHONPATH=. python deliverables/cycle-01/src/k10_gateway/k10_gateway.py --port $PORT --k10-id $K10_ID"

if [ "$VERIFY" -eq 1 ]; then
  echo "[verify] check ttdb.log grows in deliverables/cycle-01/src/data"
fi
