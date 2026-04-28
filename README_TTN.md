# Toot Toot Network (TTN)
![Toot Toot Engineering](images/time-foundry.svg)
[TTE is free, open-source software licensed under the MIT License.](https://antfriend.github.io/)   
![Release](https://img.shields.io/github/v/release/antfriend/toot-toot-engineering)

Workflow version: 3.8

# What is TTN?

The Toot Toot Network is an offline-first semantic mesh — a protocol for nodes that exchange meaning, not just bytes. Each node maintains a local TTDB, assigns cryptographic Node IDs, emits typed Semantic Events, and routes through whatever transport is available: LoRa, Wi-Fi, serial, or anything else. No cloud dependency. No central authority.

Core principles:
- **Meaning over messages** — events carry semantic intent, not raw payloads
- **Offline-first and partition-tolerant** — nodes operate independently and sync opportunistically
- **Local sovereignty** — each node owns its data; no server required
- **Transport agnostic** — LoRa, Wi-Fi, serial, BLE — TTN doesn't care
- **Explicit AI invocation only** — AI participates only when a node deliberately asks

# Compliance Levels

| Level | Description |
|-------|-------------|
| TTN-Base | Node ID, local TTDB, presence events, compact mesh grammar |
| TTN-BBS | Bulletin board — threads, replies, moderation |
| TTN-AI | AI-assisted summarization and flagging via explicit invocation |
| TTN-Gateway | Bridges between transport layers (e.g., LoRa ↔ Wi-Fi) |

# How to use

1. Generate a stable Node ID (cryptographic, stored in TTDB)
2. Initialize a local TTDB file for event storage
3. Emit a presence event on startup using TTAI join/welcome behavior
4. Exchange Semantic Events with nearby nodes using compact mesh grammar
5. Assign typed edges to relate events — see TTN-RFC-0002 for the full taxonomy
6. For LoRa links without Meshtastic, use the minimal framing in TTN-RFC-0006

# RFCs

| RFC | Topic |
|-----|-------|
| [TTN-RFC-0001](RFCs/TTN-RFC-0001.md) | Core semantic mesh specification, principles, compliance levels, etiquette |
| [TTN-RFC-0002](RFCs/TTN-RFC-0002-Typed-Edges.md) | Typed edge taxonomy (identity, conversation, AI semantics, trust) |
| [TTN-RFC-0003](RFCs/TTN-RFC-0003-Reference-Implementation.md) | Reference implementation checklist — minimal viable node requirements |
| [TTN-RFC-0004](RFCs/TTN-RFC-0004-Semantic-Compression.md) | Semantic compression and token dictionary |
| [TTN-RFC-0005](RFCs/TTN-RFC-0005-Trust-and-Reputation.md) | Trust and reputation signals |
| [TTN-RFC-0006](RFCs/TTN-RFC-0006-LoRa-Packet-Framing.md) | Minimal LoRa packet framing for non-Meshtastic nodes |
