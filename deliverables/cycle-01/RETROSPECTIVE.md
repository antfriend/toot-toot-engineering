# RETROSPECTIVE (cycle-01)

## What worked
- Clear critical path: Bootstrap → Story → Build → Review → Package.
- Deliverables are tangible (code + db + docs + tools), not just planning docs.
- The transport abstraction is simple enough to later support non-TCP links.

## What didn’t / risks observed
- Platform uncertainty (UNIHIKER K10 MicroPython APIs for Wi‑Fi + screen output) is the largest execution risk.
- Concurrency requirement isn’t met yet; “multiple sessions may exist concurrently” needs a concrete implementation choice.
- Message ID allocation is not MMPDB-faithful yet and could collide.

## Recommended workflow/plan changes
1) Add a **hardware validation checkpoint** before marking a cycle “complete” in `RELEASES.md`:
   - Confirm Wi‑Fi AP mode works (or document exact alternative).
   - Confirm a real client can connect and interact.
2) Add an explicit **Embedded Compatibility** mini-step (or checklist item) in Core worker:
   - list required MicroPython modules present/absent (`network`, `usocket`, `_thread`, `select`).
3) Promote a reusable **protocol framing spec** into `standards/` once stabilized.

## Bootstrap offer: implement recommendations
If approved, the next cycle can:
- implement concurrency via `select` or `_thread`,
- implement a meta-node-backed MMPDB-ish ID allocator,
- tighten canonical `in_area>@AREA_ID` use for listing.

## Next-cycle prompt candidates (choose 1)

1) **Concurrency + resilience upgrade**
   - Implement multi-session support on MicroPython using `select` (preferred) or `_thread` fallback.
   - Add session timeouts and safe disconnect handling.
   - Update docs with tested concurrency limits.

2) **MMPDB-faithful storage + ID allocator**
   - Add `@META` node storing next coordinates and collision policy.
   - Make all messages use canonical `in_area>@AREA_ID`, `thread_root`, `reply_to` edges.
   - Add compacting/cleanup tool (PC-side) to reduce file size.

3) **Meshtastic-class transport simulation**
   - Add a simulated transport with MTU <= 200 bytes and seconds-latency.
   - Ensure protocol output chunking is always under MTU.
   - Demonstrate store-and-forward delivery of posted messages.
