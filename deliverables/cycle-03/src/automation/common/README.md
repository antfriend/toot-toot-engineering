# Automation Kit (cycle-03)

## Goals
- Repeatable deployment for all six devices.
- Minimal, inspectable scripts with dry-run and verify modes.
- Clear fallback notes when automation isn't possible.

## Assumptions
- Hub is Windows 10/11 with Python 3.10+.
- K10 runs Linux with Python 3.10+.
- Heltec and T-Deck use Meshtastic firmware builds.

## Conventions
- Scripts accept `--dry-run` to show actions.
- Scripts accept `--verify` to run post-steps checks.
- Environment variables are defined in `deploy.env` per device.
