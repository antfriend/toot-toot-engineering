# RETROSPECTIVE (cycle-01)

## What went well
- Clear role handoffs and a sensible doc-first critical path.
- Deliverable is skimmable (tables + recipes) and includes key warnings (LoRa band selection).
- Reviewer feedback was actionable and quickly incorporated.

## What to improve next time
1. **Source precision for “supported hardware”**
   - Add a dedicated “Compatibility references” section in the main doc with direct links (Meshtastic hardware page, key vendor pages).
2. **Add a minimal “inputs/UI” checklist**
   - Builders often forget buttons/encoder, buzzer, and status LEDs—include a short options table.
3. **Optionally add a PDF packaging step**
   - If the human wants a print/share-ready PDF, add a PDF assembler step next cycle.
4. **Pricing methodology**
   - Consider adding a second price column: “US distributor” vs “marketplace” to set expectations.

## Recommended plan changes (framework-level)
- For document-only cycles, allow the Reviewer step to request a quick “revise” micro-step if needed (rather than implicitly folding revisions into the Core worker step).

## Next-cycle prompts (human must choose 1)
1. **Build guide:** “Select one of the reference builds and write a complete build guide: wiring/pin map, parts list with purchase links, firmware flashing steps (Meshtastic or MicroPython), and a quick-start troubleshooting checklist.”
2. **Ultra-low-power design brief:** “Create a power-optimization brief: sleep strategy, regulator selection, display power gating, and a battery-life estimator spreadsheet outline.”
3. **Screen UI prototype:** “Design a minimal on-device UI for a tiny screen: key screens, navigation buttons, font/layout guidance, and example MicroPython/CircuitPython display code skeleton.”

## Bootstrap offer
If you choose one prompt above, Bootstrap can reset the plan for cycle-02 and scaffold the new deliverables folder.
