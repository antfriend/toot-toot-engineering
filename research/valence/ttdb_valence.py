#!/usr/bin/env python3
"""
ttdb_valence.py - Tier 1 signed valence diffusion over a TTDB store.

Solves the signed Dirichlet problem with decay:

    minimize  1/2 * sum_uv w_uv (phi(u) - sigma_uv phi(v))^2  +  gamma/2 * sum_v phi(v)^2
    subject to phi(v) = seed(v) for seeded v

via damped Jacobi. Reports the field, per-node frustration, seed
leave-one-out error, and two permutation nulls.

The nulls are the point. A smooth-looking field over a graph proves
nothing; the question is whether it beats a sign-shuffled or
seed-shuffled version of itself. If it doesn't, the framing is
decoration and you've learned that for the cost of an afternoon.

Pure stdlib. No numpy. Runs anywhere, including on a Pi.

Usage:
    python3 ttdb_valence.py STORE... --seeds seeds.tsv
    python3 ttdb_valence.py STORE... --dump-parse        # ALWAYS DO THIS FIRST
    python3 ttdb_valence.py STORE... --seeds seeds.tsv --csv field.csv

STORE may be files or directories (walked for *.md).
"""

import argparse
import csv
import os
import random
import re
import sys
from collections import defaultdict, deque

# ---------------------------------------------------------------------------
# FORMAT ASSUMPTIONS - edit this block, not the parser below.
# ---------------------------------------------------------------------------

# A node address. Coordinate addressing with an optional namespace prefix
# and optional trailing tag, per TTDB-RFC-0001 §3 and the @BELIEF:/@PERCEPT:
# namespaces of TTDB-RFC-0007/-0008:
#   @LAT20LON3   @LAT-10LON-10   @BELIEF:LAT20LON3   @LAT20LON3:before
NODE_TOKEN = (r'@(?:[A-Za-z][A-Za-z0-9_]*:)?LAT-?\d+LON-?\d+'
              r'(?::[A-Za-z0-9_\-]+)?')

# A record header line. TTDB-RFC-0001 §3 makes this the ONLY thing that
# declares a record:
#   @LATxLONy | created:<int> | updated:<int> | relates:<edge_list>
# Bodies may mention addresses freely (and rfc.ttdb.md quotes the header
# grammar itself in prose); only header lines count, so prose can't inject
# phantom nodes.
NODE_DECL_RE = re.compile(r'^(?P<addr>' + NODE_TOKEN + r')\s*\|(?P<fields>.*)$')

# The relates: field within a header line, up to the next pipe or EOL.
RELATES_RE = re.compile(r'\brelates:\s*(?P<edges>[^|]*)')

# One typed edge from a comma-separated relates: list. Tolerates both
# declared syntaxes in the corpus -- "type@TARGET" (TTDB-RFC-0003 §1
# default, used by agent-memory-system_ttdb.md and rfc.ttdb.md) and
# "type>@TARGET" (feelings_ttdb.md). Unambiguous because '>' cannot occur
# in a type token. An untyped bare target is accepted and reported.
EDGE_RE = re.compile(
    r'^\s*(?:(?P<type>[A-Za-z_][A-Za-z0-9_\-]*)\s*>?\s*)?'
    r'(?P<target>' + NODE_TOKEN + r')\s*$'
)

# The declared edge syntax, read from the mmpdb block for reporting only.
# Parsing is tolerant of both forms; this exists so a store whose records
# disagree with its own declaration is visible rather than silent.
SYNTAX_RE = re.compile(r'^\s*syntax:\s*["\']?(?P<syntax>[^"\'\n]+)')

# TBEW block delimiters (TTDB-RFC-0005 §3).
EW_OPEN_RE = re.compile(r'^\s*\[ew\]\s*$', re.I)
EW_CLOSE_RE = re.compile(r'^\s*\[/ew\]\s*$', re.I)

# TBEW / metadata fields, captured for reporting and optional weighting.
FIELD_RE = re.compile(r'^\s*(conf|sal|rev|touched)\s*:\s*(\S+)', re.I)

# Edge type -> sign. THIS IS THE SUBSTANTIVE MODELING CHOICE.
# Everything downstream depends on it. Types not listed here are reported
# as unmapped and default to DEFAULT_SIGN.
SIGN_MAP = {
    'supports':     +1,
    'implies':      +1,
    'refines':      +1,
    'extends':      +1,
    'instantiates': +1,
    'cites':        +1,
    'depends_on':   +1,
    'part_of':      +1,
    'contradicts':  -1,
    'refutes':      -1,
    'blocks':       -1,
    'supersedes':   -1,
    'conflicts':    -1,
    'negates':      -1,
    'excludes':     -1,
}
DEFAULT_SIGN = +1

# Optional per-type weights. Missing types get 1.0.
WEIGHT_MAP = {}
DEFAULT_WEIGHT = 1.0

# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def iter_files(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, _, names in os.walk(p):
                for n in sorted(names):
                    if n.endswith(('.md', '.markdown', '.txt')):
                        yield os.path.join(root, n)
        else:
            yield p


def parse_store(paths):
    """Return (nodes, edges, meta, unmapped, stats).

    nodes: set of addresses
    edges: list of (u, v, type, weight, sign)
    meta:  address -> {conf, sal, rev, touched}
    """
    nodes = set()
    edges = []
    meta = defaultdict(dict)
    unmapped = defaultdict(int)
    stats = {'files': 0, 'node_decls': 0, 'edge_lines': 0, 'self_loops': 0,
             'malformed_edges': 0, 'syntaxes': {}}

    for path in iter_files(paths):
        stats['files'] += 1
        current = None
        in_ew = False
        in_mmpdb = False
        try:
            with open(path, 'r', encoding='utf-8', errors='replace') as fh:
                lines = fh.readlines()
        except OSError as exc:
            print(f'  ! could not read {path}: {exc}', file=sys.stderr)
            continue

        for line in lines:
            # mmpdb block: pick up the declared edge syntax for reporting.
            if line.startswith('```mmpdb'):
                in_mmpdb = True
                continue
            if in_mmpdb:
                if line.startswith('```'):
                    in_mmpdb = False
                else:
                    syn = SYNTAX_RE.match(line)
                    if syn:
                        stats['syntaxes'][path] = syn.group('syntax').strip()
                continue

            decl = NODE_DECL_RE.match(line)
            if decl:
                current = decl.group('addr')
                nodes.add(current)
                stats['node_decls'] += 1
                in_ew = False

                rel = RELATES_RE.search(decl.group('fields'))
                if not rel:
                    continue
                for item in rel.group('edges').split(','):
                    item = item.strip()
                    if not item:
                        continue
                    em = EDGE_RE.match(item)
                    if not em:
                        stats['malformed_edges'] += 1
                        continue
                    target = em.group('target')
                    if target == current:
                        stats['self_loops'] += 1
                        continue
                    etype = (em.group('type') or '').lower()
                    if etype and etype not in SIGN_MAP:
                        unmapped[etype] += 1
                    sign = SIGN_MAP.get(etype, DEFAULT_SIGN)
                    weight = WEIGHT_MAP.get(etype, DEFAULT_WEIGHT)
                    nodes.add(target)
                    edges.append((current, target, etype or '<untyped>',
                                  weight, sign))
                    stats['edge_lines'] += 1
                continue

            if current is None:
                continue

            # TBEW fields are only meaningful inside an [ew] block; record
            # bodies are prose and contain colon-separated text that would
            # otherwise be captured as weights.
            if EW_OPEN_RE.match(line):
                in_ew = True
                continue
            if EW_CLOSE_RE.match(line):
                in_ew = False
                continue
            if in_ew:
                fld = FIELD_RE.match(line)
                if fld:
                    meta[current][fld.group(1).lower()] = fld.group(2)

    return nodes, edges, dict(meta), dict(unmapped), stats


def build_adjacency(nodes, edges):
    """Symmetrize. sigma_uv == sigma_vu is required for a symmetric Laplacian.

    Parallel edges between the same pair are merged; if they disagree in
    sign the weights partially cancel, which is the honest behavior --
    a pair joined by both 'supports' and 'contradicts' should carry a
    weak constraint, not an arbitrary one.
    """
    acc = defaultdict(float)
    for u, v, _t, w, s in edges:
        key = (u, v) if u <= v else (v, u)
        acc[key] += w * s

    adj = {n: [] for n in nodes}
    merged = []
    for (a, b), signed_w in acc.items():
        if signed_w == 0.0:
            continue
        w = abs(signed_w)
        s = 1 if signed_w > 0 else -1
        adj[a].append((b, w, s))
        adj[b].append((a, w, s))
        merged.append((a, b, w, s))
    return adj, merged


# ---------------------------------------------------------------------------
# Solver
# ---------------------------------------------------------------------------


def solve(nodes, adj, seeds, gamma=0.15, omega=0.8, tol=1e-7, max_iter=5000):
    phi = {n: 0.0 for n in nodes}
    for n, v in seeds.items():
        if n in phi:
            phi[n] = v

    it = 0
    delta = 0.0
    for it in range(1, max_iter + 1):
        delta = 0.0
        nxt = {}
        for n in nodes:
            if n in seeds:
                nxt[n] = seeds[n]
                continue
            num = 0.0
            den = gamma
            for (m, w, s) in adj[n]:
                num += w * s * phi[m]
                den += w
            val = num / den if den > 0 else 0.0
            val = (1.0 - omega) * phi[n] + omega * val
            nxt[n] = val
            d = abs(val - phi[n])
            if d > delta:
                delta = d
        phi = nxt
        if delta < tol:
            break
    return phi, it, delta


def node_frustration(adj, phi):
    """Per-node residual energy.

    Note: the SIGNED sum sum_u w(phi_v - s*phi_u) is ~0 at the fixed point
    by construction -- that's the stationarity condition, so it detects
    nothing. The SUM OF SQUARES is not zero, and it localizes exactly the
    regions where no consistent assignment exists. That's the quantity
    worth reading.
    """
    out = {}
    for n, nbrs in adj.items():
        e = 0.0
        for (m, w, s) in nbrs:
            r = phi[n] - s * phi[m]
            e += w * r * r
        out[n] = e
    return out


def total_energy(merged, phi):
    return sum(w * (phi[a] - s * phi[b]) ** 2 for a, b, w, s in merged)


def components(nodes, adj):
    seen = set()
    comps = []
    for start in nodes:
        if start in seen:
            continue
        comp = set()
        q = deque([start])
        seen.add(start)
        while q:
            n = q.popleft()
            comp.add(n)
            for (m, _w, _s) in adj[n]:
                if m not in seen:
                    seen.add(m)
                    q.append(m)
        comps.append(comp)
    return comps


def greedy_frustration_count(nodes, adj):
    """BFS 2-coloring; count edges that violate it.

    This is an UPPER BOUND on the frustration index, not the index itself
    -- exact minimum frustration is NP-hard. A count of 0 does prove the
    graph is balanced. A nonzero count does not prove it is unbalanced by
    that amount.
    """
    color = {}
    violations = 0
    counted = set()
    for start in nodes:
        if start in color:
            continue
        color[start] = 1
        q = deque([start])
        while q:
            n = q.popleft()
            for (m, _w, s) in adj[n]:
                want = color[n] * s
                if m not in color:
                    color[m] = want
                    q.append(m)
                else:
                    key = (n, m) if n <= m else (m, n)
                    if key not in counted and color[m] != want:
                        counted.add(key)
                        violations += 1
    return violations


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else 0.0


def stdev(xs):
    xs = list(xs)
    if len(xs) < 2:
        return 0.0
    m = mean(xs)
    return (sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5


def pearson(xs, ys):
    if len(xs) < 2:
        return float('nan')
    mx, my = mean(xs), mean(ys)
    num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    dx = sum((a - mx) ** 2 for a in xs) ** 0.5
    dy = sum((b - my) ** 2 for b in ys) ** 0.5
    return num / (dx * dy) if dx and dy else float('nan')


def seed_loo(nodes, adj, seeds, **kw):
    """Hold out each seed, predict it from the rest. The falsifiability test."""
    if len(seeds) < 3:
        return None
    actual, predicted = [], []
    for held in seeds:
        rest = {k: v for k, v in seeds.items() if k != held}
        phi, _, _ = solve(nodes, adj, rest, **kw)
        actual.append(seeds[held])
        predicted.append(phi.get(held, 0.0))
    errs = [abs(a - p) for a, p in zip(actual, predicted)]
    baseline = [abs(a - mean(actual)) for a in actual]
    return {
        'mae': mean(errs),
        'baseline_mae': mean(baseline),
        'r': pearson(actual, predicted),
        'pairs': list(zip(seeds.keys(), actual, predicted)),
    }


def permutation_nulls(nodes, adj, merged, seeds, trials, rng, **kw):
    """Two nulls.

    sign-shuffle: keeps topology and seeds, permutes edge signs. Tests
      whether the SIGN STRUCTURE carries anything.
    seed-shuffle: keeps topology and signs, permutes seed values across
      seed nodes. Tests whether WHERE you seeded matters.
    """
    obs_phi, _, _ = solve(nodes, adj, seeds, **kw)
    obs_spread = stdev(obs_phi.values())
    obs_energy = total_energy(merged, obs_phi)

    sign_spread, sign_energy = [], []
    for _ in range(trials):
        signs = [s for _a, _b, _w, s in merged]
        rng.shuffle(signs)
        adj2 = {n: [] for n in nodes}
        for (a, b, w, _s), s2 in zip(merged, signs):
            adj2[a].append((b, w, s2))
            adj2[b].append((a, w, s2))
        m2 = [(a, b, w, s2) for (a, b, w, _s), s2 in zip(merged, signs)]
        p, _, _ = solve(nodes, adj2, seeds, **kw)
        sign_spread.append(stdev(p.values()))
        sign_energy.append(total_energy(m2, p))

    seed_spread = []
    keys = list(seeds.keys())
    vals = list(seeds.values())
    for _ in range(trials):
        shuffled = vals[:]
        rng.shuffle(shuffled)
        p, _, _ = solve(nodes, adj, dict(zip(keys, shuffled)), **kw)
        seed_spread.append(stdev(p.values()))

    def pct(obs, null):
        return sum(1 for x in null if x >= obs) / len(null) if null else float('nan')

    return {
        'obs_spread': obs_spread,
        'obs_energy': obs_energy,
        'sign_spread_mean': mean(sign_spread),
        'sign_energy_mean': mean(sign_energy),
        'p_energy_lower': sum(1 for x in sign_energy if x <= obs_energy) / max(len(sign_energy), 1),
        'seed_spread_mean': mean(seed_spread),
        'p_spread_sign': pct(obs_spread, sign_spread),
        'p_spread_seed': pct(obs_spread, seed_spread),
    }


# ---------------------------------------------------------------------------
# Seeds
# ---------------------------------------------------------------------------


def load_seeds(path, nodes):
    seeds = {}
    missing = []
    with open(path, 'r', encoding='utf-8') as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            parts = re.split(r'[\t,]+|\s{2,}|\s+', line)
            if len(parts) < 2:
                continue
            addr, val = parts[0], parts[-1]
            try:
                v = float(val)
            except ValueError:
                continue
            if addr not in nodes:
                missing.append(addr)
                continue
            seeds[addr] = max(-1.0, min(1.0, v))
    return seeds, missing


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------


def hr(title=''):
    print('\n' + ('== ' + title + ' ').ljust(72, '=') if title else '=' * 72)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('store', nargs='+', help='TTDB files or directories')
    ap.add_argument('--seeds', help='TSV/CSV: address <tab> value in [-1, 1]')
    ap.add_argument('--dump-parse', action='store_true',
                    help='print what the parser found and exit')
    ap.add_argument('--gamma', type=float, default=0.15,
                    help='decay; characteristic length ~ sqrt(1/gamma) hops (default 0.15)')
    ap.add_argument('--omega', type=float, default=0.8, help='Jacobi damping')
    ap.add_argument('--tol', type=float, default=1e-7)
    ap.add_argument('--max-iter', type=int, default=5000)
    ap.add_argument('--trials', type=int, default=200, help='permutation trials')
    ap.add_argument('--top', type=int, default=12)
    ap.add_argument('--seed-rng', type=int, default=0)
    ap.add_argument('--csv', help='write per-node field to CSV')
    args = ap.parse_args()

    nodes, edges, meta, unmapped, stats = parse_store(args.store)

    hr('PARSE')
    print(f'files scanned      {stats["files"]}')
    print(f'node declarations  {stats["node_decls"]}')
    print(f'unique addresses   {len(nodes)}')
    print(f'edge lines         {stats["edge_lines"]}')
    print(f'self-loops dropped {stats["self_loops"]}')
    print(f'malformed edges    {stats["malformed_edges"]}')
    print(f'nodes with TBEW    {len(meta)}')

    if stats['syntaxes']:
        print('\ndeclared edge syntax (mmpdb.typed_edges.syntax):')
        for p, s in sorted(stats['syntaxes'].items()):
            print(f'  {os.path.basename(p):<32} {s}')

    if not nodes:
        print('\n!! No records parsed. NODE_DECL_RE expects the TTDB-RFC-0001 §3')
        print('   header line:  @LATxLONy | created:<int> | ... | relates:<edges>')
        print('   Edit NODE_TOKEN / NODE_DECL_RE at the top of this file.')
        return 1

    tc = defaultdict(int)
    for _u, _v, t, _w, _s in edges:
        tc[t] += 1
    print('\nedge types found:')
    for t, c in sorted(tc.items(), key=lambda kv: -kv[1]):
        sign = SIGN_MAP.get(t, None)
        mark = f'{sign:+d}' if sign is not None else f'{DEFAULT_SIGN:+d} (UNMAPPED)'
        print(f'  {c:5d}  {t:<20} {mark}')
    if unmapped:
        print('\n!! Unmapped types defaulted to %+d. Add them to SIGN_MAP.' % DEFAULT_SIGN)

    adj, merged = build_adjacency(nodes, edges)
    npos = sum(1 for _a, _b, _w, s in merged if s > 0)
    nneg = len(merged) - npos
    print(f'\nmerged edges       {len(merged)}  (+{npos} / -{nneg})')

    if args.dump_parse:
        hr('SAMPLE NODES')
        for n in sorted(nodes)[:25]:
            d = len(adj[n])
            m = meta.get(n, {})
            print(f'  {n:<40} deg={d:<4} {m}')
        print('\nVerify these look right before trusting any numbers below.')
        return 0

    if nneg == 0:
        print('\n!! No negative edges. The signed problem degenerates to plain')
        print('   smoothing and the maximum principle applies: no node can')
        print('   exceed your seed extremes. Check SIGN_MAP.')

    comps = components(nodes, adj)
    comps.sort(key=len, reverse=True)
    print(f'components         {len(comps)}  (largest {len(comps[0])})')

    if not args.seeds:
        print('\nNo --seeds given. Parse looks usable; seed ~12 nodes and rerun.')
        print('Seed file format:  @LAT20LON3<TAB>0.8')
        return 0

    seeds, missing = load_seeds(args.seeds, nodes)
    if missing:
        print(f'\n!! {len(missing)} seed addresses not present in store:')
        for m in missing[:10]:
            print(f'     {m}')
    if not seeds:
        print('\n!! No usable seeds matched the store. Nothing to propagate.')
        return 1
    print(f'seeds loaded       {len(seeds)}')

    unseeded = [c for c in comps if not (set(c) & set(seeds))]
    if unseeded:
        n_un = sum(len(c) for c in unseeded)
        print(f'!! {n_un} nodes in {len(unseeded)} seedless components -> field will be 0 there')

    kw = dict(gamma=args.gamma, omega=args.omega, tol=args.tol, max_iter=args.max_iter)
    phi, iters, delta = solve(nodes, adj, seeds, **kw)

    hr('FIELD')
    print(f'converged in {iters} iters (delta={delta:.2e})')
    vals = [phi[n] for n in nodes if n not in seeds]
    print(f'free nodes: n={len(vals)} mean={mean(vals):+.4f} sd={stdev(vals):.4f} '
          f'min={min(vals):+.4f} max={max(vals):+.4f}' if vals else 'no free nodes')

    ranked = sorted((n for n in nodes if n not in seeds), key=lambda n: phi[n])
    print(f'\nmost negative ({args.top}):')
    for n in ranked[:args.top]:
        print(f'  {phi[n]:+.4f}  {n}')
    print(f'\nmost positive ({args.top}):')
    for n in reversed(ranked[-args.top:]):
        print(f'  {phi[n]:+.4f}  {n}')

    hr('FRUSTRATION')
    fr = node_frustration(adj, phi)
    E = total_energy(merged, phi)
    gfc = greedy_frustration_count(nodes, adj)
    print(f'total signed energy   {E:.4f}')
    print(f'greedy violating edges {gfc} / {len(merged)}  (UPPER bound on frustration index)')
    print(f'\nhighest local frustration - ambivalence points ({args.top}):')
    for n in sorted(fr, key=lambda x: -fr[x])[:args.top]:
        print(f'  {fr[n]:8.4f}  phi={phi[n]:+.4f}  deg={len(adj[n]):<3} {n}')

    hr('SEED LEAVE-ONE-OUT')
    loo = seed_loo(nodes, adj, seeds, **kw)
    if loo is None:
        print('need >=3 seeds')
    else:
        print(f'MAE {loo["mae"]:.4f}   vs mean-baseline MAE {loo["baseline_mae"]:.4f}'
              f'   r={loo["r"]:+.3f}')
        verdict = 'BEATS baseline' if loo['mae'] < loo['baseline_mae'] else 'NO BETTER than baseline'
        print(f'-> {verdict}')
        print('\n  actual   pred    node')
        for addr, a, p in loo['pairs']:
            print(f'  {a:+.3f}  {p:+.3f}   {addr}')

    hr('PERMUTATION NULLS')
    rng = random.Random(args.seed_rng)
    nulls = permutation_nulls(nodes, adj, merged, seeds, args.trials, rng, **kw)
    print(f'observed spread      {nulls["obs_spread"]:.4f}')
    print(f'  sign-shuffled mean {nulls["sign_spread_mean"]:.4f}   p={nulls["p_spread_sign"]:.3f}')
    print(f'  seed-shuffled mean {nulls["seed_spread_mean"]:.4f}   p={nulls["p_spread_seed"]:.3f}')
    print(f'observed energy      {nulls["obs_energy"]:.4f}')
    print(f'  sign-shuffled mean {nulls["sign_energy_mean"]:.4f}   '
          f'p(lower)={nulls["p_energy_lower"]:.3f}')
    print('\nIf both p-values sit near 0.5, the sign structure is carrying')
    print('nothing and the field is decoration. That is a real result. Stop here.')

    if args.csv:
        with open(args.csv, 'w', newline='', encoding='utf-8') as fh:
            w = csv.writer(fh)
            w.writerow(['node', 'phi', 'frustration', 'degree',
                        'pos_edges', 'neg_edges', 'is_seed',
                        'conf', 'sal', 'rev', 'touched'])
            for n in sorted(nodes, key=lambda x: -phi[x]):
                p = sum(1 for (_m, _w, s) in adj[n] if s > 0)
                q = len(adj[n]) - p
                m = meta.get(n, {})
                w.writerow([n, f'{phi[n]:.6f}', f'{fr[n]:.6f}', len(adj[n]),
                            p, q, int(n in seeds),
                            m.get('conf', ''), m.get('sal', ''),
                            m.get('rev', ''), m.get('touched', '')])
        print(f'\nwrote {args.csv}')
        print('This is your derived @VALENCE: namespace. Recomputable, not stored.')

    return 0


if __name__ == '__main__':
    sys.exit(main())
