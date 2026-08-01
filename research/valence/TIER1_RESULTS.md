# Tier 1 Results

**Run date:** 2026-08-01
**Sign map:** as proposed in `SIGN_MAP_PROPOSAL.md`, applied in full
(hub excluded, `amends` left at −1 as statistically inert, φ = endorsement for
the RFC stores, the two stores run as separate graphs).
**Reproduce:**

```bash
python research/valence/ttdb_valence.py feelings_ttdb.md \
    --seeds research/valence/seeds.feelings.tsv --gamma 0.05 --trials 500
```

---

## Verdict

**Propagation passes decisively. The balance/frustration experiment did not run
on the feelings store, and did run — unexpectedly — on the RFC corpus, where it
found one genuine structural contradiction.**

No §6 stop condition was triggered. One §6 criterion (the seed-shuffle null)
turned out to be measuring the wrong quantity and was corrected; see §4.

---

## 1. Propagation on `feelings_ttdb.md` — passes

73 valence-bearing edges over 39 affective records, 12 seeds, ground truth
`φ_true = lat/40` from the store's own declared globe mapping.

| Test | Result | Verdict |
|---|---|---|
| Seed leave-one-out | MAE **0.174** vs mean-baseline **0.708**, r = **+0.948** | Beats baseline |
| **All free nodes vs ground truth** | n=29, r = **+0.930**, MAE 0.211 vs baseline 0.562 | Passes |
| **Sign recovery, free nodes** | **29 / 29 correct** | Passes |
| Seed-shuffle null (energy) | observed 1.08 vs null mean 16.93, **p < 0.002** | Placement matters |
| Seed-shuffle null (ground-truth r, 2000 trials) | observed +0.930 vs null mean **+0.007**, **p = 0/2000** | Placement matters |

The free-node test is the stronger one and is not in the script: it scores every
never-seeded node against its own latitude, so it cannot be gamed by seed
choice. Every single free node landed on the correct side of zero.

### 1.1 The hub exclusion was the whole result

Same store, same seeds, only difference being whether the 55 hub edges are
included:

| Hub edges | LOO r |
|---|---|
| Included at +1 | **−0.963** |
| Excluded | **+0.948** |

Held-out seeds went from being predicted with *reversed* sign to being predicted
well. This is the single decision that mattered, and it was made from the
store's semantics — the hub asserts membership, not valence — rather than from
the outcome.

### 1.2 Errors are systematic shrinkage, not noise

Every free-node error is an *underestimate*. That is the `−γφ` decay term plus
the maximum principle (§1.4–1.5), not a propagation failure:

| γ | r | MAE |
|---|---|---|
| 0.5 | +0.883 | 0.292 |
| 0.15 (default) | +0.930 | 0.211 |
| 0.05 | +0.946 | 0.169 |
| 0.01 | +0.946 | 0.163 |

Plateaus around γ ≈ 0.05. The default 0.15 is mildly over-damped for this store.
Correlation is the honest headline statistic here since it is scale-invariant;
MAE is inflated by a shrinkage with a known cause.

### 1.3 Caveats that must travel with this result

- **One seed cannot be scored.** `@LAT30LON40` (Compassion) predicts 0.000 under
  leave-one-out because it lands in a seedless component when held out. That is
  a connectivity artifact, not a miss. It contributes a 0.75 error to the
  reported MAE; excluding it gives MAE ≈ 0.121.
- **Excluding the hub fragmented the graph** into 6 components (largest 20 of 43
  nodes), 3 of them seedless. This is a real cost of the exclusion and the main
  argument for testing the `@LAT0LON0 = 0.0` boundary-seed alternative.
- **The store was authored as a coherent affective landscape.** It is not an
  adversarial test. Recovering its geometry proves the method works on a
  well-formed store; it does not prove the method survives a messy one.
- **This validates propagation only.** Nothing here supports the mood/emotion
  spectral conjecture (§1.6), the ρ-from-`@PERCEPT` claim (§4), or anything in
  Tier 2+.

---

## 2. Balance on `feelings_ttdb.md` — did not run

0 violating edges out of 49, because **all 49 are positive**. The store's
polarity lives in its coordinates, not its edges.

This is the absence of an experiment, not a negative result, and the script now
says so explicitly rather than reporting `p = 1.000` as though it were evidence.
Permuting signs that are all `+1` is a no-op; the p-value is arithmetic.

---

## 3. Balance on the RFC corpus — ran, and found something

φ = endorsement. Both RFC stores as one graph: 41 nodes, 125 merged edges, 3
negative, one connected component.

**Greedy 2-coloring: 2 violating edges. The corpus is genuinely unbalanced.**
On a connected graph the coloring is forced once any node is fixed, so this is
not a traversal-order artifact — a consistent endorsement assignment does not
exist.

### 3.1 The frustrated triangle

Verified by sign product (−1, an odd number of negative edges):

```
@LAT98LON0  --contradicts(-1)--> @LAT40LON4     BELIEF vs A32-RFC-0004
@LAT40LON4  --depends_on(+1)---> @LAT40LON1     A32-RFC-0004 on A32-RFC-0001
@LAT98LON0  --refines(+1)------> @LAT40LON1     BELIEF refines A32-RFC-0001
```

In words: the belief **"the A32 RFCs say PlatformIO; robot_team uses
arduino-cli"** contradicts A32-RFC-0004 (Claude Code Project Setup) while
simultaneously refining A32-RFC-0001 (Architecture) — and A32-RFC-0004 depends
on A32-RFC-0001. The belief is therefore required to be both aligned with and
opposed to the same cluster. No consistent endorsement assignment exists.

This is exactly the §8 item-1 use case — *"RFC-12 supersedes RFC-4, but RFC-19
still builds on RFC-4. Nobody notices until something breaks"* — found
automatically, with checkable ground truth. The tension is real and already
documented in prose at `@LAT40LON4` (*"build tooling superseded in robot_team —
see @LAT98LON0"*). What the method adds is that it was **found structurally,
without reading the corpus**.

### 3.2 How much weight this carries

Limited, and the limit should be stated plainly:

- **n = 1.** One frustrated triangle out of 125 edges, resting on 3 negative
  edges total. This demonstrates the mechanism fires on a true positive; it is
  not evidence about precision or recall.
- **It was already known.** The prose records it. The method did not surface
  something nobody knew — it surfaced something nobody had *indexed*.
- **Not degree-driven** (§6's trivia check): the triangle sits on nodes of
  degree 3–4, not on hubs.
- The `amends`/`amended_by` = −1 judgment does **not** affect this finding — the
  triangle uses `contradicts`, `depends_on`, and `refines` only.

---

## 4. Correction to the falsification protocol

**The seed-shuffle null in §6 was measuring the wrong quantity.** Scored on
spread (sd), it returns p ≈ 0.69 on a run where seed placement demonstrably
matters — because shuffling values across a fixed seed set preserves the
multiset of seed values, so overall spread barely moves regardless of where they
land.

Measured on the same 300 shuffles:

| Statistic | Observed | Null mean | p |
|---|---|---|---|
| Spread (sd) — previous | 0.551 | 0.568 | **0.690** |
| Total energy — now used | 1.246 | 17.58 | **< 0.004** |
| LOO MAE | 0.173 | 0.800 | **< 0.004** |

Since §6 makes this null a stop condition, scoring it on spread risked a false
*"archive this document"* verdict on a working method. The script now scores
both nulls on energy, reports spread as explicitly non-diagnostic, and refuses
to present a vacuous sign-shuffle as evidence.

**This supersedes the seed-shuffle row of VALENCE_FIELD.md §6.**

---

## 5. What this does and does not license

**Licensed:**
- Signed diffusion recovers a known valence field from sparse seeds on a
  well-formed store. §6's propagation stop conditions are cleared.
- Frustration detection fires on a real structural contradiction in a real
  corpus, on the application §8 ranks most defensible.

**Not licensed:**
- Drafting a TTDB RFC. `VALENCE_FIELD.md` §4 says not before Tier 1 returns;
  Tier 1 has now returned on propagation only, on one authored store, with the
  balance half untested where it was supposed to be tested.
- The §6 question that matters most is **still unrun**: *does valence-weighted
  EPS beat plain EPS at retrieval or dream-cycle consolidation?* Given the
  V-shaped valence–arousal relation, `sal` and `|φ|` may be substantially
  redundant. Until that head-to-head runs, valence has not earned a channel.

**Recommended next**, in order:
1. Run the EPS head-to-head. It is the cheapest remaining test and it is the one
   that can still kill the idea.
2. Decide the `@LAT0LON0 = 0.0` boundary-seed alternative against exclusion, to
   recover the 3 seedless components.
3. Only then consider whether the corpus should mint a negative edge type — a
   TTDB-RFC-0003 taxonomy question, judged on whether the corpus needs to
   express opposition, not on whether it would make this experiment light up.
