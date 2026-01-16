# SOLUTION (cycle-01)

## Outputs
- `deliverables/cycle-01/earth-rotate.gif` (animated rotating Earth, 960x402, 24 frames, logo embedded)
- `deliverables/cycle-01/hello-world-banner.gif` (cinematic banner, 960x402, logo embedded)
- `deliverables/cycle-01/assets/logo/toot-toot-logo.png` (companion logo asset)

## Build notes
- The Earth GIF is assembled by rasterizing the SVG frames with Inkscape and using ffmpeg with a generated palette.
- The Earth animation uses procedural shading and shifting surface bands to simulate rotation in the SVG source.
- The banner uses a cinematic gradient panel with a serif \"HELLO WORLD!\" title rendered from SVG.
- The official logo is overlaid onto both GIFs via ffmpeg.

## Alignment to prompt
- Both assets target a cinematic widescreen ratio; Earth GIF uses 2.39:1 and banner uses a wide frame.
- The deliverables include a small Toot Toot Engineering logo as a companion asset.
