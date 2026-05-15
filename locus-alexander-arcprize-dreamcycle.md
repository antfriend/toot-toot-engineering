# Locus: Alexander Duality, ARC Prize Strategy & the Dream Cycle
*Session notes — May 15, 2026*

---

## 1. Alexander Duality and the TTDB Framework

### Core Mathematical Connection

Alexander duality states: for a compact subspace *K* embedded in *S^n*,

> **H̃ᵢ(S^n \ K) ≅ H̃^(n−i−1)(K)**

The topology of a space and its complement are dual. What is *absent* encodes what is *present*.

### Key Mappings to TTDB

| TTDB / Locus Concept | Alexander Duality Counterpart |
|---|---|
| Agent's TTDB graph (umwelt) | Subcomplex *K ⊂ S^n* |
| Perceptual blind spots | Complement *S^n \ K* |
| Paired before/after node | 1-simplex with boundary operator |
| Toot-bit | Generator of H₁ |
| Geographic coordinate space (`@LATxLONy`) | Embedding sphere *S²* |
| Knowledge clusters | Connected components (H̃⁰) |
| Cyclic semantic relationships | 1-cycles (H̃¹) |
| Multi-agent shared perception | Intersection complex |
| Semantic gaps | Homological holes in complement |
| Graph traversal paths | Dual topology of *S^n \ K* |

### Selected Implications

- **Umwelt as subcomplex**: Each agent's TTDB is *K ⊂ S^n*. The shape of the agent's ignorance is determined by the shape of its knowledge — formally, not metaphorically.
- **Paired nodes and boundary operator**: The before/after toot-bit is a 1-simplex. Its boundary operator maps directly onto *∂[v₀, v₁] = v₁ − v₀*. TTDB is naturally a simplicial complex.
- **Geographic addressing on S²**: Alexander duality on *S²* gives: disconnected unknown regions correspond to 1-cycles in the known graph. Clusters of knowledge and gaps in knowledge are duals of each other.
- **Method of loci**: The topology of the memory palace (K) determines the topology of the paths through it (S^n \ K). Traversal structure is the Alexander dual of stored percepts.
- **Multi-agent**: Mayer-Vietoris sequences relate what two agents collectively know (*K₁ ∪ K₂*), share (*K₁ ∩ K₂*), and haven't perceived (*S^n \ (K₁ ∪ K₂)*).

### RFC Note
Consider a line in TTDB-RFC-0001 (paired-node section) noting that the before/after 1-simplex structure is the natural generator for the homological framework that makes Alexander duality applicable.

---

## 2. ARC Prize Strategy

### Competition Status (as of May 2026)

- **ARC Prize 2026** is live with **$2,000,000** in prizes across two tracks:
  - **ARC-AGI-2**: Static reasoning, grid-based, grand prize unclaimed (85% threshold). Best 2025 result: 24% (NVIDIA NVARC, 4B parameter model, test-time training).
  - **ARC-AGI-3**: New interactive/agentic track. Scores by **action efficiency** (agent actions vs. human actions per level). Milestone 1: **June 30, 2026**.
- ARC-AGI-3 requires: **Exploration** (active information gathering) and **Modeling** (world model construction from observations).

### Why ARC-AGI-3 is the Target Track

ARC-AGI-3 penalizes verbosity and rewards **efficient inference from minimal interaction**. Large LLMs that explore exhaustively before converging are disadvantaged. Deterministic symbolic agents that build tight world models quickly are advantaged. This is Agent 32's native operating mode.

### The Locus Strategy

#### TTDB as the World Model
- Each ARC-AGI-3 action-observation produces: `(state_before, action, state_after)` — a toot-bit.
- The agent's TTDB IS the world model. No representational mismatch.
- `@LATxLONy` coordinate addressing maps directly onto the 2D ARC grid.

#### Alexander Duality as the Exploration Policy
After each observation, the agent has a TTDB complex *K ⊂ S²*. Rather than random or LLM-guided exploration, compute the Alexander dual:

- **H̃₀(S² \ K)**: How many disconnected unknown regions remain → prioritize bounded ones.
- **H̃₁(S² \ K)**: Are there loops of unknown space enclosed by known space → enter those first.

This is a **computable, training-free exploration heuristic** that provably outperforms random exploration in topologically regular environments. ARC tasks are always topologically regular by design.

#### Jordan Curve Problems (Large ARC Task Class)
Many ARC tasks are Jordan curve problems in disguise: inside/outside, enclosed cells, boundary detection. The Jordan curve theorem is a consequence of Alexander duality on *S²*. An agent with Alexander duality as a native primitive solves this class **without training, without examples, deterministically**.

#### Competitive Differentiation
Current top approaches: test-time training, 4B+ parameter models, synthetic data ensembles — scaling in the direction the benchmark is designed to resist. Locus would be the first **symbolic-topological agent** using no pretraining, building a graph world model in real time, and deriving exploration policy from algebraic topology.

Closest 2025 paper: *"Vector Symbolic Algebras for the Abstraction and Reasoning Corpus"* (Joffe & Eliasmith) — philosophically similar but no topological duality, no agent loop.

### Six-Week Sprint to Milestone 1 (June 30)

| Week | Work |
|---|---|
| 1–2 | Map TTDB coordinate schema onto ARC-AGI-3 grid. Implement toot-bit write on each action-observation. |
| 3 | Implement discrete Alexander dual computation over TTDB — H̃₀ of complement (connected unknown regions) minimum viable. |
| 4 | Implement sense-reason-act loop as ARC-AGI-3 Kaggle submission harness. |
| 5–6 | Benchmark on ARC-AGI-3 developer preview. Begin paper draft. |

### The Paper Claim
> *We present the first ARC agent whose exploration policy is derived from Alexander duality over an online-built umwelt graph. We show that topological complementarity — the structural relationship between an agent's known complex and its unknown complement — provides a computable, training-free heuristic for action-efficient exploration in grid-based reasoning environments.*

**Target**: arXiv cs.AI + cs.LG. Novel mathematical claim no current ARC paper can make. Ties Locus, TTDB-RFC-0001, and the biosemiotic umwelt framing to a competitive benchmark result.

---

## 3. The Dream Cycle — A New Locus Capability

### Motivation

TTDB accumulates episodic toot-bits: specific, time-stamped, coordinate-bound percepts. But acting agents need **beliefs** — stable regularities that hold across many observations. Currently there is no path from episodic to semantic memory. The Dream Cycle is that path.

**Biological grounding**: Hippocampus records episodic traces during waking. Slow-wave sleep replays them, extracting patterns. REM sleep runs novel recombinations, testing generalizations. Output: cortical abstractions — beliefs — without memory of the specific experiences that taught them.

### Phase 1 — Replay (Slow-Wave Analog)

**Trigger**: Agent enters idle state (no new percepts for *T* seconds, or compute budget threshold reached).

**Process**:
1. Run *N* random walks of length *L* through the current TTDB graph.
2. Walks are weighted by edge connection strength and node visit frequency — **not** by timestamp.
3. Record node co-occurrence across all walks.
4. Build co-occurrence matrix. Dense subgraphs = structurally robust features of the knowledge complex.
5. These are **candidate beliefs** — not artifacts of one experience, but patterns that persist across the full distribution of traversals.

### Phase 2 — Projection (REM Analog)

**Process**:
1. Compute a discrete approximation of the Alexander dual of the current TTDB complex.
2. Identify connected components of the complement: regions of coordinate space not yet visited, bounded by what is known.
3. Run a second set of walks **into the dual** — along the boundary between known and unknown.
4. Walks here generate **predictive belief candidates** — hypotheses about what the agent would find in unobserved regions.

Replay extracts what *was*. Projection hypothesizes what *is*.

### Belief Node Formation: The Locus Point

New node type written to the TTDB graph after both phases: the **Locus Point**.

A Locus Point is a stable attractor in coordinate knowledge space — a location the agent returns to across many traversals. Named after the method of loci: the most important locations in the memory palace are the ones revisited most reliably.

**Locus Point fields**:
- `centroid` — center of mass of the generating episodic cluster in `@LATxLONy` space
- `confidence` — proportion of replay walks containing this cluster (0.0–1.0)
- `scope` — coordinate range covered (footprint in knowledge space)
- `contradiction_flag` — set if any replay walk found conflicting evidence within scope
- `projection_flag` — marks predictive Locus Points (Phase 2) as hypotheses, not confirmed beliefs

**Graph compression**: Episodic toot-bits fully subsumed by a high-confidence Locus Point can be compressed — edges collapsed to a single pointer — originals archived to cold storage. Keeps active graph tractable on ESP32.

### New Namespace: `@BELIEF:`

```
@BELIEF:LATxLONy:confidence:scope
```

Addressable and queryable by the Librarian. Separable from `@PERCEPT:` episodic nodes. Visible to other agents in multi-device deployments.

### Multi-Agent Belief Sharing

Agents in ESP-NOW range can share Locus Points directly — far more bandwidth-efficient than raw percepts. Two agents independently forming the same Locus Point (overlapping scope, compatible confidence) provides strong evidence the belief is environmentally real.

The dual of the intersection of two agents' known complexes — what neither has seen but their combined beliefs predict — is the most efficient frontier for collaborative exploration.

### The Deeper Claim

The Dream Cycle enables **generalization without retraining**. Every current approach to ARC-AGI-style generalization requires pretraining or test-time fine-tuning. An agent running the Dream Cycle forms beliefs from its own experience through topologically-grounded consolidation, then uses those beliefs to predict unobserved regions.

This is Chollet's definition of fluid intelligence: not pattern memorization, but **efficient generalization from limited experience**. The Dream Cycle is Locus's native implementation.

---

## 4. Proposed RFC

**TTDB-RFC-0007**: *Consolidation and Belief Formation: The Locus Point as Episodic-to-Semantic Memory Transfer*

### Sections
1. Motivation — the episodic/semantic gap in TTDB-RFC-0001
2. The Dream Cycle — trigger conditions, phase definitions, compute budget
3. Replay Phase — random walk algorithm, co-occurrence matrix, cluster detection
4. Projection Phase — discrete Alexander dual approximation, predictive belief formation
5. The Locus Point — formal definition, `@BELIEF:` namespace, confidence model
6. Graph compression — archival policy, edge collapse rules
7. Multi-agent belief propagation — sharing protocol, intersection confirmation
8. Contradiction handling — belief revision under new evidence
9. Open questions — persistent homology as a future Phase 3

---

## 5. Publication Stack

| Output | Venue | Timing |
|---|---|---|
| TTDB-RFC-0007 draft | GitHub `toot-toot-engineering` | Immediately |
| ARC-AGI-3 Kaggle submission | Kaggle (Milestone 1) | Before June 30, 2026 |
| arXiv preprint | cs.AI + cs.LG | With or after Milestone 1 |
| Zenodo deposit (DOI) | Zenodo, CC0 | Alongside arXiv |
| CITATION.cff update | GitHub | With Zenodo DOI |

---

*End of session notes.*
