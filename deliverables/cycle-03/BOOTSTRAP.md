---
cycle: 03
role: Bootstrap
---

# Cycle 03 Bootstrap

## Prompt source
`TTE_PROMPT.md`

> Please make a Unihiker K10 A32 sample project. Refer to the RFCs, unihiker_k10, and related folders and files. Develop a simple touch screen UI with interactive sounds. Make the UI show navigation of a TTDB on the embedded file system (not to an SD card).
>
> Deliverable: an arduino project folder and files.

## Context from prior cycles

- **Cycle 01** produced `k10_ttdb_navigator.ino` — a working TTDB navigator using SD card storage, button A/B navigation, tilt gestures, and startup tones. Source in `unihiker_k10/`.
- **Cycle 02** produced `k10_ttdb_configurator.py` — a host-side tool for configuring the navigator JSON config.

The cycle-01 sketch is the primary prior art. Cycle 03 builds on it with three targeted improvements:
1. Replace SD with LittleFS (embedded flash filesystem, per A32-RFC-0002 §1.1).
2. Add touch screen navigation zones (on-screen PREV / NEXT tap areas).
3. Add richer interactive sounds (nav beep + wrap chime, distinct from startup toot).

## Team composition

| Role | Purpose |
|------|---------|
| Bootstrap (this doc) | Interpret prompt, scope work, propose plan |
| Storyteller | Frame the device experience narrative |
| Orchestrator | Finalize plan, update PLAN.md and LOG.md |
| Core Worker | Write `k10_a32_navigator.ino`, `data/ttdb.md`, `SOLUTION.md` |
| Reviewer | Verify correctness against A32 RFCs and K10 API |
| Delivery Packager | Assemble final assets, update RELEASES.md |
| Retrospective | Capture lessons, propose next prompts |

SVG Engineer: not applicable (no SVG output).

## Objectives

1. Produce `deliverables/cycle-03/k10_a32_navigator/k10_a32_navigator.ino` that:
   - Mounts LittleFS and reads `/ttdb.md` from embedded flash.
   - Renders a scrollable record list on the K10 screen.
   - Accepts input from buttons A/B, tilt gesture, AND touch screen zones.
   - Plays interactive tones: startup melody, navigation beep, wrap-around chime.
2. Produce `deliverables/cycle-03/k10_a32_navigator/data/ttdb.md` — the TTDB data file to upload to LittleFS.
3. Document the PlatformIO `uploadfs` workflow for deploying the data partition.

## Plan adjustments recommended

- Skip SVG Engineer step (not applicable).
- Storyteller should be brief (1 page max); this is a utility tool, not a narrative product.
- Core Worker is the critical step; allocate full attention to the sketch.
- Reviewer must check: LittleFS API correctness, LVGL touch polling, sound API usage.

## Suggested next-cycle prompts (choose one after this cycle is complete)

1. **A32 Agent Loop** — "Add a sense-reason-act agent loop to the K10 navigator. Read typed edges from the TTDB and use tilt sensor readings as the sense input to select the nearest TTDB node automatically. Produce an updated .ino file."
2. **TTDB Authoring Tool** — "Build a Python CLI that authors a new TTDB file from a JSON input, validates it against TTDB-RFC-0001, and outputs a `.md` file ready to upload to LittleFS on the K10."
3. **Multi-screen UI** — "Redesign the K10 navigator UI to use three screens: list view, detail view, and edges view. Swiping left/right switches views; touch zones navigate within each view. Produce an updated .ino file."

---

## Retrospective (added after cycle completion)

### What worked well
- Targeting three specific improvements (LittleFS, touch, richer sounds) kept scope tight.
- Reusing the cycle-01 TTDB parser structure minimized risk.
- The LVGL `lv_indev_get_next` / `lv_indev_get_point` pattern is the correct public API path and avoids internal struct access.

### What to improve next cycle
- **Touch press-state detection:** The point-change approach detects taps but not stationary holds. Next cycle should add `lv_indev_get_state()` support or LVGL event callbacks if press-hold is needed.
- **`canvasClear` color overload ambiguity:** The DFRobot header has no uint32_t overload. Calling `canvasClear(0x000000)` silently resolves to `canvasClear(uint8_t row=0)`. Document this as a known quirk in the project AGENTS.md if it persists across cycles.
- **`max_nodes` from TTDB header:** `MAX_RECORDS=24` is hard-coded. A future cycle should read `cursor_policy.max_nodes` from the `mmpdb` block at load time.

### Role/plan changes recommended
- No structural changes needed.
- If the next cycle involves the agent loop (prompt 1), add an **Agent Loop** role between Core Worker and Reviewer to verify sense-reason-act correctness separately from UI correctness.

