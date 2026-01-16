# BOOTSTRAP (cycle-01)

## Prompt (from README.md)
Create an animated gif of a rotating earth and a banner that reads "Hello World!" in a grand cinematic aspect ratio.

## Team composition
- Bootstrap (this step): interpret prompt, propose plan/roles.
- Storyteller: define the cinematic look/feel, title treatment, and motion notes.
- Orchestrator: finalize plan, files, and logging; adjust steps.
- Image producer: generate earth frames and any textures/overlays programmatically.
- Core worker: assemble the banner layout and final GIF(s), include logo.
- Reviewer: verify deliverables, aspect ratio, motion quality, and logo inclusion.
- Delivery packager: bundle assets, notes, and release updates.
- Retrospective: recommend process improvements for next cycle.

## Objectives
- Produce a smooth looping animated GIF of a rotating Earth.
- Create a cinematic banner reading "Hello World!" that matches the GIF's mood.
- Use a widescreen cinematic aspect ratio (target 2.39:1 or 16:9 if constraints arise).
- Include a small Toot Toot Engineering logo in the final media or as a companion asset.
- Document sources/constraints for any third-party textures or references used.

## Plan adjustments (recommendations to Orchestrator)
- Add an Image producer step before Core worker to generate earth frames and any background plates.
- Clarify deliverables: `earth-rotate.gif`, `hello-world-banner.png`, and a short `NOTES.md` with sources/build steps in `deliverables/cycle-01/`.
- Specify target resolution for cinematic ratio (e.g., 1920x804 for 2.39:1) to keep outputs consistent.
- Include a lightweight QC checklist in the Reviewer step: loop seamlessness, text legibility, and logo presence.

## Risks and constraints
- GIF size and color banding: may need palette tuning or fewer frames.
- If no external texture source is permitted, generate a stylized Earth procedurally.
- Ensure the banner typography remains legible at final GIF dimensions.

## Retrospective (pre-emptive)
- If frame generation proves heavy, add a reusable script template for image pipelines.
- Consider a dedicated "Asset sourcing" micro-step when third-party textures are required.
- Offer to implement these changes and reset the plan after delivery if approved.

## Next-cycle prompts (choose one)
1. Build a short looping "Toot Toot Engineering" factory animation in the same cinematic style, including the logo as a watermark.
2. Create a two-panel before/after banner that shows raw vs. polished assets for this cycle, with a succinct caption.
3. Produce a minimalist animated logo sting (3–5 seconds) suitable for video intros, plus a static poster frame.

Please choose 1, 2, or 3 for the next cycle.

## Retrospective update (cycle-01)
- Add a preflight step to check for rasterization tools (ImageMagick, ffmpeg, or Python) and log fallbacks early.
- Maintain a lightweight internal font/palette module so banner text can look more cinematic without external dependencies.
- Consider promoting the procedural GIF generator into `library/` for reuse when tooling is limited.

If you'd like, I can implement these changes and reset the plan for the next cycle using your selected prompt.
