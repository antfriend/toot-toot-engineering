# BOOTSTRAP (cycle-01)

## Prompt (from README.md)
Please make a build guide with a fritzing diagram and steps to run a micro/circuit python hello world for an Adafruit QT Py RP2040 and a ST7735S 128 x 160.

## Interpretation
You want a practical, reproducible maker guide that gets a QT Py RP2040 wired to an ST7735S 128x160 TFT, then running a minimal “hello world” (text + optional color fill) in CircuitPython (and/or MicroPython if desired).

Key deliverables implied by the prompt:
- A wiring guide (pin mapping) between QT Py RP2040 and ST7735S display.
- A “Fritzing-style” diagram (at least a clear breadboard/wiring diagram; ideally a real Fritzing .fzz/.fzpz source).
- Step-by-step instructions to install firmware, libraries, and run a minimal example.

Assumptions / uncertainties to resolve explicitly in the guide:
- Many ST7735S breakouts vary (pins, backlight, onboard regulator/level shifting). The guide should include a “verify your breakout” section and a safe default wiring.
- QT Py RP2040 is 3.3V logic; most ST7735 breakouts accept 3.3V logic but some expect 5V with level shifting.

## Team composition (recommended roles)
- Storyteller: Keep the guide approachable and “maker friendly” while staying technically correct.
- Orchestrator: Adjust the plan to include a diagram asset and a runnable code asset; set acceptance criteria.
- Core worker: Produce the actual build guide, wiring table, CircuitPython code, and (if feasible) a Fritzing source or an SVG/PNG wiring diagram.
- Reviewer: Validate wiring logic, library choices, and identify common pitfalls.
- Delivery packager: Package outputs into a tidy folder, include the TTE logo, and update RELEASES.
- (Optional) Image producer: If we can’t generate a true Fritzing file, produce a clean wiring diagram image (SVG/PNG) programmatically.

## Recommended plan adjustments
1. Add an explicit “Diagram” step/output:
   - `deliverables/cycle-01/diagram/` containing either a Fritzing `.fzz` (best) or a clearly labeled wiring diagram image (acceptable fallback).
2. Add an explicit “Code” output:
   - `deliverables/cycle-01/code/` with `code.py` (CircuitPython) and `lib/` notes.
3. Clarify “definition of done” for this prompt:
   - Guide includes exact pins, exact libraries, and a minimal test that draws text on the screen.
4. Decide target language: CircuitPython is most natural for Adafruit boards; include MicroPython notes only if time permits.

## Acceptance criteria (cycle-01)
- A single build guide document exists under `deliverables/cycle-01/`.
- Includes a pin mapping table and power guidance.
- Includes a diagram asset (Fritzing file or wiring diagram image).
- Includes CircuitPython steps and a working example `code.py` that renders text on the screen.

## Next-cycle prompts (choose one)
1. “Extend the guide by adding an on-device menu UI (buttons + simple state machine) and show how to structure the code for multiple screens.”
2. “Add a performance and power section: measure FPS, optimize display refresh, and document battery options for QT Py RP2040 + ST7735S.”
3. “Port the example to MicroPython (rp2) using an ST7735 driver and compare differences vs CircuitPython (setup, libraries, memory).”

## Retrospective (cycle-01, end-of-cycle)
### What went well
- Produced a complete, minimal deliverable set: build guide + wiring diagram + runnable CircuitPython `code.py`.
- Explicitly documented common ST7735-family sources of confusion (pin label variants, BGR/RGB, rotation).

### What to improve next time
- If the prompt explicitly requires a **true Fritzing project file** (`.fzz/.fzpz`), add a dedicated “Fritzing file production” step and either:
  - standardize on known Fritzing parts (Adafruit QT Py + a specific ST7735 breakout), or
  - request the exact breakout link/photo and the desired pin mapping before diagram generation.

### Suggested workflow tweak
Add an optional step between Core worker and Reviewer:
- **Hardware compatibility check**: a short matrix of known ST7735S breakout variants (common pin labels, BL behavior, voltage) and what to change in code.

### Next cycle prompt options (choose one)
1. “Add buttons and implement a simple on-device menu UI (3 screens) on the ST7735S using CircuitPython.”
2. “Create a variant of this guide for a specific ST7735S breakout (provide a pin-labeled photo) and generate a matching Fritzing diagram.”
3. “Port the ‘hello world’ to MicroPython (rp2) and document the full setup and driver differences.”
