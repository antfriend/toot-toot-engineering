# SVG_ENGINEER (cycle-03)

## Scope
Engineer two self-contained SVG animations (`one_drop_portrait.svg`, `raining.svg`) that satisfy the narrative direction and remain easy to tune in future cycles.

## Strengths of SVG for this cycle
- Resolution-independent source assets for iterative art direction.
- Native animation primitives (`animate`, `animateTransform`) keep files portable.
- Layered composition supports parallax-like scene depth with low complexity.

## Constraints and risks
- Cross-viewer support for SMIL animation can vary.
- Very high element counts can make manual timing edits brittle.
- Without external rendering, effects must stay within lightweight filter/gradient usage.

## Engineering decisions
- Use nested groups for transform rigs (bob/tilt/squash) in the portrait.
- Use symbolic raindrop reuse (`<symbol>` + `<use>`) for maintainable scene density.
- Encode scene progression using key-timed opacity/scale transitions for cloud, fog, lake, and sink phases.
- Keep color values explicit and readable for later palette swaps.

## Deliverable-specific design
### one_drop_portrait.svg
- Exactly three visible shape primitives define character body/highlight.
- Personality comes from transform and highlight motion only.

### raining.svg
- 20-second looping timeline with continuous descent illusion.
- Environmental layers: sky, cloud, fog, lake, splashes, sink overlay.
- Surrounding drops include mixed opacity/size for near/far depth cues.

## Handoff to Core worker
- Build files directly under `deliverables/cycle-03/`.
- Keep IDs and section structure clear for downstream export tooling.
