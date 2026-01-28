# TTDB-RFC-0003
## Typed Edge Semantics for TTDB
### Version 0.1

Status: Draft

This RFC defines typed edge syntax and behavior in TTDB records.

---

## 1. Syntax
Typed edges MUST use the syntax declared in `mmpdb.typed_edges.syntax`.
The default syntax is:

```
<type>@<TARGET_ID>
```

---

## 2. Directionality
- All edges are directional from the record to the target.
- Implementations MUST NOT infer reverse edges unless explicitly present.

---

## 3. Multiplicity
- A record MAY include multiple edges of the same type.
- Duplicate edges SHOULD be deduplicated during rendering.

---

## 4. Taxonomy
TTDB edge types are free-form tokens, but TTDB implementations SHOULD
align with the TTN typed edge taxonomy where applicable.

---

## 5. Embedded Node Graphs
Records MAY include embedded TTDB node graphs that visualize a subgraph
local to the record. These graphs are non-authoritative render hints and
MUST NOT change the canonical edge list declared in the record header.

End TTDB-RFC-0003
