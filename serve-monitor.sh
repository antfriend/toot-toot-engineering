#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Simple local server for monitor.html
python3 -m http.server 8000
