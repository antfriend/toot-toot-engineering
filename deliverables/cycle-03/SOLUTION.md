---
cycle: 03
role: Core Worker
---

# Cycle 03 Solution

## Primary deliverable

`deliverables/cycle-03/k10_a32_navigator/` — Arduino project folder.

| File | Purpose |
|------|---------|
| `k10_a32_navigator.ino` | Main sketch |
| `data/ttdb.md` | TTDB data file for LittleFS partition |

## Key design decisions

### 1. LittleFS replaces SD (per A32-RFC-0002 §1.1)

```cpp
#include <LittleFS.h>
// ...
fsOk = LittleFS.begin(true);          // mount; format on first use
File f = LittleFS.open(TTDB_PATH, "r"); // open /ttdb.md
```

`SPIFFS` is deprecated in the Arduino ESP32 core. `LittleFS` is the
mandated default per A32-RFC-0002. The `SD.h` / `SPI.h` includes from
cycle-01 are removed entirely. The SD slot is free for other use.

Deploy the data partition from PlatformIO:
```
pio run --target uploadfs
```
This uploads `data/ttdb.md` to the K10 flash as `/ttdb.md`.

### 2. Touch screen zones

Two rectangular tap zones are drawn at the bottom of the screen
(y=245, height=32):
- **Left zone** (x=0..117): PREV — tap to go to previous record.
- **Right zone** (x=123..240): NEXT — tap to go to next record.

Touch detection uses LVGL's public pointer input device API:
```cpp
lv_indev_t* dev = lv_indev_get_next(NULL);
lv_point_t pt;
lv_indev_get_point(dev, &pt);
```
A new tap is detected when the last registered point changes to a
position inside a touch zone. Debounce: 300 ms.

The K10 SDK registers the touch controller as an LVGL pointer indev
during `k10.begin()`. No additional setup is required.

### 3. Interactive sounds

| Event | Tone(s) | Rationale |
|-------|---------|-----------|
| Startup | 196 Hz + 262 Hz | Two ascending tones — "ready" |
| Nav step | 330 Hz | Single mid tone — confirms movement |
| Wrap-around | 523 Hz → 392 Hz | Descend/ascend — list restarted |

`music.playTone(freq, samples)` is the K10 API. 8000 samples = 1 beat.

### 4. Navigation inputs (all three supported)

| Input | Direction |
|-------|-----------|
| Button A | Previous record |
| Button B | Next record |
| Tilt left | Previous record |
| Tilt right | Next record |
| Touch left zone | Previous record |
| Touch right zone | Next record |

### 5. TTDB parsing

Parser is unchanged from cycle-01 except:
- File opened via `LittleFS.open()` instead of `SD.open()`.
- `f.close()` called explicitly after parse (good practice with LittleFS).
- Fallback record message updated to reference `uploadfs`.

Parses: `mmpdb` block (`db_name`), record headers (`@LATxLONy`), titles
(`## Title`), and body text. Max 24 records, 260 chars body per record.

### 6. Render layout (portrait 240×280)

```
Row  1   DB name (accent)
Row  3   Record list window (5 rows, current highlighted in C_SELECT)
  ...
Row  9   Current record ID (muted)
Row 11   Body preview up to 80 chars (text)
Row 13   Position: "n/total" (muted)
Row 14   FS status (muted / warning)
Row 15   File status / size (muted / warning)
y=245   Touch zones (dark rectangles with labels)
```

## PlatformIO notes

Add to `platformio.ini`:
```ini
board_build.filesystem = littlefs
```
This enables `pio run --target uploadfs` to build and upload the
LittleFS image from the `data/` directory.

The sketch itself does not require any extra libraries beyond the
DFRobot UniHiker K10 Arduino SDK (which bundles LVGL and LittleFS).
