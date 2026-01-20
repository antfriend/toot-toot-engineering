# SVG ENGINEER (cycle-01)

## SVG constraints and approach
- Base aspect ratio: `1600x600` from `time-foundry.svg` (wide cinematic banner). Use this as the slideshow canvas.
- Animation: keep CSS animations minimal or disabled for export to video; rely on static frames for each slide (export as individual SVGs or a single SVG with grouped slide layers).
- Typography: `time-foundry.svg` uses Georgia/Times; keep serif tone for consistency, but allow a clean sans for body labels if needed.
- Asset reuse: lift background groups from `time-foundry.svg` for opening and closing scenes; insert `toot-toot-logo.svg` as a small stamp on all slides or at least intro/outro.
- Legibility: large, high-contrast headings; avoid overly dense text (max 3-5 lines per slide).

## Proposed slide system
- Single SVG file with a `<g id="slide-XX">` per slide, each occupying full canvas.
- A simple convention for export: toggle visibility by setting `display="none"` except for the active slide.
- Use a consistent title block and caption area (e.g., top-left title, mid-right body, bottom-left step indicator).

## Layout grid
- Safe area: 120px margin on all sides.
- Title zone: y=90 to y=180 (large 52-64px text).
- Body zone: y=200 to y=420 (30-36px text).
- Footer zone: y=470 to y=560 (step indicator, small icon, logo).

## Opening/closing scenes
- Opening: use `time-foundry.svg` intact with a simple overlay title and subtitle (Slide 01).
- Closing: reuse the same scene but replace the subtitle with a call to action (Slide 24).

## Export notes
- If exporting to video, render each slide as a separate SVG/PNG to avoid SMIL/CSS animation variability.
- Ensure the logo is embedded via `toot-toot-logo.svg` with relative path from slideshow file.

## Risks and mitigations
- Text overflow on 1600x600: enforce line lengths and reduce copy to fit.
- Animation inconsistencies in renderers: default to static visuals for export.
- Font availability: provide a simple fallback stack in the SVG.
