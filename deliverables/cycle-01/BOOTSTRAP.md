# BOOTSTRAP (cycle-01)

## Prompt (from `README.md`)
Create a how-to guide and code files in circuit/micro python for the Unihiker K10 which puts a horizon line on the current camera image, using the accelerometer.

## Interpretation
We are building a small “artificial horizon” overlay:
- Read accelerometer data to estimate device roll (and optionally pitch).
- Overlay a horizon line and minimal HUD elements on top of the live camera image.
- Provide a practical how-to for setup, calibration, and troubleshooting on Unihiker K10.

This is primarily an embedded UI + sensor fusion-lite problem. Accuracy expectations should be set appropriately: accelerometer-only tilt is good when stationary/slow-moving, but degrades during linear acceleration.

## Recommended team (roles)
- Storyteller: define user story, clarity, and the “instrument” feel.
- Orchestrator: refine the critical path into concrete artifacts and filenames; ensure plan references match actual outputs.
- Core worker: implement MicroPython code + how-to guide; include calibration and axis-check utilities.
- Reviewer: validate math, readability, and that code is plausible for Unihiker K10 APIs.
- Delivery packager: assemble final deliverables, ensure logo inclusion, and update `RELEASES.md`.

## Objectives / Definition of Done (cycle-01)
1. A concise **HOWTO** document explaining installation/run, calibration, and troubleshooting.
2. One or more **MicroPython code files** that:
   - show raw accelerometer readings (axis check),
   - compute roll angle (and optionally pitch),
   - draw a horizon overlay over the camera image.
3. A short **review** capturing correctness, limitations, and fixes.
4. A **delivery** note listing what to copy to device and how to run.

## Deliverables produced (this cycle)
- `deliverables/cycle-01/HOWTO.md`
- `deliverables/cycle-01/src/main.py`
- `deliverables/cycle-01/src/accel_axis_check.py`
- `deliverables/cycle-01/src/accel_calibrate.py`
- `deliverables/cycle-01/REVIEW.md`
- `deliverables/cycle-01/DELIVERY.md`
- `deliverables/cycle-01/toot-toot-logo.svg`

## Retrospective (what to change next time)
What worked:
- Adapter-first structure allowed progress despite uncertain Unihiker K10 API specifics.
- Separating axis-check and calibration reduced ambiguity for end users.

What to improve:
1. **Confirm platform APIs early**: add a short “Platform API verification” step at the start of Core Worker in future cycles (or an explicit role) to identify the exact module names for:
   - camera capture/preview
   - drawing primitives / overlay
   - accelerometer reads
2. **Stronger axis mapping**: allow axis *selection* (not just sign flips) in `main.py`.
3. **Add a minimal reference adapter** once a specific firmware is targeted (e.g., DFRobot UNIHIKER firmware) so the solution is runnable out-of-box for that variant.

## Next-cycle prompt suggestions (human must choose one)
1. Add a complementary **digital level** mode with on-screen bubble + audible beep when level, including adjustable thresholds.
2. Upgrade to a **sensor-fusion** approach (complementary filter using gyro if available) for smoother horizon during motion.
3. Turn the overlay into a small reusable **Unihiker K10 UI library** module (camera overlay primitives + sensor helpers) with examples.

## Offer
I can implement the retrospective recommendations and reset the plan for cycle-02 once you choose one of the prompts above.
