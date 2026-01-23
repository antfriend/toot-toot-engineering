# SVG_ENGINEER (cycle-01)

## Applicability check
The prompt is about **live camera imagery with a horizon overlay** on a Unihiker K10 using **MicroPython/CircuitPython**. This is primarily a **real-time raster display** problem, not an SVG output problem.

Conclusion: **SVG is not a central output format** for this cycle.

## If SVG is still desired (optional)
If the platform’s UI stack supports drawing vector primitives, SVG could be used only as a *design artifact* (e.g., a reference for line styles, reticle marks), but runtime rendering would likely still be via the device’s native graphics API.

## Constraints / guidance
- Real-time overlays should be done with:
  - simple line drawing primitives,
  - minimal allocations per frame,
  - limited redraw regions if possible.
- If any “logo” is needed for the deliverables, include it as a **static companion asset** (PNG/SVG) for documentation, not as a runtime-rendered SVG.

## Handoff recommendation
Skip further SVG-specific work; proceed to Orchestrator to finalize a plan focused on MicroPython camera+display APIs and accelerometer math.
