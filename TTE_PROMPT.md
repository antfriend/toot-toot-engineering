# TTN 3-Node Messaging Network 

Design a minimal, complete system that builds a **simple 3-node TTN** where devices can:
- Send direct messages to each other.
- Broadcast to the whole group.
- Use end-user configured **node name** and **IP address**.
- Provide clear instructions for users to configure those values.
- For technical clarifications, refer to the RFCs in the `RFCs/` folder.

This version targets a **3-node IP network** plus an optional Windows 11 host for tooling:
- **Node A:** Unihiker K10
- **Node B:** Lilygo T-Deck Plus
- **Node C:** Windows 11 PC
- **Optional host:** Windows 11 PC for simulation, testing, or monitoring

No Meshtastic, no LoRa, no radio-specific requirements.

---

## High-Level Goal
Build a **simple TTN** where:

**Node message** → **TTN message format** → **direct or broadcast delivery** → **group receipt**

The system must be easy to run locally on a single subnet and easy to configure by non-experts.

---

## Network Topology (Must Build)
1. All three nodes are on the same IP network.
2. Each node has:
   - A user-configured **display name**
   - A user-configured **static IP address** (or a reserved DHCP lease)
3. Nodes send messages over the network using a **single transport** (choose one):
   - UDP (simplest, no broker)
   - TCP (simple, direct)
   - MQTT (if a broker is used)

Pick one transport and keep it consistent across all nodes.

---

## User Configuration (Must Include)
Each node must expose a simple config file (or environment variables) with:
- `NODE_NAME` (user-friendly display name)
- `NODE_IP` (the node's own IP address)
- `NODE_PORT` (port to listen on)
- `GROUP_IP` and `GROUP_PORT` (for broadcast or group messaging)
- `NODE_PEERS` (list of the other node IPs, if direct messaging is needed)

Provide clear, step-by-step instructions that explain:
1. How to pick and set a unique `NODE_NAME`.
2. How to assign or reserve a static IP address.
3. How to edit the config file.
4. How to start each node.
5. How to test direct and broadcast messages.

---

## Deliverables
Produce a repo-style project with:
1. `TTN_README.md` that includes:
   - Network setup requirements
   - Step-by-step configuration for each node
   - How to run the nodes
   - How to send direct and broadcast messages
2. A minimal runnable implementation for the 3 nodes
3. A simple message format spec (TTN message schema)
4. A demo script that:
   - Starts or simulates 3 nodes
   - Sends direct messages between nodes
   - Broadcasts to the group
5. Optional: a lightweight monitor view or log output to confirm message flow

Use **Python 3.10** as the default implementation language unless a smaller, clearer option is better for the target devices.

---

## Minimal Message Format (TTN)
Define a simple JSON message with these fields:
```json
{
  "msg_id": "uuid",
  "from_name": "node-alpha",
  "from_ip": "192.168.1.10",
  "to": "node-beta|broadcast",
  "ts": "2026-01-27T18:14:02Z",
  "text": "Hello team"
}
```

---

## Demo Scenario (Must Generate)
Demonstrate:
- Node A sends a direct message to Node B
- Node B replies to Node A
- Node C sends a broadcast to all nodes
- All nodes log received messages

---

## Constraints
- Keep the system as simple as possible.
- Avoid unnecessary dependencies.
- No Meshtastic or LoRa references or requirements.
- Provide clear config and run instructions for non-experts.

---

## Output Format Requested From the Agent
Return:
1. Design overview
2. Folder/module layout
3. TTN message schema
4. Transport choice and rationale
5. Configuration instructions for node name and IP address
6. Minimal runnable demo steps

---

## Definition of Done
I can:
- Configure unique names and IPs for three nodes.
- Start all three nodes.
- Send direct messages between any two nodes.
- Broadcast a message that all nodes receive.
