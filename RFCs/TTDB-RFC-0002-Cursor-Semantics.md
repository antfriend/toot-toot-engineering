# TTDB-RFC-0002
## Cursor Semantics and Selection Rules
### Version 0.1

Status: Draft

This RFC defines the `cursor` block schema and its deterministic update rules.

---

## 1. `cursor` Block Schema
The `cursor` fenced block MUST be valid YAML with these keys:
- `selected` (list of record IDs, required)
- `preview` (map of record ID to short text, required)
- `agent_note` (string, optional)
- `dot` (string, optional)

When the TTDB container is LaTeX, the same logical fields MUST be present
within a deterministic LaTeX environment or comment block.

---

## 2. Selection Rules
- `selected` is an ordered list. The first element is the primary selection.
- If a requested selection is ambiguous, the implementation MUST either:
  - ask for clarification, or
  - select the most recently updated matching record and note the assumption.

---

## 3. Preview Rules
- `preview` entries MUST be truncated to `cursor_policy.max_preview_chars`.
- `preview` MUST contain entries for all `selected` records.

---

## 4. Dot Graph
- If `dot` is present, it MUST be a valid Graphviz dot fragment.
- `dot` SHOULD include the `selected` node(s) when possible.

End TTDB-RFC-0002
