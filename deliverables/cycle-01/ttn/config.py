from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Literal

GroupMode = Literal["multicast", "broadcast"]


@dataclass(frozen=True)
class NodeConfig:
    node_name: str
    node_ip: str
    node_port: int

    group_mode: GroupMode
    group_ip: str
    group_port: int

    # Map peer name -> ip
    node_peers: Dict[str, str]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NodeConfig":
        required = [
            "NODE_NAME",
            "NODE_IP",
            "NODE_PORT",
            "GROUP_MODE",
            "GROUP_IP",
            "GROUP_PORT",
            "NODE_PEERS",
        ]
        missing = [k for k in required if k not in d]
        if missing:
            raise ValueError(f"Missing config keys: {missing}")

        group_mode = d["GROUP_MODE"]
        if group_mode not in ("multicast", "broadcast"):
            raise ValueError("GROUP_MODE must be 'multicast' or 'broadcast'")

        peers = d["NODE_PEERS"]
        if not isinstance(peers, dict):
            raise ValueError("NODE_PEERS must be an object mapping peer_name -> peer_ip")

        node_port = int(d["NODE_PORT"])
        group_port = int(d["GROUP_PORT"])

        # Strongly recommend the simplest working configuration: a single UDP port
        # for both direct and group messaging.
        if group_port != node_port:
            raise ValueError(
                "For this reference implementation, GROUP_PORT must equal NODE_PORT "
                "(single-port design). Set GROUP_PORT to the same value as NODE_PORT."
            )

        return NodeConfig(
            node_name=str(d["NODE_NAME"]),
            node_ip=str(d["NODE_IP"]),
            node_port=node_port,
            group_mode=group_mode,  # type: ignore
            group_ip=str(d["GROUP_IP"]),
            group_port=group_port,
            node_peers={str(k): str(v) for k, v in peers.items()},
        )


def load_config(path: str | Path) -> NodeConfig:
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    return NodeConfig.from_dict(data)
