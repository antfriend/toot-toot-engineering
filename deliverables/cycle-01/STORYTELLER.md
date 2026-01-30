# STORYTELLER (cycle-01)

## The creative thread: “Three nodes in a workshop”
This TTN build is framed as a small workshop network where three devices learn each other’s names, announce presence, and pass short notes across the room.

- **Node A (Unihiker K10)** is the bench instrument: small, hands-on, meant to be carried.
- **Node B (Lilygo T-Deck Plus)** is the pocket terminal: quick replies, fast iteration.
- **Node C (Windows 11 PC)** is the workbench: stable, visible logs, easy tooling.

The user experience goal is to make the network feel **human-scale**:
1. Pick a name.
2. Give it an address.
3. Start the node.
4. Speak directly, or speak to the whole room.

## Narrative requirements translated into documentation requirements
To keep the system “non-expert friendly”, the docs should:
- Explain *what a node is* (a small program that listens on a port).
- Explain *what direct vs broadcast means* using a concrete example.
- Treat configuration as a “label + address + mailbox”.

## Naming and identity tone
Use consistent terminology:
- **Node name**: friendly label shown in logs and messages (e.g., `node-alpha`).
- **Node IP/port**: where the node listens.
- **Group IP/port**: where broadcast/multicast messages go.

Encourage names that match stickers a human might put on devices:
- `k10-alpha`, `tdeck-beta`, `pc-charlie`

## Message ritual (demo scenario as a story beat)
We present the demo as a small play:
1. **A → B:** “Can you hear me?”
2. **B → A:** “Loud and clear.”
3. **C → broadcast:** “Workshop check-in: everyone report status.”
4. **All nodes** log what they heard.

This makes the testing sequence memorable and reduces “did it work?” confusion.

## Clarity guardrails (to be enforced by Orchestrator/Core Worker)
- Provide copy/paste-able commands for Windows.
- Provide a “Known pitfalls” section (firewall, wrong subnet, port conflicts).
- If hardware runtimes are uncertain, say so explicitly and provide a Windows-first runnable reference plus porting notes.

## Optional magic (only if time allows)
Add a “presence” message that appears when a node starts:
- Helps users immediately see that the node is alive.
- Supports the workshop metaphor: “I’m here; I’m listening.”

Deliverable intent: This file should guide the Orchestrator and Core Worker to write a TTN_README that feels friendly, concrete, and testable.
