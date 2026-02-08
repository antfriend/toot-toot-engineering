# TTGE TTDB Schema (Draft)

This schema is a minimal, explicit structure for the TTGE knowledge graph and its audit trail. It is intended as a starting point and can evolve.

## Core payload

```json
{
  "identity": {
    "name": "TTGE-0",
    "role": "Self-Improving System Engineer",
    "allowed_actions": [],
    "forbidden_actions": []
  },
  "goedel_goal": {
    "description": "string",
    "invariant": true
  },
  "system_state": {
    "timestamp": "ISO-8601 UTC",
    "repo_snapshot": {
      "commit": "optional",
      "paths_indexed": 0
    },
    "known_constraints": []
  },
  "graph": {
    "nodes": [],
    "edges": []
  },
  "claims": [],
  "tests": [],
  "validations": [],
  "iterations": [],
  "self_modifications": [],
  "metrics": {
    "progress_score": 0,
    "goal_threshold": 10
  }
}
```

## Node types

Each node has a unique `id`, a `type`, and a `props` object.

```json
{
  "id": "DOC:README_TTGE.md",
  "type": "Document",
  "props": {
    "source_path": "README_TTGE.md",
    "checksum": "sha256",
    "last_seen": "ISO-8601 UTC",
    "title": "string",
    "status": "active"
  }
}
```

Allowed `type` values:

- `Document`
- `Tool`
- `Role`
- `Process`
- `Spec`
- `Deliverable`
- `Cycle`
- `Claim`
- `Test`
- `Metric`

## Edge types

Each edge has a unique `id`, a `type`, a `from`, a `to`, and optional `props`.

```json
{
  "id": "EDGE:README_TTGE.md->ttge_runner.py:mentions",
  "type": "mentions",
  "from": "DOC:README_TTGE.md",
  "to": "TOOL:ttge_runner.py",
  "props": {
    "evidence": ["line:1", "line:12"],
    "confidence": 0.7
  }
}
```

Allowed `type` values:

- `mentions`
- `defines`
- `depends_on`
- `implements`
- `supersedes`
- `violates`
- `supports`
- `contradicts`
- `validated_by`

## Claims

Claims are falsifiable statements tied to sources and tests.

```json
{
  "id": "CLAIM:GE-H-001",
  "statement": "string",
  "status": "active",
  "sources": ["DOC:TTE_PROMPT.md"],
  "tests": ["TEST:GE-T-001"],
  "confidence": 0.4,
  "created_at": "ISO-8601 UTC"
}
```

## Tests

Tests are scenario definitions. They do not need to be Python tests.

```json
{
  "id": "TEST:GE-T-001",
  "claim": "CLAIM:GE-H-001",
  "scenario": {
    "description": "string",
    "duration_iterations": 3,
    "notes": "string"
  },
  "success_criteria": [],
  "status": "planned",
  "created_at": "ISO-8601 UTC"
}
```

## Validations

Human validations are required for Bell Events.

```json
{
  "id": "VAL:BE-2026-02-08-001",
  "type": "bell_event",
  "status": "accepted",
  "validated_by": "human",
  "summary": "string",
  "evidence": ["DOC:README_TTGE.md"],
  "timestamp": "ISO-8601 UTC"
}
```

## Iterations

Iteration logs are append-only.

```json
{
  "iteration_id": "0001",
  "timestamp": "ISO-8601 UTC",
  "actions_taken": [],
  "outcome": "progress",
  "notes": "string",
  "progress_delta": 1,
  "progress_score": 1
}
```

## Self modifications

Self modifications must include a justification.

```json
{
  "mod_id": "SM-001",
  "description": "string",
  "justification": {
    "improves_goal_progress": true,
    "reason": "string"
  },
  "applied": true,
  "timestamp": "ISO-8601 UTC"
}
```

## Metrics

```json
{
  "progress_score": 0,
  "goal_threshold": 10
}
```
