# SPDX-FileCopyrightText: 2026
# SPDX-License-Identifier: MIT
#
# QT Py RP2040 + ST7735S (128x160) "Hello World" (CircuitPython)
#
# Copy this file to the board as CIRCUITPY/code.py
# Libraries needed (copy into CIRCUITPY/lib):
# - adafruit_st7735r.mpy (from Adafruit CircuitPython Bundle)
# - adafruit_display_text/ (folder, from bundle)
# - adafruit_displayio_layout/ (optional; not used here)
#
# Notes:
# - Many ST7735S breakouts work with the ST7735R driver in CircuitPython.
# - If colors look wrong, try bgr=True/False.
# - If the image is shifted, you may need different colstart/rowstart.

import board
import busio
import displayio
import terminalio

from adafruit_display_text import label
import adafruit_st7735r

# Release any resources currently in use for the displays
displayio.release_displays()

# --- Pin choices (edit to match your wiring) ---
# Use the QT Py pin labels on the silkscreen.
TFT_CS = board.TX      # pick any free digital pin
TFT_DC = board.A3      # pick any free digital pin
TFT_RST = board.A2     # optional but recommended

spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)

display_bus = displayio.FourWire(
    spi,
    command=TFT_DC,
    chip_select=TFT_CS,
    reset=TFT_RST,
)

# 128x160 ST7735 family displays often need these tweaks.
# If your display is blank, start by toggling bgr and rotation.
WIDTH = 128
HEIGHT = 160

display = adafruit_st7735r.ST7735R(
    display_bus,
    width=WIDTH,
    height=HEIGHT,
    rotation=90,
    bgr=True,
)

# Make the display context
splash = displayio.Group()
display.root_group = splash

# Background color fill
bg = displayio.Bitmap(WIDTH, HEIGHT, 1)
pal = displayio.Palette(1)
pal[0] = 0x003366  # dark blue
splash.append(displayio.TileGrid(bg, pixel_shader=pal))

# Hello text
text = "hello, QT Py RP2040"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=5, y=20)
splash.append(text_area)

# Keep showing forever
while True:
    pass
