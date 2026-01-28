# cycle-01 RETROSPECTIVE

## What went well
- Clear simulator-first approach produced real artifacts (DB + monitor + topic map) quickly.
- Deterministic semantic rules cover the key demo intents and keep mesh-side parsing simple.
- Generated TTDB markdown provides a tangible “graph memory” anchor for future services.

## What to improve next time
1. **Fix correctness/legibility issues before calling a cycle complete**
   - Entity IDs are double-prefixed in the DB output.
   - Monitor edge parsing doesn’t currently align with the DB edge formatting.

2. **Add a thin “golden outputs” test**
   - Keep `deliverables/cycle-01/generated/` as golden fixtures.
   - Add a simple script/test that regenerates outputs and diff-checks key sections.

3. **Add MQTT publish/subscribe wiring (opt-in)**
   - Make `demo/simulate_day.py` support `--mqtt` to publish semantic events to a broker.
   - Keep `--dry-run` as default.

4. **Implement at least one real receiver transport**
   - Start with Meshtastic serial on Windows 11 (most practical) with clear troubleshooting.

5. **AI librarian**
   - Implement a minimal subscriber that can answer `@AI summarize 6h` by reading the DB and returning a mesh-short answer.
   - Enforce “only speak when invoked” at the protocol boundary.

## Recommended role/plan changes
- Add a small **“Fix-it”** sub-step right after Reviewer in future cycles to immediately apply reviewer-caught formatting issues.
- Keep simulator-driven artifacts as acceptance tests and require they render properly before delivery.

## Bootstrap offer
If approved, Bootstrap can:
- implement the two review fixes (entity rendering + monitor edge parsing) immediately,
- add a `--mqtt` publishing mode to the demo,
- and reset the plan for cycle-02 based on one selected prompt.

## 3 next-cycle prompts (choose 1)
1. **Fix & harden**: Fix DB entity rendering and monitor edge parsing; add golden-output regression check; mark cycle-01 complete.
2. **MQTT + librarian**: Wire MQTT publishing/subscribing end-to-end and implement a minimal AI librarian that summarizes last N hours when invoked.
3. **Meshtastic serial integration**: Implement and document a working Meshtastic serial receiver on Windows 11 (T-Deck Plus → gateway), plus live capture → semantic events → MQTT.
