# cycle-01 STORYTELLER

## The story we are telling (creative thread)
This system isn’t “just a bridge.” It’s a **field narrative machine**: raw radio/IP chatter becomes a legible, queryable sequence of typed events that can be replayed, summarized, and reasoned about.

The core creative thread is:

> **Transport is messy; meaning must be stable.**

So the gateway acts like a careful archivist:
- it preserves the raw message,
- extracts meaning deterministically,
- gives that meaning a stable identity,
- then publishes and stores it so a human (or AI) can follow the trail.

## Cast of characters (nodes)
- **node:tdeck-plus** — the *voice on the mesh*. It speaks short, bandwidth-limited, often ambiguous text.
- **node:unihiker-k10** — the *IP scribe*. It can send richer structured updates over Wi‑Fi, but we constrain it into the same semantic shape.
- **node:esp32-field** — the *quiet sensor*. It emits periodic readings and occasionally an alert.
- **gateway:win11** — the *foundry*. It normalizes, interprets, assigns IDs, publishes, stores, and renders.
- **@AI (librarian)** — the *silent analyst*. It watches everything via MQTT but only speaks on the mesh when explicitly invoked.

## “Day on the mesh” (demo narrative)
A single day provides enough texture to prove the whole pipeline:

### Act I — Morning roll call (presence)
- Each node announces it is alive.
- The gateway records presence and publishes `tte/state/node/<id>`.

**Story trail:** `node -> presence_probe -> node_state`.

### Act II — Routine telemetry (temperature readings)
- Ten temperature readings arrive throughout the day.
- Most are normal; one begins trending high.

**Story trail:** `sensor:temp -> sensor_reading.temperature -> time-series -> drift suspicion`.

### Act III — A threshold is crossed (sensor alert)
- A single reading crosses an alert threshold.
- The event is typed and highlighted.

**Story trail:** `sensor_alert -> (causes) -> logistics_request` (if relevant), or `sensor_alert -> (precedes) -> emergency`.

### Act IV — People move things (logistics request/offer)
- Someone requests supplies or assistance.
- Another node offers help.
- The system links them with typed edges (`requests`, `offers`, `responds_to`).

**Story trail:** `request -> offer -> acknowledgement -> resolution`.

### Act V — Medical emergency + acknowledgement
- A short urgent message triggers a medical emergency event.
- Others acknowledge and coordinate.

**Story trail:** `emergency_medical -> acknowledgements -> status_updates -> resolved`.

### Act VI — Bulletin thread (shared memory)
- A broadcast bulletin is posted.
- Replies form a thread.

**Story trail:** `bulletin_post -> bulletin_reply* -> thread`.

## What “story trails” mean in the monitor
A “story trail” is a path through the graph via typed edges:
- `responds_to`
- `acknowledges`
- `reports_sensor`
- `references`
- `addresses`
- `follows`

The offline monitor should let a human click an event and see:
- upstream: what it’s replying to / acknowledging
- downstream: what it triggered / what replied to it

## Mesh constraints as narrative constraints
Mesh bandwidth limits become a stylistic choice:
- messages are short and coded (`TEMP 17.4`, `HELP MEDICAL`, `@AI summarize 6h`)
- the gateway is where richness is reconstructed (typed events + structured payloads)

## AI librarian: dramatic rule
The librarian is intentionally “mute” unless invoked.
That makes it feel reliable and non-spammy in the field:
- It *listens* constantly (MQTT).
- It *speaks* only when addressed explicitly (`@AI ...`).

In the narrative, this creates a satisfying moment:
- the mesh is chaotic,
- then someone asks `@AI triage`,
- and a compressed, high-signal response appears.

## Acceptance criteria (story-level)
When the demo is run, we should be able to:
1. Follow the day from presence → routine readings → alert → coordination → resolution.
2. See linked threads (bulletin and emergency acknowledgements).
3. Ask the librarian for a summary and get a **mesh-short** answer that references event IDs and key nodes.
