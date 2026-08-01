# TTN-RFC-0002: Typed Edge Taxonomy

**Version:** 1.1
**Status:** Stable
**RFC Number:** 0002
**Project:** toot-toot-engineering
**Component:** Toot Toot Network (TTN)
**Depends on:** TTN-RFC-0001 (Core Mesh Specification), TTDB-RFC-0003 (Typed Edges)
**Author:** antfriend
**Created:** 2026-04-05

---

## Identity / Topology
- knows
- seen_near
- routes_via
- connected_over

## Conversation / BBS
- board_contains
- thread_root
- replies_to
- mentions
- moderates
- supersedes

## AI Semantics
- asks_ai
- ai_summarizes
- ai_flags
- ai_responds_to
- ai_refuses
- ai_confidence_low

## Sensors / Actions
- reports_sensor
- alerts
- commands
- acknowledges
- escalates

## Knowledge Graph
- supports
- contradicts
- refines
- duplicates
- derived_from

## Semantic Polarity
- opposes

Distinct from `contradicts` in Knowledge Graph. `contradicts` is *epistemic* —
two claims that cannot both hold. `opposes` is *semantic* — two concepts at
opposite ends of one dimension, both of which may be perfectly true. Symmetric;
see TTDB-RFC-0003 §7.

## Moderation / Trust
- trusted_by
- muted_by
- blocked_by
- flagged_as_spam
- quarantined
