This document is intended for humans and should be ignored by agents unless a human explicitly requests it.

# Token Usage Estimate (1 TTE Cycle)

## Baseline context included in estimate
- `README.md` (1312 words)
- `AGENTS.md` (764)
- `CHECKLIST.md` (216)
- `WHAT.md` (296)
- `RELEASES.md` (165)
- `MORTAL-ENGINES-FRAMEWORK-RELEASES.md` (259)

Total: 3012 words, approximately 3900-4200 tokens after tokenization overhead.

## Per-cycle estimate (8 steps)
- Input tokens per step: ~4-6k
- Output tokens per step (typical):
  - Bootstrap: 800-1200
  - Storyteller: 600-1200
  - SVG engineer (if used): 400-800
  - Orchestrator: 600-1200
  - Core worker: 1500-4000
  - Reviewer: 600-1200
  - Delivery packager: 600-1200
  - Retrospective: 600-1200

## Roll-up estimate
- Total input tokens: ~32k-48k
- Total output tokens: ~6k-12k
- Grand total per cycle: ~38k-60k tokens

## Notes on variance
- Larger deliverables (e.g., STL spec, SVG, or long reports) increase output tokens.
- Including prior cycle artifacts in context can raise input tokens substantially.
- Tool outputs pasted into model context count toward input tokens.
