import sys

from config import NodeConfig
from message import TTNMessage
from transport_udp import UDPTransport


def _parse_args(argv):
    config = None
    cmd = None
    args = []
    i = 0
    while i < len(argv):
        if argv[i] == "--config" and i + 1 < len(argv):
            config = argv[i + 1]
            i += 2
            continue
        if cmd is None:
            cmd = argv[i]
            i += 1
            continue
        args.append(argv[i])
        i += 1
    return config, cmd, args


def run_listener(config_path):
    cfg = NodeConfig.load(config_path)
    sock, multicast_ok = UDPTransport(cfg.node_port, cfg.group_ip, cfg.group_port).open_socket()
    print("[node] listen ports=%s group=%s:%s multicast_joined=%s" % (cfg.node_port, cfg.group_ip, cfg.group_port, multicast_ok))

    while True:
        data, (src_ip, src_port) = sock.recvfrom(65535)
        try:
            msg = TTNMessage.from_json_bytes(data)
            print("[node] RX %s@%s to=%s id=%s text=%s" % (msg.from_name, msg.from_ip, msg.to, msg.msg_id, msg.text))
        except Exception as e:
            print("[node] RX malformed from %s:%s err=%s" % (src_ip, src_port, e))


def send_direct(config_path, to_name, text):
    cfg = NodeConfig.load(config_path)
    t = UDPTransport(cfg.node_port, cfg.group_ip, cfg.group_port)
    to_ip, to_port = cfg.resolve_peer(to_name)
    msg = TTNMessage.new(cfg.node_name, cfg.node_ip, to_name, text)
    t.send_unicast(msg.to_json_bytes(), to_ip, to_port)
    print("[node] TX direct to %s@%s:%s id=%s" % (to_name, to_ip, to_port, msg.msg_id))


def send_broadcast(config_path, text):
    cfg = NodeConfig.load(config_path)
    t = UDPTransport(cfg.node_port, cfg.group_ip, cfg.group_port)
    msg = TTNMessage.new(cfg.node_name, cfg.node_ip, "broadcast", text)
    try:
        t.send_group(msg.to_json_bytes())
        print("[node] TX broadcast multicast id=%s" % msg.msg_id)
        return
    except Exception:
        pass
    if not cfg.peers:
        raise RuntimeError("Broadcast failed; set NODE_PEERS for fallback.")
    for _, ip in cfg.peers.items():
        t.send_unicast(msg.to_json_bytes(), ip, cfg.node_port)
    print("[node] TX broadcast peer_fanout peers=%d id=%s" % (len(cfg.peers), msg.msg_id))


def main():
    config, cmd, args = _parse_args(sys.argv[1:])
    if not config or not cmd:
        print("Usage: python node.py --config <path> listen|direct|broadcast [args]")
        return 2

    if cmd == "listen":
        run_listener(config)
        return 0
    if cmd == "direct":
        if len(args) < 2:
            print("Usage: direct <peer_name> <text>")
            return 2
        send_direct(config, args[0], " ".join(args[1:]))
        return 0
    if cmd == "broadcast":
        if not args:
            print("Usage: broadcast <text>")
            return 2
        send_broadcast(config, " ".join(args))
        return 0

    print("Unknown command: %s" % cmd)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
