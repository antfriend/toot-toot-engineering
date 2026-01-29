# LOG

## Entries
- Step: 1
- Role: Bootstrap
- Summary: Interpreted cycle-01 prompt; selected UDP (unicast + multicast) as the single transport; proposed repo layout, team roles, objectives, and plan adjustments; provided three grounded next-cycle prompt options.
- Decisions: Use UDP for direct + group messaging; prefer multicast group address with optional peer-fanout fallback; SVG engineer not required for this cycle.
- Open questions: Confirm multicast support on target device networks; decide config format (.env vs .json) for easiest non-expert editing.
- Next step: Storyteller produces deliverables/cycle-01/STORYTELLER.md

- Step: 2
- Role: Storyteller
- Summary: Defined the user-facing narrative and happy-path demo for the 3-node TTN: simple config-driven nodes, direct + group messaging, clear naming/IP guidance, and log-driven confirmation of message flow.
- Decisions: Use approachable “broadcast to group” wording while implementing via UDP multicast; keep the first demo deterministic (A→B, B→A, C→all).
- Open questions: None blocking; orchestrator should decide the exact CLI entrypoints and config file format.
- Next step: Orchestrator bootstraps the repo and sets the plan.

- Step: 4
- Role: Orchestrator
- Summary: Skipped SVG engineer step as non-applicable; created repo skeleton for a minimal UDP-based TTN (ttn/ package, config examples, demo helper script); updated top-level README with schema, configuration, and run steps; confirmed CLI can send a direct message.
- Decisions: Use .env-style config files under config/; implement “broadcast” via UDP multicast with peer-fanout fallback to NODE_PEERS.
- Open questions: Validate multicast receive behavior across OS/device targets; decide whether to keep a single NODE_PORT for all nodes vs per-node ports.
- Next step: Core worker produces primary solution assets (cycle-01).

- Step: 5
- Role: Core worker
- Summary: Implemented the minimal TTN node runtime and supporting modules (config loader, message schema, UDP transport) plus example configs and a demo helper script; added a cycle solution summary document.
- Decisions: Keep implementation dependency-free; provide multicast broadcast with a peer-fanout fallback; use `.env` config format for simple editing.
- Open questions: Perform real multi-host test on an actual LAN to confirm multicast behavior and firewall requirements.
- Next step: Reviewer checks for correctness and gaps (cycle-01).

- Step: 6
- Role: Reviewer
- Summary: Verified prompt coverage; identified and fixed multicast receive port mismatch by updating listener to listen on both NODE_PORT and GROUP_PORT; updated review notes accordingly.
- Decisions: Keep separate NODE_PORT and GROUP_PORT supported; use select-based two-socket approach to avoid extra dependencies.
- Open questions: None blocking.
- Next step: Delivery packager assembles final assets and export notes (cycle-01).

- Step: 7
- Role: Delivery packager
- Summary: Assembled delivery notes in deliverables/cycle-01/DELIVERY.md and updated RELEASES.md with cycle-01 artifacts.
- Decisions: Keep delivery instructions focused on the happy path with ports/firewall/multicast notes as export considerations.
- Open questions: None.
- Next step: Retrospective recommends improvements and Bootstrap resets plan/prompt for next cycle.

- Step: 8
- Role: Retrospective + Bootstrap
- Summary: Added retrospective and next-cycle prompts to deliverables/cycle-01/BOOTSTRAP.md; marked cycle-01 status complete in RELEASES.md.
- Decisions: Recommend adding an automated demo harness and clearer multicast capability signaling next cycle.
- Open questions: Human: choose one of the three proposed cycle-02 prompts in BOOTSTRAP.md.
- Next step: Human feedback / select cycle-02 prompt.

- Step: 9
- Role: Bootstrap
- Summary: Interpreted cycle-02 hardening prompt; set objectives for structured logging, clearer CLI UX, and explicit multicast fallback visibility.
- Decisions: Add a small logging utility; introduce an info subcommand for config visibility; keep stdout logging dependency-free.
- Open questions: None blocking.
- Next step: Storyteller produces deliverables/cycle-02/STORYTELLER.md

- Step: 10
- Role: Storyteller
- Summary: Defined the UX narrative for explicit event logging, multicast visibility, and consistent CLI output.
- Decisions: Use named events (tx/rx/multicast_failed) to keep logs machine-friendly and readable.
- Open questions: None.
- Next step: Orchestrator updates PLAN/LOG scaffolding for cycle-02.

- Step: 11
- Role: Orchestrator
- Summary: Updated plan and logging scaffolding for cycle-02; prepared paths for new deliverables.
- Decisions: Keep roles consistent; skip SVG engineer.
- Open questions: None.
- Next step: Core worker implements CLI/logging hardening.

- Step: 12
- Role: Core worker
- Summary: Added structured logging, log-level controls, multicast join visibility, and improved CLI (info subcommand); updated docs.
- Decisions: Keep logging stdout-based; emit JSON on demand; surface multicast failure before fallback.
- Open questions: Consider automated demo harness in a future cycle.
- Next step: Reviewer validates cycle-02 requirements.

- Step: 13
- Role: Reviewer
- Summary: Verified CLI UX improvements, structured logging, and explicit multicast fallback behavior; no dependency regressions.
- Decisions: Keep runtime dependency-free.
- Open questions: None.
- Next step: Delivery packager assembles cycle-02 release notes.

- Step: 14
- Role: Delivery packager
- Summary: Packaged cycle-02 deliverables and updated release notes.
- Decisions: Highlight structured logging and multicast visibility in delivery notes.
- Open questions: None.
- Next step: Retrospective recommends next-cycle prompts.

- Step: 15
- Role: Retrospective
- Summary: Documented cycle-02 learnings and proposed device-targeting, observability, and automation prompts.
- Decisions: Recommend device-targeting as the next priority.
- Open questions: None.
- Next step: Bootstrap cycle-03.

- Step: 16
- Role: Bootstrap
- Summary: Interpreted cycle-03 device-targeting prompt; planned device guides and MicroPython reference implementation.
- Decisions: Add docs/DEVICE_GUIDES.md and ttn_mpy/ without altering CPython runtime.
- Open questions: None.
- Next step: Storyteller produces deliverables/cycle-03/STORYTELLER.md

- Step: 17
- Role: Storyteller
- Summary: Framed device guidance as a consistent, schema-preserving story across CPython and MicroPython.
- Decisions: Emphasize config-first setup and schema consistency.
- Open questions: None.
- Next step: Orchestrator updates PLAN/LOG scaffolding for cycle-03.

- Step: 18
- Role: Orchestrator
- Summary: Updated plan and logging scaffolding for cycle-03; prepared new deliverable paths.
- Decisions: Keep roles consistent; skip SVG engineer.
- Open questions: None.
- Next step: Core worker implements device guides and MicroPython reference.

- Step: 19
- Role: Core worker
- Summary: Added device-specific guides and MicroPython-friendly reference implementation; updated README pointers.
- Decisions: Provide MicroPython implementation in separate ttn_mpy/ folder to avoid CPython changes.
- Open questions: None.
- Next step: Reviewer validates device guidance and schema consistency.

- Step: 20
- Role: Reviewer
- Summary: Verified device guides and MicroPython reference align with TTN schema and prompt requirements.
- Decisions: Keep guidance assumption-based with explicit notes.
- Open questions: None.
- Next step: Delivery packager assembles cycle-03 release notes.

- Step: 21
- Role: Delivery packager
- Summary: Packaged cycle-03 deliverables and updated release notes.
- Decisions: Highlight MicroPython reference and device guides.
- Open questions: None.
- Next step: Retrospective recommends next-cycle prompts.

- Step: 22
- Role: Retrospective
- Summary: Documented cycle-03 learnings; proposed observability, automation, and interop testing prompts.
- Decisions: Recommend observability as the next priority.
- Open questions: None.
- Next step: Bootstrap cycle-04.

- Step: 23
- Role: Bootstrap
- Summary: Interpreted cycle-04 observability prompt; planned monitor module and export option.
- Decisions: Implement monitor as a lightweight module and CLI subcommand; reuse logging utilities.
- Open questions: None.
- Next step: Storyteller produces deliverables/cycle-04/STORYTELLER.md

- Step: 24
- Role: Storyteller
- Summary: Framed monitor as a control-tower view of group traffic with periodic summaries and optional exports.
- Decisions: Avoid terminal UI dependencies; keep summary heartbeat.
- Open questions: None.
- Next step: Orchestrator updates PLAN/LOG scaffolding for cycle-04.

- Step: 25
- Role: Orchestrator
- Summary: Updated plan and logging scaffolding for cycle-04; prepared new deliverable paths.
- Decisions: Keep roles consistent; skip SVG engineer.
- Open questions: None.
- Next step: Core worker implements monitor.

- Step: 26
- Role: Core worker
- Summary: Implemented monitor module, wired CLI subcommand, and updated README usage.
- Decisions: Use periodic summaries and optional JSON-lines export to avoid dependencies.
- Open questions: None.
- Next step: Reviewer validates monitor behavior.

- Step: 27
- Role: Reviewer
- Summary: Verified monitor functionality, export behavior, and documentation updates.
- Decisions: Accept monitor scope limited to group traffic.
- Open questions: None.
- Next step: Delivery packager assembles cycle-04 release notes.

- Step: 28
- Role: Delivery packager
- Summary: Packaged cycle-04 deliverables and updated release notes.
- Decisions: Highlight monitor usage and export format in delivery notes.
- Open questions: None.
- Next step: Retrospective finalizes cycle-04.

- Step: 29
- Role: Retrospective
- Summary: Documented cycle-04 learnings and proposed automation, interop testing, and diagnostics prompts.
- Decisions: Recommend automation as the next priority.
- Open questions: None.
- Next step: Human selects next-cycle prompt.
