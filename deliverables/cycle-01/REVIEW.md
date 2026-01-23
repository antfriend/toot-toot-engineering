# REVIEW (cycle-01)

## Scope reviewed
- `deliverables/cycle-01/HARDWARE_OPTIONS.md`

## What’s strong
- Good builder-centric structure: quick choices → criteria → tables → recipes → pitfalls.
- Correct high-level warning about regional LoRa bands.
- Includes a reasonable spread of options (all-in-one boards + mix-and-match).

## Corrections / tighten-ups recommended
1. **Meshtastic compatibility specificity**
   - Current text says “confirm in Meshtastic docs” but does not link to the exact supported-hardware page.
   - Recommendation: add a direct link to Meshtastic’s supported hardware section and clarify that *support is per exact model/revision*.
   - Meshtastic home is linked; add: https://meshtastic.org/docs/hardware/ (verify structure if it changes).

2. **CircuitPython vs ESP32 nuance**
   - ESP32 family does have CircuitPython ports/boards, but support is **not universal** across all cheap dev boards.
   - Recommendation: reword ESP32 row to: “MicroPython is broadly supported; CircuitPython is strong on specific boards/ports.”

3. **nRF52 for LoRa mesh clarification**
   - The reference build #3 mentions nRF52 “for non-LoRa tasks”. That can confuse readers.
   - Recommendation: either remove nRF52 from that recipe or explicitly say: “nRF52 is great for ultra-low power BLE devices, but for Meshtastic specifically you’ll typically be on ESP32-class hardware today.”

4. **Power section link for MCP73831**
   - The Microchip link is a generic search suggestion; better to use a stable product page or datasheet link.
   - Recommendation: replace with a direct MCP73831 product page or datasheet URL.

5. **Pricing disclaimers**
   - Prices are labeled as ballpark and dated (good). Consider adding a note that “all-in-one boards from marketplaces often vary by revision; verify onboard LoRa chip (SX1262 vs SX127x).”

## Potential omissions (optional improvements)
- Add a tiny “buttons/input” note: 2–3 tactile buttons or a rotary encoder are common for screen navigation.
- Add a line about **GPS** as optional but power-hungry (already hinted); could be a bullet in selection criteria.
- Add a short note about **regulatory** considerations (duty cycle limits in some regions, transmit power limits).

## Ready-to-ship assessment
- **Mostly yes**, as a high-level options brief.
- For “excellent” correctness, apply the tighten-ups above (especially Meshtastic supported-hardware link and ESP32/CircuitPython nuance).

## Required actions before Delivery step
- Update `HARDWARE_OPTIONS.md` to incorporate the corrections above (no placeholders).

