# SVG_ENGINEER (cycle-01)

## Applicability
Cycle-01 does not *require* SVG engineering, but the Storyteller recommended a small generated SVG badge as a tangible production artifact. This note documents practical constraints and a safe, deterministic approach.

## SVG constraints & best practices (for this repo)
- **Determinism**: generate SVG with fixed dimensions, fixed fonts, and no external references.
- **Portability**:
  - Avoid relying on system fonts that may differ across environments.
  - Use a conservative font stack in `font-family`, e.g. `system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif`.
  - Prefer simple shapes (`rect`, `circle`, `path`) and plain text.
- **Sizing**:
  - Use an explicit `width`, `height`, and matching `viewBox`.
  - For a badge, something like `width=800 height=300 viewBox="0 0 800 300"` is easy to reason about.
- **Text placement**:
  - Use `text-anchor="middle"` and set `x` to half-width.
  - Keep `dominant-baseline` usage minimal; it can vary. Instead, position with tested `y` values.
- **No embedded raster**: keep it pure vector.

## Recommended artifact spec (Cycle-01 Foundry Token)
Output file:
- `deliverables/cycle-01/assets/cycle-01-badge.svg`

Content guidelines:
- Title: `TTE cycle-01`
- Motto: `One step. One role. One artifact.`
- Visual motif: rails/gear suggested via simple circles and rectangles.

## Generation approach
- Create a small Python script (committed as part of step 5) that writes the SVG string to disk.
- Validate by:
  - Ensuring the file opens in browsers.
  - Ensuring no placeholders and no external references.

## Coordination note
The Core Worker can implement this without additional tooling. If later cycles require print-ready output, we can add a PDF assembly step using a known library (e.g., CairoSVG or reportlab), but cycle-01 should stay minimal.
