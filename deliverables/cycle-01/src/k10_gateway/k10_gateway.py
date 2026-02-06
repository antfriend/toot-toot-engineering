import argparse
import json
import time
from pathlib import Path

from common.ttdb import append_record, utc_now

try:
    import meshtastic
    from meshtastic.serial_interface import SerialInterface
except ImportError:
    meshtastic = None
    SerialInterface = None


def presence_record(observer_id: str, subject_id: str, via: str, signal=None):
    return {
        "kind": "presence",
        "observer_id": observer_id,
        "subject_id": subject_id,
        "time_utc": utc_now(),
        "via": via,
        "signal": signal or {},
    }


def meshtastic_packet_record(rx_by_id: str, packet: dict):
    return {
        "kind": "meshtastic_packet",
        "time_utc": utc_now(),
        "rx_by_id": rx_by_id,
        "from_node_num": packet.get("fromId"),
        "portnum": packet.get("decoded", {}).get("portnum"),
        "payload_b64": packet.get("decoded", {}).get("payload")
    }


def message_record(from_id: str, content: str, channel: str = "field"):
    return {
        "kind": "message",
        "id": f"msg-{int(time.time() * 1000)}",
        "time_utc": utc_now(),
        "from_id": from_id,
        "channel": channel,
        "content": content,
        "content_type": "text",
    }


def node_record(node_id: str, label: str, roles, interfaces, capabilities):
    return {
        "kind": "node",
        "id": node_id,
        "label": label,
        "roles": roles,
        "interfaces": interfaces,
        "capabilities": capabilities,
    }


def handle_packet(log_path: str, k10_id: str, packet: dict):
    append_record(log_path, meshtastic_packet_record(k10_id, packet))
    from_node = packet.get("fromId")
    if from_node is not None:
        subject_id = f"meshtastic:{from_node}"
        append_record(log_path, presence_record(k10_id, subject_id, "meshtastic"))
    decoded = packet.get("decoded", {})
    text = decoded.get("text")
    if text:
        append_record(log_path, message_record(f"meshtastic:{from_node}", text))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", required=True, help="Serial port for Meshtastic device")
    parser.add_argument("--k10-id", default="hw:k10", help="TTN node id for K10")
    parser.add_argument("--log", default="./data/ttdb.log")
    args = parser.parse_args()

    Path(args.log).parent.mkdir(parents=True, exist_ok=True)
    append_record(args.log, node_record(
        args.k10_id,
        "K10",
        ["ui_console", "serial_gateway"],
        {"usb": True, "wifi": True, "lora": False},
        {"display": True, "keyboard": False},
    ))

    if SerialInterface is None:
        raise SystemExit("meshtastic package is required. Install with: pip install meshtastic")

    interface = SerialInterface(args.port)

    def on_receive(packet, interface=None):
        handle_packet(args.log, args.k10_id, packet)

    interface.onReceive = on_receive

    print("K10 gateway running. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
