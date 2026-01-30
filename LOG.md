# LOG

## Entries
- Step: 1
- Role: Bootstrap
- Summary: Interpreted the cycle-01 prompt (3-node TTN messaging over IP) and produced a transport recommendation, team composition, plan adjustments, risks, and next-cycle prompt suggestions.
- Decisions: Chose UDP as the simplest single transport; recommend multicast (preferred) with broadcast fallback; include lightweight presence/hello to align with TTN reference checklist without implementing full semantic mesh.
- Open questions: Exact runtime stacks on Unihiker K10 and Lilygo T-Deck Plus (CPython vs MicroPython); multicast support on target LAN; router-specific steps for DHCP reservation.
- Next step: Storyteller

- Step: 2
- Role: Storyteller
- Summary: Defined a human-scale “three nodes in a workshop” narrative thread to guide TTN_README tone, terminology, and demo flow; recommended a simple presence ritual and clear non-expert guardrails.
- Decisions: Use consistent terms (node name, node IP/port, group IP/port); present demo as a memorable 3-beat exchange.
- Open questions: Whether to implement presence as a dedicated message type or reuse the standard text message with a reserved `to` value.
- Next step: Orchestrator

- Step: 4
- Role: Orchestrator
- Summary: Created a concrete cycle-01 repo layout plan and added an Orchestrator artifact; marked the optional SVG step as skipped; advanced PLAN to Core worker.
- Decisions: Keep implementation stdlib-only Python 3.10; JSON config per node under `deliverables/cycle-01/config/`; include demo script that can simulate all three nodes locally.
- Open questions: Final choice of multicast vs broadcast default; whether to add `msg_type` to schema for presence.
- Next step: Core worker

- Step: 5
- Role: Core worker
- Summary: Implemented a minimal UDP-based TTN reference node (direct + group), JSON config loader, message schema helpers, CLI runner, example per-node configs, a 3-node demo script, end-user TTN_README, and created the requested zip bundle.
- Decisions: Implemented multicast group messaging by default with a documented broadcast fallback; added optional `msg_type` to support presence without changing required schema fields; kept dependencies stdlib-only.
- Open questions: Multicast/broadcast behavior and firewall rules on some Wi‑Fi networks; best runtime path for Unihiker K10 / T-Deck Plus (CPython vs MicroPython).
- Next step: Reviewer

- Step: 6
- Role: Reviewer
- Summary: Verified prompt coverage and reviewed protocol/implementation; identified and fixed a potential group-port misconfiguration by enforcing a single-port design (GROUP_PORT == NODE_PORT), updated configs and documentation, and noted multicast limitations on some environments.
- Decisions: Prefer single-port UDP design for simplicity and reduced OS variance.
- Open questions: Confirm multicast works on target LAN; otherwise instruct users to use broadcast mode.
- Next step: Delivery packager

- Step: 7
- Role: Delivery packager
- Summary: Assembled delivery notes, ensured zip bundle exists, and updated RELEASES.md with cycle-01 deliverables.
- Decisions: Marked zip and TTN_README as primary artifacts; kept status in progress pending retrospective completion.
- Open questions: None.
- Next step: Retrospective
