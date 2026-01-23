"""accel_axis_check.py

Print raw accelerometer readings so you can determine axis orientation.

Edit the `read_accel_g()` function to match your Unihiker K10 firmware APIs.
"""

import time


def read_accel_g():
    """Return (ax, ay, az) in units of g.

    PLATFORM ADAPTER:
    Replace this implementation with your device's accelerometer read call.

    Expected conventions:
    - ax, ay, az are floats
    - 1 g ~ 1.0 when aligned with gravity
    """
    # --- Example placeholder ---
    # from unihiker import Accelerometer
    # acc = Accelerometer()
    # return acc.get_x(), acc.get_y(), acc.get_z()

    raise NotImplementedError(
        "Update read_accel_g() with Unihiker K10 accelerometer API for your firmware"
    )


def run(period_s=0.1):
    print("Accelerometer axis check (Ctrl+C to stop)")
    while True:
        ax, ay, az = read_accel_g()
        print("ax={:+.3f}g  ay={:+.3f}g  az={:+.3f}g".format(ax, ay, az))
        time.sleep(period_s)


if __name__ == "__main__":
    run()
