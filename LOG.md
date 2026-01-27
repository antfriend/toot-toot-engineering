# LOG

## Entries
- Step: 1
- Role: Bootstrap
- Summary: Interpreted the project prompt (MicroPython TCP BBS for UNIHIKER K10), defined constraints and success criteria, proposed role/team composition, and recommended plan adjustments (skip SVG engineer; add explicit code/docs/tests artifacts).
- Decisions: Treat deliverable as software + documentation; prioritize transport-agnostic core with narrow I/O interface; use mpdb-lite file for persistence.
- Open questions: Exact UNIHIKER K10 MicroPython firmware details (AP setup specifics, filesystem paths, availability of select/poll).
- Next step: Storyteller produces deliverables/cycle-01/STORYTELLER.md

- Step: 2
- Role: Storyteller
- Summary: Defined the BBS experiential narrative ("modem-era calm"), tone/copy rules, required screens, and protocol UX guidance emphasizing paging, determinism, and low bandwidth.
- Decisions: Keep UI ASCII + short lines; map menu selections to the same line-command protocol; enforce server-driven pagination with a simple MORE gate.
- Open questions: Exact page budget/line limits to tune for typical telnet clients; whether to treat ENTER as implicit MORE.
- Next step: Orchestrator updates PLAN/repo structure to incorporate Bootstrap adjustments and formalize artifacts.

- Step: 3
- Role: Orchestrator
- Summary: Updated PLAN to incorporate Bootstrap adjustments (explicit code/docs/tests outputs; skipped SVG step). Authored initial supporting docs: ARCHITECTURE, PROTOCOL, SETUP, and TESTS for cycle-01.
- Decisions: Keep strict transport boundary; define response frames with SCR/TXT/END and a MORE gate; treat tests as host-side for parsing/serialization.
- Open questions: Finalize message ID generation strategy suitable for MicroPython; decide draft handling policy for interrupted POST.
- Next step: Core worker implements the MicroPython codebase and starter mpdb-lite database.

- Step: 4
- Role: Core worker
- Summary: Implemented the MicroPython TCP BBS MVP codebase (transport-agnostic protocol + TCP adapter + session + mpdb-lite storage + deterministic screens), provided starter mpdb-lite DB, and added host-side unit tests for mpdb-lite and protocol parsing.
- Decisions: Use file-based mpdb-lite persistence; create draft message immediately on POST for recoverability; implement simple line-based body collection for MVP; keep accept loop single-session sequential for simplicity.
- Open questions: Improve POST body handling to accept exact raw bytes (not line-based) to fully match protocol; implement server-driven pagination with MORE gate in protocol layer (currently single-frame responses).
- Next step: Reviewer validates completeness vs prompt, identifies gaps, and proposes fixes.

- Step: 5
- Role: Reviewer
- Summary: Reviewed implementation against prompt; confirmed MVP works but identified key gaps: POST does not yet read exact raw bytes, pagination/MORE gate not implemented, and multi-session concurrency is limited. Provided recommended fixes.
- Decisions: Accept current state as MVP with documented limitations; prioritize documenting gaps and next steps in DELIVERY.
- Open questions: Whether to implement select-based multiplexing on K10 firmware; best approach for exact-byte POST while keeping transport boundary narrow.
- Next step: Delivery packager produces DELIVERY.md and updates RELEASES.md with deliverables.

- Step: 6
- Role: Delivery packager
- Summary: Assembled delivery documentation (DELIVERY.md) including file tree and run instructions; updated RELEASES.md with cycle-01 deliverables and status.
- Decisions: Mark cycle as complete MVP with known gaps documented; keep setup instructions conservative due to device firmware variability.
- Open questions: None blocking; improvements tracked in REVIEW.md.
- Next step: Retrospective step to propose process/plan upgrades for next cycle.

- Step: 7
- Role: Retrospective (Bootstrap)
- Summary: Updated BOOTSTRAP.md with retrospective learnings and proposed next-cycle prompts grounded in delivered MVP (protocol compliance, concurrency, Meshtastic-ready adapter simulation).
- Decisions: Recommend adding explicit protocol-compliance hardening step and on-device constraints audit in future cycles.
- Open questions: Human selection of next-cycle prompt (required to start cycle-02).
- Next step: Human chooses one of the 3 proposed cycle-02 prompts; then Bootstrap can reset PLAN for cycle-02.
