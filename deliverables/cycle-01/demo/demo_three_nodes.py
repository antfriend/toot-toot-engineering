from __future__ import annotations

import sys
from pathlib import Path
import time

# Ensure imports work when running this file directly.
THIS_DIR = Path(__file__).resolve().parent
CYCLE_ROOT = THIS_DIR.parent
sys.path.insert(0, str(CYCLE_ROOT))

from ttn.config import NodeConfig  # noqa: E402
from ttn.node import TTNNode  # noqa: E402

# Localhost simulation uses three different loopback IPs.
# On most systems, 127.0.0.0/8 is loopback.
# If your OS only supports 127.0.0.1, change NODE_IPs to 127.0.0.1 and use different NODE_PORTs.

CFG_A = NodeConfig(
    node_name="k10-alpha",
    node_ip="127.0.0.2",
    node_port=5005,
    group_mode="multicast",
    group_ip="224.1.1.1",
    group_port=5006,
    node_peers={"tdeck-beta": "127.0.0.3", "pc-charlie": "127.0.0.4"},
)
CFG_B = NodeConfig(
    node_name="tdeck-beta",
    node_ip="127.0.0.3",
    node_port=5005,
    group_mode="multicast",
    group_ip="224.1.1.1",
    group_port=5006,
    node_peers={"k10-alpha": "127.0.0.2", "pc-charlie": "127.0.0.4"},
)
CFG_C = NodeConfig(
    node_name="pc-charlie",
    node_ip="127.0.0.4",
    node_port=5005,
    group_mode="multicast",
    group_ip="224.1.1.1",
    group_port=5006,
    node_peers={"k10-alpha": "127.0.0.2", "tdeck-beta": "127.0.0.3"},
)


def run_node(cfg: NodeConfig):
    def on_rx(rec):
        m = rec.msg
        print(f"[{cfg.node_name}] RX from={m.from_name} to={m.to} ts={m.ts} text={m.text}")

    n = TTNNode(cfg, on_receive=on_rx)
    n.start()
    n.announce_presence()
    return n


def main():
    a = run_node(CFG_A)
    b = run_node(CFG_B)
    c = run_node(CFG_C)

    # Give sockets time to bind and join group
    time.sleep(0.3)

    print("\n--- DEMO: A -> B direct ---")
    a.send_direct(to_name="tdeck-beta", text="Can you hear me?")
    time.sleep(0.3)

    print("\n--- DEMO: B -> A reply ---")
    b.send_direct(to_name="k10-alpha", text="Loud and clear.")
    time.sleep(0.3)

    print("\n--- DEMO: C -> broadcast ---")
    c.send_group(text="Workshop check-in: everyone report status.")
    time.sleep(0.5)

    a.stop(); b.stop(); c.stop()


if __name__ == "__main__":
    main()
