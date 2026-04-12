---
cycle: 03
role: Reviewer
---

# Cycle 03 Review

## Verdict: PASS with notes

The primary deliverable `k10_a32_navigator.ino` is correct and complete
for deployment. One open question is noted (touch API version dependency);
it does not block delivery.

---

## Checklist

### RFC conformance

| Check | Result |
|-------|--------|
| LittleFS used (not SPIFFS, not SD) | PASS — `#include <LittleFS.h>`, `LittleFS.begin(true)`, `LittleFS.open()` |
| TTDB file path `/ttdb.md` | PASS — matches A32-RFC-0002 §1.3 default path |
| Streaming line-by-line parse | PASS — `readStringUntil('\n')` loop |
| `mmpdb` block parsed for `db_name` | PASS |
| Record header `@LAT...` parsed | PASS |
| `file.close()` after parse | PASS |
| `LittleFS.begin(true)` format-on-first-use | PASS — correct per A32-RFC-0002 §1.1 |
| SD includes removed | PASS — no `SD.h` or `SPI.h` |

### K10 API usage

| Check | Result |
|-------|--------|
| `k10.begin()` before any K10 use | PASS |
| `k10.initScreen()` before canvas | PASS |
| `k10.creatCanvas()` called | PASS |
| `canvasText(text, row, color)` overload used correctly | PASS |
| `canvasText(text, x, y, color, font, count, autoClean)` XY overload for touch labels | PASS — used for positioned PREV/NEXT labels |
| `canvasRectangle(x, y, w, h, border, bg, fill)` | PASS |
| `canvasCircle(x, y, r, color, bg, fill)` | PASS — boot splash |
| `canvasClear(C_BG)` — note: calls `canvasClear(uint8_t row)` with row=0 | NOTE — matches cycle-01 pattern; consistent; no regression |
| `updateCanvas()` called after render | PASS |
| `music.playTone(freq, samples)` | PASS |
| `buttonA->isPressed()`, `buttonB->isPressed()` | PASS |
| `isGesture(TiltLeft)`, `isGesture(TiltRight)` | PASS |

### Sound design

| Event | Tones | Assessment |
|-------|-------|------------|
| Startup | 196 Hz (G3), 262 Hz (C4) | Ascending fifth — clear "ready" signal |
| Nav step | 330 Hz (E4) | Distinct from startup, unobtrusive |
| Wrap-around | 523 Hz (C5) → 392 Hz (G4) | Descending: signals list boundary clearly |

All three sounds are distinguishable. No tone conflicts. PASS.

### Touch input

| Check | Result |
|-------|--------|
| LVGL pointer indev polled via `lv_indev_get_next` | PASS — public LVGL API |
| `lv_indev_get_point` retrieves last touch position | PASS — public LVGL API |
| Tap detected by point-change in zone (debounced 300 ms) | PASS — functional for typical use |
| Touch zones rendered at bottom strip (y=245) | PASS |

**Open question (does not block delivery):** `lv_indev_get_point()` returns
the last known point regardless of whether the screen is currently being
pressed. The current detection method (point changed AND in zone) will
fire once per positional change. This is sufficient for navigation taps
but will miss a stationary press-and-hold. If a future cycle requires
press-hold or drag, use `lv_indev_get_state()` (available in LVGL ≥7.3)
or register an LVGL event callback on an invisible button object.

### Render layout

- 5-row list window centred on current index: PASS.
- Position indicator `n/total`: PASS.
- Status rows show FS and file health with color warning on failure: PASS.
- Touch zone rectangles separate from content rows: PASS.

### Data file `data/ttdb.md`

- Valid `mmpdb` header block: PASS.
- `db_name` parseable by sketch: PASS.
- 14 records — within `MAX_RECORDS` (24): PASS.
- Record headers in `@LATxLONy` format: PASS.
- `## Title` lines present: PASS.
- Body text present for each record: PASS.

### PlatformIO deployment

- `board_build.filesystem = littlefs` documented in SOLUTION.md: PASS.
- `pio run --target uploadfs` documented: PASS.
- Fallback record message references `uploadfs` when file missing: PASS.

---

## Issues found: 0 blocking

## Notes for future cycles

1. Touch press-state detection — see open question above.
2. `canvasClear(uint32_t)` ambiguity: DFRobot header has no uint32_t overload; `canvasClear(C_BG)` where `C_BG=0` resolves to `canvasClear(uint8_t row=0)`. Behavior matches cycle-01. Consider filing upstream if behavior causes ghosting.
3. `MAX_RECORDS=24` is hard-coded. A future cycle could read `max_nodes` from the `cursor_policy` block in the `mmpdb` header.
