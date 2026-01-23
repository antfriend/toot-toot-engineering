"""main.py

Artificial horizon overlay on live camera image using accelerometer tilt.

You MUST adapt the PLATFORM ADAPTER section to your Unihiker K10 firmware.

Math:
- roll is derived from accelerometer: roll = atan2(ay, az) (after axis mapping)
- optional pitch can be derived from ax

We then draw a line through screen center with angle = roll.
"""

import math
import time

# -----------------------------
# CALIBRATION OFFSETS (update from accel_calibrate.py)
# -----------------------------
OFF_X = 0.0
OFF_Y = 0.0
OFF_Z = 0.0

# -----------------------------
# AXIS CONFIG (update after accel_axis_check.py)
# Map device accel readings to logical axes used for roll/pitch math.
# -----------------------------
# If your firmware returns (ax, ay, az) in a different orientation, swap here.
# Also flip sign by multiplying by -1.0 where needed.
ROLL_Y_SIGN = 1.0
ROLL_Z_SIGN = 1.0

# Smoothing (0..1). Higher = snappier, lower = smoother.
ALPHA = 0.15

# UI
LINE_COLOR = 0xFFFFFF
TEXT_COLOR = 0xFFFFFF


# -----------------------------
# PLATFORM ADAPTER
# -----------------------------

def camera_init():
    """Initialize camera and display."""
    # Replace with your platform calls.
    # Example ideas (NOT guaranteed):
    #   from unihiker import Camera, Screen
    #   cam = Camera(); scr = Screen()
    #   cam.start(); return cam, scr
    raise NotImplementedError("Implement camera_init() for your Unihiker K10 firmware")


def camera_get_frame(cam):
    """Return a frame/image object compatible with your draw API."""
    raise NotImplementedError("Implement camera_get_frame()")


def display_show_frame(scr, frame):
    """Show the frame on screen."""
    raise NotImplementedError("Implement display_show_frame()")


def draw_line(scr_or_frame, x0, y0, x1, y1, color):
    """Draw a line overlay."""
    raise NotImplementedError("Implement draw_line()")


def draw_text(scr_or_frame, x, y, text, color):
    """Draw text overlay."""
    raise NotImplementedError("Implement draw_text()")


def read_accel_g():
    """Return (ax, ay, az) in g."""
    raise NotImplementedError("Implement read_accel_g()")


def screen_size(scr):
    """Return (width, height)."""
    raise NotImplementedError("Implement screen_size()")


# -----------------------------
# Core logic
# -----------------------------

def _lp(prev, new, alpha):
    return prev + alpha * (new - prev)


def _horizon_endpoints(cx, cy, angle_rad, half_len):
    """Compute line endpoints centered at (cx,cy) with given angle."""
    dx = math.cos(angle_rad) * half_len
    dy = math.sin(angle_rad) * half_len
    return int(cx - dx), int(cy - dy), int(cx + dx), int(cy + dy)


def run(fps=15):
    cam, scr = camera_init()
    w, h = screen_size(scr)
    cx, cy = w // 2, h // 2
    half_len = int(min(w, h) * 0.6)

    roll_f = 0.0

    period = 1.0 / fps

    while True:
        # sensor
        ax, ay, az = read_accel_g()
        ax -= OFF_X
        ay -= OFF_Y
        az -= OFF_Z

        # Map axes/signs for roll calculation
        y = ROLL_Y_SIGN * ay
        z = ROLL_Z_SIGN * az

        # roll angle (rad). Adjust formula if your axis mapping differs.
        roll = math.atan2(y, z)
        roll_f = _lp(roll_f, roll, ALPHA)

        # camera
        frame = camera_get_frame(cam)

        # overlay
        x0, y0, x1, y1 = _horizon_endpoints(cx, cy, roll_f, half_len)
        draw_line(frame, x0, y0, x1, y1, LINE_COLOR)
        draw_text(frame, 4, 4, "roll={:+.1f} deg".format(roll_f * 180.0 / math.pi), TEXT_COLOR)

        # present
        display_show_frame(scr, frame)
        time.sleep(period)


if __name__ == "__main__":
    run()
