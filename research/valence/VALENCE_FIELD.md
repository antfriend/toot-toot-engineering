# Valence as a Scalar Field over TTDB

**Status:** Tier 1 run 2026-08-01. Propagation validated against external human
norms at r = +0.941 on never-seeded nodes. Tiers 2–4 remain unrun.
**Purpose:** context transfer — the reasoning behind the work. Read this before
touching `ttdb_valence.py`; read `TIER1_RESULTS.md` for what actually happened.
**Owner decision — resolved:** this line of work **survives Tier 1**. No §6 stop
condition triggered; the redundancy criterion in §6 was tested and not met
(valence carries ~99% independent variance). It has **not** earned an RFC — the
retrieval half of §6 is still unrun. See `TIER1_RESULTS.md` §5, §6.

> **Where this document is now superseded.** The design reasoning below stands
> as written. Three claims about *status* do not, and are corrected in place:
> §3 (Tier 1 is run), §6 (one stop condition was defective — see §6.0), and §10
> (the synthetic fixture is no longer the only evidence).

---

## 0. Orientation (read this if nothing else)

A TTDB store is a graph of claims. Some claims support each other, some
contradict each other. Assign a signed number to each node — call it valence —
anchor a few by hand, and let the rest settle into the assignment that best
respects the edge signs.

The output people expect is the settled numbers. **The output that matters is
where the settling fails**: nodes that cannot be consistently assigned because
their neighborhood pulls both ways. Those are structural contradictions in the
corpus, findable without reading it.

Everything below is elaboration on that. The elaboration is worth having, but
if the frustration measure doesn't flag anything real in the golden store, the
elaboration is decoration and this document should be archived.

---

## 1. The mathematical core

### 1.1 Field and operators

A valence field is a function on nodes, `φ: V → ℝ`, conventionally in `[-1, 1]`.

Its gradient lives on **edges**:

```
(∇φ)(u,v) = φ(v) − φ(u)
```

This is the first substantive claim: affective difference is natively a
property of relations, not of concepts. A node has no valence in isolation; it
has valence relative to its neighborhood.

The graph Laplacian measures departure from local consensus:

```
(Lφ)(v) = Σ_u w_uv (φ(v) − φ(u))
```

### 1.2 Signed edges are mandatory, not an enhancement

Antonyms are distributionally near-identical. Unsigned smoothing drags
*good* and *bad* together — this is the documented failure mode of
embedding-based sentiment induction, and it is why Hatzivassiloglou & McKeown
(1997) used conjunction-derived sign constraints rather than similarity alone.

So every edge carries `σ ∈ {+1, −1}` and the energy becomes:

```
E(φ) = ½ Σ_uv w_uv (φ(u) − σ_uv φ(v))²
```

The signed Laplacian `L_σ` is the operator of this form.

**Requirement:** `σ_uv = σ_vu`. The Laplacian must be symmetric or the
spectral claims below are void. `build_adjacency()` enforces this by
symmetrizing; TTDB's typed edges are directed, so this is a real projection
and a real loss of information. Accepted for Tier 1, revisit later.

### 1.3 Balance theory gives us a measurement, not just correctness

A signed graph is **balanced** iff every cycle contains an even number of
negative edges (Heider 1946; Cartwright & Harary 1956). Equivalently: the
nodes can be 2-partitioned so all positive edges are within parts and all
negative edges across.

Spectral statement: the smallest eigenvalue of `L_σ` is 0 **iff** the graph is
balanced. The **frustration index** — minimum edges to delete to achieve
balance — quantifies the shortfall.

This is the payoff. Cognitive dissonance becomes a spectral quantity, localized
on the eigenvector of the smallest nonzero eigenvalue. Regions where no
consistent valence assignment exists are computable.

**Hardness caveat, do not lose this:** computing the exact frustration index is
NP-hard (reduces to MAX-CUT). The script's BFS 2-coloring gives an **upper
bound**. A count of 0 *proves* balance. A nonzero count does *not* prove
imbalance of that magnitude.

### 1.4 Decay: valence is not conserved

Pure diffusion has no forgetting. The honest dynamics are reaction-diffusion:

```
∂φ/∂t = −α L_σ φ − γ φ + ρ(t)
```

The `−γφ` term is hedonic adaptation. It gives a characteristic length:

```
ℓ = √(α/γ)
```

Green's function falls off like `e^(−r/ℓ)`, so `ℓ` is literally *how many hops
affect travels before dissipating*. This is a tunable with a semantic
interpretation, which is rare and worth exploiting. `--gamma` in the script.

### 1.5 Diffusion cannot create extremes — the grounding constraint

Minimizing Dirichlet energy with seeds fixed gives **harmonic extension** (Zhu,
Ghahramani & Lafferty 2003; the standard method behind graph-based sentiment
lexicon induction, e.g. Velikovich et al. 2010).

Harmonic functions obey a **maximum principle**: extrema occur only on the
boundary. **No propagated node can be more extreme than your most extreme
seed.**

To get novel affective extremes you need the Poisson form `L_σ φ = ρ` with
source terms `ρ` that are *not* semantic — interoception, reward prediction
error, bodily state. The field must be anchored in something that is not more
graph.

This is the grounding problem in compact form, and it is the whole reason §4
(Tier 2) exists. Note the decay term partially breaks the strict maximum
principle, but not in a way that manufactures meaningful new extrema.

### 1.6 Spectral decomposition — hold as analogy, not claim

Decompose `φ` in the Laplacian eigenbasis. Low-frequency components are smooth
and global; high-frequency are sharp and localized.

**Conjecture:** mood is the DC component of the valence field; discrete
emotions are localized high-frequency spikes.

This predicts mood should be hard to shift locally and emotions should be easy
— which matches phenomenology, so it has some teeth. But it is an analogy that
happens to postdict correctly, not a result. Do not write it into an RFC as
established.

Supporting context worth knowing: Osgood, Suci & Tannenbaum (1957) found
**evaluation** to be the first principal component of connotative meaning
across dozens of languages. Valence is not one field among many — it is close
to the dominant mode of semantic structure generally. That is why this is worth
trying at all.

### 1.7 Topology of the field

Morse theory on `φ`: local minima are negative attractors, maxima positive,
saddles are ambivalence points. A rumination basin is a deep minimum with high
escape energy.

Persistent homology of the sublevel filtration tracks how basins merge as the
threshold sweeps. **This is where the existing Alexander duality framing bites:**
the shape of the field's basins and the shape of its ridges determine each
other. The established Locus claim is that the shape of ignorance is determined
by the shape of knowledge; this extends it to say the shape of ambivalence is
too.

Not implemented in Tier 1. Listed because it is the natural Tier 4 and because
it connects to machinery already in the corpus.

---

## 2. Design decisions already made (with rationale, so they can be reversed
knowingly)

### 2.1 Do NOT add `val` to the TBEW tuple

TBEW is `conf`, `sal`, `rev`, `touched`. Leave it alone.

The golden conformance store's entire virtue is that the spec is an instance of
the structure it defines. Mutating the core weight quadruple is a breaking
change that costs Draft 04 conformance.

**Instead:** valence lives in a derived `@VALENCE:` namespace, *computed over*
the store rather than *stored in* it. Recomputable, versionable, fails safe.
The CSV output of `ttdb_valence.py` is the prototype of this namespace.

### 2.2 Scalar first, even though scalar is known-insufficient

A single signed scalar cannot distinguish *neutral* from *strongly both*. Real
ambivalence needs `φ: V → ℝ²≥0` with two independently diffusing channels
(positive and negative), which is the bivariate position in the
bipolar-vs-bivariate debate.

Deferred anyway. It doubles memory and complicates the fixed-point path. Build
scalar, find where it fails, let the failures say whether the second channel is
needed. See §7.1.

### 2.3 Sign map is the model; everything else is arithmetic

`SIGN_MAP` in `ttdb_valence.py` is the only place real modeling judgment
enters. Edge type → sign is a coarse projection of typed-edge semantics onto
`{+1,−1}`. Richer edge types properly want a **sheaf Laplacian** rather than a
scalar sign (see §7.2), but that is live research.

Unmapped types are reported with counts rather than silently defaulted. Keep
that behavior.

> **Correction from Tier 1: `{+1,−1}` was not enough, and `SIGN_MAP` was not the
> only place judgment enters.** A third value is required — **0, exclude** — for
> edges that are structurally real but assert nothing about valence, and it
> turned out to carry more weight than any sign assignment.
>
> `feelings_ttdb.md` has 55 edges into its neutral origin asserting *membership*
> ("this state belongs to the experiencer"), not valence. Forced to `+1` they
> instruct the solver to make *Serenity* and *Unease* agree. Excluding them
> moved free-node r from **+0.788 to +0.946** — a larger effect than any sign
> choice in the map. Narrative traversal edges (a story arc deliberately
> crossing valence) need the same treatment, and are notably *not* `−1`: `−1`
> asserts consistent opposition, which an arc crossing zero twice is not.
>
> This lives in `EXCLUDE_TYPES`. Treat it as co-equal with `SIGN_MAP`, not as a
> filter — deciding an edge means nothing is as substantive as deciding it means
> opposition.

### 2.4 Pure stdlib

No numpy. Runs on anything including a Pi, and the ESP32 port (§5) is closer if
nothing exotic is assumed. Signed diffusion is sparse matvec plus decay; that's
it.

---

## 3. Tier 1 — RUN (2026-08-01)

> **Status: complete. Results in `TIER1_RESULTS.md`.** The plan below is kept as
> written; what actually happened diverged from it in two ways worth knowing
> before reading further.
>
> **The store changed.** Tier 1 was planned against the RFC corpus. It ran
> against `feelings_ttdb.md`, because that store declares `lat = valence` in its
> own globe mapping and therefore supplies **ground truth** — the RFC corpus
> supplies none. The RFC corpus was still used, for balance (§3.1 question 1),
> where it turned out to be the *only* store with enough negative edges to ask
> the question at all.
>
> **The two questions split cleanly across the two stores.** Question 1
> (frustration localizes real tension) was answered **yes, on the RFC corpus** —
> one genuine frustrated triangle, a belief that both refines an architecture
> and contradicts a document depending on it. Question 2 became a stronger test
> than planned: propagation was scored against *external* human norms rather
> than intuition, at r = +0.941 on never-seeded nodes.

### 3.1 What it is

Assign signs to existing RFC edge types, seed ~12 nodes by hand, run signed
Jacobi to convergence over the 28-RFC golden store, and check two things:

1. Does the frustration measure localize where you'd expect tension?
2. Does the anomaly measure flag nodes you already suspected were misfiled?

Cost: an afternoon. That is the point — it is cheap enough to be genuinely
falsifiable rather than defended.

### 3.2 Protocol

```bash
# ALWAYS FIRST. Silent parse failure produces a flat field, which looks
# exactly like a negative result. Verify addresses, degrees, edge types.
python3 ttdb_valence.py path/to/store --dump-parse

# Seed ~12 nodes: address <TAB> value in [-1, 1]
# Choose seeds that are (a) confidently signed, (b) spread across the graph,
# (c) NOT all in one component.
python3 ttdb_valence.py path/to/store --seeds seeds.tsv --csv field.csv
```

Format assumptions are isolated in one block at the top of the script
(`NODE_TOKEN`, `NODE_DECL_RE`, `EDGE_RE`, `FIELD_RE`). Edit there, not in the
parser body.

### 3.3 Correction worth carrying forward

The per-node anomaly measure is **not** `|Lφ|`. At the fixed point the *signed*
sum is zero on free nodes by construction — that is the stationarity condition,
so it detects nothing. Early framing in the design conversation got this wrong.

The script uses the per-node **residual sum of squares**:

```
frustration(v) = Σ_u w_uv (φ(v) − σ_uv φ(u))²
```

which is nonzero and localizes exactly where no consistent assignment exists.
That list is the primary deliverable of Tier 1.

---

## 4. Tier 2 — where ρ comes from (the actual hard problem)

§1.5 says the field needs non-semantic sources or it can only interpolate
between hand-set seeds.

**The claim:** TTDB already contains the answer. RFC-0001's paired
`@PERCEPT:before` / `@PERCEPT:after` node **is a discrete derivative** — the
primary datum is a difference, not a state. Prediction error over that pair is
exactly the source term the field needs, and it is non-semantic by
construction, which is what escapes the maximum principle.

This lands directly on `@LAT20LON3` (Learning from Action), the
highest-EPS unimplemented item, deliberately left open in Draft 04. Valence-as-
ρ-from-outcome is a credible reading of what's missing there.

It also closes the gap previously identified in the Locus arXiv paper: the
active inference loop was noted as having a hole on the action side. Same move
closes it. Precision-weighting ↔ TBEW is the existing correspondence; valence ↔
expected free energy gradient would be the new one.

**Status: credible, unproven — and still unrun.** Tier 1 has returned (§3), so
that gate is cleared, but nothing here has been touched: no `@PERCEPT:` pair has
been used as a source term. The gate on an RFC is now the *retrieval* half of
§6.1, not Tier 1.

---

## 5. Tier 3 — hardware, where it stops being metaphor

Signed diffusion on ESP32-S3 class silicon: int8 valence, int32 accumulators,
CSR edge storage in PSRAM. Straightforwardly feasible.

But the more interesting instantiation is a field over the **mesh**, not over
concepts:

- vertices = physical nodes (K10, Heltec V4, T-Deck)
- edge weights = RSSI/SNR and umwelt overlap (existing TTN semantic positioning
  machinery)
- `ρ` = each node's local sensor state

The deliberate sensor heterogeneity across nodes — already a design principle
for TDoA disambiguation — is exactly what makes the field informative rather
than uniform. A physically grounded valence field on hardware already on the
bench.

---

## 6. Falsification criteria — the stop conditions

Written down in advance so they can't be renegotiated afterward.

### 6.0 One of these criteria was defective — corrected 2026-08-01

Writing stop conditions in advance protects against renegotiating them. It does
not protect against one of them being **wrong**, which is what happened.

**The seed-shuffle null was scored on spread (sd), and spread cannot detect seed
placement.** Shuffling values across a fixed seed set preserves the multiset of
seed values, so the field's overall spread barely moves no matter where they
land. Measured on identical shuffles of the golden store:

| Statistic | Observed | Null mean | p |
|---|---|---|---|
| Spread (sd) — as originally specified | 0.551 | 0.568 | **0.690** |
| Total energy — now used | 1.246 | 17.58 | **< 0.004** |
| LOO MAE | 0.173 | 0.800 | **< 0.004** |

Row 1 of the table below would therefore have read *"archive this document"* on
a run where placement demonstrably mattered. Both nulls are now scored on
**energy**; spread is reported and flagged non-diagnostic.

**A second failure mode, not originally anticipated:** on a store with no
negative edges, sign-shuffle is a *no-op* and returns p = 1.000 as pure
arithmetic. That is the **absence of the experiment**, not a result, and must
not be read against row 1 either. The script now says so explicitly.

The lesson generalizes past this document: a falsification criterion is itself a
measurement, and can be miscalibrated. Fix the instrument before honoring its
verdict.

The script computes two permutation nulls:

- **sign-shuffle** — keeps topology and seeds, permutes edge signs. Tests
  whether sign *structure* carries anything.
- **seed-shuffle** — keeps topology and signs, permutes seed values across seed
  nodes. Tests whether seed *placement* matters.

Plus **leave-one-out** on seeds: hold each out, predict from the rest, compare
MAE against a predict-the-mean baseline.

**Stop conditions:**

| Observation | Conclusion |
|---|---|
| Both null p-values ≈ 0.5 | Sign structure carries nothing. Field is decoration. **Archive this document.** |
| LOO MAE ≥ baseline MAE | Propagation is not recovering held-out valence. Seeds may be too sparse or too clustered — retry once with better spread, then stop. |
| Frustration list is topologically trivial (all high-degree hubs) | Measuring degree, not dissonance. Needs degree normalization before it means anything. |
| Field is flat (sd ≈ 0) | Check for parse failure and for zero negative edges *before* concluding anything. |

**And the one that matters most:**

> Does valence-weighted EPS beat plain EPS at retrieval or dream-cycle
> consolidation?

Given the V-shaped valence–arousal relation in the affective norms (Bradley &
Lang; Warriner et al. 2013) — extreme charge in *either* direction raises
arousal — `sal` and `|φ|` should partly duplicate each other. **If valence adds
nothing beyond what salience already captures, it is a redundant channel and
should be cut.** Run the head-to-head before writing any RFC, not after.

### 6.1 The redundancy half: answered. The retrieval half: still open.

**Answered — valence is not redundant.** `sal` was taken from the arousal column
of Warriner et al. (2013) and *only* that column, because hand-authoring `sal`
would have encoded `|lat|` and confirmed this hypothesis spuriously. On
never-seeded nodes `|φ|` and `sal` correlate at **r = +0.102** — about 1% shared
variance. The V-shape is real in the source data (+0.281) but far too weak to
justify cutting the channel. Valence carries ~99% independent variance.

**Still open — whether valence-weighted EPS is *better*.** It re-ranks, but the
magnitude is a free parameter: `EPS × (1 + λ|φ|)` gives Spearman +0.932 at
λ=0.5 and +0.591 at λ=10. Choosing λ, or declaring a winner, needs a retrieval
quality metric that does not exist in this corpus. **"Different ranking" is not
"better ranking,"** and this half of the criterion still gates the RFC.

Full detail: `TIER1_RESULTS.md` §6.

---

## 7. Deferred — known-hard, do not build a spec on these yet

### 7.1 Ambivalence needs two channels

`φ: V → ℝ²≥0`. Doubles memory, complicates convergence. Defer until scalar
demonstrably fails in a way that two channels would fix.

### 7.2 Context-dependence wants sheaves

*Rain* for a farmer vs. *rain* for a wedding. `φ` is properly a **section of a
bundle over the graph**, not a function on it. Cellular sheaves and the sheaf
Laplacian (Hansen & Ghrist 2019) are the right generalization, and would also
subsume §2.3's sign-as-projection problem — edge types become restriction maps
rather than scalars.

Live research. Not settled machinery. Do not spec against it.

### 7.3 Directed edges

Symmetrization (§1.2) is a real loss. Non-symmetric Laplacians break the
spectral results. Open.

**Partially addressed for one type.** TTDB-RFC-0003 v1.1 §7 (minted 2026-08-01)
introduces *symmetric* types, of which `opposes` is the first. For those,
symmetrization loses nothing — the relation is genuinely mutual, and both
directions are written explicitly since §2 of that RFC still forbids inferring
reverses. This does not solve the general problem: `depends_on` and `refines`
remain directed and are still being flattened.

---

## 8. Where this leads (framing for outside readers)

Ordered by defensibility, strongest first:

1. **Contradiction-finding in a spec corpus.** RFC-12 supersedes RFC-4, but
   RFC-19 still builds on RFC-4. Nobody notices until something breaks.
   Checkable ground truth — you go look and the flagged node is either tangled
   or it isn't. Generalizes to legal codes, regulatory compliance, codebases
   with deprecation edges.
2. **Belief-state debugging in an autonomous agent.** Agent 32 can point at
   which of its beliefs cannot all be true together. Genuinely different
   failure mode from "confidently wrong." Interesting *because* it runs on a
   microcontroller.
3. **Sensor mesh as physical field.** Tangible; makes graph Laplacians legible
   to people who bounce off the math.
4. **Disagreement mapping in a discourse corpus.** Most likely to produce
   confident nonsense — edge signs in real discourse are ambiguous in ways RFC
   types are not. Aspiration only.

The idea worth communicating to a curious non-specialist: this is a formal
claim that an agent's affective state and its knowledge structure are the same
object viewed two ways, and that incoherence in one shows up as measurable
topology in the other.

---

## 9. Provenance of claims — what is established vs. what is ours

**Established literature:**
- Signed Laplacian, balance theory, spectral balance criterion
- Frustration index NP-hardness
- Harmonic extension, maximum principle, label propagation
- Graph-based sentiment lexicon induction
- Osgood evaluation-as-first-factor
- Russell circumplex; Lewin's original borrowing of *valence* from chemistry
- V-shaped valence–arousal relation in affective norms
- Sleep-to-forget/sleep-to-remember (Walker & van der Helm 2009) — the REM
  affective-decoupling parallel to the Dream Cycle
- Cellular sheaf Laplacians (recent, active)

**Ours / speculative — still unrun:**
- Mood-as-DC-component, emotion-as-high-frequency (§1.6)
- `@PERCEPT:before/after` as the ρ source (§4)
- Valence field over a hardware mesh (§5)
- Extension of the Alexander duality framing to ambivalence (§1.7)

**Ours / now empirically supported (Tier 1, `TIER1_RESULTS.md`):**
- Signed diffusion recovers a known valence field on a TTDB store from ~12
  seeds — r = +0.941 against external human norms on never-seeded nodes. The
  *method* is standard (harmonic extension); what is ours is that it works on
  this data structure.
- Frustration detection localizes a real structural contradiction in a real spec
  corpus. **n = 1**, and the contradiction was already known in prose — what was
  new is that it was found without reading the corpus. Do not upgrade this to a
  precision/recall claim.
- Valence is not redundant with salience — r = +0.102 against arousal-derived
  `sal` on unseeded nodes. This *weakens* a prior of ours, and is stated because
  it cuts against the tidier story.

Keep this separation when drafting anything public. The existing corpus has
credibility precisely because it doesn't blur it — and note that two of the
three supported items above carry their own limits in the same breath. That is
the format to keep.

---

## 10. Files

- `ttdb_valence.py` — Tier 1 implementation. Stdlib only. Format assumptions in
  the top block (`NODE_TOKEN`, `NODE_DECL_RE`, `RELATES_RE`, `EDGE_RE`,
  `EW_OPEN_RE`, `FIELD_RE`); `SIGN_MAP` and `EXCLUDE_TYPES` below it.
- `TIER1_RESULTS.md` — what actually happened. Read this alongside §3 and §6.
- `SIGN_MAP_PROPOSAL.md` — the sign assignments and the evidence for each,
  written before the run so they could not be fitted to it.
- `seeds.feelings.tsv` — the 12 Tier 1 seeds, values from the store's own
  declared globe mapping.
- `arousal_from_norms.py` — derives `sal` from published arousal norms. Read its
  header before touching salience by hand; the reason it exists is that
  hand-authored `sal` silently encodes valence.
- `seeds.example.tsv` — seed file format reference.

**Evidence status.** The original note here read: *"Verified end-to-end on a
synthetic fixture: parses, converges (66 iters), LOO r = +0.97 vs baseline, both
nulls separate. The synthetic fixture was constructed to work. It proves the code
runs. It proves nothing about the real store."*

That caution was correct and has been discharged. The parser did not work on a
real store at all — it matched zero records against the canonical
TTDB-RFC-0001 §3 header format, which is exactly the silent-flat-field failure
§3.2 warns about. After repair, on `feelings_ttdb.md`:

- 41 records, 73 valence-bearing edges, 0 malformed — the store as it stood
  when these numbers were taken. It now carries 95, after 22 `opposes` edges
  were minted (§7.3); those postdate every figure below and, being authored
  between coordinate-mirrored pairs, must never be used to restate them
- free-node r = **+0.946** against the store's own coordinates
- free-node r = **+0.941** against *external* human norms (Warriner et al. 2013),
  on nodes that were never seeded — the evidence that does not depend on this
  repository at all
- both nulls separate on energy, p < 0.004

The synthetic fixture is no longer the only evidence, and the external
correlation is the number to quote if only one is quoted.
