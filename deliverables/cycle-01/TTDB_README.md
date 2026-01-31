# TTDB Dungeon Crawler for the UNIHIKER K10

The cave is lit. The campfire is warm. The dungeon is *polite*.

Welcome to a tap-to-choose dungeon crawler where every ending is silly, every corridor is a metaphor, and one of the metaphors is a **real, usable MyMentalPalaceDB (mmpdb)** you can learn from.

This bundle includes:
- A runnable Python game for the UNIHIKER K10 touchscreen
- A dedicated, populated TTDB / mmpdb markdown database the game can browse

---

## What you get (deliverables)
- `ttdb_dungeon_crawler.py` — the game application (touch-friendly UI with big buttons)
- `ttdb_dungeon_db.md` — a purpose-built MyMentalPalaceDB file, aligned to:
  - `RFCs/TTDB-RFC-0001-File-Format.md`
  - `RFCs/TTDB-RFC-0002-Cursor-Semantics.md`
  - `RFCs/TTDB-RFC-0003-Typed-Edges.md`

---

## Installation and configuration (device)
Assumptions:
- You can copy files onto the UNIHIKER K10.
- The device has Python 3 available.
- The device is running with a GUI/display available (this is a tkinter app).

### 1) Create a folder on the device
Create a folder (example):
- `TTDB_DUNGEON/`

### 2) Copy the installation bundle files
Copy these files into `TTDB_DUNGEON/`:
- `ttdb_dungeon_crawler.py`
- `ttdb_dungeon_db.md`
- `TTDB_README.md`

### 3) (Optional) Verify tkinter availability
This game uses `tkinter` (Python standard library) for the touchscreen UI.

If `tkinter` is not available on your particular device image, you’ll need to either:
- install/enable tkinter in the device’s Python environment, or
- port the UI layer to the K10’s preferred UI toolkit.

---

## Folder and file structure of the installation bundle
Recommended on-device layout:

```
TTDB_DUNGEON/
  ttdb_dungeon_crawler.py
  ttdb_dungeon_db.md
  TTDB_README.md
```

---

## How to run on the device
From a terminal / launcher on the K10:

1. Change into the folder:

```bash
cd TTDB_DUNGEON
```

2. Run the game:

```bash
python3 ttdb_dungeon_crawler.py
```

Controls:
- Tap the large buttons to choose.
- Use the bottom buttons:
  - **Home**: return to the campfire opening
  - **DB**: open the TTDB database browser
  - **Quit**: exit

---

## Notes on the included mmpdb
The database file `ttdb_dungeon_db.md` follows the TTDB format:
- A `#` title line
- a fenced `mmpdb` YAML block (properties)
- a fenced `cursor` YAML block (selection/preview state)
- record sections separated by `---`

Records have a header line like:

```
@LATxLONy | created:<int> | updated:<int> | relates:<edge_list>
```

### Typed edge syntax note
TTDB-RFC-0003 expresses typed edges as `<type>@<TARGET_ID>`.

This bundle uses a close, device-friendly variant in `relates:` lists:
- `type>@target_id`

This matches the lightweight parser pattern used by `tte_monitor.py` (and the one embedded in `ttdb_dungeon_crawler.py`).

---

## Provenance / references
Reference patterns consulted while building this:
- `tte_monitor.py` (ttdb parsing + simple UI rendering patterns)
- TTDB RFC documents under `RFCs/`
- The TTE agent umwelt: `standards/umwelt/TTE_Agent_Umwelt_v1.yaml`
