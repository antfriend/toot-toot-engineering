# STORYTELLER (cycle-01)

## Narrative intent for the build guide
Make the guide feel like a confident, friendly bench-side walkthrough: you (human maker) and the board (QT Py RP2040) are “bringing the tiny screen to life.” The story arc is:
1) Identify the parts and constraints (3.3V logic; many ST7735S variants).
2) Wire safely and verify pin labels.
3) Install CircuitPython and the exact libraries.
4) Run “hello world” and see first pixels.
5) Troubleshoot the common gotchas.

## Tone & structure recommendations
- Start with a one-paragraph outcome statement: “By the end, your ST7735S will show text from the QT Py RP2040.”
- Use short sections with checkpoints:
  - “Checkpoint: Board shows up as a USB drive.”
  - “Checkpoint: Screen backlight turns on.”
  - “Checkpoint: Text renders.”
- Treat uncertainty explicitly:
  - Include a small callout: “Your display breakout may label pins differently; verify before powering.”
- Prefer a single, minimal wiring variant (SPI) and make the optional lines (backlight control, reset) clearly optional.

## Visual guidance
The prompt asks for a Fritzing diagram. If a true `.fzz` cannot be produced reliably (missing part definitions), provide a “Fritzing-style” wiring diagram (clean SVG/PNG) plus a precise pin mapping table. The diagram should:
- Label signals: SCK, MOSI, CS, DC, RST, VCC, GND, (optional) BL.
- Label QT Py pins by their silkscreen names (not only GPIO numbers).

## “Hello world” experience
Recommend the first-run program do exactly two things:
1) Fill the screen with a solid color (proves addressing / init).
2) Draw a short text string (proves font pipeline): “hello, QT Py RP2040”.

## Troubleshooting beats to include
- Blank screen:
  - Verify VCC voltage requirement (3.3V vs 5V), common ground, and backlight pin.
  - Confirm CS/DC/RST wiring and that the correct driver (ST7735R vs ST7735S variants) / init sequence is used.
- Garbled colors:
  - Swap color order (BGR vs RGB) in driver init.
- Upside-down / offset image:
  - Adjust rotation / column/row offsets.

## Ask the Orchestrator to add acceptance checks
- “Guide includes a wiring table and diagram asset.”
- “A minimal `code.py` exists and uses Adafruit displayio + ST7735R/ST7735 compatible library.”
