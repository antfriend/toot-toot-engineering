# DELIVERY (cycle-02)

## What shipped
- Structured logging (`text` or `json`) and log level controls
- `info` CLI subcommand for quick config inspection
- Explicit multicast join status and failure/fallback logging

## How to run
Examples:
```bash
python -m ttn.node --config config/node_a.env --log-format text --log-level info listen
python -m ttn.node --config config/node_a.env info
python -m ttn.node --config config/node_a.env broadcast "Hello group"
```

## Export notes
- Logs can be consumed by humans or machine parsers (`--log-format json`).
- If multicast send fails, the CLI logs the failure before peer-fanout fallback (when peers exist).
