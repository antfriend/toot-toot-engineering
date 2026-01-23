# BOOTSTRAP (cycle-01)

## Prompt (from README.md)
Create a summary document of hardware options, with pricing and info links for making a new, low cost, wireless mesh networking device. Optimally using LoRa and Meshtastic but other possibilities are welcome. We want to include a small screen and a low cost, low power microcontroller that can run CircuitPython/MicroPython.

## Interpretation
We are producing a buyer-oriented, builder-friendly hardware options brief for a DIY low-cost mesh device.

Primary focus:
- LoRa + Meshtastic-compatible radios (Sub-GHz)
- Low-power microcontrollers that support CircuitPython/MicroPython
- Small displays (OLED/e-ink/LCD) suitable for handheld devices
- Practical, low-cost BOM combinations with links and ballpark pricing

Secondary/optional:
- Alternative radios/meshes (2.4GHz, Wi-Fi, BLE, Thread) for comparison
- Power options (LiPo + charger IC, AA/AAA, solar) and enclosure notes

## Objectives (definition of done for this cycle)
1. Produce a single, skimmable summary document with tables:
   - MCU/Dev boards options (MicroPython/CircuitPython)
   - LoRa radio/module options and Meshtastic-friendly boards
   - Display options
   - Power/charging options
   - Recommended “reference builds” (3–6) with approximate total cost
2. Include links to official product pages and/or reputable distributors.
3. Clearly label price assumptions (USD, typical single-unit retail, as-of date) and note that prices vary.
4. Call out region/frequency variants (EU868/US915/etc.) and key selection criteria.

## Proposed team composition
- Storyteller: Set the narrative frame: “how to choose parts” and reader journey.
- Orchestrator: Ensure plan/assets/logging are correct; adjust plan for a doc-first delivery.
- Core worker (Hardware researcher/technical writer): Draft the actual options summary and reference builds.
- Reviewer (RF + embedded sanity check): Verify compatibility claims, frequencies, and common pitfalls.
- Delivery packager: Ensure final deliverable is clean, linked, and release-noted.

(Optional additions if plan allows):
- Sourcing/Costing specialist: tighten pricing, add alternates/out-of-stock notes.

## Recommended plan adjustments
Current PLAN.md shows Step 1 checked in “Current step” but the critical path list is unchecked; normalize this.

Also, for this prompt, the optional SVG engineer step is not needed.

Recommend:
- Remove SVG engineer step from the critical path (or mark as not-applicable).
- In Core worker step, explicitly name the primary artifact:
  - `deliverables/cycle-01/HARDWARE_OPTIONS.md`
- Add a small “BOM reference builds” section requirement.

## Risks / open questions
- Exact pricing changes rapidly; we will provide ballpark ranges with date stamp and links.
- Meshtastic compatibility depends on specific radio/MCU combos and community firmware support.

## Next-cycle prompts (human must choose 1)
1. “Turn the best reference build into a complete build guide: wiring diagram, firmware flashing steps, and a printable quick-start card.”
2. “Create a power-optimization and enclosure design brief: battery sizing, duty-cycling, and weatherproof enclosure options.”
3. “Prototype a minimal UI/UX for the device screen: key screens, button mapping, and font/layout recommendations for tiny displays.”
