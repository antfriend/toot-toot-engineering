# BOOTSTRAP (cycle-01)

## Prompt (interpreted)
Build a UNIHIKER K10 touchscreen **text-based dungeon crawler** with a **tap-to-choose** UI.

Story requirements:
- Opens at the entrance to a cave with a little campfire inside.
- Multiple paths leading to **silly** good/bad endings.
- One path: step-by-step, accurate, helpful explanation of **mmpdb usage & applications**.
- One path: a **cosmic dimension of eyeball nodes** casting longing gazes at one another.
- One path: the adventurer discovers they are **food** being eaten and digested.

Engineering requirements:
- Delivered as a repo-style project with:
  1) `TTDB_README.md` (dramatic intro + device installation + bundle structure + run steps)
  2) An **installation bundle** containing:
     - a purpose-built **mmpdb**
     - python files
     - anything else needed
- Must refer to TTDB RFC docs, standards docs, and `tte_monitor.py` patterns/examples.

## Proposed team composition (roles)
Minimum roles to hit “complete game + bundle”:
1. **Storyteller**: craft the branching narrative, ensure each path hits the required themes and stays silly.
2. **Orchestrator**: refine plan, define repo layout, add needed roles/steps, ensure RFC alignment + logging.
3. **Core worker**: implement the game (UI + state machine + story graph + mmpdb integration) and create the install bundle.
4. **Reviewer**: validate on-paper correctness (structure, run steps, RFC alignment), spot gaps.
5. **Delivery packager**: assemble final deliverables, ensure `TTDB_README.md` completeness, update `RELEASES.md`.

Strongly recommended additions (to reduce risk):
- **DB/Content builder** (can be part of Core worker): create the dedicated populated mmpdb with records that the game references.
- **Device UI compatibility check** (can be part of Reviewer): ensure the UI approach is plausible on UNIHIKER K10 (Tkinter/canvas/buttons).

## High-level objectives (cycle-01)
- Deliver a runnable K10 dungeon crawler with a simple touchscreen-friendly choice UI.
- Provide a small, dedicated mmpdb (markdown DB file) that is both:
  - used by the game for “lore” and/or tutorial content
  - demonstrative of TTDB cursor semantics and typed edges (per RFCs)
- Provide an installable bundle and a clear `TTDB_README.md`.

## Key design decisions (recommended)
- Implement the story as a **node graph** (JSON or Python dict) with:
  - `node_id`, `text`, `choices[]`, optional `effects`, `ending` flags
  - Choices are displayed as large buttons (tap-friendly)
- Store tutorial “mmpdb path” content in the **mmpdb itself** (records that the story nodes can quote or summarize), so the player “discovers” documentation inside the dungeon.
- Use a **single-file DB** similar to `MyMentalPalaceDB.md` style, aligned to TTDB-RFC-0001.
- Keep dependencies minimal (prefer standard library). If tkinter is used, note any device constraints in `TTDB_README.md`.

## Plan adjustments (recommended)
The default plan needs a bit more explicit engineering around the bundle + DB.
I recommend Orchestrator updates `PLAN.md` to include:
- A concrete repo/bundle layout step.
- A DB schema/content step.
- A “run smoke test” step (even if only scripted).

Suggested updated critical path (proposed):
1. Bootstrap (this step)
2. Storyteller: story graph + tone + required paths mapped
3. Orchestrator: finalize plan, repo layout, RFC mapping checklist
4. Core worker: implement game engine + UI
5. Core worker: build dedicated mmpdb content + integrate
6. Reviewer: review + fix list
7. Delivery packager: assemble bundle + write `TTDB_README.md` + update releases
8. Retrospective

## Risks / unknowns
- **UNIHIKER K10 runtime**: availability of tkinter and exact input handling; may require alternate UI framework. If tkinter is unavailable, fall back to a console-like UI with large text and simple tap regions (needs platform confirmation).
- **mmpdb library**: unclear if there is an existing Python API in this repo; may need to implement lightweight parsing for TTDB markdown DB format.

## Retrospective (cycle-01)
What worked:
- Keeping everything **stdlib-only** made the bundle small and portable.
- Treating the story as a **node graph** made it straightforward to satisfy the three required branches.
- Bundling a dedicated TTDB markdown DB gives a concrete “learn mmpdb by spelunking” artifact.

What to improve next cycle:
1. **Resolve UI runtime certainty for K10**
   - Add a tiny “environment check” script or mode that prints Python version and confirms tkinter availability on-device.
   - If tkinter is missing, plan a UI port to the device’s preferred toolkit.
2. **Clarify TTDB typed-edge literal syntax**
   - The repo’s reference parser (`tte_monitor.py`) reads `type>@target`.
   - Consider updating TTDB-RFC-0003 (or adding a note/compat section) to make the delimiter unambiguous.
3. **Add a primitive-query loop (@AI) inside the game**
   - The DB advertises `librarian.enabled` and primitive queries; the game currently only browses records.
   - Next cycle could implement a tiny `@AI` command input that supports `select/find/edges/status`.

## Next-cycle prompt suggestions (human must choose one)
1. “Add an in-game `@AI` console that supports primitive queries (`select/find/edges/status/note`) against the bundled TTDB, and log player discoveries back into the DB cursor fields.”
2. “Port the UI layer from tkinter to the UNIHIKER K10’s preferred UI toolkit (if tkinter is absent) and improve touch ergonomics (fonts, spacing, animations).”
3. “Expand the dungeon into a second chapter that teaches TTN concepts (typed edges taxonomy, trust/reputation) using in-world ‘eyeball node diplomacy’ puzzles.”
