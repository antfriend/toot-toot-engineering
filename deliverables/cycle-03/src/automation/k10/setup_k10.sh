#!/usr/bin/env bash
set -euo pipefail

DRY_RUN=0
VERIFY=0

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --verify) VERIFY=1 ;;
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

step "Create venv" "python3 -m venv .venv"
step "Activate venv" "source .venv/bin/activate"
step "Upgrade pip" "python -m pip install --upgrade pip"
step "Install meshtastic" "pip install meshtastic"

if [ "$VERIFY" -eq 1 ]; then
  echo "[verify] meshtastic version"
  if [ "$DRY_RUN" -eq 0 ]; then
    python -c "import meshtastic; print(meshtastic.__version__)"
  fi
fi
