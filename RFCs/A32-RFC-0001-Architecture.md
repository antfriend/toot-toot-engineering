# A32-RFC-0001

## Agent 32 Architecture Overview

### Version 0.1

Status: Draft

This RFC defines the architecture of an Agent 32 application: an autonomous
device built on ESP32 hardware using the Arduino framework, with a
MyMentalPalaceDB (TTDB) file as its onboard knowledge base and decision engine.

---

## 1. Purpose and Scope

Agent 32 is a framework for building autonomous ESP32 devices that reason and
act without cloud connectivity or neural network inference. The "intelligence"
of an Agent 32 device comes entirely from a pre-authored TTDB file stored in
flash or on an SD card. The device reads its TTDB, navigates its knowledge
graph, matches sensor inputs to known nodes, and executes actions defined by
typed edges and record content.

This RFC covers the high-level architecture. Companion RFCs cover the TTDB
storage layer (A32-RFC-0002), the agent loop (A32-RFC-0003), and Claude Code
project setup (A32-RFC-0004).

---

## 2. Design Principles

1. **No cloud dependency.** An Agent 32 device MUST operate fully offline
   once its TTDB is loaded. Wi-Fi and BLE MAY be used for peer communication
   or telemetry, but MUST NOT be required for core reasoning.

2. **TTDB is the model.** All domain knowledge, decision rules, and action
   mappings live in the TTDB file. The firmware is a generic interpreter;
   the TTDB file gives it purpose.

3. **Human-readable knowledge.** TTDB files are Markdown (or LaTeX). A human
   MUST be able to read, audit, and edit the device's knowledge base with a
   text editor. No opaque binary models.

4. **Arduino-first.** Reference implementations target the Arduino framework
   via PlatformIO or the Arduino IDE. ESP-IDF MAY be used for advanced cases,
   but Arduino is the default.

5. **Separation of concerns.** The firmware has three layers:
   - **TTDB Layer** — parses and queries the TTDB file.
   - **Agent Layer** — runs the sense-reason-act loop.
   - **Hardware Layer** — abstracts GPIO, sensors, actuators, and comms.

---

## 3. System Architecture

```
┌─────────────────────────────────────────────────┐
│               Agent 32 Device                   │
│                                                 │
│  ┌───────────┐  ┌───────────┐  ┌─────────────┐ │
│  │  Sensors   │  │ Actuators │  │   Comms     │ │
│  │ (GPIO/I2C/ │  │ (GPIO/PWM/│  │ (WiFi/BLE/  │ │
│  │  SPI/ADC)  │  │  Servo)   │  │  Serial)    │ │
│  └─────┬─────┘  └─────▲─────┘  └──────▲──────┘ │
│        │               │               │        │
│  ┌─────▼───────────────┴───────────────┴──────┐ │
│  │           Hardware Abstraction Layer        │ │
│  └─────────────────────┬──────────────────────┘ │
│                        │                        │
│  ┌─────────────────────▼──────────────────────┐ │
│  │              Agent Loop                     │ │
│  │  ┌────────┐  ┌─────────┐  ┌──────────┐    │ │
│  │  │ Sense  ├──▶ Reason  ├──▶  Act      │    │ │
│  │  └────────┘  └────┬────┘  └──────────┘    │ │
│  │                   │                        │ │
│  └───────────────────┼────────────────────────┘ │
│                      │                          │
│  ┌───────────────────▼────────────────────────┐ │
│  │             TTDB Layer                      │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐ │ │
│  │  │  Parser  │  │  Cursor  │  │ Librarian│ │ │
│  │  └──────────┘  └──────────┘  └──────────┘ │ │
│  └────────────────────┬───────────────────────┘ │
│                       │                         │
│  ┌────────────────────▼───────────────────────┐ │
│  │         TTDB File (flash or SD)            │ │
│  └────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

---

## 4. Hardware Requirements

### 4.1 Minimum Target

- ESP32-S3 with 8 MB flash and 2 MB+ PSRAM (recommended).
- ESP32-WROOM with 4 MB flash is supported for small TTDB files.

### 4.2 Storage

- TTDB files under 512 KB SHOULD be stored in SPIFFS or LittleFS on flash.
- TTDB files over 512 KB SHOULD use an SD card via SPI.
- Implementations MUST support LittleFS. SD card support is OPTIONAL.

### 4.3 Peripherals

Agent 32 does not prescribe specific sensors or actuators. The Hardware
Abstraction Layer (see A32-RFC-0003) provides a registration mechanism
for arbitrary GPIO, I2C, SPI, and analog peripherals.

---

## 5. TTDB Integration

The TTDB file is the sole knowledge source. At boot, the firmware:

1. Mounts the filesystem (LittleFS or SD).
2. Opens the TTDB file and parses the `mmpdb` header block.
3. Validates `db_id` and `umwelt` fields.
4. Initializes the cursor at the configured starting node.
5. If a `librarian` is enabled, loads the primitive query table.

The Agent Loop then uses the TTDB Layer to navigate records, follow typed
edges, and match sensor readings to node coordinates.

---

## 6. Umwelt as Device Identity

Each Agent 32 device operates within the umwelt defined by its TTDB file.
The umwelt constrains what the device "knows" and how it interprets inputs.
Two devices with identical hardware but different TTDB files will behave
differently because they have different umwelts.

This is intentional and central to the framework. The umwelt concept from
TTDB-RFC-0001 maps directly to device personality and capability.

---

## 7. Compatibility with Toot Toot Engineering

Agent 32 projects SHOULD use the TTE workflow (WORKFLOW.md, PLAN.md,
CHECKLIST.md, etc.) for development. The TTDB file that ships on the
device is authored and maintained using TTE conventions.

Claude Code projects for Agent 32 SHOULD include:
- `CLAUDE.md` or `AGENTS.md` with Agent 32-specific guidance.
- The TTE workflow files at the repo root.
- The TTDB file(s) in a `data/` directory.

---

## 8. Non-Goals

- Agent 32 does NOT include LLM inference, cloud AI APIs, or neural networks.
- Agent 32 does NOT define a messaging protocol (Telegram, MQTT, etc.),
  though implementations MAY add one.
- Agent 32 does NOT prescribe a specific UI. Devices MAY be headless.

---

End A32-RFC-0001
