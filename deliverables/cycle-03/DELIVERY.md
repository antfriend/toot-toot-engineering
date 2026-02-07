# DELIVERY (cycle-03)

## What shipped
- Deployment automation scripts for Windows hub, K10 gateway, and Meshtastic nodes.
- Network bootstrap checks and shared configuration template.

## How to run
1. Copy and edit `deliverables/cycle-03/src/automation/common/deploy.env.example` to `deploy.env`.
2. Source the env file on Linux:
   ```bash
   set -a; source deploy.env; set +a
   ```
3. Run Windows hub scripts:
   ```powershell
   powershell -ExecutionPolicy Bypass -File deliverables/cycle-03/src/automation/windows/setup_hub.ps1
   powershell -ExecutionPolicy Bypass -File deliverables/cycle-03/src/automation/windows/run_hub.ps1
   ```
4. Run K10 scripts:
   ```bash
   bash deliverables/cycle-03/src/automation/k10/setup_k10.sh
   bash deliverables/cycle-03/src/automation/k10/run_gateway.sh --port=/dev/ttyACM0
   ```
5. Flash and configure Meshtastic nodes:
   ```bash
   bash deliverables/cycle-03/src/automation/meshtastic/flash_meshtastic.sh --port=/dev/ttyUSB0 --bin=firmware.bin
   bash deliverables/cycle-03/src/automation/meshtastic/configure_meshtastic.sh --port=/dev/ttyUSB0 --name=Heltec-1
   ```
6. Verify network bootstrap:
   ```bash
   bash deliverables/cycle-03/src/automation/meshtastic/bootstrap_network.sh
   ```

## Notes
- Install `esptool.py` for flashing: `pip install esptool`.
- Some Meshtastic devices may require GUI tools; document local requirements.
