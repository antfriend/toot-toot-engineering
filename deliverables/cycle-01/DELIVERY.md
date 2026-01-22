# DELIVERY (cycle-01)

## What to use (the deliverables)
- Build guide: `deliverables/cycle-01/BUILD_GUIDE.md`
- CircuitPython example: `deliverables/cycle-01/code/code.py`
- Wiring diagram (Fritzing-style SVG): `deliverables/cycle-01/diagram/wiring.svg`
- Review notes: `deliverables/cycle-01/REVIEW.md`

## How to run (quick)
1. Install CircuitPython on the QT Py RP2040.
2. Copy libraries to `CIRCUITPY/lib/`:
   - `adafruit_st7735r.mpy`
   - `adafruit_display_text/`
3. Copy `deliverables/cycle-01/code/code.py` to `CIRCUITPY/code.py`.
4. Wire per `deliverables/cycle-01/diagram/wiring.svg`.

Expected result: dark blue background with yellow text: `hello, QT Py RP2040`.

## Packaging notes
- This repo includes Toot-Toot Engineering logo assets (`toot-toot-logo.svg` / `toot-toot-logo.png`). For this documentation-centric deliverable, reference the logo as a companion asset rather than embedding it into the wiring diagram.
- If you export the guide to PDF, include the logo on the title page.

## Known variance / disclaimers
- ST7735S breakouts vary in pin labels, backlight wiring, and init offsets. If your display is blank or shifted, follow the troubleshooting section in `BUILD_GUIDE.md`.
