# SVG_ENGINEER

## Scope
The prompt is SVG-centered, so this role is required. The goal is a self-contained, richly detailed stained glass window illustration that renders cleanly in modern browsers.

## SVG constraints and best practices
- Use a clear `viewBox` (e.g., `0 0 1000 1600`) and explicit `width`/`height` for predictable scaling.
- Avoid external assets; rely only on inline SVG definitions (`<defs>`) and vector paths.
- Prefer grouped layers: frame, tracery, glass panes, highlights, and lead lines for clarity.
- Use path-based leadwork strokes with consistent widths; avoid hairlines that vanish when scaled.

## Structural recommendations
- Frame: outer rectangle with stone-like border using subtle gradients.
- Tracery: circles and arcs; use `path` + `stroke` to define lead lines.
- Glass panes: fill shapes with gradients and slight noise patterns for texture.
- Highlights: soft overlays with low opacity to simulate light bloom.

## Technical notes
- Define a small set of gradients in `<defs>` and reuse them via `fill="url(#...)"`.
- Consider a subtle grain pattern using an SVG `<filter>` with `feTurbulence`.
- Keep IDs unique and descriptive to avoid collisions.
- Use `vector-effect="non-scaling-stroke"` sparingly; avoid if it harms visual weight at scale.

## Risks
- Overly complex filters may degrade performance; keep filter usage minimal.
- Too many tiny paths can bloat file size; balance detail with readability.

## Handoff to Core worker
- Produce `deliverables/cycle-01/stained-glass.svg` as the main asset.
- Include a brief `deliverables/cycle-01/SOLUTION.md` describing structure, palette, and how to render.
