# cycle-01 REVIEW

## Scope check (prompt compliance)
Covered by produced artifacts:
- Deterministic semantic rules engine: `semantic/semantic_rules.py`
- Stable ID assignment + collision rule (SE stepping): `addressing/stable_ids.py`
- TTDB markdown writer: `db/ttdb_writer.py`
- Demo generator (day on the mesh): `demo/simulate_day.py`
- Generated DB: `deliverables/cycle-01/generated/MyMentalPalaceDB.md`
- Generated topic taxonomy: `deliverables/cycle-01/generated/topic_map.md`
- Offline monitor: `deliverables/cycle-01/generated/monitor.html`

Partially covered / missing vs prompt:
- MQTT publishing integration exists as a stub client (`mqtt/mqtt_client.py`) but demo currently does **not** publish.
- Pluggable Meshtastic receivers (`receiver_meshtastic_serial.py`, `receiver_meshtastic_tcp.py`, `receiver_meshtastic_ble.py`) are **not implemented** (only types exist). This is acceptable for a simulator-first cycle if documented as a follow-up.
- AI librarian service folder exists but no implementation yet.

## Correctness findings
1. **Entity IDs are duplicated with prefixes**
   - In generated DB, entities show like `node:node:tdeck-plus` and `sensor:sensor:temp`.
   - Root cause: TTDB writer prepends `{type}:` while entity.id already contains `node:`/`sensor:`.
   - Severity: low/medium (cosmetic + impacts graph readability).
   - Fix: either store entity.id as bare IDs (`tdeck-plus`, `temp`) or render without prepending type.

2. **Monitor graph edge parsing will likely not render edges**
   - DB edges are written as `  - edge_type: source -> target`.
   - monitor.html regex expects lines beginning with `- <edge_type>: ...` (no indentation/bullet format mismatch).
   - Severity: medium (graph output becomes empty).
   - Fix: adjust monitor.html regex to match `^\s*\-\s+([a-zA-Z_]+):\s+(.*)\s+->\s+(.*)$` *and* include the two-space indentation variant, or change DB writer to output edges without the extra list nesting.

3. **`demo/simulate_day.py` module-run requirement**
   - It works with `python -m demo.simulate_day` (imports are package-style).
   - Running as `python demo/simulate_day.py` may fail due to import path.
   - Severity: low (document correct invocation).

4. **AI invocation naming**
   - Demo uses `to_id="node:AI"` and command `@AI summarize 6h`.
   - Semantic rules convert it to `target: node:AI`.
   - Good: respects “only speak when invoked” principle (no actual mesh transmit implemented yet).

## Security/safety notes
- No secrets files accessed.
- MQTT client uses paho-mqtt but is not actively connecting/publishing in demo.

## Recommendation
Accept cycle-01 as a simulator-first milestone, with two small follow-up fixes strongly recommended before “complete”:
- Fix entity rendering in TTDB.
- Fix monitor edge parsing so graph shows edges.

## Next step
Delivery packager: write `deliverables/cycle-01/DELIVERY.md`, update `RELEASES.md`, and capture run instructions and known limitations.
