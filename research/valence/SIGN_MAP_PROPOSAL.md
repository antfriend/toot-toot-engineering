# SIGN_MAP Proposal — Phase 4 input

**Status:** proposal, nothing applied. `SIGN_MAP` in `ttdb_valence.py` is
unchanged pending review.
**Purpose:** assign signs to the 36 edge types actually present in the corpus
(19 across the two RFC stores, 17 in `feelings_ttdb.md`, no overlap), with the
evidence for each, before Tier 1 runs.
**Read first:** `VALENCE_FIELD.md` §1.2 (signs are mandatory) and §2.3 (the sign
map is the only place real modeling judgment enters).

---

## 0. The criterion, stated precisely

The energy being minimized is

```
E(φ) = ½ Σ_uv w_uv (φ(u) − σ_uv φ(v))²
```

so `σ` answers exactly one question:

> **Does this edge assert that its two endpoints carry the SAME valence, or
> OPPOSITE valence?**

It does **not** mean "is this relationship good or bad." `blocks` sounds
negative and is `−1` in the current stub map, but only because A blocking B
implies they cannot both be endorsed — not because blocking is unpleasant.
Getting this backwards is the easiest available mistake and it silently
produces a plausible-looking field.

A third value is needed and the machinery already supports it:

- `+1` — endpoints should agree
- `−1` — endpoints should oppose
- **`0` — the edge asserts nothing about valence and must be excluded**

`0` is expressed as a `WEIGHT_MAP` entry of `0.0`; `build_adjacency()` already
drops zero-weight pairs. Without this third option, structurally meaningful but
affectively neutral edges get forced to `+1` and actively destroy the field
(§2 below). Recommend adding an explicit `EXCLUDE` set so the intent is legible
rather than hidden in a weight table.

---

## 1. `feelings_ttdb.md` — 17 types, 134 edges

The store declares `lat = valence` in its `mmpdb.umwelt.globe.mapping`, so every
assignment below is **checkable against the latitude of the endpoints**, not
inferred from the type name. That is the whole reason this store is the Tier 1
target.

### 1.1 Same-valence — propose `+1` (73 edges)

| Type | n | Evidence (endpoint latitudes) |
|---|---|---|
| `resonates_with` | 36 | +30↔+20, −30↔−20, +40↔+30, +10↔+10 — never crosses zero |
| `enabled_by` | 9 | +30←+10, +30←+20, +40←+40 |
| `enables` | 7 | +20→+30, −30→−40, +40→+40 |
| `can_become` | 6 | +30→+40 |
| `can_deepen_into` | 4 | +10→+20, +20→+30, −10→−20, −20→−30 |
| `intensified_from` | 4 | +40←+30, −40←−30 |
| `can_intensify_into` | 4 | symmetric counterpart of the above |
| `intensifies_into` | 2 | +30→+40, −30→−40 |
| `opens_toward` | 1 | +10→+10 |

Every one of these preserves sign and increases |lat|. They encode intensity
gradients within a valence polarity, which is precisely `+1`.

### 1.2 Hub edges — propose `0`, exclude (55 edges)

| Type | n | Target |
|---|---|---|
| `feels` | 13 | `@LAT0LON0` |
| `is_disposition_of` | 11 | `@LAT0LON0` |
| `disposed_toward` | 11 | from `@LAT0LON0` |
| `emotes` | 8 | `@LAT0LON0` |
| `is_intent_of` | 6 | `@LAT0LON0` |
| `intends` | 6 | from `@LAT0LON0` |

**All 55 touch the neutral origin**, giving `@LAT0LON0` degree 55 in a
41-record store. These edges assert "this affective state belongs to the
experiencer" — a membership claim, not a valence claim. Serenity (+10) and
Unease (−10) both point at the origin; at `+1` the solver is instructed to make
both agree with a neutral node and therefore with each other.

This is not hypothetical. The Phase 3 smoke test with all types defaulted to
`+1` returned **LOO r = −0.963** — held-out seeds predicted with reversed sign,
the signature of a hub smearing opposite polarities together. Excluding these 55
is the single highest-leverage decision in this document.

*Alternative worth considering:* keep them at `+1` but seed `@LAT0LON0 = 0.0` as
a fixed boundary node. That preserves the membership structure while pinning the
hub, and is closer to the store's own semantics. Untested; excluding is the
safer Tier 1 default.

### 1.3 Narrative edges — propose `0`, exclude (6 edges)

| Type | n | Traversal |
|---|---|---|
| `plays` | 5 | +10 → −10 → −30 → −30 → +20 → +30 |
| `starts_at` | 1 | entry point of the arc |

These belong to `@LAT88LON0` ("Story: The Hero's Arc — from serenity through
darkness and back to joy"). The arc **deliberately crosses valence**; that is
what makes it a story. They encode traversal order, which is exactly
TTDB-RFC-0009's claim that pattern targets are stored as traversal order, and
they parallel the `ttdb-scene` block in the same record — render hints under
TTDB-RFC-0003 §5, not epistemic assertions.

Tempting to call them `−1` since they cross polarity. Resist it: a `−1` asserts
*consistent* opposition, and a six-beat arc crossing zero twice is not that.

### 1.4 Two records are not affective states

`@LAT88LON0` (the story record) and `@LAT-90LON0` ("Discovery Settings") sit
outside the ±40 band that every genuine affective state occupies. They are
metadata, and their latitudes are addressing, not valence — reading ground truth
off them would assign Discovery Settings a valence of −2.25.

Both drop out naturally under the proposals above: `@LAT-90LON0` already carries
no edges in either direction, and `@LAT88LON0` retains only the excluded
narrative edges, leaving it at degree 0. Worth asserting explicitly in the run
rather than relying on that coincidence.

### 1.5 What survives

**73 valence-bearing edges over 39 affective records, with ground truth
`φ_true(v) = lat(v) / 40`.** That is a real Tier 1 propagation experiment.

---

## 2. `agent-memory-system_ttdb.md` and `rfc.ttdb.md` — 19 types, 146 edges

Over an RFC corpus `φ` cannot mean affect. The only coherent reading is
**endorsement**: is this claim currently load-bearing, or superseded? This
should be stated in the run notes, because it is a different quantity from the
feelings store's valence and the two must not be pooled into one graph.

### 2.1 Propose `+1` — structural agreement

`depends_on` (77), `supports` (19), `refines` (12), `requires` (10),
`derived_from` (5), `demonstrates` (5), `implemented_by` (2),
`propagated_by` (2), `implements` (1), `applied_by` (1), `aligns_with` (1),
`generalizes` (1), `generalized_by` (1), `duplicates` (1)

### 2.2 Propose `−1` — opposition

| Type | n | Rationale |
|---|---|---|
| `contradicts` | 2 | Unambiguous |
| `amends` / `amended_by` | 2 | `@LAT40LON5 amends @LAT40LON2` — the amended portion is displaced by the amending text. Weaker than `contradicts`; flag for review |

### 2.3 Propose `0` — exclude

| Type | n | Rationale |
|---|---|---|
| `renders` | 3 | Presentation relation (viewer renders record). No epistemic content |
| `default_log` | 1 | Pointer to a log location, not a claim |

---

## 3. The finding that governs Phase 4

**After honest assignment the corpus contains at most 4 negative edges out of
280.** Two `contradicts` in `rfc.ttdb.md`, plus the two `amends`/`amended_by` if
that reading is accepted. `feelings_ttdb.md` yields **zero** — its polarity is
carried by coordinates, not by edges.

Consequences, stated before anything runs so they can't be renegotiated after:

1. **The balance / frustration half of Tier 1 is unrunnable.** A signed graph
   with ~zero negative edges is trivially balanced: frustration index 0, greedy
   violation count 0, sign-shuffle a no-op (`p = 1.000`, already observed). This
   is not a negative result about valence — it is the absence of an experiment.
   Reporting it as a §6 stop condition would be wrong.

2. **The propagation half is runnable and genuinely falsifiable** on
   `feelings_ttdb.md`: 73 edges, 41 records, ground truth from latitude. Seed 12
   spread across quadrants, LOO against the mean baseline, both nulls. If
   harmonic extension cannot recover held-out valence on a store whose geometry
   *is* valence, it will not do so anywhere, and §6's stop condition applies
   honestly.

3. **Minting a negative edge type is a TTDB-RFC-0003 amendment**, not a script
   change, and should be judged on whether the corpus needs to express
   opposition at all — not on whether it would make this experiment light up.
   `contradicts` already exists and is used twice; the question is whether
   `supersedes` / an explicit antonym type earns its place in the taxonomy.

---

## 4. Decisions needed before Phase 4 runs

1. **Exclude the 55 hub edges, or pin `@LAT0LON0 = 0.0` as a boundary seed?**
   Recommend exclude for Tier 1, revisit if propagation succeeds.
2. **Is `amends` / `amended_by` genuinely `−1`?** It is the only judgment call
   in §2 and it doubles the negative-edge count from 2 to 4 — which changes
   nothing statistically, so the honest answer may be that it does not matter yet.
3. **Confirm `φ` = endorsement for the RFC stores**, and that the two store
   families are run separately rather than as one graph.
4. **The two dangling edges in `feelings_ttdb.md`** (`@LAT10LON20 →
   @LAT10LON10`, `@LAT-20LON-30 → @LAT-30LON-40`) still need resolving — unlike
   `@LAT77LON7` in `agent-memory-system_ttdb.md`, which is a deliberate
   conformance fixture and must be left broken.
