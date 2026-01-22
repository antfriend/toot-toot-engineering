#!/usr/bin/env bash
set -euo pipefail

python3 tte_monitor.py >/tmp/tte_monitor.log 2>&1 &
disown

python3 tte_agent.py
