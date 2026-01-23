# STORYTELLER (cycle-01)

## Narrative thread / creative framing
This build is about giving a tiny handheld device a pilot’s sense of “level” in the world: the Unihiker K10 becomes a small horizon-finder that overlays an artificial horizon line on top of the live camera feed, driven by the accelerometer.

Treat it like a mini avionics instrument:
- The **camera** is the outside world.
- The **accelerometer** is the inner ear.
- The **horizon line** is the truth you can trust when your eyes are fooled.

The deliverable should feel like a pragmatic, field-ready recipe: clear wiring assumptions (if any), explicit coordinate conventions, and an explainable mapping from tilt → line angle/offset.

## User story
As a maker using a Unihiker K10, I want to see a stable horizon overlay on the camera image so that I can quickly assess device pitch/roll and keep the frame level when recording or navigating.

## What “excellent” looks like
- A runnable MicroPython/CircuitPython-style script that:
  - starts the camera preview,
  - reads accelerometer values at a steady rate,
  - applies smoothing/calibration,
  - draws a horizon line overlay (and optionally a center reticle),
  - updates without excessive flicker.
- A short how-to guide that explains:
  - how to run it on Unihiker K10,
  - how to calibrate “level”,
  - troubleshooting (sensor orientation, axis swaps, jitter).

## Key narrative choices to make explicit
1. **Orientation convention**: define which axis is “up” for the device as held. Provide a quick test mode that prints raw accel values so users can confirm axis mapping.
2. **Math simplicity**: prioritize robust roll (rotation around camera axis) and optionally pitch (vertical offset) if reliable.
3. **Smoothing**: a simple low-pass filter makes the overlay feel “instrument-like”.

## Suggested visual details (optional but adds production value)
- Draw:
  - a horizon line (thick, high-contrast)
  - a small center dot/crosshair
  - numeric roll angle in degrees
- Use a “sky/ground” hint by drawing two short ticks or a small ladder near center (only if performance allows).

## Risks / pitfalls to call out
- Accelerometer axis orientation can differ by firmware; include a quick axis-check step.
- Pure accelerometer tilt is noisy during motion; tell the user this is best when not accelerating strongly.
- Camera draw performance: overlay should be lightweight; avoid full-frame heavy compositing if the platform is slow.

## Handoff to Orchestrator
Ensure the plan includes:
- a Core Worker step that produces: code + how-to + calibration notes under `deliverables/cycle-01/`.
- a Reviewer step that checks math/orientation clarity and runtime feasibility.
- Delivery packaging that bundles the script(s) and a concise README for the user.
