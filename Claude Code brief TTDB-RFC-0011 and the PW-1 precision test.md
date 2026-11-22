# Claude Code brief: TTDB-RFC-0011 and the PW-1 precision test

Nov 22, 2026 · @Dan Ray

## How to use this brief

This brief covers two jobs in two repos: add TTDB-RFC-0011 to `toot-toot-engineering`, then run falsifier PW-1 offline in the `robot_team` checkout that holds the 78 archived TTDBs. Export this doc as Markdown, save it as `BRIEF-RFC-0011.md` at the root of each checkout, and paste the prompt from the last section into Claude Code.

Have these on hand before you start:

- **The RFC file.** Use `TTDB-RFC-0011-Precision-Weighting-and-the-Ignition-Filter.md` from our chat, saved into `toot-toot-engineering/RFCs/`. The `ttdb-rfc-0011.patch` file does the same and also adds the `INDEX.md` and `rfc.ttdb.md` entries (`git apply ttdb-rfc-0011.patch`).
- **The `robot_team` checkout**, with the archive directory TTDB-RFC-0010 calls `master/` (the 78 TTDBs) and the existing parsers (`companion.py`, `sid_probe`).
- **Python 3.10+** and nothing else. PW-1 is laptop-only: no firmware, flashing or radio.

Part 1 takes about 15 minutes and is pure file work. Part 2 is the real work. Its result decides whether stages 3–7 of the RFC happen at all.

## Part 1: Add TTDB-RFC-0011 to toot-toot-engineering

Part 1 puts the RFC in the repo and tightens PW-1 before anything runs, so the test cannot be tuned after the fact.

1. On a new branch `rfc-0011-precision`, apply `ttdb-rfc-0011.patch`. If you only have the `.md` file, copy it into `RFCs/` and add the two entries by hand:
   - `INDEX.md`: one line under the TTDB section, after TTDB-RFC-0010.
   - `rfc.ttdb.md`: a record `@LAT10LON11` between `@LAT10LON10` and `@LAT20LON1`, with `[ew] conf:120 rev:0 sal:130`, edges `depends_on` 0005/0006/0007/0010 and `refines@LAT10LON5`.
2. Check that the lanes are still free. Grep both repos for `LAT103` and `LAT104`. If either is already in use, stop and ask Dan which lanes to use instead. Don't renumber them yourself.
3. Check the SALIENT toot type. Find the real toot type enum in `robot_team` firmware. If type `14` is already taken, change §6.3 to the next free number and leave it marked provisional.
4. **Amend §8 PW-1 before running it.** As written, PW-1 can be passed by picking different `pe_span` and `prec_scale` values per channel, because those constants alone move `π` around. Replace the PW-1 row with the pre-registered protocol in Part 2 below: a fixed `prec_scale`, `pe_span` set from physical ranges, and a split-half stability check. Add a changelog row: `2026-11-22 | 0.1.2 — PW-1 pre-registered (constants fixed from physical ranges; split-half stability added)`.
5. Commit with the message `TTDB-RFC-0011 v0.1.2: precision weighting and the ignition filter (proposed)`. Don't push until Dan has read the diff.

## Part 2: The PW-1 replay test

PW-1 asks one question: does `π` learned from archived residuals differ between channels, and stay put within a channel? If it doesn't, the gain rule falls back to fixed steps and the RFC stops at stage 2.

### Inputs

- Every TTDB under `robot_team/master/`. Count them and report the count. The RFC assumes 78.
- Evidence lanes `@LAT94`–`@LAT97` only. Never read `@LAT101` (a FIELD lane, which TTDB-RFC-0010 §6.1 forbids as a source of measured quantities).
- A series is one `(node_id, channel)` pair, ordered by stream `t_ms`. Restart the series whenever the stream id changes, and never compute a residual across two streams.
- Before writing any parser, open three real records from each lane and print their bodies. Reuse `companion.py`'s record and run-length parsing rather than writing new regexes.

### Residuals: prediction = the previous window

| Lane | Channel | `pe` (0–255) | `pe_span` source |
| --- | --- | --- | --- |
| `@LAT94` | acoustic | \|levelₜ − levelₜ₋₁\| × 255 / `pe_span` | Full-scale level from the firmware constant |
| `@LAT95` | motion | \|magnitudeₜ − magnitudeₜ₋₁\| × 255 / `pe_span` | IMU full-scale range from the firmware config |
| `@LAT96` | entity | Jaccard distance of BSSID sets × 255 | none (already 0–1) |
| `@LAT97` | link | \|meanRSSIₜ − meanRSSIₜ₋₁\| × 255 / 100, per peer, pooled per node | 100 dB (−120 to −20 dBm) |

Take `pe_span` from firmware headers or datasheets, never from the archive. Write each value and its file and line into the report *before* running the fold. If a constant can't be found, stop and ask Dan.

If a field named above doesn't exist in a lane, use the lane's primary scalar and say which one you used. Clamp `pe` to 255.

⚠ **Run-length.** `@LAT95` (and possibly other lanes) logs only on change, so unchanged windows are folded into a run count. A run of `n` windows means `n − 1` zero residuals. Compute every result twice, once with runs expanded and once without, and report both. Skipping the zeros biases `π` low on exactly the change-triggered channels.

### The fold

Use the RFC §4.3 integer fold exactly, in Python with explicit `//` and `>>`:

```
var = 0
for r in residuals:
    var += ((r*r) - var) >> 4      # pi_alpha = 4
pi = (255 * PI_SCALE) // (PI_SCALE + var)
```

Set `PI_SCALE = 8192` for every channel. Also compute `π` from the plain (non-EWMA) mean of `r²` as a cross-check. If the two disagree by more than 24, flag it: the series is drifting.

Add a unit test with a hand-worked series of 5 residuals and their expected `var` and `π`, so Dan can check the arithmetic on the ESP32 later.

### Pre-registered decision rule

Only series with at least 30 residuals count, the same minimum as the TTDB-RFC-0010 baseline gates.

| Check | Measure | Pass | Kill |
| --- | --- | --- | --- |
| Separation | Range of per-channel median `π` across nodes | > 32 | ≤ 16 |
| Stability | Chronological split-half: share of series with \|π₁ − π₂\| ≤ 24, both halves ≥ 30 | ≥ 70 % | < 50 % |
| Robustness | Channel rank order by median `π` at `PI_SCALE` = 4096, 8192, 16384 | Same order at all three | Order changes |

PW-1 **passes** only if all three pass. It **kills** the RFC if Separation or Stability kills. Anything else is **inconclusive**: report it, and don't change the thresholds.

## Deliverables and guardrails

The test leaves three files in `robot_team/tools/pw1/` and changes no existing file.

| File | Contents |
| --- | --- |
| `pw1_fold.py` | Parser, residuals, fold and decision rule. Read-only on `master/`; takes paths as arguments |
| `test_pw1_fold.py` | The 5-residual hand-worked case, plus one tiny synthetic TTDB per lane |
| `PW1-REPORT.md` | The pre-registered constants with their sources; a table of node · channel · n · π (EWMA) · π (mean) · π₁ · π₂, with runs expanded and not; the three checks; the verdict |

The verdict line is the first line of the report: `PW-1: PASS | KILL | INCONCLUSIVE`, followed by the one number that decided it.

Guardrails for Claude Code:

- **Never write to `master/`** or to any TTDB. Open the archive read-only.
- **Fix the constants first.** Commit `pe_span`, `PI_SCALE` and the thresholds in a first commit, before any code reads the archive. Their sources go in the message.
- **Never tune after looking.** If the result is uncomfortable, report it as it is. A KILL is a valid outcome and gets written back to the RFC as a result, as TTDB-RFC-0009 §9.1 does with a blockage.
- **Exclusions get logged.** List every skipped file, record or series and why. An unparseable record counts as an exclusion, not an error to fix by guessing.
- **Report the surprises.** If a lane's format differs from what the RFCs say, note it in the report as a candidate `lat 98` divergence belief for `rfc.ttdb.md`. Don't fix the RFC to match.

## Prompt to paste into Claude Code

Start Claude Code in the parent folder that holds both checkouts, then paste:

```
Read BRIEF-RFC-0011.md and follow it exactly, in order.

Part 1 (toot-toot-engineering): create branch rfc-0011-precision, add
TTDB-RFC-0011 using the patch or file I've put in RFCs/, run the lane and
toot-type checks, amend PW-1 to the pre-registered protocol in Part 2,
and commit. Do not push.

Part 2 (robot_team): before writing the fold, print three real records
from each of lanes @LAT94-97 and show me which fields you'll use. Then
find pe_span for each channel in the firmware and commit the constants
with their sources, before any code reads master/. Then write
tools/pw1/pw1_fold.py and its tests, run it read-only over master/, and
write PW1-REPORT.md with the verdict as the first line.

Stop and ask me if a lane is taken, a constant can't be found, or the
archive count isn't 78. Never change a threshold after seeing data.
```

The prompt has two built-in pauses: the field check and the constants commit. Each is a chance to catch a wrong assumption before it affects the result.
