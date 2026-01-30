# DELIVERY (cycle-01)

## What this delivers
A minimal 3-node TTN messaging package (UDP) with:
- Direct messages (unicast)
- Group messages (multicast by default; broadcast fallback)
- Per-node JSON configuration
- CLI node runner + send command
- A local demo script
- A zip bundle for distribution

## Primary artifacts
- `deliverables/cycle-01/TTN_README.md` (end-user instructions)
- `deliverables/cycle-01/ttn/` (reference implementation)
- `deliverables/cycle-01/config/` (example node configs)
- `deliverables/cycle-01/demo/demo_three_nodes.py` (demo scenario)
- `deliverables/cycle-01/TTN_delivery_cycle-01.zip` (distribution bundle)

## How to run (quick demo)
On Windows 11 with Python 3.10+:
```powershell
cd deliverables\cycle-01
python -m ttn.cli --config config\node_a.json run --presence
```
(repeat in separate terminals for node_b and node_c)

Send direct:
```powershell
cd deliverables\cycle-01
python -m ttn.cli --config config\node_a.json send --to tdeck-beta --text "Can you hear me?"
```

Send broadcast:
```powershell
cd deliverables\cycle-01
python -m ttn.cli --config config\node_c.json send --to broadcast --text "Workshop check-in: everyone report status."
```

## Build the zip
Already built:
- `deliverables/cycle-01/TTN_delivery_cycle-01.zip`

To rebuild, see:
- `deliverables/cycle-01/MAKE_ZIP.md`

## Notes / known issues
- Some networks block multicast; if group messages do not arrive, set `GROUP_MODE` to `broadcast` and (optionally) set `GROUP_IP` to `255.255.255.255`.
- Windows Firewall may need an allow rule for Python UDP inbound.
