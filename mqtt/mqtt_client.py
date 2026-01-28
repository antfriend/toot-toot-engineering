from __future__ import annotations

import json
from typing import Any, Optional

try:
    import paho.mqtt.client as mqtt  # type: ignore
except Exception:  # pragma: no cover
    mqtt = None


class MqttBus:
    def __init__(self, host: str = "localhost", port: int = 1883, topic_prefix: str = "tte/"):
        self.host = host
        self.port = port
        self.topic_prefix = topic_prefix.rstrip("/") + "/"
        self._client = None

    def connect(self) -> None:
        if mqtt is None:
            raise RuntimeError("paho-mqtt not installed")
        self._client = mqtt.Client()
        self._client.connect(self.host, self.port, keepalive=60)

    def publish_json(self, topic: str, payload: Any, retain: bool = False) -> None:
        if self._client is None:
            raise RuntimeError("MQTT client not connected")
        data = json.dumps(payload, ensure_ascii=False)
        self._client.publish(self.topic_prefix + topic.lstrip("/"), data, retain=retain)

    def disconnect(self) -> None:
        if self._client is not None:
            self._client.disconnect()
            self._client = None

