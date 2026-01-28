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
