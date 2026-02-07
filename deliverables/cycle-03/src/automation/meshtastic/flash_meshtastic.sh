#!/usr/bin/env bash
set -euo pipefail

DRY_RUN=0
VERIFY=0
PORT=${1:-}
FIRMWARE_BIN=${FIRMWARE_BIN:-}

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --verify) VERIFY=1 ;;
    --port=*) PORT="${arg#*=}" ;;
    --bin=*) FIRMWARE_BIN="${arg#*=}" ;;
  esac
done

if [ -z "$PORT" ] || [ -z "$FIRMWARE_BIN" ]; then
  echo "Usage: flash_meshtastic.sh --port=/dev/ttyUSB0 --bin=firmware.bin [--dry-run] [--verify]"
  exit 1
fi

step() {
  echo "[step] $1"
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "[dry-run] $2"
  else
    eval "$2"
  fi
}

step "Erase flash" "esptool.py --port $PORT erase_flash"
step "Flash firmware" "esptool.py --port $PORT write_flash 0x10000 $FIRMWARE_BIN"

if [ "$VERIFY" -eq 1 ]; then
  echo "[verify] open Meshtastic client and confirm node boots"
fi
