from __future__ import annotations

"""Gateway runner.

In this cycle we prioritize a dry-run demo that writes outputs to disk.
A live gateway would:
- read from a receiver (meshtastic serial/tcp/ble or ip)
- normalize to NormalizedPacket
- interpret to SemanticEvent
- assign stable IDs
- publish raw + semantic events to MQTT
- write to TTDB markdown file

See demo/simulate_day.py for the runnable end-to-end pipeline.
"""

if __name__ == "__main__":
    from demo.simulate_day import generate_outputs

    generate_outputs("deliverables/cycle-01/generated", id_step_lat=0.0001, id_step_lon=0.0001)
    print("Generated cycle-01 demo artifacts.")
