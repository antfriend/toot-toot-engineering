# DELIVERY (cycle-04)

## What shipped
- `ttn/monitor.py` monitor CLI with summaries and export
- `ttn.node monitor` subcommand

## How to run
```bash
python -m ttn.node --config config/node_a.env monitor --summary-seconds 5
python -m ttn.node --config config/node_a.env monitor --export monitor.log
```

## Export notes
- Export file is JSON lines (one record per message).
- Monitor listens only to group traffic (broadcast/multicast).
