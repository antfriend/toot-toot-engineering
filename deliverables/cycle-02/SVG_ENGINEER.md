# SVG_ENGINEER

## Scope
The SVG remains the core asset; lighting effects are layered via CSS in a surrounding HTML context. The SVG should remain self-contained and unmodified unless class hooks are required.

## Constraints and guidance
- Keep the SVG inline in the HTML to allow CSS targeting and blend effects.
- Apply lighting through wrapper layers rather than editing the SVG paths.
- Use CSS filters and overlays; avoid heavy SVG filters that could degrade performance.

## CSS lighting recommendations
- Use multiple `drop-shadow` passes for glow and bloom.
- Apply a directional radial gradient overlay with `mix-blend-mode: screen`.
- Add a subtle vignette layer to center attention.

## Technical notes
- Maintain a fixed container size to preserve aspect ratio (1000x1600).
- Ensure the SVG remains crisp by avoiding CSS scaling beyond 1x where possible.
- Document lighting variables for easy tuning.

## Handoff to Core worker
- Produce `deliverables/cycle-02/lighting-demo.html` with inline CSS and the SVG embedded.
- Document lighting choices and how to view the demo in `deliverables/cycle-02/SOLUTION.md`.
