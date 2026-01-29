# STORYTELLER (cycle-02)

## Narrative focus
This cycle turns TTN into a “confident CLI tool”: every command clearly announces what it’s doing, and every failure path is explicit and self-explanatory. The user should feel they can trust the logs to diagnose multicast and fallback behavior without digging into code.

## UX narrative beats
- **Clarity at startup:** listeners declare ports, group address, and multicast status up front.
- **Human-readable events:** each message (send/receive/fallback) is a named event.
- **Structured output:** the same events can be consumed by a human in text or a tool in JSON.

## Suggested phrasing
- “multicast_joined=true|false” on listener startup
- “multicast_failed” event before fanout fallback
- “tx_direct”, “tx_broadcast”, “rx_message” events for consistency
