# Agent 32 — Autonomy for ESP32 Devices
![Toot Toot Engineering](images/time-foundry.svg)
[TTE is free, open-source software licensed under the MIT License.](https://antfriend.github.io/)   
![Release](https://img.shields.io/github/v/release/antfriend/toot-toot-engineering)

Workflow version: 3.8

# What is Agent 32?

Agent 32 is a framework for building autonomous ESP32 devices that reason and act without cloud connectivity or neural network inference. The device's "intelligence" lives entirely in a TTDB file stored in flash or on an SD card. Sensor inputs map to TTDB coordinates; typed edges drive action; the agent loop runs continuously at whatever interval the deployment requires.

No LLMs. No matrices. No cloud. Just a $5 microcontroller reading a text file.

# How to use

1. Set up a PlatformIO project for your ESP32 board

2. Add the TTDB files from this repo to your project's `RFCs/` directory per [A32-RFC-0004](RFCs/A32-RFC-0004-Claude-Code-Setup.md)

3. Author a TTDB file in `data/ttdb.md` — see [README_TTDB](README_TTDB.md) for format. Map your sensor axes to lat/lon coordinates in the `mmpdb` umwelt block

4. Implement the firmware sketch using the three-layer architecture:
   - **TTDB Layer** — parses and queries the TTDB file (LittleFS or SD)
   - **Agent Layer** — runs the sense-reason-act loop
   - **Hardware Layer** — registers sensors and actuators

```cpp
#include <TTDB.h>
#include <Agent32.h>

TTDB db;
Agent32 agent(&db);

void setup() {
    LittleFS.begin(true);
    db.begin("/ttdb.md");
    agent.registerSensor(&mySensor);
    agent.registerActuator(&myActuator);
}

void loop() {
    agent.sense();
    agent.reason();
    agent.act();
    delay(agent.intervalMs());
}
```

5. Upload the TTDB file to flash: `pio run --target uploadfs`

6. Flash the firmware and open the serial monitor to verify the agent loop is running

# RFCs

| RFC | Topic |
|-----|-------|
| [A32-RFC-0001](RFCs/A32-RFC-0001-Architecture.md) | Architecture overview, design principles, system layers |
| [A32-RFC-0002](RFCs/A32-RFC-0002-TTDB-Storage.md) | TTDB storage and parsing on ESP32 (LittleFS, streaming parser, index) |
| [A32-RFC-0002 Amendment A](RFCs/A32-RFC-0002-Amendment-A-TBEW.md) | C++ implementation of TBEW epistemic weight fields |
| [A32-RFC-0003](RFCs/A32-RFC-0003-Agent-Loop.md) | Agent loop and hardware abstraction (sense-reason-act, sensor/actuator registry) |
| [A32-RFC-0004](RFCs/A32-RFC-0004-Claude-Code-Setup.md) | Claude Code project setup, CLAUDE.md reference, PlatformIO config |
