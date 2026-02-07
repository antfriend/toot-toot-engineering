#!/usr/bin/env bash
set -euo pipefail

DRY_RUN=0
VERIFY=0
PORT=${PORT:-/dev/ttyUSB0}
CHANNEL=${MESH_CHANNEL:-field}
PSK=${MESH_PSK:-}
REGION=${MESH_REGION:-US}
NAME=${NODE_NAME:-}

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --verify) VERIFY=1 ;;
    --port=*) PORT="${arg#*=}" ;;
    --name=*) NAME="${arg#*=}" ;;
  esac
done

if [ -z "$PSK" ]; then
  echo "MESH_PSK is required (set in deploy.env)"
  exit 1
fi

if [ -z "$NAME" ]; then
  echo "NODE_NAME is required (use --name=)"
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

step "Set region" "meshtastic --port $PORT --set lora.region $REGION"
step "Set channel name" "meshtastic --port $PORT --set channel.name $CHANNEL"
step "Set channel PSK" "meshtastic --port $PORT --set channel.psk $PSK"
step "Set node long name" "meshtastic --port $PORT --set device.longName $NAME"

if [ "$VERIFY" -eq 1 ]; then
  echo "[verify] node info"
  if [ "$DRY_RUN" -eq 0 ]; then
    meshtastic --port $PORT --info
  fi
fi
