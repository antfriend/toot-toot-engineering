# SOLUTION (cycle-03)

## Executive summary
This cycle delivers a deployment automation kit for the six-device TTN build. It includes repeatable scripts for Windows hub setup and launch, K10 gateway setup and run, Meshtastic flashing/configuration, and a network bootstrap check. Every script supports `--dry-run` and `--verify` modes.

## Automation matrix
- Windows hub: PowerShell scripts for venv setup and hub launch.
- K10 gateway: Bash scripts for venv setup and gateway run.
- Heltec + T-Deck: Bash scripts for flashing and Meshtastic configuration.
- Network bootstrap: Bash script for hub health checks and dashboard link.

## Scripts and workflows

### Common configuration
- `deliverables/cycle-03/src/automation/common/deploy.env.example`
- Set `MESH_PSK`, `MESH_CHANNEL`, `MESH_REGION`, ports, and hub host.

### Windows hub
- Setup: `deliverables/cycle-03/src/automation/windows/setup_hub.ps1`
- Run: `deliverables/cycle-03/src/automation/windows/run_hub.ps1`

### K10 gateway
- Setup: `deliverables/cycle-03/src/automation/k10/setup_k10.sh`
- Run: `deliverables/cycle-03/src/automation/k10/run_gateway.sh`

### Meshtastic nodes (Heltec + T-Deck)
- Flash firmware: `deliverables/cycle-03/src/automation/meshtastic/flash_meshtastic.sh`
- Configure node: `deliverables/cycle-03/src/automation/meshtastic/configure_meshtastic.sh`

### Network bootstrap
- Bootstrap checks: `deliverables/cycle-03/src/automation/meshtastic/bootstrap_network.sh`

## Operator sequence (recommended)
1. Prepare `deploy.env` from the example and export variables.
2. Run Windows hub setup and start the hub.
3. Flash Meshtastic firmware on Heltec nodes and T-Deck.
4. Configure each node with shared channel settings and unique names.
5. Setup K10 and start the gateway.
6. Run bootstrap check to verify hub health and dashboard.

## Verification signals
- Hub responds at `http://<hub>:8081/health` and `/monitor_v2.html`.
- Meshtastic `--info` shows configured channel and long name.
- K10 `ttdb.log` grows after messages are received.

## Notes and fallbacks
- If `esptool.py` is not available, install via `pip install esptool`.
- Some Meshtastic flashing steps may require GUI tools; document local constraints.
- Always validate region/channel settings with local regulatory requirements.

## Artifacts
- `deliverables/cycle-03/src/automation/`
- `deliverables/cycle-03/SOLUTION.md`
