# REVIEW (cycle-01)

## Scope reviewed
- `deliverables/cycle-01/BUILD_GUIDE.md`
- `deliverables/cycle-01/code/code.py`
- `deliverables/cycle-01/diagram/wiring.svg`

## What looks good
- Clear wiring table and a diagram asset exists (SVG).
- CircuitPython approach is appropriate for Adafruit QT Py boards.
- Code uses `displayio` + `adafruit_display_text` and keeps the first test minimal.
- Troubleshooting section anticipates the most common failure modes (blank screen, wrong colors, offset/rotation).

## Issues / risks
1. **Pin defaults may not match user expectation**
   - Using `board.TX`, `board.A3`, `board.A2` is fine, but the guide should emphasize that these are *choices* and must match the wiring.

2. **Driver naming vs ST7735S**
   - The library is `adafruit_st7735r` even when the controller is marketed as ST7735S. This is common in CircuitPython land, but it can confuse readers.

3. **Backlight current**
   - Many breakouts let you tie `BL/LED` to 3.3V directly, but some need a resistor/transistor path or already have it onboard.

## Recommended edits (non-blocking)
- In `BUILD_GUIDE.md`, add one sentence explicitly stating: “CS/DC/RST can be any free digital pins; the defaults here match `code.py`.”
- In `BUILD_GUIDE.md`, add a small callout: “CircuitPython uses the `adafruit_st7735r` driver for many ST7735-family displays.”

## Acceptance criteria check
- Build guide exists: ✅
- Diagram asset exists: ✅ (`wiring.svg`)
- CircuitPython example exists: ✅ (`code.py`)
- Minimal hello world behavior defined: ✅

## Ready for delivery?
Yes, with minor clarity tweaks if desired (not required to proceed).
