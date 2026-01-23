# REVIEW (cycle-01)

## Scope reviewed
- `deliverables/cycle-01/HOWTO.md`
- `deliverables/cycle-01/src/main.py`
- `deliverables/cycle-01/src/accel_axis_check.py`
- `deliverables/cycle-01/src/accel_calibrate.py`

## What’s good
- Clear separation between:
  - axis discovery (`accel_axis_check.py`)
  - calibration (`accel_calibrate.py`)
  - horizon overlay application (`main.py`)
- The code explicitly calls out a **PLATFORM ADAPTER** section, which is appropriate given uncertain Unihiker K10 firmware APIs.
- Roll calculation via `atan2(y, z)` is a standard accelerometer-only approach.
- Low-pass filtering (`ALPHA`) is included to reduce jitter.

## Gaps / required fixes before “plug-and-play”
1. **Not runnable as-is**: the adapter functions raise `NotImplementedError`.
   - This is acceptable only if the deliverable explicitly states it is a template requiring adaptation.
   - The HOWTO does state this, but we should further tighten instructions by naming likely modules for Unihiker K10.
2. **Axis config limited**: `main.py` only allows sign flips for y/z; many devices require *swapping axes*.
   - Recommend expanding axis mapping to allow selecting which raw axis maps to logical y and z.
3. **Pitch not implemented**: prompt doesn’t require it, but a note explaining “roll only” choice would help.

## Risk notes
- Accelerometer-only roll is wrong during strong acceleration (walking/running/vehicle turns). Documented in HOWTO.
- Performance: overlay might require drawing directly onto the displayed buffer rather than copying frames. Depends on firmware.

## Suggested improvements (non-blocking)
- Add a simple “center reticle” (small cross) if draw API supports it.
- Add a configuration block to set `fps`, `ALPHA`, and overlay length.
- Include an example adapter implementation once the target firmware modules are confirmed.

## Review verdict
- **Conceptually correct** and well-structured.
- **Requires platform-specific adapter completion** to be executable on a real Unihiker K10.

