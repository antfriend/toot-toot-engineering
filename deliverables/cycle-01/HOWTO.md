# Unihiker K10 Artificial Horizon (Accelerometer + Camera Overlay)

## Goal
Show an artificial horizon line on top of the live camera image using the device accelerometer.

This is **accelerometer-only tilt**: it is most reliable when the device is not undergoing strong linear acceleration.

## What you’ll copy to the device
Copy the `src/` folder to your Unihiker K10:
- `src/accel_axis_check.py`
- `src/accel_calibrate.py`
- `src/main.py`

## Step 1 — Verify accelerometer axes (critical)
Run:

```python
# on device
import accel_axis_check
accel_axis_check.run()
```

Observe how `ax, ay, az` change when you:
- tilt the device left/right (roll)
- tip it forward/back (pitch)

Write down which axis corresponds to each motion and whether signs are inverted.

If the roll direction is reversed, you’ll later flip the sign in `main.py` (see `AXIS CONFIG`).

## Step 2 — Calibrate “level” offset
Place the device on a known level surface in the orientation you will use.

Run:

```python
import accel_calibrate
accel_calibrate.run(samples=200)
```

It prints recommended offsets (biases). Copy them into `main.py` (`CALIBRATION OFFSETS`).

## Step 3 — Run the artificial horizon overlay
Run:

```python
import main
main.run()
```

You should see:
- live camera
- a horizon line that rotates with roll
- (optional) a numeric roll angle

## Troubleshooting
### Horizon moves the wrong way
- Flip the sign of the roll axis in `main.py`.

### Horizon is very jittery
- Increase smoothing (low-pass filter alpha) in `main.py`.
- Reduce update rate (increase sleep).

### Horizon “leans” when the device is level
- Re-run calibration and update offsets.

### Looks wrong when walking / moving quickly
- This is expected with accelerometer-only tilt; consider next-cycle prompt #2 (gyro/complementary filter) if gyro is available.

## Notes on platform APIs
Unihiker K10 firmware variants may expose different modules for camera/display/sensor access.
The provided code uses a **thin adapter approach**:
- `main.py` contains a section labeled `PLATFORM ADAPTER`.
- If your firmware uses different module names, edit only that section.
