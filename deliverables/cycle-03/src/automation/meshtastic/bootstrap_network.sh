#!/usr/bin/env bash
set -euo pipefail

DRY_RUN=0
VERIFY=0
HUB_HOST=${HUB_HOST:-localhost}
HUB_PORT=${HUB_PORT:-8081}

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

step "Check hub health" "curl -fsS http://$HUB_HOST:$HUB_PORT/health"
step "Check sync health" "curl -fsS http://$HUB_HOST:$HUB_PORT/sync/health"

if [ "$VERIFY" -eq 1 ]; then
  echo "[verify] open http://$HUB_HOST:$HUB_PORT/monitor_v2.html"
fi
