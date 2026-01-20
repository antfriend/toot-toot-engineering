# REVIEW (cycle-01)

## Findings (ordered by severity)
- Medium: `deliverables/cycle-01/SLIDESHOW-cycle.svg` references `../../toot-toot-logo.svg` externally; some SVG renderers/video pipelines do not resolve relative external assets, which can drop the logo in exports.
- Medium: The prompt asked to use `time-foundry.svg` for opening/closing scenes if feasible; the slideshow re-creates the scene rather than referencing the source file, which may not fully satisfy the requirement.
- Medium: The prompt asked to use `toot-toot-toolbox/MyMentalPalaceDB.db` if feasible; only `toot-toot-toolbox/MyMentalPalaceDB.md` was updated, so DB storage remains unverified.
- Low: Only slide 01 is set to visible (`class="active"`); exporting all slides requires manual toggling or a script to flip visibility.

## Recommendations
- Embed the logo as inline SVG or swap to a data URI to ensure portability for exports.
- Confirm whether direct reuse of `time-foundry.svg` is required; if yes, reference it via `<image>` or `<use>` with a linked symbol.
- Decide whether to create a `MyMentalPalaceDB.db` (SQLite or other) and document the schema, or explicitly document why Markdown is the chosen fallback.
- If exporting to video, create a simple process note or script to toggle slide visibility per frame.

## Verification notes
- Monologue aligns to 24 slide beats at 10 seconds each; wording is concise and likely within the time window.
