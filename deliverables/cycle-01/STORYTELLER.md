# STORYTELLER (cycle-01)

## Narrative frame: “From idea to a working mesh node”
This deliverable should read like a confident guide for a practical builder who wants a low-cost, wireless mesh node with a tiny screen.

### The core story
You are choosing parts for a pocket-sized “digital trail marker”:
- it can send/receive short messages without cell service,
- it runs for a long time on a small battery,
- it has a simple screen so it works even when your phone is dead,
- it’s buildable from widely available modules.

Meshtastic + LoRa is the default path because it’s a mature ecosystem with real-world community usage. But the document should keep the door open to alternatives when cost/availability/power constraints require it.

## Reader journey (recommended section flow for HARDWARE_OPTIONS.md)
1. **What you’re building (one paragraph)**
   - A low-cost mesh node with LoRa radio, low-power MCU, small display, battery.

2. **Quick choices (the “if you only read one section” box)**
   - Pick your region band (US915/EU868/etc.)
   - Pick your platform approach:
     - **All-in-one Meshtastic board** (fastest path)
     - **Mix-and-match MCU + LoRa module** (cheapest/most flexible)

3. **Selection criteria (5–7 bullets)**
   - Frequency/region, firmware/ecosystem support, sleep current, antenna connector, availability, size, charging, screen readability.

4. **Hardware options tables (the meat)**
   - **Meshtastic-friendly boards (fast path)**
   - **MCUs that run CircuitPython/MicroPython**
   - **LoRa modules (SX1262/SX1276 family, etc.)**
   - **Displays (OLED vs e-ink vs LCD)**
   - **Power (battery, chargers, regulators)**

5. **Reference builds (3–6 “recipes”)**
   Each recipe is a tiny story:
   - “Cheapest workable node”
   - “Best battery life”
   - “Best screen outdoors”
   - “Smallest build”
   - “Most available parts”

   For each: estimated cost, key tradeoffs, and a short “why you’d pick this”.

6. **Pitfalls & gotchas (save the builder pain)**
   - Wrong frequency band
   - Antenna mismatch/poor ground plane
   - Power budget surprises (screen backlight, GPS)
   - Level shifting / I/O voltage mismatches
   - Deep sleep not actually deep sleep (USB-UART, regulators)

7. **Alternatives corner (brief, non-distracting)**
   - If LoRa parts are unavailable/too costly: mention Wi‑Fi mesh / BLE / Thread as *different trade spaces* (range/power/phone dependence).

## Tone and formatting notes
- Use tables for scanability; keep prose short.
- Put links in a consistent “Info” column.
- Put price ranges in a consistent “Typical price (USD, single qty, as-of YYYY‑MM)” column.
- Clearly label what is **Meshtastic-ready** vs **general-purpose**.

## “Magic moments” to emphasize
- The first time two nodes exchange a message without infrastructure.
- The “battery life unlock” moment when deep sleep is configured correctly.
- The practicality of a screen: quick status without a phone.

## Suggested additions to plan (optional)
If time allows in the Core worker step, add a one-page appendix:
- “How to sanity-check a candidate board in 60 seconds” (band, chip, antenna connector, USB-UART, regulator, display bus).
