# Tier 1 Results

**Run date:** 2026-08-01
**Sign map:** as proposed in `SIGN_MAP_PROPOSAL.md` (hub excluded, φ =
endorsement for the RFC stores, the two stores run as separate graphs), with two
later changes: **`opposes: −1`** added when that type was minted (§7.5), and
**`amends` reclassified −1 → +1** once the criterion existed to judge it (§3.2).
Results in §§1, 6 were measured before either change and are unaffected —
neither type occurs in the propagation graph.
**Reproduce:**

```bash
python research/valence/ttdb_valence.py feelings_ttdb.md \
    --seeds research/valence/seeds.feelings.tsv --gamma 0.05 --trials 500
```

---

## Verdict

**Propagation passes decisively, and is corroborated against external human
norms at r = +0.941 on never-seeded nodes (§6.2). Valence is not a redundant
channel (§6.3). Balance is a weaker story than first written: on the RFC corpus
it is real but uninformative, because imbalance there is structurally guaranteed
(§3.3); on `feelings_ttdb.md` it became measurable only after `opposes` was
minted, and returns *balanced* (§7.6). The contrast between the two is the part
worth keeping.**

No §6 stop condition was triggered. Three criteria needed repair before they
could be trusted: the seed-shuffle null was measuring the wrong quantity (§4),
the redundancy test was unrunnable until `sal` was sourced from outside the
store (§6.1), and the frustration count was order-dependent and irreproducible
(§3.1).

**Still no RFC.** The retrieval half of §6 remains undecided — see §6.4.

> **Reading note.** Sections marked *Correction* record where an earlier draft
> of this document was wrong. They are kept rather than silently rewritten,
> because the corrections are the more useful artifact: §1.1, §3.1, §3.2, §3.3,
> §4, §7.3.

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

### 1.1 The hub exclusion matters, and its size depends on seed density

An earlier draft of this section claimed the hub exclusion alone flipped LOO r
from −0.963 to +0.948. **That was wrong** — it compared a 4-seed smoke test
against the 12-seed protocol run, conflating hub exclusion with a threefold
increase in seeds. Isolating the two factors (γ=0.15):

| Seeds | Hub edges | LOO r | LOO MAE |
|---|---|---|---|
| 4 (ad hoc) | included | **−0.952** | 0.745 |
| 4 (ad hoc) | excluded | +0.719 | 0.440 |
| 12 (protocol) | included | +0.899 | 0.374 |
| 12 (protocol) | excluded | **+0.948** | 0.173 |

Hub inclusion is genuinely damaging at both seed counts, but **the damage scales
inversely with seed density**. With sparse seeds the degree-55 origin dominates
and inverts the field; with well-spread seeds it merely blurs it.

The effect is much clearer on free nodes than on LOO, because LOO scores only
the 12 seeds — which are well-connected by construction — while the blurring
lands on everything else (γ=0.05):

| Hub edges | Free-node r | Free-node MAE |
|---|---|---|
| Included | +0.788 | 0.384 |
| Excluded | **+0.946** | **0.169** |

The decision was made from the store's semantics — the hub asserts membership,
not valence — before any of these numbers existed. That ordering is what keeps
it from being outcome-fitting.

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

### 1.3 The boundary-seed alternative is rejected

`SIGN_MAP_PROPOSAL.md` §1.2 offered an alternative to excluding the hub: keep
the 55 edges at +1 but pin `@LAT0LON0 = 0.0` as a fixed boundary node,
preserving the membership structure while stopping the origin from floating.
Tested head-to-head (12 seeds, γ=0.05):

| Config | Edges | Components | Seedless | Free-node r | MAE |
|---|---|---|---|---|---|
| **A — hub excluded** | 49 | 6 | 3 | **+0.946** | **0.169** |
| B — hub kept, origin pinned 0.0 | 87 | 3 | 2 | +0.787 | 0.398 |
| C — hub kept, unpinned (control) | 87 | 3 | 2 | +0.788 | 0.384 |

**B ≈ C.** Pinning the origin changes essentially nothing — it is very slightly
*worse* on MAE than not pinning. The damage is done by the 55 hub edges
themselves dragging every affective state toward a common value, not by the
origin's own value being unconstrained, so fixing that value repairs nothing.

Exclusion stands. It costs connectivity — 6 components against 3, and one extra
seedless component — and buys a large accuracy gain. **The connectivity cost is
the honest price and is not recovered by this alternative;** recovering it needs
more or better-spread seeds, not a different treatment of the hub.

### 1.4 Caveats that must travel with this result

- **One seed cannot be scored.** `@LAT30LON40` (Compassion) predicts 0.000 under
  leave-one-out because it lands in a seedless component when held out. That is
  a connectivity artifact, not a miss. It contributes a 0.75 error to the
  reported MAE; excluding it gives MAE ≈ 0.121.
- **Excluding the hub fragmented the graph** into 6 components (largest 20 of 43
  nodes), 3 of them seedless. This is a real and unrecovered cost — the
  boundary-seed alternative that might have repaired it does not (§1.3).
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

**This is repairable, and §7 shows how.** The store has 11 antonym pairs it
cannot currently express as edges; supplying them makes the balance experiment
runnable, whereupon it returns a real answer — the affective landscape is
provably *balanced*, in contrast to the RFC corpus in §3.

---

## 3. Balance on the RFC corpus — ran, but the result is weaker than first reported

φ = endorsement. Both RFC stores as one graph. **An earlier draft of this
section overclaimed, in three ways that are corrected below.**

### 3.1 Correction 1 — the violation count is order-dependent

The earlier draft reported *"Greedy 2-coloring: 2 violating edges"* and argued
*"on a connected graph the coloring is forced once any node is fixed, so this is
not a traversal-order artifact."*

**That reasoning is wrong.** The coloring is forced only along a spanning tree;
when a conflict appears, *which* edge gets blamed depends on visit order. Over
2000 random traversal orders the count ranged **2 to 28**. The earlier figure of
2 happened to be the minimum, reported as though it were stable.

Worse, the function iterated a Python `set`, so it silently gave different
answers in different processes — a reproducibility bug that would have surfaced
as an unexplainable number change. It now iterates `sorted(nodes)`, and the
docstring says plainly not to quote the value as stable.

What *is* order-independent is the balance **decision**, and that decision is
polynomial — only the minimum-deletion frustration *index* is NP-hard. There was
never a reason to infer balance from a greedy count. `is_balanced()` now decides
it exactly: contract the positive-only components, flag any negative edge inside
one, then test the contracted negative multigraph for bipartiteness. Across all
2000 orders the graph was unbalanced every time, and the exact test agrees.

### 3.2 Correction 2 — two of the three "contradictions" were mine

Of the three negative edges originally reported:

| Edge | Verdict |
|---|---|
| `@LAT40LON2` ↔ `@LAT40LON5` (`amends`/`amended_by`) | **Not opposition.** Sign map error — see below. |
| `@LAT98LON0` → `@LAT40LON1` (`refines`) | **Spurious edge.** Removed from the store. |
| `@LAT40LON4` ↔ `@LAT98LON0`, `@LAT40LON5` ↔ `@LAT98LON3` (`contradicts`) | Genuine. |

**`amends` was mis-signed at −1.** `SIGN_MAP_PROPOSAL.md` §2.2 flagged it as the
one real judgment call and guessed wrong. The criterion now exists, in the
taxonomy minted in §7: TTDB-RFC-0003 v1.1 §7.2 requires that opposition means *at
most one endpoint is true*. A32-RFC-0002 Amendment A does not make A32-RFC-0002
false — it extends it, and both are Stable and current. That is agreement.
Reclassified to **+1**, which is a pleasing outcome: the vocabulary was minted to
describe an affective store and immediately caught an error in the RFC store.

**`refines@LAT40LON1` on `@LAT98LON0` was simply wrong.** The belief is entirely
about build tooling — arduino-cli, sketch layout, filesystem upload scripts. A32-
RFC-0001 is the architecture overview: offline reasoning, three layers,
umwelt-as-identity, no build content whatsoever. The belief refines nothing in
it. Removed; the record stays connected via `contradicts@LAT40LON4`.

The corpus now reads 124 merged edges, **+122 / −2**, both negatives genuine.

### 3.3 Correction 3 — the imbalance was structurally guaranteed

This is the one that matters, and it undercuts the original framing.

**All 41 nodes form a single positive-only connected component** (122 positive
edges — an RFC corpus where everything `depends_on` a shared foundation). Any
negative edge between two nodes of that mass closes a cycle carrying exactly one
negative edge, and is therefore frustrated **automatically**.

So the finding is not *"the method discovered a hidden contradiction."* It is
*"the corpus contains `contradicts` edges, inside a positively-connected mass."*
Every negative edge frustrates; the measure cannot discriminate among them. The
"frustrated triangle" singled out earlier was one of three, all frustrated for
the same structural reason, and the two survivors remain frustrated now.

This is a close cousin of `VALENCE_FIELD.md` §6's own trivia check — *"frustration
list is topologically trivial (all high-degree hubs) → measuring degree, not
dissonance."* Here it is measuring **positive connectivity**, not dissonance.
`is_balanced()` now warns when one positive component covers >80% of nodes.

### 3.4 What survives

The genuine conflict is real and worth stating, just not as a discovery:

```
@LAT98LON0  --contradicts(-1)--> @LAT40LON4     BELIEF vs A32-RFC-0004
@LAT40LON4  --depends_on(+1)---> @LAT40LON1     A32-RFC-0004 on A32-RFC-0001
```

The belief *"the A32 RFCs say PlatformIO; robot_team uses arduino-cli"*
contradicts A32-RFC-0004, which depends on the shared architecture that the
belief does not dispute. Endorsement cannot be consistently assigned. But this
was **already explicitly typed as `contradicts` by the store's author**, and
already documented in prose at `@LAT40LON4` (*"build tooling superseded in
robot_team — see @LAT98LON0"*). The `lat 98` belief lane exists precisely to
record it. Nothing was found that was not already written down.

**Honest verdict on the balance experiment: it ran, it is correctly implemented
now, and on this corpus it is uninformative.** It would become informative on a
store whose positive relations do *not* form one blob — where some negative edges
frustrate and others do not, and the difference means something. Whether the
corpus can be restructured that way, or whether RFC corpora are simply the wrong
shape for this measure, is open.

The one measurement that did discriminate is in §7.2: the same test returns
**balanced** on `feelings_ttdb.md` and **unbalanced** here. That contrast is real
because the affective store's positive edges do *not* form a single blob spanning
both polarities.

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
1. ~~Run the EPS head-to-head.~~ **Done — see §6. Valence is not redundant
   (r=+0.102 against arousal on unseeded nodes); the retrieval half is still
   open and needs a quality metric.**
2. ~~Decide the `@LAT0LON0 = 0.0` boundary-seed alternative against exclusion.~~
   **Resolved — see §1.3. Rejected; exclusion stands.**
3. Only then consider whether the corpus should mint a negative edge type — a
   TTDB-RFC-0003 taxonomy question, judged on whether the corpus needs to
   express opposition, not on whether it would make this experiment light up.

---

## 6. The EPS head-to-head — ran, on external norms. Valence survives.

The blocker reported in an earlier draft — `sal ≡ 0` across all 40 records of
`feelings_ttdb.md`, so `EPS = sal × (255 − conf)/255` is identically zero — was
resolved the only way it honestly could be: by taking `sal` from a source blind
to valence.

### 6.1 Where `sal` came from, and why it could not be authored

Hand-assigning salience would have destroyed the test. The intuitive way to
score the salience of *Rage* or *Serenity* is to ask how strongly it registers,
which in this store **is** `|lat|` — i.e. `|φ_true|` exactly. Hand-authored
`sal` therefore encodes valence by construction and returns a strong spurious
confirmation of §6's own redundancy hypothesis. The test would appear to run and
be dead on arrival.

`sal` is instead derived from the **arousal** column of Warriner, Kuperman &
Brysbaert (2013) — 13,905 lemmas, ~1,800 raters — via
`sal = round((arousal − 1)/8 × 255)`. The valence column of that dataset is
never read into `sal`. 34 of 41 records matched by exact lemma or, for intents,
the verb (*To Nurture* → `nurture`). The remaining 7 are **left unset, not
inferred**: hyphenated compounds (*Self-Compassion*, *Self-Contempt*) have no
lexicon entry and their head words would discard the self-directedness the
store's longitude encodes; *Unease* and *Equanimity* are absent from the
lexicon; three records are non-affective.

Regenerate with `arousal_from_norms.py`; the derived table is
`arousal.feelings.tsv`.

### 6.2 A free external validation of the store itself

The norms make a check possible that was not previously available: Warriner's
valence ratings are an *independent* measurement of the same 34 emotions, so the
store's hand-authored geometry can be scored against 1,800 human raters.

| Comparison | All matched (n=34) | **Free nodes only (n=23)** |
|---|---|---|
| corr(store `lat`, Warriner valence) | +0.920 | +0.920 |
| corr(**propagated φ**, Warriner valence) | +0.932 | **+0.941** |

Two things follow. First, `feelings_ttdb.md` is a **well-calibrated store** — its
author's coordinate assignment agrees with published norms at r = +0.92.
Second, and more strongly: on the 23 nodes that were *never seeded*, the
propagated field agrees with independent human ratings at **r = +0.941**,
slightly better than the store's own coordinates do.

This is substantially stronger evidence than §1's internal test. §1 scored φ
against `lat`, which is the same quantity the seeds were drawn from. This scores
it against a dataset with no connection to the store, this repository, or the
method.

### 6.3 The §6 redundancy test — valence is NOT redundant

| Correlation with arousal-derived `sal` | All (n=34) | **Free (n=23)** |
|---|---|---|
| \|store `lat`\| | +0.234 | **+0.063** |
| \|propagated φ\| | +0.307 | **+0.102** |
| \|Warriner valence\| *(V-shape in the source data)* | +0.232 | +0.281 |

**On never-seeded nodes, `|φ|` and `sal` share r = +0.102 — about 1% of
variance.** §6's stop condition reads: *"If valence adds nothing beyond what
salience already captures, it is a redundant channel and should be cut."*
Valence carries ~99% independent variance. **The criterion is not met; valence
survives.**

The V-shaped valence–arousal relation is real in the source data (+0.281) but
modest, and the store's own geometry reproduces even less of it (+0.063) — its
intensity dimension is *more* orthogonal to arousal than real affective norms
are. The premise behind §6's redundancy worry holds directionally and is far too
weak to justify cutting the channel.

### 6.4 The retrieval question is still undecided

With real `sal` and real `conf`, EPS is now computable and valence-weighting
does re-rank it — but the magnitude remains a free parameter in
`EPS × (1 + λ|φ|)`:

| λ | 0.5 | 1 | 2 | 5 | 10 |
|---|---|---|---|---|---|
| Spearman vs plain EPS | +0.932 | +0.832 | +0.745 | +0.624 | +0.591 |
| Top-10 overlap | 9/10 | 8/10 | 7/10 | 7/10 | 7/10 |

The re-ranking is more substantial than in the RFC attempt and saturates rather
than collapsing, which is mildly encouraging. But **"different ranking" is still
not "better ranking."** Choosing λ, or declaring a winner, needs a retrieval
quality metric that does not exist in this corpus. That half of §6 remains open.

### 6.5 What this licenses

**Licensed:** valence is not a redundant channel, established against external
norms rather than internal structure. The propagation result of §1 is
corroborated by an independent dataset at r = +0.941 on unseeded nodes.

**Still not licensed:** an RFC. The retrieval half of §6 is unrun, the balance
half is unrun on affective data (§2), and Tier 2's ρ-from-`@PERCEPT` claim is
untouched. What has changed is that the cheapest remaining test that could have
killed the idea was run, and the idea survived it.

### 6.6 License — resolved: the derived table is not committed

The Warriner ratings are **CC BY-NC-ND 3.0**; this repository is **MIT**. That
is a one-way incompatibility — `NC` and `ND` are both restrictions MIT does not
carry, so shipping the derived table inside an MIT tree would promise downstream
users commercial use and modification rights they do not actually have for that
file.

`ND` bites harder on the derived table than it would on the raw dataset:
`arousal.feelings.tsv` rescales arousal (1–9) onto `sal` (0–255) and re-keys it
to TTDB addresses, which makes it an *adaptation* — precisely what `ND` forbids
distributing. Redistributing the untouched source CSV would be safer than this
34-row transform.

(The countervailing argument is real but not relied on: facts are not
copyrightable in the US after *Feist* (1991), the EU database right covers only
"substantial" extraction and this is 0.24% of the rows, and reuse of published
affective norms is universal academic practice. Low risk is not compatibility.)

**Resolution:** `arousal.feelings.tsv` is gitignored. `arousal_from_norms.py` is
committed — it is original code containing no Warriner data — and regenerates
the table byte-identically from the source CSV. Reproducibility is preserved in
full; nobody downstream inherits a file whose stated terms are wrong.

**To reproduce §6 from a clean checkout:**

```bash
# 1. Fetch the norms (CC BY-NC-ND 3.0; not redistributed here)
curl -sLO https://raw.githubusercontent.com/JULIELab/XANEW/master/Ratings_Warriner_et_al.csv

# 2. Regenerate the derived salience table
python research/valence/arousal_from_norms.py Ratings_Warriner_et_al.csv --out research/valence/arousal.feelings.tsv
```

---

## 7. Should the corpus mint a negative edge type?

§5's third recommendation, with its own framing preserved: judged on **whether
the corpus needs to express opposition**, not on whether it would make this
experiment light up.

### 7.1 The representational gap is real

`feelings_ttdb.md` contains 11 clean antonym pairs at mirrored coordinates
`(lat, lon) ↔ (−lat, lon)`:

| | | | |
|---|---|---|---|
| Serenity / Unease | Bliss / Despair | Ecstasy / Rage | Hope / Frustration |
| Pride / Guilt | Contentment / Sadness | Compassion / Hostility | Excitement / Fear |
| Generosity / Contempt | Equanimity / Shame | Self-Compassion / Disappointment | |

**None of the 11 carries any edge.** The store encodes their opposition purely
positionally — the graph cannot say *"Serenity is the opposite of Unease."* A
consumer reading only the edge list, which is what every implementation in this
corpus actually does, cannot recover the single most obvious relation in an
affective landscape.

That is the answer to the question as posed. The gap is representational and
exists independently of anything valence diffusion wants.

### 7.2 What an `opposes` type would change structurally

Simulating 11 `opposes` edges (σ = −1) between the mirror pairs (this was a
simulation when first run; it has since been **minted and written** — see §7.5):

| | As authored | With `opposes` |
|---|---|---|
| Merged edges | 49 | 60 |
| Negative edges | 0 | 11 |
| Components | 6 | 4 |
| **Largest component** | **20 / 43** | **40 / 43** |
| Balance experiment runnable | **no** — sign-shuffle vacuous | **yes** |

Two consequences worth having, neither of which is about prediction accuracy:

1. **The graph stops being fragmented.** All 40 genuine affective states join a
   single component. The three remaining isolates are exactly the non-affective
   records — `@LAT0LON0` (umwelt origin), `@LAT88LON0` (story), `@LAT-90LON0`
   (Discovery Settings) — which *should* be isolated once hub and narrative
   edges are excluded. This directly repairs the connectivity cost that §1.3
   found the boundary-seed alternative could not.

2. **The balance experiment becomes real, and returns an answer.** Frustration
   is 0 of 60 violating edges — and with 11 negative edges present that is a
   *proof* of balance rather than the arithmetic tautology it was in §2. The
   affective landscape is coherently bipolar: every cycle carries an even number
   of negative edges, and no region resists consistent assignment.

That contrast is itself the useful output. The same measurement returns
**balanced** on `feelings_ttdb.md` and **unbalanced** on the RFC corpus (§3) —
the instrument discriminates, which is the thing §6 of `VALENCE_FIELD.md` most
needed to know and could not previously test.

### 7.3 What was deliberately not measured

**Whether adding these edges improves φ's agreement with the Warriner norms.**

The mirror pairs are defined by `(lat, −lat)` — i.e. by the store's valence
coordinates. An `opposes` edge between them asserts "these two have opposite
valence," which is a restatement of the ground truth being predicted. Adding
them would improve valence recovery by construction, and the improvement would
measure nothing but the tautology.

This is precisely the trap §5 warned against, so the number was not computed. It
should not be computed later and quoted as support either.

### 7.4 Recommendation

**Mint the type — on representational grounds, with the structural benefits as
secondary.** Specifically:

- A symmetric `opposes` (or `antonym_of`) type in the TTDB-RFC-0003 taxonomy.
  Symmetry matters: §1.2 of `VALENCE_FIELD.md` requires `σ_uv = σ_vu`, and an
  antonym relation is genuinely mutual, so this is one of the few types where
  symmetrization loses nothing.
- Distinct from `contradicts`, which the RFC corpus uses for *epistemic*
  conflict (this claim and that claim cannot both hold). `opposes` is
  *semantic* polarity (these two sit at opposite ends of a dimension). Collapsing
  them would conflate "these disagree" with "these are antonyms."
- Adding the 11 edges to `feelings_ttdb.md` is a **separate** store-authoring
  decision from amending the taxonomy, and should be taken separately.

### 7.5 Minted — what was changed

Accepted and applied on 2026-08-01, in four places, because this corpus's spec
is an instance of itself and a taxonomy change that lands in only one of them
goes stale immediately:

| File | Change |
|---|---|
| `RFCs/TTN-RFC-0002-Typed-Edges.md` | v1.0 → **1.1**. New *Semantic Polarity* group holding `opposes`, with the distinction from `contradicts` stated inline. |
| `RFCs/TTDB-RFC-0003-Typed-Edges.md` | v1.0 → **1.1**. New §7 (symmetric types; `opposes` semantics; the comparison table; rationale) and §8 changelog. §§1–6 untouched — all 1.0-conformant files remain valid. |
| `RFCs/rfc.ttdb.md` | Records `@LAT10LON3` and `@LAT20LON2` re-compressed to match, `updated`/`touched` bumped, `rev` 0 → 1. |
| `feelings_ttdb.md` | 22 `opposes` edges across the 11 antonym pairs. |

**Both directions were written** (22 edges, not 11). TTDB-RFC-0003 §2 forbids
inferring reverse edges, and §7.1 deliberately did not carve out an exception —
a symmetric type is a convention about meaning, not a change to traversal, so
every existing parser stays correct without modification.

**`rev` was *not* bumped on the 22 affective records** (only `updated` and
`touched`). `rev` is TBEW's revision counter and feeds surprise: bumping it
would assert these beliefs had been *wrong* before. Nothing was corrected — a
relation that always held was finally written down. Bumping `rev` would have
distorted EPS across a fifth of the store to record an act of completion.

`opposes: -1` was added to `SIGN_MAP`, with the §7.3 circularity warning carried
into the code comment so it survives separation from this document.

### 7.6 What the mint actually verified

The store now reads: 60 merged edges (+49 / −11), 4 components, largest **40**,
matching the §7.2 simulation exactly.

**Legitimate:** frustration is **0 of 60**. With 11 negative edges present this
is a *proof* of balance rather than the arithmetic of §2 — and it could have
failed. Had the `resonates_with` / `intensifies_into` / `enables` structure
disagreed anywhere with the antonym partition, a frustrated cycle would have
appeared. None did. The positive relational structure and the polarity structure
are mutually consistent.

**Not legitimate, and not claimed:** the accuracy gain, and the sign-shuffle
null now returning p ≈ 0. The `opposes` edges were authored between
coordinate-mirrored pairs, so both the field's improvement *and* the sign
structure's apparent informativeness restate the ground truth being predicted.
§7.3 applies to both. The externally-validated numbers that stand are the ones
in §6.2, measured **before** these edges existed.
