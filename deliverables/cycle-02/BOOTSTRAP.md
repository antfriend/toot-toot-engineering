# BOOTSTRAP (cycle-02)

## Prompt
Create a single `hello-world.svg` where the text "Hello World" orbits around the Earth.

## Team composition
- Bootstrap (this step): interpret prompt, propose plan/roles.
- Storyteller: define the orbiting text motion style and overall cinematic/graphic tone.
- SVG engineer: document SVG animation constraints, path text guidance, and export tips.
- Orchestrator: finalize plan, files, and logging; adjust steps.
- Core worker: build the SVG deliverable with Earth + orbiting text and logo inclusion.
- Reviewer: verify SVG validity, animation loop, and logo requirements.
- Delivery packager: assemble notes and update releases.
- Retrospective: recommend improvements for next cycle.

## Objectives
- Deliver a single `hello-world.svg` with an orbiting "Hello World" text path around Earth.
- Ensure smooth, looping SVG animation without external dependencies.
- Keep output readable at typical viewport sizes (desktop and mobile).
- Include a small Toot Toot Engineering logo in the SVG.

## Plan adjustments (recommendations to Orchestrator)
- Make SVG engineer a required step for this cycle.
- Add a brief SVG validation checklist in the Reviewer step (looping, text legibility, logo presence).
- Target a standard cinematic aspect ratio (2.39:1) unless the orbit composition demands a square format.

## Risks and constraints
- SVG animation support varies across viewers; use simple SMIL or CSS animations.
- Text-on-path readability can suffer if the orbit is too tight or too fast.

## Next-cycle prompts (choose one)
1. Create a "Toot Toot" orbital logo reveal SVG with two concentric text orbits and subtle starfield.
2. Produce a minimalist SVG poster for the cycle deliverable with a short caption and embedded logo.
3. Build a short animated SVG showing the Earth sunrise behind the banner, with a static title.

Please choose 1, 2, or 3 for the next cycle.

## Retrospective update (cycle-02)
- Consider adding a CSS animation fallback for viewers without SMIL support.
- Provide a small inline logo variant to reduce base64 payload size.
- Add a viewer compatibility note in delivery docs for SVG animation behavior.

If you'd like, I can implement these changes and reset the plan for the next cycle using your selected prompt.
