#!/usr/bin/env python3
"""
arousal_from_norms.py - derive a salience side-table for feelings_ttdb.md from
published affective norms.

WHY THIS EXISTS, AND WHY IT MUST NOT BE DONE BY HAND
----------------------------------------------------
VALENCE_FIELD.md §6 asks whether `sal` and `|phi|` duplicate each other, on the
reasoning that extreme valence in either direction raises arousal (the V-shaped
valence-arousal relation). If that redundancy holds, valence is a wasted channel
and should be cut.

That question cannot be answered with hand-authored `sal`. The intuitive way to
score the salience of *Rage* or *Serenity* is to ask how strongly it registers --
which in feelings_ttdb.md IS |lat|, i.e. |phi_true| exactly. Hand-assigned
salience encodes valence by construction and returns a strong spurious
confirmation of the very hypothesis under test.

So `sal` is taken from a source blind to valence: the AROUSAL column of the
Warriner norms, and only that column. Valence is never read into `sal`.

SOURCE
------
Warriner, A. B., Kuperman, V., & Brysbaert, M. (2013). Norms of valence,
arousal, and dominance for 13,915 English lemmas. Behavior Research Methods,
45(4), 1191-1207. doi:10.3758/s13428-012-0314-x

The ratings file is distributed under CC BY-NC-ND 3.0, which is NOT the same
license as this repository (MIT). This script regenerates the derived table on
demand so the norms need not be vendored; see LICENSE NOTE in
arousal.feelings.tsv before committing that file to a public tree.

USAGE
-----
    python arousal_from_norms.py path/to/Ratings_Warriner_et_al.csv \\
        [--store feelings_ttdb.md] [--out arousal.feelings.tsv]

MATCHING RULES (deliberately strict -- see "unset, not inferred" below)
    exact       record title is a single lemma present in the norms
    verb lemma  "To Nurture" -> "nurture"; the intent's verb is looked up
    unset       hyphenated compounds (Self-Compassion) have no lexicon entry,
                and the head word would discard the self-directedness that the
                store's longitude encodes. Non-affective records (the umwelt,
                the story record, Discovery Settings) are likewise skipped.

Records with no match are LEFT UNSET rather than filled by inference. A guessed
value here is exactly the contamination this script exists to avoid.
"""

import argparse
import csv
import re
import sys

AROUSAL_MIN, AROUSAL_MAX = 1.0, 9.0   # Warriner rating scale
SAL_MAX = 255                          # TTDB-RFC-0005 field range


def load_arousal(path):
    """Load ONLY the arousal column. Valence is deliberately not read."""
    out = {}
    with open(path, newline='', encoding='utf-8') as fh:
        rd = csv.DictReader(fh)
        if 'A.Mean.Sum' not in rd.fieldnames:
            sys.exit("!! no 'A.Mean.Sum' column -- is this the Warriner ratings file?")
        for row in rd:
            try:
                out[row['Word'].strip().lower()] = float(row['A.Mean.Sum'])
            except (ValueError, KeyError):
                continue
    return out


def parse_records(store):
    """(address, lat, title) for every record, title from its first heading."""
    lines = open(store, encoding='utf-8').read().split('\n')
    recs = []
    for i, line in enumerate(lines):
        m = re.match(r'^(@LAT(-?\d+)LON-?\d+)\s*\|', line)
        if not m:
            continue
        body = '\n'.join(lines[i + 1:i + 18])
        t = re.search(r'^##+ (.+)$', body, re.M)
        recs.append((m.group(1), int(m.group(2)),
                     t.group(1).strip() if t else None))
    return recs


def lemma_for(title, lat):
    """Return (lemma, how) or (None, why-not)."""
    if title is None:
        return None, 'no title'
    if abs(lat) > 40:
        return None, 'non-affective record (outside the +-40 valence band)'
    key = title.lower().strip()
    if key.startswith('to '):
        return key[3:].strip(), 'verb lemma'
    if '-' in key:
        return None, 'hyphenated compound - no lexicon entry'
    return key, 'exact'


def to_sal(arousal):
    """Linear map of the 1-9 arousal scale onto the 0-255 TBEW field."""
    frac = (arousal - AROUSAL_MIN) / (AROUSAL_MAX - AROUSAL_MIN)
    return round(max(0.0, min(1.0, frac)) * SAL_MAX)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('ratings', help='Ratings_Warriner_et_al.csv')
    ap.add_argument('--store', default='feelings_ttdb.md')
    ap.add_argument('--out', default='arousal.feelings.tsv')
    args = ap.parse_args()

    arousal = load_arousal(args.ratings)
    print(f'arousal entries loaded: {len(arousal)}  (valence column not read)')

    hits, misses = [], []
    for addr, lat, title in parse_records(args.store):
        lemma, how = lemma_for(title, lat)
        if lemma and lemma in arousal:
            hits.append((addr, title, lemma, arousal[lemma], to_sal(arousal[lemma]), how))
        else:
            misses.append((addr, title, how if lemma is None
                           else f'"{lemma}" not in lexicon'))

    with open(args.out, 'w', encoding='utf-8', newline='') as fh:
        fh.write('# Derived salience for feelings_ttdb.md -- DO NOT HAND-EDIT.\n')
        fh.write('# Regenerate with arousal_from_norms.py; see that file for why.\n#\n')
        fh.write('# sal = round((arousal - 1) / 8 * 255), from the AROUSAL column only.\n')
        fh.write('# Valence plays no part in this mapping -- that is what makes the\n')
        fh.write('# VALENCE_FIELD.md section 6 redundancy test non-circular.\n#\n')
        fh.write('# SOURCE: Warriner, Kuperman & Brysbaert (2013), Behavior Research\n')
        fh.write('# Methods 45(4), 1191-1207. doi:10.3758/s13428-012-0314-x\n')
        fh.write('# LICENSE NOTE: the source ratings are CC BY-NC-ND 3.0, which is not\n')
        fh.write('# this repository\'s MIT license. Decide deliberately before committing\n')
        fh.write('# this file to a public tree; it can be regenerated instead.\n#\n')
        fh.write('# address\tsal\tarousal\tlemma\tmatch\n')
        for addr, title, lemma, a, sal, how in sorted(hits, key=lambda r: -r[3]):
            fh.write(f'{addr}\t{sal}\t{a:.2f}\t{lemma}\t{how}\n')
        fh.write('#\n# UNSET (not inferred -- a guess here would contaminate the test):\n')
        for addr, title, why in misses:
            fh.write(f'#   {addr}\t{title}\t{why}\n')

    print(f'matched {len(hits)} / {len(hits) + len(misses)} records -> {args.out}')
    print(f'unset (not inferred): {len(misses)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
