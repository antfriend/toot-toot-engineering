from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SemanticEdge:
    edge_type: str
    source: str
    target: str
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SemanticEntity:
    type: str
    id: str
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SemanticEvent:
    event_id: str
    event_type: str
    intent: str
    confidence: float
    ts: str
    reported_by: str
    addressed_to: str

    mesh_meta: Dict[str, Any] = field(default_factory=dict)
    entities: List[SemanticEntity] = field(default_factory=list)
    payload: Dict[str, Any] = field(default_factory=dict)
    edges: List[SemanticEdge] = field(default_factory=list)

    raw_ref: str = ""  # e.g., raw:sha256:...
    rationale: Optional[str] = None  # for AI enricher (optional)

