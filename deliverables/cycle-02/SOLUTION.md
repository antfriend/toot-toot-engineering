# SOLUTION (cycle-02)

This cycle hardens the CLI UX and logging without adding dependencies.

## Highlights
- Added `ttn/logging_utils.py` for structured logging (text or JSON).
- `ttn.node` now supports `--log-format` and `--log-level`, plus an `info` subcommand.
- Multicast join status is logged at listener start; multicast failures are explicitly logged before peer-fanout fallback.
- Config loading now validates required keys and missing files.

## Files changed
- `ttn/logging_utils.py` (new)
- `ttn/node.py` (logging, info subcommand, explicit multicast visibility)
- `ttn/transport_udp.py` (return multicast join status)
- `ttn/config.py` (validation)
- `TTN_README.md` (logging and fallback notes)
