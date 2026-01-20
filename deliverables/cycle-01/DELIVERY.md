# DELIVERY (cycle-01)

## Delivered assets
- `deliverables/cycle-01/SLIDESHOW-cycle.svg` (24-slide SVG slideshow, 1600x600)
- `deliverables/cycle-01/MONOLOGUE-cycle.md` (4-minute monologue aligned to slides)
- `toot-toot-toolbox/MyMentalPalaceDB.md` (storyboard records)

## Export notes
- To export a single slide, set that slide group to `class="slide active"` and set others to `class="slide"`; then render to PNG.
- If your exporter fails to resolve `../../toot-toot-logo.svg`, embed the logo inline or replace with a data URI.
- Opening and closing scenes are based on the `time-foundry.svg` composition; use the source file directly if your pipeline prefers linked assets.

## Deviations and constraints
- No `MyMentalPalaceDB.db` file exists in the repo; the storyboard is stored in Markdown as a fallback.
- The slideshow uses external logo references for simplicity; embedding is recommended for portability.

## Checklist
- Logo included on each slide (external reference).
- Monologue aligned to 24 slides at 10 seconds each.
- Storyboard stored in MyMentalPalaceDB format.
