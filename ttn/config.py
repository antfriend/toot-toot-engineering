from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple


def _parse_env_file(path: Path) -> Dict[str, str]:
    """Parse a simple KEY=VALUE env file. Lines starting with # are ignored."""
    out: Dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"Invalid line (expected KEY=VALUE): {raw_line}")
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def _parse_peers(peers: str) -> Dict[str, str]:
    """NODE_PEERS format: name@ip,name2@ip2"""
    peers = peers.strip()
    if not peers:
        return {}
    mapping: Dict[str, str] = {}
    for part in peers.split(","):
        part = part.strip()
        if not part:
            continue
        if "@" not in part:
            raise ValueError("NODE_PEERS entries must look like name@ip")
        name, ip = part.split("@", 1)
        mapping[name.strip()] = ip.strip()
    return mapping


@dataclass(frozen=True)
class NodeConfig:
    node_name: str
    node_ip: str
    node_port: int
    group_ip: str
    group_port: int
    peers: Dict[str, str]

    @staticmethod
    def load(path: str) -> "NodeConfig":
        p = Path(path)
        env = _parse_env_file(p)
        return NodeConfig(
            node_name=env["NODE_NAME"],
            node_ip=env["NODE_IP"],
            node_port=int(env.get("NODE_PORT", "5005")),
            group_ip=env.get("GROUP_IP", "239.255.0.1"),
            group_port=int(env.get("GROUP_PORT", "5006")),
            peers=_parse_peers(env.get("NODE_PEERS", "")),
        )

    def resolve_peer(self, peer_name: str) -> Tuple[str, int]:
        if peer_name not in self.peers:
            raise KeyError(f"Unknown peer name: {peer_name}. Known: {sorted(self.peers.keys())}")
        return self.peers[peer_name], self.node_port
