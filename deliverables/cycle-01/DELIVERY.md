# DELIVERY (cycle-01)

## Deliverables
- How-to guide: `deliverables/cycle-01/HOWTO.md`
- Source code (copy to device):
  - `deliverables/cycle-01/src/main.py`
  - `deliverables/cycle-01/src/accel_axis_check.py`
  - `deliverables/cycle-01/src/accel_calibrate.py`
- Review notes: `deliverables/cycle-01/REVIEW.md`
- Companion logo asset: `deliverables/cycle-01/toot-toot-logo.svg` (copied from repo root asset)

## How to run (quick)
1. Copy `deliverables/cycle-01/src/` onto the Unihiker K10.
2. Edit the **PLATFORM ADAPTER** sections in the scripts to match your firmware module names.
3. Run axis check:
   - `import accel_axis_check; accel_axis_check.run()`
4. Run calibration:
   - `import accel_calibrate; accel_calibrate.run(samples=200)`
   - Copy offsets into `main.py`.
5. Run main:
   - `import main; main.run()`

## Notes / assumptions
- This solution uses an adapter pattern because Unihiker K10 firmware APIs for camera/display/accelerometer may differ.
- Roll is accelerometer-derived (best when not accelerating strongly).

## Packaging notes
- If you want to distribute, zip:
  - `HOWTO.md`
  - `src/`
  - `toot-toot-logo.svg`

