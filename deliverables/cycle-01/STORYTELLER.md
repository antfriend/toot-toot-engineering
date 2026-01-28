# STORYTELLER (cycle-01)

## The story we’re telling (to the user)
You have three machines on one local network. Each machine is a **node** with a **friendly name** and a **fixed address**. Once configured, the nodes can speak in two modes:

1. **Direct**: “Send this message to *that* node.”
2. **Group**: “Tell everyone in the workshop.”

Every message is a small JSON envelope (the **TTN message**) that carries:
- who spoke (`from_name`, `from_ip`)
- who should hear it (`to` = a node name or `broadcast`)
- when it happened (`ts`)
- what was said (`text`)

The system is intentionally humble: one transport (UDP), one schema (JSON), one happy-path demo (A→B, B→A, C→all). This keeps the first build understandable and runnable by non-experts.

## Naming + UX narrative
We lean into simple, memorable node identities:
- **Node A**: `node-a` (Unihiker K10)
- **Node B**: `node-b` (Lilygo T-Deck Plus)
- **Node C**: `node-c` (Windows 11 PC)

Users should be able to:
- open a config file
- set the name and network values
- run `python -m ttn.node --config config/node_a.env`
- see logs like:
  - `RX direct from node-a: "Hello"`
  - `RX broadcast from node-c: "Status check"`

## The “happy path” demo scenario (must be easy)
A good demo is short, deterministic, and visibly confirms delivery.

**Scene:** Three nodes start listening.
1. Node A sends a direct message to Node B: “Hello node-b”
2. Node B replies to Node A: “Hi node-a”
3. Node C broadcasts: “Hello everyone”
4. All nodes print receipts with msg_id + from + to + text.

The user should experience this as: *“I started three listeners; I fired three commands; I saw the receipts; it worked.”*

## Key clarity points for non-experts
### Node name
- Pick any short unique label, lowercase with dashes is easiest.
- Names are used for human readability and for `to` addressing.

### Node IP
- Prefer **DHCP reservation** (router assigns the same IP each time) or set a static IP.
- Every node needs a stable IP so peers can reach it.

### Ports
- All nodes can use the same listening port (e.g., `5005`) unless a device requires otherwise.
- Group traffic uses one group IP/port shared by all.

## Multicast vs “broadcast” wording
We can say “broadcast to the group” in the user-facing docs, while implementing it via **UDP multicast** on a configured `GROUP_IP`.
- In the story: it’s “broadcast.”
- In the engineering: it’s “multicast group send.”

## Suggested documentation tone for README
- Start with a one-paragraph promise: “In 10 minutes you’ll have 3 nodes chatting.”
- Then a numbered checklist: configure names/IPs → start nodes → send direct → send group.
- Put troubleshooting (firewall, multicast) after the demo so momentum stays high.

## Acceptance test (narrative)
If a user can copy-paste the commands and see:
- Node B logs A’s direct message
- Node A logs B’s reply
- All three log C’s broadcast
…then the story lands.
