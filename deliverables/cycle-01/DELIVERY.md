# DELIVERY (cycle-01)

## Primary deliverable
A runnable, tap-to-choose dungeon crawler (tkinter) plus a dedicated, populated TTDB/mmpdb markdown database.

Deliverables root:
- `deliverables/cycle-01/`

## What to copy to the UNIHIKER K10
Create a folder on device, for example:
- `TTDB_DUNGEON/`

Copy these files into it:
- `ttdb_dungeon_crawler.py`
- `ttdb_dungeon_db.md`
- `TTDB_README.md`

## How to run
On the K10:

```bash
cd TTDB_DUNGEON
python3 ttdb_dungeon_crawler.py
```

## Notes / constraints
- This is a GUI app (tkinter). It must be run with an active display.
- If tkinter is not present in the K10 image, port the UI layer to the device’s preferred toolkit.

## Included docs
- `BOOTSTRAP.md` — interpretation, team, plan advice
- `STORYTELLER.md` — story graph and narrative beats
- `REVIEW.md` — review notes and minor doc fixes
- `INSTALL_BUNDLE.md` — minimal bundle manifest

## Verification performed
- `python -m py_compile deliverables/cycle-01/ttdb_dungeon_crawler.py`

(Full runtime execution wasn’t performed here because the environment may be headless; run on-device to validate touch UI.)
