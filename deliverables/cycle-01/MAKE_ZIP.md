# MAKE_ZIP (cycle-01)

The prompt requests “all of the above bundled in a zip”.

From repo root (Windows PowerShell):
```powershell
python -m zipfile -c deliverables\cycle-01\TTN_delivery_cycle-01.zip deliverables\cycle-01\*
```

Or from inside `deliverables/cycle-01`:
```powershell
python -m zipfile -c TTN_delivery_cycle-01.zip .
```

Result:
- `deliverables/cycle-01/TTN_delivery_cycle-01.zip`
