# Build guide: QT Py RP2040 + ST7735S (128×160) SPI TFT

## Goal
Wire an **Adafruit QT Py RP2040** to an **ST7735S 128×160 SPI TFT** and run a minimal **CircuitPython “hello world”** that fills the screen and draws text.

## Parts
- Adafruit QT Py RP2040
- ST7735S 128×160 SPI TFT breakout
- Jumper wires
- (Optional) Breadboard

## Before you wire (important)
ST7735S breakouts vary. **Confirm the pin labels on your exact module** before powering:
- Common labels: `VCC`, `GND`, `SCL`/`SCK`, `SDA`/`MOSI`/`DIN`, `CS`, `DC`/`A0`, `RST`/`RES`, `BL`/`LED`.
- Logic level: QT Py RP2040 is **3.3V logic**. Most ST7735 breakouts accept 3.3V.

If your breakout has a `VIN` pin and onboard regulator, it might accept 5V power—but **don’t assume**. When in doubt, use **3.3V**.

Note on drivers: In CircuitPython, many ST7735-family SPI TFTs (including modules sold as **ST7735S**) work with the `adafruit_st7735r` driver.

## Wiring (SPI)
See the diagram: `deliverables/cycle-01/diagram/wiring.svg`

### Wiring table (safe default)
CS/DC/RST can be **any free digital pins**—the choices below are just defaults and must match what you set in `code.py`.

| ST7735S pin | Connect to QT Py RP2040 | Notes |
|---|---|---|
| VCC | 3V | Use 3.3V unless your breakout explicitly expects VIN/5V |
| GND | GND | Common ground required |
| SCK / SCL | SCK | SPI clock |
| MOSI / SDA / DIN | MOSI | SPI data out |
| CS | TX (or any free digital pin) | Chip select; must match code |
| DC / A0 | A3 (or any free digital pin) | Data/command; must match code |
| RST / RES | A2 (or any free digital pin) | Reset; optional but recommended |
| BL / LED | 3V (or leave as-is) | Backlight; some boards tie this high internally |

Notes:
- `MISO` is typically **not used** for these TFTs.
- If your TFT has `SDA` and `SCL` pins, on these modules they are usually **SPI** (`MOSI` and `SCK`), not I2C.

## Install CircuitPython on QT Py RP2040
1. Download the latest CircuitPython UF2 for **QT Py RP2040** from Adafruit.
2. Put the board into bootloader mode (usually double-tap reset).
3. Drag-and-drop the UF2 onto the `RPI-RP2` drive.
4. After reboot, you should see a `CIRCUITPY` USB drive.

Checkpoint: **A `CIRCUITPY` drive appears.**

## Install libraries
1. Download the matching Adafruit CircuitPython Bundle for your CircuitPython version.
2. Copy these into `CIRCUITPY/lib/`:
   - `adafruit_st7735r.mpy`
   - `adafruit_display_text/` (folder)

## Copy the example code
Copy this file to your board:
- `deliverables/cycle-01/code/code.py` → `CIRCUITPY/code.py`

Checkpoint: **The screen fills dark blue and shows yellow text**: `hello, QT Py RP2040`.

## Troubleshooting
### Blank screen
- Confirm `VCC` and `GND` are correct (and you share ground).
- Backlight:
  - If the screen is *very* dark, wire `BL/LED` to **3V** (if your breakout exposes it).
- Verify `CS`, `DC`, `RST` wiring matches the pins defined in `code.py`.

### Wrong colors
- In `code.py`, toggle `bgr=True` to `bgr=False`.

### Shifted / cropped image
- Some ST7735 variants need different offsets.
- Try changing `rotation` (0/90/180/270).
- If still shifted, you may need a different driver or init parameters specific to your breakout.

## MicroPython note (optional)
MicroPython support depends on the driver you use (often community drivers for ST7735). CircuitPython is recommended here because Adafruit provides maintained display drivers and examples.

## Files produced in this cycle
- Guide: `deliverables/cycle-01/BUILD_GUIDE.md`
- Code: `deliverables/cycle-01/code/code.py`
- Diagram: `deliverables/cycle-01/diagram/wiring.svg`
