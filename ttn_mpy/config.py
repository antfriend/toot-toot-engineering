from __future__ import annotations


def _parse_env_file(path):
    out = {}
    with open(path, "r") as f:
        for raw_line in f.read().splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ValueError("Invalid line (expected KEY=VALUE): %s" % raw_line)
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def _parse_peers(peers):
    peers = peers.strip()
    if not peers:
        return {}
    mapping = {}
    for part in peers.split(","):
        part = part.strip()
        if not part:
            continue
        if "@" not in part:
            raise ValueError("NODE_PEERS entries must look like name@ip")
        name, ip = part.split("@", 1)
        mapping[name.strip()] = ip.strip()
    return mapping


class NodeConfig:
    def __init__(self, node_name, node_ip, node_port, group_ip, group_port, peers):
        self.node_name = node_name
        self.node_ip = node_ip
        self.node_port = node_port
        self.group_ip = group_ip
        self.group_port = group_port
        self.peers = peers

    @staticmethod
    def load(path):
        env = _parse_env_file(path)
        if "NODE_NAME" not in env or "NODE_IP" not in env:
            raise ValueError("Missing required keys: NODE_NAME, NODE_IP")
        return NodeConfig(
            env["NODE_NAME"],
            env["NODE_IP"],
            int(env.get("NODE_PORT", "5005")),
            env.get("GROUP_IP", "239.255.0.1"),
            int(env.get("GROUP_PORT", "5006")),
            _parse_peers(env.get("NODE_PEERS", "")),
        )

    def resolve_peer(self, peer_name):
        if peer_name not in self.peers:
            raise KeyError("Unknown peer name: %s" % peer_name)
        return self.peers[peer_name], self.node_port
