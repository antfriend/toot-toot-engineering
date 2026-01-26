# SOLUTION

## Asset
- `deliverables/cycle-01/stained-glass.svg`

## Approach
A single, self-contained SVG renders a cathedral-style stained glass window with a rose window, lancet panels, and a central medallion. The composition relies on layered gradients, repeated geometry, and a subtle grain filter to evoke glass texture. Leadwork is emphasized with strokes and a low-opacity lead pattern overlay.

## Structure
- Frame: stone and inner frame rectangles with gradients.
- Glass layers: rose window, twin lancets, medallion, and decorative borders.
- Leadwork: strokes and a pattern grid to imply solder lines.
- Texture: `feTurbulence` filter blended for grain.

## Palette
Deep reds, cobalt blues, emerald greens, and amber accents to mimic traditional stained glass hues.

## Render notes
Open the SVG in any modern browser; it scales cleanly due to a fixed `viewBox` and explicit dimensions.
