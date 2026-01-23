# Low-cost wireless mesh device: hardware options (LoRa + Meshtastic focus)

**Goal:** a low-cost, low-power handheld mesh node with a small screen, built from accessible modules.

**Pricing note:** price ranges below are **typical single-unit retail in USD** (often from Adafruit, SparkFun, Digi-Key/Mouser, AliExpress/Amazon, or board vendors) and can swing significantly by region/stock. **As-of:** 2026-01.

**Region/band note (LoRa):** choose hardware for your local ISM band (common: **US915**, **EU868**, **AU915**, **AS923**, **IN865**, **KR920**). A “wrong band” radio is a common failure mode.

---

## If you only read one section: quick choices

### Fastest path (least wiring)
Choose an **all-in-one Meshtastic-capable board** (ESP32 + LoRa + power management, sometimes GPS/screen). You’ll spend a bit more per unit but save time and reduce integration risk.

### Cheapest / most flexible path
Choose a **MicroPython/CircuitPython MCU board** + a **LoRa module (SX1262/SX127x)** + a **small display**. This is great for experimentation and cost control, but requires careful power + pin planning.

---

## Selection criteria (what matters most)
- **Ecosystem/firmware support:** Meshtastic support is strongest on certain ESP32+LoRa boards.
- **Sleep current:** board-level regulators, USB-UART chips, power LEDs, and GPS can dominate standby drain.
- **LoRa chip family:** SX1262 (newer) vs SX1276/78 (older, still common). Both can work.
- **Antenna connector:** u.FL/IPEX vs SMA; plan for strain relief and real antennas.
- **I/O voltage:** many LoRa modules are 3.3V logic only.
- **Display readability & power:** OLED is easy; e-ink wins for sunlight + ultra-low idle.
- **Availability:** pick parts with at least 2 sourcing options.

---

## A. Meshtastic-friendly “all-in-one” boards (fast path)
These options typically bundle **ESP32 + LoRa** (often SX1262) and sometimes **GPS** and/or **screen**.

| Option | What you get | Typical price (USD) | Why pick it | Info |
|---|---|---:|---|---|
| Heltec LoRa 32 (ESP32 + LoRa + OLED variants) | ESP32 + LoRa + small OLED on some models | $18–$35 | Very common in hobby LoRa ecosystem; integrated screen on some versions | https://heltec.org/ |
| LilyGO TTGO/T-Beam / T-LoRa series | ESP32 + LoRa; some variants include GPS, battery support | $20–$45 | Popular for Meshtastic projects; many variants to match needs | https://lilygo.cc/ |
| RAK WisBlock (modular) | Modular base + LoRa + add-on screen/GPS | $25–$60+ | Flexible, field-focused ecosystem; good modularity | https://store.rakwireless.com/ |

**Meshtastic compatibility:** confirm the *exact* board model/revision against Meshtastic’s supported hardware list:
- Meshtastic hardware docs: https://meshtastic.org/docs/hardware/

*Marketplace caution:* “same name” boards can ship with different LoRa chips (SX1262 vs SX127x) or PMIC revisions—verify before buying if you care about specific firmware support or sleep current.

---

## B. Microcontrollers that run CircuitPython / MicroPython (mix-and-match path)

| MCU/Board family | Pros | Cons | Typical price (USD) | Info |
|---|---|---|---:|---|
| ESP32 / ESP32-S3 dev boards | Cheap, abundant, lots of peripherals; strong community; **MicroPython is widely supported** | Deep sleep depends heavily on board design; **CircuitPython is strongest on specific supported boards/ports**, not every generic dev board | $4–$20 | https://www.espressif.com/ |
| RP2040 boards (Raspberry Pi Pico + compatibles) | Great value; lots of MicroPython/CircuitPython tutorials | Needs external radio; power/sleep story differs by board (no single “standard” deep sleep across all designs) | $4–$12 | https://www.raspberrypi.com/products/raspberry-pi-pico/ |
| nRF52 boards (e.g., nRF52840) | Very low power; great BLE; CircuitPython-friendly (many boards) | Not a LoRa MCU; LoRa must be external; boards can cost more | $15–$35 | https://www.nordicsemi.com/ |
| SAMD21/SAMD51 (Adafruit Feather, etc.) | Excellent CircuitPython support; good docs | Less compute than ESP32; external LoRa needed | $10–$30 | https://www.adafruit.com/ |

---

## C. LoRa radio modules (for mix-and-match)

| Module / chip | Notes | Typical price (USD) | Info |
|---|---|---:|---|
| Semtech SX1262-based modules | Newer generation; common in newer boards | $6–$20 | https://www.semtech.com/ |
| Semtech SX1276/78-based modules | Older but widespread; lots of libraries | $4–$15 | https://www.semtech.com/ |
| HopeRF RFM95/96/98 family (SX127x based) | Very popular small modules; widely supported in Arduino/CircuitPython ecosystems | $6–$15 | https://www.hoperf.com/ |
| Ebyte LoRa modules | Many form factors; common on marketplaces; check pinout carefully | $4–$20 | https://www.ebyte.com/ |

*Integration notes:*
- Ensure **SPI** compatibility (most LoRa modules are SPI).
- Budget pins for **NSS/CS, RST, DIO/IRQ**, plus SPI.
- Confirm the module is for your **band** (e.g., 868 vs 915 MHz).

---

## D. Small display options

| Display type | Pros | Cons | Typical price (USD) | Info |
|---|---|---|---:|---|
| 0.96"–1.3" OLED (SSD1306/SH1106) | Cheap, easy I2C; great libraries | Not as sunlight-readable; continuous draw when on | $2–$10 | SSD1306 overview: https://learn.adafruit.com/monochrome-oled-breakouts |
| Small TFT LCD (ST7735/ST7789) | Color; crisp UI | Higher power; backlight dominates | $5–$20 | Adafruit TFTs: https://www.adafruit.com/category/63 |
| Small e-ink/e-paper | Best sunlight readability; ultra-low power when static | Slower refresh; more expensive; more complex | $10–$35 | Waveshare e-paper: https://www.waveshare.com/ |

---

## E. Power options (battery + charging)

| Option | Pros | Cons | Typical price (USD) | Info |
|---|---|---|---:|---|
| 1S LiPo + charger (USB) | Common, compact; rechargeable | Must manage safety; charger + protection matters | $5–$20 | MCP73831 overview: https://ww1.microchip.com/downloads/en/DeviceDoc/20001984g.pdf |
| Li-ion 18650 + holder + charger | Cheap cells; high capacity | Larger; mechanical complexity | $5–$20 (plus cell) | Battery basics: https://learn.adafruit.com/li-ion-and-lipoly-batteries |
| AA/AAA alkaline/NiMH | Easy field replacement | Voltage regulation complexity; bulkier | $2–$10 | — |
| Solar + LiPo charge controller | Long-lived deployments | More parts; weatherproofing | $15–$50 | Adafruit solar charging: https://learn.adafruit.com/adafruit-solar-charging-battery-pack |

*Power budget tip:* a “low power” MCU can still drain fast if the board includes a hungry regulator, power LED, or USB-UART that never sleeps.

---

## Reference builds (“recipes”)

### 1) Fastest Meshtastic node (minimal wiring)
- **Board:** ESP32 + LoRa “all-in-one” (Heltec/LilyGO/RAK class)
- **Display:** built-in OLED (if present)
- **Power:** onboard LiPo charging (if available) or external charger board
- **Estimated total:** $20–$45
- **Why:** quickest route to a functioning mesh node with the fewest integration surprises.

### 2) Cheapest workable DIY node (mix-and-match)
- **MCU:** RP2040 or low-cost ESP32 dev board
- **LoRa module:** SX127x/RFM95 class
- **Display:** 0.96" I2C OLED
- **Power:** basic LiPo + charger
- **Estimated total:** $15–$35
- **Why:** parts are extremely common; great for learning and iteration.

### 3) Best outdoors readability + low idle draw (screen-centric)
- **MCU:** carefully selected low-sleep-current board (often ESP32-class for Meshtastic today; board power design matters as much as the MCU)
- **LoRa module:** SX1262 module (or all-in-one board that includes SX1262)
- **Display:** small e-ink
- **Power:** LiPo with efficient regulator
- **Estimated total:** $30–$70
- **Why:** e-ink can be visible in sunlight with near-zero power when static.

### 4) Smallest practical build
- **MCU:** compact board (SAMD21/QT Py class or small ESP32)
- **LoRa:** compact module with u.FL
- **Display:** 0.91" OLED or no screen (LED + phone UI)
- **Estimated total:** $20–$50
- **Why:** when size matters more than UI richness.

---

## Pitfalls & gotchas (common ways builds fail)
- **Wrong frequency band** (EU868 vs US915) → you may “hear nothing”.
- **Bad antenna setup**: no antenna, wrong connector, poor ground, or indoor-only test conditions.
- **Power surprises**: TFT backlights, GPS modules, and always-on LEDs kill battery life.
- **“Deep sleep” not deep**: USB-UART chips/regulators can dominate standby draw.
- **Voltage mismatch**: 5V logic into 3.3V radio pins can damage modules.

---

## Alternatives corner (brief)
If LoRa/Meshtastic parts are unavailable or your use case is short-range:
- **Wi‑Fi mesh**: higher throughput, higher power, depends on Wi‑Fi radios and topology.
- **BLE mesh**: phone-friendly, short range.
- **Thread / 802.15.4**: strong IoT ecosystem; different tooling and often not “long-range” like LoRa.

---

## Suggested next step
After selecting a reference build, the next deliverable can be a **build guide** (wiring + firmware flashing + enclosure/power notes) tailored to the chosen parts.
