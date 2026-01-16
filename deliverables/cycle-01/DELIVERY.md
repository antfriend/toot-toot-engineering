# DELIVERY (cycle-01)

## Delivered assets
- `deliverables/cycle-01/earth-rotate.gif` (animated rotating Earth, 960x402, logo embedded)
- `deliverables/cycle-01/hello-world-banner.gif` (cinematic banner, 960x402, logo embedded)
- `deliverables/cycle-01/assets/logo/toot-toot-logo.png` (companion logo asset)

## Supporting files
- `deliverables/cycle-01/BOOTSTRAP.md`
- `deliverables/cycle-01/STORYTELLER.md`
- `deliverables/cycle-01/SVG_ENGINEER.md`
- `deliverables/cycle-01/IMAGE_ASSETS.md`
- `deliverables/cycle-01/SOLUTION.md`
- `deliverables/cycle-01/REVIEW.md`

## Export notes
- Earth GIF is assembled from SVG frames via Inkscape rasterization and ffmpeg palette-based GIF encoding.
- Earth GIF loops by design and uses 24 frames at 12 fps.
- Banner GIF is built from a dedicated SVG banner rasterized with Inkscape.
- Official logo is overlaid bottom-right on both GIFs via ffmpeg.
- The banner is static; if higher-fidelity typography is needed, regenerate with a richer font pipeline.
- The official logo is included as a companion asset; embedding it into the GIFs would require rasterization tools.
