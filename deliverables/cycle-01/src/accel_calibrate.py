"""accel_calibrate.py

Compute simple accelerometer offsets (bias) by averaging samples while device is held still.

This helps remove constant bias so the computed roll/pitch is closer to true level.

Edit `read_accel_g()` to match your Unihiker K10 firmware APIs.
"""

import time


def read_accel_g():
    # See accel_axis_check.py for adapter notes.
    raise NotImplementedError(
        "Update read_accel_g() with Unihiker K10 accelerometer API for your firmware"
    )


def run(samples=200, period_s=0.01):
    print("Calibration: keep device still and level...")
    sx = sy = sz = 0.0
    for _ in range(samples):
        ax, ay, az = read_accel_g()
        sx += ax
        sy += ay
        sz += az
        time.sleep(period_s)

    ox = sx / samples
    oy = sy / samples
    oz = sz / samples

    print("Measured avg (g):")
    print("  ax={:+.5f}  ay={:+.5f}  az={:+.5f}".format(ox, oy, oz))
    print("Suggested offsets (subtract these):")
    print("  OFF_X = {:+.5f}".format(ox))
    print("  OFF_Y = {:+.5f}".format(oy))
    print("  OFF_Z = {:+.5f}".format(oz))


if __name__ == "__main__":
    run()
