# STORYTELLER (cycle-01)

## Narrative focus
The six-device TTN is a distributed workshop: each node is a specialist, and TTDB is their shared memory. The human operator is the conductor, guiding discovery, message flow, and gradual convergence. The story should read as a field guide: set up the bench, bring each specialist online, watch the network wake up, and prove that memory spreads without a single authority.

## Core story arc
1. **Awakening the workshop**: power on the Windows hub and K10 console; establish the first two “voices.”
2. **Adding the mesh**: bring Heltec nodes and the T-Deck online as radio scouts; show how they announce themselves.
3. **Memory takes shape**: TTDB records are appended everywhere, edges connect observations, and sync diffs begin to circulate.
4. **Convergence**: despite interruptions and power cycles, the network reconstructs the same shared memory over time.
5. **Proof**: acceptance tests demonstrate discovery, resilience, and TTDB integrity.

## Tone and style
- Pragmatic, field-ready, and teachable.
- Emphasize observability and tangible checks: “see it, log it, prove it.”
- Avoid lore; keep the magic in the system’s behavior and the operator’s results.

## Narrative anchors for the guide
- **Roles as characters**: Hub (Archivist), K10 (Operator), Heltecs (Scouts), T-Deck (Scribe).
- **TTDB as memory**: append-only, inspectable, convergent.
- **Edges as meaning**: observations become relationships, not just logs.
- **Diffs as gossip**: no authority, only convergence.

## Suggested section framing
- "Meet the six devices" as a roster with roles and capabilities.
- "How the mesh speaks" (Meshtastic → TTDB mapping).
- "How memory spreads" (diff exchange and compaction).
- "Prove it" (acceptance tests with expected evidence).

## UX narrative beats
- Each device has a simple “hello” moment on first boot.
- The K10 console becomes the operator’s window into the mesh.
- The Windows hub visualizes the growing constellation of nodes.
- Every acceptance test leaves a visible trace in TTDB.
