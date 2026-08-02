#!/usr/bin/env python3
"""
folder_valence.py - signed valence field over an arbitrary folder tree.

WHAT THIS IS
------------
ttdb_valence.py solves a signed Dirichlet problem over a TTDB store, where the
graph is given: records are nodes and `relates:` edges carry declared types that
a hand-audited sign map turns into sigma. That is the easy case. This script asks
whether the same machinery survives when NOTHING is declared -- when the input is
just a folder of files and the graph has to be manufactured from raw text.

It reuses ttdb_valence.solve() and ttdb_valence.node_frustration() unchanged.
That reuse is the point: if the solver needs modification to handle free text,
the free-text framing is doing something different and should say so.

THE SUBSTANTIVE CLAIM BEING TESTED
----------------------------------
Edge signs come from DISCOURSE CONNECTIVES. Two adjacent segments joined by
"and"/"moreover" are asserted to carry the same polarity (sigma=+1); joined by
"but"/"however"/"whereas" they are asserted to carry opposite polarity
(sigma=-1). This is Hatzivassiloglou & McKeown (1997) applied to running prose
instead of a curated store, and it is the reason VALENCE_FIELD.md 1.2 insists
signed edges are mandatory: unsigned smoothing drags antonyms together.

Whether that holds outside a curated store is an OPEN EMPIRICAL QUESTION, which
is why --nulls is not optional decoration. Tier 1 hit r=+0.941 on a store whose
edge types were audited by hand. Free text will be noisier. The sign-shuffle
null tells you how much of the resulting field is structure and how much is the
smoother being a smoother. Read the nulls before you read the field.

PIPELINE
--------
    walk -> readable filter -> segment -> lexicon seed -> connective edges
         -> solve -> frustration -> importance rank -> report

"Important parts" is operationalised as a weighted blend (see IMPORTANCE_WEIGHTS)
of affective magnitude |phi|, per-node frustration, lexical affect density, and
structural position. Frustration carries the largest single share on purpose:
VALENCE_FIELD.md 0 argues the output that matters is where the settling FAILS,
not the settled numbers.

Pure stdlib. No numpy.

USAGE
    python folder_valence.py ROOT [ROOT...] [options]
    python folder_valence.py . --dump-segments | head -40    # DO THIS FIRST
    python folder_valence.py . --report scan.md --nulls
    python folder_valence.py . --lexicon path/to/norms_derived.tsv

OPTIONS OF CONSEQUENCE
    --no-tech-neutral   disable technical-vocabulary suppression. Do this once,
                        on a source tree, to see why it is on by default.
    --min-hits N        lexicon hits required before a segment may seed (1).
    --nulls             run sign-shuffle and seed-shuffle permutation nulls.
"""

import argparse
import fnmatch
import hashlib
import json
import math
import os
import random
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ttdb_valence  # noqa: E402  - solve() and node_frustration() are reused as-is


# ---------------------------------------------------------------------------
# MODELING ASSUMPTIONS - edit this block, not the machinery below.
# ---------------------------------------------------------------------------

# Contrastive connectives assert OPPOSITE polarity across the join (sigma=-1).
# Ordered longest-first so multiword forms match before their prefixes.
CONTRASTIVE = [
    "on the other hand", "that said", "even so", "in contrast", "by contrast",
    "then again", "all the same", "at the same time", "having said that",
    "nevertheless", "nonetheless", "conversely", "however", "whereas",
    "although", "though", "instead", "rather", "unfortunately", "regrettably",
    "unlike", "despite", "yet", "but", "except",
]

# Additive connectives assert SAME polarity across the join (sigma=+1).
ADDITIVE = [
    "in addition", "for that matter", "what is more", "not only",
    "furthermore", "moreover", "similarly", "likewise", "besides",
    "additionally", "equally", "and", "also", "indeed", "further",
]

# Negators flip the polarity of a following lexicon hit within NEG_WINDOW tokens
# and damp it: "not unreasonable" is weaker than "reasonable", not its mirror.
NEGATORS = {
    "not", "no", "never", "none", "nothing", "neither", "nor", "cannot",
    "can't", "won't", "don't", "doesn't", "didn't", "isn't", "aren't",
    "wasn't", "weren't", "shouldn't", "couldn't", "wouldn't", "hardly",
    "barely", "scarcely", "without", "lacks", "lack", "fails", "far from",
}
NEG_WINDOW = 3
NEG_DAMP = -0.6

# Intensifiers and downtoners scale a following hit.
INTENSIFIERS = {
    "very": 1.4, "extremely": 1.7, "deeply": 1.5, "highly": 1.4, "truly": 1.4,
    "utterly": 1.7, "profoundly": 1.6, "remarkably": 1.5, "strongly": 1.4,
    "really": 1.3, "so": 1.2, "quite": 1.15, "particularly": 1.3,
    "somewhat": 0.6, "slightly": 0.5, "mildly": 0.5, "fairly": 0.7,
    "marginally": 0.5, "a bit": 0.6, "kind of": 0.6, "sort of": 0.6,
}
INTENS_WINDOW = 2

# TECHNICAL VOCABULARY SUPPRESSION. This is the single largest failure mode of
# lexicon sentiment on a software corpus and it is not a detail.
#
# In general English these are strongly negative. In a repository they are
# neutral nouns and verbs of the domain -- "the test fails", "abort the run",
# "kill the process", "dead code", "error budget", "critical path", "blocked on
# review". Scoring them at face value makes EVERY source tree read as miserable,
# and the resulting field is a detector for how technical a file is, not how it
# feels about anything.
#
# Suppressed means dropped from seeding entirely, not down-weighted: a partial
# credit here still ranks the most technical files as the saddest.
# Disable with --no-tech-neutral and read the delta; the count of suppressions
# is always reported so the decision stays visible rather than silent.
TECH_NEUTRAL = {
    "error", "errors", "fail", "fails", "failed", "failing", "failure",
    "failures", "abort", "aborts", "aborted", "kill", "kills", "killed",
    "dead", "deadlock", "panic", "panics", "crash", "crashes", "crashed",
    "critical", "blocked", "blocking", "blocks", "block", "fatal", "severe",
    "exception", "exceptions", "bug", "bugs", "defect", "defects", "warning",
    "warnings", "invalid", "illegal", "corrupt", "corrupted", "stale",
    "orphan", "orphaned", "leak", "leaks", "dirty", "clean", "cleanup",
    "reject", "rejected", "rejects", "violation", "violations", "conflict",
    "conflicts", "collision", "collisions", "drop", "dropped", "loss",
    "lost", "missing", "null", "empty", "negative", "positive", "false",
    "true", "hard", "soft", "strong", "weak", "poor", "rich", "safe",
    "unsafe", "risk", "risky", "threat", "attack", "attacks", "malicious",
    "victim", "master", "slave", "abandoned", "deprecated", "legacy",
    "obsolete", "brittle", "smell", "smells", "noise", "noisy", "waste",
    "wasted", "expensive", "cheap", "slow", "fast", "degraded", "broken",
}

# Weights for the manufactured graph. Sequence within a paragraph is the most
# reliable adjacency signal; the section star exists only so unseeded sections
# inherit something rather than collapsing to zero under the gamma decay.
W_SEGMENT = 1.00   # adjacent segments inside one sentence (explicit connective)
W_SENTENCE = 0.70  # adjacent sentences inside one paragraph
W_PARAGRAPH = 0.35  # last segment of a paragraph -> first of the next
W_SECTION = 0.12   # every segment -> its section's opening segment
W_LINK = 0.30      # a markdown link -> the target file's opening segment
STAR_FANOUT = 20   # section-star total weight is capped at this many spokes

# Importance blend. Frustration leads deliberately: see module docstring.
#
# DENSITY IS DELIBERATELY SMALL, and this was measured rather than guessed.
# Density is lexicon hits per token, which is exactly zero for every segment the
# lexicon did not fire on -- i.e. for precisely the segments propagation exists
# to surface. At 0.20 it acted as a flat penalty on graph-discovered material:
# ranking by |phi| alone put 36 unseeded segments in the top 100, frustration
# alone put 17, and the blend put ONE. The blend was a lexicon echo wearing a
# graph as decoration. See ABLATION section of SCAN_SELF.md.
IMPORTANCE_WEIGHTS = {
    "frustration": 0.35,
    "affect": 0.35,
    "density": 0.10,
    "structure": 0.20,
}

# Files we will not attempt to read as text, by extension. These are not
# "unreadable" in principle -- pdf/docx/ipynb all have extractors -- they are
# unreadable BY THIS SCRIPT, and are counted and reported separately from
# binaries so the gap in coverage is visible rather than inferred.
NEEDS_EXTRACTOR = {
    ".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".odt", ".epub",
    ".ipynb", ".rtf",
}
BINARY_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".ico", ".tif", ".tiff",
    ".mp3", ".mp4", ".wav", ".avi", ".mov", ".mkv", ".flac", ".ogg",
    ".zip", ".gz", ".tar", ".bz2", ".xz", ".7z", ".rar", ".jar",
    ".exe", ".dll", ".so", ".dylib", ".bin", ".o", ".a", ".pyc", ".class",
    ".ttf", ".otf", ".woff", ".woff2", ".eot",
    ".db", ".sqlite", ".sqlite3", ".pack", ".idx",
}
ALWAYS_SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv",
                    ".mypy_cache", ".pytest_cache", "dist", "build", ".idea",
                    ".vscode-test", "target", ".next", ".cache"}

MAX_BYTES = 2 * 1024 * 1024
SNIFF_BYTES = 8192


# ---------------------------------------------------------------------------
# Walk and readability
# ---------------------------------------------------------------------------


class Skips:
    def __init__(self):
        self.counts = defaultdict(int)
        self.examples = defaultdict(list)

    def add(self, reason, path):
        self.counts[reason] += 1
        if len(self.examples[reason]) < 3:
            self.examples[reason].append(path)


def load_gitignore(root):
    """Minimal .gitignore support: literal names, globs, dir/ and /anchored.

    Deliberately not a full implementation -- no negation, no ** semantics.
    Patterns it cannot express are handled by ALWAYS_SKIP_DIRS. Anything this
    misses shows up as extra scanned files, never as silently dropped ones.
    """
    pats = []
    p = os.path.join(root, ".gitignore")
    if not os.path.isfile(p):
        return pats
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("!"):
                    continue
                pats.append(line.rstrip("/"))
    except OSError:
        pass
    return pats


def ignored(relpath, pats):
    parts = relpath.replace(os.sep, "/").split("/")
    for pat in pats:
        if pat.startswith("/"):
            if fnmatch.fnmatch(relpath.replace(os.sep, "/"), pat.lstrip("/")):
                return True
            continue
        if fnmatch.fnmatch(relpath.replace(os.sep, "/"), pat):
            return True
        for part in parts:
            if fnmatch.fnmatch(part, pat):
                return True
    return False


def is_readable_text(path, skips, rel):
    """Decide readability by CONTENT, not by extension alone.

    Extension gets the obvious cases out of the way cheaply; the NUL sniff and
    the full UTF-8 decode settle the rest. A file with no extension and valid
    UTF-8 content (LICENSE, Makefile, .gitattributes) is text and is read.
    """
    ext = os.path.splitext(path)[1].lower()
    if ext in BINARY_EXT:
        skips.add("binary (by extension)", rel)
        return None
    if ext in NEEDS_EXTRACTOR:
        skips.add("needs an extractor (not implemented)", rel)
        return None
    try:
        size = os.path.getsize(path)
    except OSError:
        skips.add("unstattable", rel)
        return None
    if size == 0:
        skips.add("empty", rel)
        return None
    if size > MAX_BYTES:
        skips.add("over size cap", rel)
        return None
    try:
        with open(path, "rb") as fh:
            head = fh.read(SNIFF_BYTES)
            if b"\x00" in head:
                skips.add("binary (NUL byte)", rel)
                return None
            rest = fh.read()
    except OSError:
        skips.add("unreadable", rel)
        return None
    try:
        return (head + rest).decode("utf-8")
    except UnicodeDecodeError:
        skips.add("not valid UTF-8", rel)
        return None


def walk(roots, skips, extra_ignores=()):
    out = []
    for root in roots:
        root = os.path.abspath(root)
        if os.path.isfile(root):
            text = is_readable_text(root, skips, os.path.basename(root))
            if text is not None:
                out.append((os.path.basename(root), text))
            continue
        pats = list(load_gitignore(root)) + list(extra_ignores)
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = sorted(
                d for d in dirnames
                if d not in ALWAYS_SKIP_DIRS
                and not ignored(os.path.relpath(os.path.join(dirpath, d), root), pats)
            )
            for fn in sorted(filenames):
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, root).replace(os.sep, "/")
                if ignored(rel, pats):
                    skips.add("gitignored", rel)
                    continue
                text = is_readable_text(full, skips, rel)
                if text is not None:
                    out.append((rel, text))
    return out


# ---------------------------------------------------------------------------
# Segmentation
# ---------------------------------------------------------------------------

# Sentence boundary: terminal punctuation, closing quotes/brackets allowed,
# then whitespace, then something that starts a sentence. Abbreviations are
# handled by a short exception list rather than a model; the failure mode of
# over-splitting here is extra weak edges, not wrong signs.
ABBREV = {"e.g", "i.e", "cf", "vs", "etc", "al", "fig", "eq", "no", "vol",
          "ch", "sec", "approx", "dr", "mr", "ms", "st", "ref"}
SENT_END = re.compile(r'([.!?])(["\')\]]*)(\s+)(?=[A-Z0-9"\'(\[])')

FENCE = re.compile(r"^\s*(```|~~~)")
HEADING = re.compile(r"^\s{0,3}(#{1,6})\s+(.*)$")
UNDERLINE_H = re.compile(r"^\s{0,3}(=+|-+)\s*$")
LIST_ITEM = re.compile(r"^\s*([-*+]|\d+[.)])\s+")
TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$")
QUOTE = re.compile(r"^\s*>")
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)")

CODE_EXT = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".c", ".h", ".cpp", ".hpp", ".cc",
    ".java", ".go", ".rs", ".rb", ".php", ".cs", ".swift", ".kt", ".scala",
    ".sh", ".bash", ".zsh", ".ps1", ".sql", ".r", ".lua", ".pl", ".ino",
}
DATA_EXT = {".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".csv", ".tsv",
            ".xml", ".lock", ".properties"}


class Segment:
    __slots__ = ("nid", "path", "text", "kind", "section", "para", "sent",
                 "seg", "join", "hits", "tokens", "seed", "phi", "frust",
                 "importance", "line")

    def __init__(self, nid, path, text, kind, section, para, sent, seg, join, line):
        self.nid = nid
        self.path = path
        self.text = text
        self.kind = kind
        self.section = section
        self.para = para
        self.sent = sent
        self.seg = seg
        self.join = join          # connective that attached this to the previous segment
        self.line = line
        self.hits = []
        self.tokens = 0
        self.seed = None
        self.phi = 0.0
        self.frust = 0.0
        self.importance = 0.0


def file_kind(path):
    base = os.path.basename(path)
    # Dotfiles and lockfiles are configuration. Their '#' comments would
    # otherwise parse as markdown headings and their contents as prose, which
    # produces confident-looking segments out of ignore patterns and settings.
    if base.startswith(".") or base in {"Makefile", "Dockerfile", "CODEOWNERS"}:
        return "data"
    ext = os.path.splitext(path)[1].lower()
    if ext in CODE_EXT:
        return "code"
    if ext in DATA_EXT:
        return "data"
    if ext in {".md", ".markdown", ".rst", ".txt", ".tex", ".org"}:
        return "prose"
    return "prose"


def strip_code_comments(text, path):
    """For source files, keep only comments and docstrings.

    Rationale: the evaluative content of a source file lives in its comments.
    Identifiers and keywords are vocabulary, not opinion, and feeding them to a
    lexicon produces exactly the technical-misery artefact TECH_NEUTRAL exists
    to prevent. Crude on purpose -- a real parser per language is out of scope
    for v1, and the failure mode is dropped text, not invented text.
    """
    out = []
    in_doc = False
    doc_delim = None
    for i, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if in_doc:
            out.append((i, s.replace(doc_delim, "")))
            if doc_delim in s:
                in_doc = False
            continue
        for d in ('"""', "'''"):
            if s.startswith(d) or (d in s and path.endswith(".py")):
                rest = s.split(d, 1)[1] if d in s else ""
                if s.count(d) >= 2:
                    out.append((i, s.replace(d, "")))
                else:
                    in_doc = True
                    doc_delim = d
                    out.append((i, rest))
                break
        else:
            m = re.match(r"^\s*(#|//|--|;|\*|/\*)\s?(.*)$", line)
            if m:
                out.append((i, m.group(2)))
            continue
    return out


def split_sentences(text):
    parts = []
    start = 0
    for m in SENT_END.finditer(text):
        head = text[start:m.end(2)]
        word = re.split(r"[\s(]", head.strip())[-1].rstrip(".").lower()
        if word in ABBREV or (len(word) == 1 and word.isalpha()):
            continue
        parts.append(head.strip())
        start = m.end(3)
    tail = text[start:].strip()
    if tail:
        parts.append(tail)
    return [p for p in parts if p]


def split_on_connectives(sentence):
    """Split one sentence at explicit discourse connectives.

    Returns [(text, connective_or_None)]. The connective is what JOINS this
    piece to the previous one and is what sets sigma on the resulting edge.
    Only clause-initial matches count -- requiring a preceding comma or
    semicolon for mid-sentence forms keeps "but" the conjunction and rejects
    "nothing but", "all but done", "yet another".
    """
    pattern = "|".join(sorted(
        (re.escape(c) for c in CONTRASTIVE + ADDITIVE), key=len, reverse=True))
    # The trailing [,;:]? is load-bearing: "However, x" is by far the commonest
    # form and a bare \b\s+ does not match it.
    rx = re.compile(r"(?:^|[,;:]\s+|\s+)(" + pattern + r")\b[,;:]?\s+", re.I)
    pieces = []
    last = 0
    last_conn = None
    for m in rx.finditer(sentence):
        conn = m.group(1).lower()
        pre_char = sentence[max(0, m.start() - 1):m.start() + 1]
        clause_initial = m.start() == 0 or "," in pre_char or ";" in pre_char or ":" in pre_char
        if not clause_initial:
            continue
        chunk = sentence[last:m.start()].strip(" ,;:")
        # A SENTENCE-INITIAL connective ("However, x") yields an empty chunk.
        # That is the most common and most reliable form in edited prose, and
        # dropping it here is why an earlier version of this script found 40
        # negative edges in 10262. Carry the connective forward instead: it
        # signs the join to the PRECEDING sentence, which is exactly its job.
        if not chunk:
            last_conn = conn
            last = m.end()
            continue
        # A short left chunk ("This is good, but it is slow") used to be dropped
        # here, discarding the contrast -- the one thing this split exists to
        # find. Split anyway and let coalesce() protect the result: a segment
        # created by an explicit contrast marker is evidence, not a runt.
        if len(chunk.split()) < 2:
            continue
        pieces.append((chunk, last_conn))
        last_conn = conn
        last = m.end()
    tail = sentence[last:].strip(" ,;:")
    if tail:
        pieces.append((tail, last_conn))
    if not pieces:
        return [(sentence.strip(), leading_connective(sentence))]
    return pieces


def leading_connective(text):
    low = text.lower().lstrip(" \t*->#")
    for c in sorted(CONTRASTIVE + ADDITIVE, key=len, reverse=True):
        if low.startswith(c + " ") or low.startswith(c + ","):
            return c
    return None


def sign_of(connective):
    if connective is None:
        return 1
    c = connective.lower()
    if c in CONTRASTIVE:
        return -1
    if c in ADDITIVE:
        return 1
    return 1


def segment_file(path, text):
    """Turn one file into a list of Segments plus its outbound markdown links."""
    segs = []
    links = []
    kind = file_kind(path)
    counter = [0]

    def emit(body, seg_kind, section, para, sent_i, seg_i, join, line):
        if not body or not body.strip():
            return
        # Runts that coalesce could not rescue (a standalone 3-word list item)
        # are dropped rather than scored. They carry no lexicon signal and each
        # one adds a +1 edge that dilutes the sign structure. Headings are kept
        # regardless -- they are short by nature and structurally load-bearing.
        if (seg_kind != "heading" and len(body.split()) < 4
                and sign_of(join) != -1):
            return
        counter[0] += 1
        nid = "%s#s%04d" % (path, counter[0])
        segs.append(Segment(nid, path, body.strip(), seg_kind, section,
                            para, sent_i, seg_i, join, line))

    if kind == "code":
        lines = strip_code_comments(text, path)
        para = 0
        buf = []
        buf_line = 0
        prev_line = None
        for lineno, body in lines:
            if prev_line is not None and lineno != prev_line + 1 and buf:
                _flush_prose(" ".join(buf), "comment", "", para, emit, buf_line)
                para += 1
                buf = []
            if not buf:
                buf_line = lineno
            buf.append(body)
            prev_line = lineno
        if buf:
            _flush_prose(" ".join(buf), "comment", "", para, emit, buf_line)
        return segs, links

    if kind == "data":
        return segs, links

    # Prose / markdown
    section = ""
    para = 0
    buf = []
    buf_line = 1
    in_fence = False
    prev = ""
    for lineno, raw in enumerate(text.splitlines(), 1):
        if FENCE.match(raw):
            in_fence = not in_fence
            if buf:
                _flush_prose(" ".join(buf), "prose", section, para, emit, buf_line)
                para += 1
                buf = []
            continue
        if in_fence:
            continue
        for m in MD_LINK.finditer(raw):
            links.append((path, m.group(1), lineno))
        h = HEADING.match(raw)
        if UNDERLINE_H.match(raw) and prev.strip() and not LIST_ITEM.match(prev):
            h = None
            if buf:
                buf.pop()
            section = prev.strip()
            emit(section, "heading", section, para, 0, 0, None, lineno - 1)
            para += 1
            if buf:
                _flush_prose(" ".join(buf), "prose", section, para, emit, buf_line)
                para += 1
                buf = []
            prev = raw
            continue
        if h:
            if buf:
                _flush_prose(" ".join(buf), "prose", section, para, emit, buf_line)
                para += 1
                buf = []
            section = h.group(2).strip().rstrip("#").strip()
            emit(section, "heading", section, para, 0, 0, None, lineno)
            para += 1
            prev = raw
            continue
        if not raw.strip():
            if buf:
                _flush_prose(" ".join(buf), "prose", section, para, emit, buf_line)
                para += 1
                buf = []
            prev = raw
            continue
        if TABLE_ROW.match(raw) or re.match(r"^\s*[-=|+:]{4,}\s*$", raw):
            prev = raw
            continue
        seg_kind = "quote" if QUOTE.match(raw) else "prose"
        line = QUOTE.sub("", raw).strip()
        if LIST_ITEM.match(raw):
            if buf:
                _flush_prose(" ".join(buf), "prose", section, para, emit, buf_line)
                para += 1
                buf = []
            line = LIST_ITEM.sub("", line)
            seg_kind = "list" if seg_kind == "prose" else seg_kind
        if not buf:
            buf_line = lineno
        buf.append(line)
        if seg_kind in ("quote", "list"):
            _flush_prose(" ".join(buf), seg_kind, section, para, emit, buf_line)
            para += 1
            buf = []
        prev = raw
    if buf:
        _flush_prose(" ".join(buf), "prose", section, para, emit, buf_line)
    return segs, links


# Minimum words in a node. Below this a segment cannot carry a lexicon signal:
# the first version of this script produced a median node of 9 tokens, of which
# 85% had ZERO lexicon hits, so 98% of the graph was unseeded and the field
# decayed to zero everywhere. Sub-sentence splitting is kept -- the contrast it
# exposes is the whole point -- but only where both sides are substantial;
# otherwise the connective still signs the edge and the text stays joined.
MIN_SEG_WORDS = 6


def coalesce(pieces):
    """Merge runt pieces forward so every node is long enough to score.

    The connective of a merged runt is preserved on the piece that absorbs it
    only if that piece has none of its own -- a join must not be invented.
    """
    def protected(i):
        """A piece is protected if an explicit contrast marker bounds it.

        Merging such a piece away would destroy the only negative-sign evidence
        the corpus offers, which on technical prose is scarce enough already --
        see the connective-density diagnostic in the report."""
        if i < 0 or i >= len(pieces):
            return False
        if sign_of(pieces[i][1]) == -1:
            return True
        return i + 1 < len(pieces) and sign_of(pieces[i + 1][1]) == -1

    out = []
    for i, (text, conn) in enumerate(pieces):
        if protected(i):
            out.append((text, conn))
            continue
        if out and len(text.split()) < MIN_SEG_WORDS and not protected(i - 1):
            prev_text, prev_conn = out[-1]
            joiner = (" %s " % conn) if conn else " "
            out[-1] = (prev_text + joiner + text, prev_conn)
            continue
        if out and len(out[-1][0].split()) < MIN_SEG_WORDS and not protected(i - 1):
            prev_text, prev_conn = out.pop()
            joiner = (" %s " % conn) if conn else " "
            out.append((prev_text + joiner + text, prev_conn))
            continue
        out.append((text, conn))
    return out


def _flush_prose(body, kind, section, para, emit, line):
    body = re.sub(r"`[^`]*`", " ", body)          # inline code is vocabulary, not opinion
    body = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", body)  # keep link text, drop URL
    body = re.sub(r"https?://\S+", " ", body)
    body = re.sub(r"\s+", " ", body).strip()
    if not body:
        return
    flat = []
    for si, sentence in enumerate(split_sentences(body)):
        for gi, (piece, conn) in enumerate(split_on_connectives(sentence)):
            if conn is None:
                conn = leading_connective(piece)
            flat.append((si, gi, piece, conn))
    if not flat:
        return
    coalesced = coalesce([(p, c) for _si, _gi, p, c in flat])
    idx = {p: (si, gi) for si, gi, p, _c in flat}
    for n, (piece, conn) in enumerate(coalesced):
        si, gi = idx.get(piece, (n, 0))
        emit(piece, kind, section, para, si, gi, conn, line)


# ---------------------------------------------------------------------------
# Lexicon and seeding
# ---------------------------------------------------------------------------

TOKEN = re.compile(r"[A-Za-z][A-Za-z'-]*")
SUFFIXES = ("ingly", "edly", "ing", "ies", "ied", "es", "ed", "ly", "s")


def load_lexicon(path):
    lex = {}
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                parts = line.split()
            if len(parts) < 2:
                continue
            try:
                lex[parts[0].strip().lower()] = float(parts[1])
            except ValueError:
                continue
    return lex


def lookup(lex, word):
    if word in lex:
        return lex[word], word
    for suf in SUFFIXES:
        if word.endswith(suf) and len(word) - len(suf) >= 3:
            stem = word[: -len(suf)]
            if stem in lex:
                return lex[stem], stem
            if stem + "e" in lex:
                return lex[stem + "e"], stem + "e"
    return None, None


def score_segment(seg, lex, tech_neutral, stats):
    toks = [t.lower() for t in TOKEN.findall(seg.text)]
    seg.tokens = len(toks)
    hits = []
    for i, tok in enumerate(toks):
        if tech_neutral and tok in TECH_NEUTRAL:
            if lookup(lex, tok)[0] is not None:
                stats["suppressed"] += 1
                stats["suppressed_words"][tok] += 1
            continue
        pol, matched = lookup(lex, tok)
        if pol is None:
            continue
        mult = 1.0
        negated = False
        for j in range(max(0, i - NEG_WINDOW), i):
            if toks[j] in NEGATORS:
                negated = True
        for j in range(max(0, i - INTENS_WINDOW), i):
            if toks[j] in INTENSIFIERS:
                mult *= INTENSIFIERS[toks[j]]
        val = pol * mult
        if negated:
            val = val * NEG_DAMP
        hits.append((matched, max(-1.0, min(1.0, val))))
    seg.hits = hits
    return hits


def seed_from_hits(seg, min_hits, min_abs):
    if len(seg.hits) < min_hits:
        return None
    mean = sum(v for _w, v in seg.hits) / len(seg.hits)
    if abs(mean) < min_abs:
        return None
    return max(-1.0, min(1.0, mean))


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------


def build_edges(segments, links, first_by_file):
    """Manufacture the signed graph. Every edge here is an ASSERTION about
    polarity agreement, and every one of them can be wrong -- which is what the
    sign-shuffle null is for."""
    edges = []
    by_file = defaultdict(list)
    for s in segments:
        by_file[s.path].append(s)

    section_open = {}
    for path, segs in by_file.items():
        for s in segs:
            key = (path, s.section)
            if key not in section_open:
                section_open[key] = s.nid

    for path, segs in by_file.items():
        for a, b in zip(segs, segs[1:]):
            if b.seg > 0 and b.sent == a.sent and b.para == a.para:
                w, kind = W_SEGMENT, "segment"
            elif b.para == a.para:
                w, kind = W_SENTENCE, "sentence"
            elif b.section == a.section:
                w, kind = W_PARAGRAPH, "paragraph"
            else:
                w, kind = W_PARAGRAPH * 0.5, "section-break"
            if a.kind == "heading" or b.kind == "heading":
                w *= 0.6
            edges.append((a.nid, b.nid, w, sign_of(b.join), kind, b.join))
        # Star weight is divided down in large sections. A flat W_SECTION makes
        # the opening segment of a long unheaded preamble a hub of degree 247
        # against a median of 3, and per-node frustration correlates with degree
        # at r=+0.27 -- so the docket fills up with file titles instead of
        # content. TIER1_RESULTS.md 1.1 found the same hub damage on the curated
        # store; this is that finding applied to manufactured scaffolding.
        sect_size = defaultdict(int)
        for s in segs:
            sect_size[(path, s.section)] += 1
        for s in segs:
            key = (path, s.section)
            open_nid = section_open.get(key)
            if open_nid and open_nid != s.nid:
                w = W_SECTION * min(1.0, STAR_FANOUT / max(1, sect_size[key] - 1))
                edges.append((s.nid, open_nid, w, 1, "section-star", None))

    for src_path, target, lineno in links:
        tgt = target.split("#")[0].lstrip("./")
        if not tgt:
            continue
        cand = None
        for p in first_by_file:
            if p == tgt or p.endswith("/" + tgt):
                cand = p
                break
        if cand is None or cand == src_path:
            continue
        src_nid = first_by_file.get(src_path)
        if src_nid:
            edges.append((src_nid, first_by_file[cand], W_LINK, 1, "link", None))
    return edges


# ---------------------------------------------------------------------------
# Importance
# ---------------------------------------------------------------------------


def percentile_rank(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    n = max(1, len(values) - 1)
    for pos, idx in enumerate(order):
        ranks[idx] = pos / n
    return ranks


def rank_importance(segments):
    if not segments:
        return
    affect = [abs(s.phi) for s in segments]
    frust = [s.frust for s in segments]
    density = [(len(s.hits) / s.tokens) if s.tokens else 0.0 for s in segments]
    structure = []
    for s in segments:
        v = 0.0
        if s.kind == "heading":
            v += 0.3
        if s.para <= 1:
            v += 0.4
        if s.section:
            v += 0.2
        if s.join is not None and sign_of(s.join) == -1:
            v += 0.4          # a contrast marker is an author flagging tension
        structure.append(min(1.0, v))

    ra, rf, rd = percentile_rank(affect), percentile_rank(frust), percentile_rank(density)
    w = IMPORTANCE_WEIGHTS
    for i, s in enumerate(segments):
        s.importance = (w["frustration"] * rf[i] + w["affect"] * ra[i]
                        + w["density"] * rd[i] + w["structure"] * structure[i])


# ---------------------------------------------------------------------------
# Nulls
# ---------------------------------------------------------------------------


def run_nulls(nodes, edges, seeds, phi, gamma, omega, trials, rng):
    """Two permutation nulls, matching the ttdb_valence.py protocol.

    sign-permute : keeps the topology, the seeds, AND THE NUMBER of negative
                   edges, permuting only WHICH edges are negative. This is the
                   null that can actually fail, and it is the one to read.
    sign-random  : every edge sign redrawn 50/50. Reported for reference only.
                   It is NOT evidence about the connectives: when 99% of real
                   edges are +1, a near-constant field is trivially satisfiable
                   and beats a coin-flip assignment no matter where — or
                   whether — the connectives were placed correctly. An earlier
                   version of this script used it as the primary null and read
                   1.59x off it as support. That number was measuring the
                   marginal, not the evidence. A null that cannot fail is not
                   a null; compare VALENCE_FIELD.md 6.0 on the defective stop
                   condition.
    seed-shuffle : keeps topology and signs, permutes which node gets which seed
                   value. Tests whether the lexicon is placing seeds anywhere
                   that matters.
    """
    def energy(e, f):
        return sum(w * (f[a] - s * f[b]) ** 2 for a, b, w, s in e)

    # build_adjacency wants (u, v, type, w, sigma); energy() wants (u, v, w, sigma).
    def as_adj_input(quads):
        return [(a, b, "manufactured", w, s) for a, b, w, s in quads]

    real_merged = [(a, b, w, s) for a, b, w, s, _k, _j in edges]
    real_E = energy(real_merged, phi)
    unseeded = [n for n in nodes if n not in seeds]
    real_spread = (sum(abs(phi[n]) for n in unseeded) / len(unseeded)) if unseeded else 0.0

    def run_variant(sign_fn, reset_fn=None):
        Es, spreads = [], []
        for _ in range(trials):
            if reset_fn:
                reset_fn()
            variant = [(a, b, w, sign_fn(i, s))
                       for i, (a, b, w, s) in enumerate(real_merged)]
            adjv, mergedv = ttdb_valence.build_adjacency(
                nodes, as_adj_input(variant))
            f, _it, _d = ttdb_valence.solve(
                nodes, adjv, seeds, gamma=gamma, omega=omega)
            Es.append(energy(mergedv, f))
            if unseeded:
                spreads.append(sum(abs(f[n]) for n in unseeded) / len(unseeded))
        return Es, spreads

    # Marginal-preserving: same count of -1 edges, different placement.
    perm_state = []

    def reshuffle():
        signs = [s for _a, _b, _w, s in real_merged]
        rng.shuffle(signs)
        perm_state[:] = signs

    perm_E, perm_spread = run_variant(lambda i, _s: perm_state[i], reshuffle)
    sign_E, sign_spread = run_variant(lambda _i, _s: rng.choice((1, -1)))

    seed_E = []
    seed_nodes = list(seeds.keys())
    seed_vals = list(seeds.values())
    all_nodes = list(nodes)
    adj_real, merged_real = ttdb_valence.build_adjacency(
        nodes, as_adj_input(real_merged))
    for _ in range(trials):
        picks = rng.sample(all_nodes, len(seed_nodes))
        vals = list(seed_vals)
        rng.shuffle(vals)
        fake = dict(zip(picks, vals))
        f, _it, _d = ttdb_valence.solve(nodes, adj_real, fake, gamma=gamma, omega=omega)
        seed_E.append(energy(merged_real, f))

    def mean(xs):
        return sum(xs) / len(xs) if xs else 0.0

    ne = max(1, len(real_merged))
    neg_count = sum(1 for _a, _b, _w, s in real_merged if s < 0)
    return {
        "real_energy": real_E,
        "real_energy_per_edge": real_E / ne,
        "real_spread_unseeded": real_spread,
        "negative_edges": neg_count,
        "sign_permute_energy_mean": mean(perm_E),
        "sign_permute_energy_per_edge": mean(perm_E) / ne,
        "sign_permute_spread_mean": mean(perm_spread),
        "sign_permute_energy_min": min(perm_E) if perm_E else 0.0,
        "sign_random_energy_mean": mean(sign_E),
        "sign_random_energy_per_edge": mean(sign_E) / ne,
        "sign_random_spread_mean": mean(sign_spread),
        "seed_shuffle_energy_mean": mean(seed_E),
        "seed_shuffle_energy_per_edge": mean(seed_E) / ne,
        "trials": trials,
    }


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def _docket(A, group, adj, seeds):
    """Render one frustration list with the neighbours that caused it."""
    if not group:
        A("*(none)*")
        A("")
        return
    for i, s in enumerate(group, 1):
        A("**%d. `%s:%d`** — frustration %.4f, phi %+.3f%s"
          % (i, s.path, s.line, s.frust, s.phi,
             (" *(seeded)*" if s.nid in seeds else "")))
        A("")
        A("> %s" % quote(s.text))
        A("")
        # Show the neighbours contributing most residual -- those are the ones
        # the node cannot reconcile, and the pair is what makes the finding
        # checkable by eye.
        nbrs = []
        for (m, w, sg) in adj[s.nid]:
            other = SEG_BY_ID.get(m)
            if other is None:
                continue
            nbrs.append((w * (s.phi - sg * other.phi) ** 2,
                         abs(s.phi - sg * other.phi), sg, other))
        nbrs.sort(key=lambda t: -t[0])
        for contrib, resid, sg, other in nbrs[:3]:
            if resid < 0.05:
                break
            A("  - edge asserts %s (residual %.3f, contributes %.3f) — `%s:%d` phi %+.3f: %s"
              % ("SAME polarity" if sg > 0 else "OPPOSITE polarity", resid,
                 contrib, other.path, other.line, other.phi, quote(other.text, 120)))
        A("")


def quote(text, n=200):
    t = text.strip().replace("\n", " ")
    return (t[: n - 1] + "…") if len(t) > n else t


def build_report(args, files, skips, segments, edges, seeds, stats, nulls,
                 iters, delta, adj):
    L = []
    A = L.append
    A("# Folder valence scan")
    A("")
    A("Generated by `folder_valence.py` over: `%s`" % "`, `".join(args.roots))
    A("")
    A("> **Read the nulls first.** The field below is a smoother's output over a")
    A("> graph this script invented from discourse connectives. Whether those")
    A("> connectives carry polarity information outside a curated store is the")
    A("> question under test, not an assumption. See §5.")
    A("")

    A("## 1. Coverage")
    A("")
    A("| quantity | value |")
    A("| --- | ---: |")
    A("| files read | %d |" % len(files))
    A("| segments (nodes) | %d |" % len(segments))
    A("| edges | %d |" % len(edges))
    A("| seeded segments | %d (%.1f%%) |"
      % (len(seeds), 100.0 * len(seeds) / max(1, len(segments))))
    A("| solver iterations | %d (delta %.2e) |" % (iters, delta))
    A("| lexicon entries | %d |" % stats["lexicon_size"])
    A("| tech-neutral suppressions | %d |" % stats["suppressed"])
    A("")
    if skips.counts:
        A("Skipped:")
        A("")
        A("| reason | count | examples |")
        A("| --- | ---: | --- |")
        for reason, count in sorted(skips.counts.items(), key=lambda kv: -kv[1]):
            A("| %s | %d | %s |"
              % (reason, count, ", ".join("`%s`" % e for e in skips.examples[reason])))
        A("")
    if stats["suppressed"]:
        top = sorted(stats["suppressed_words"].items(), key=lambda kv: -kv[1])[:12]
        A("Most-suppressed technical terms (would have scored as affect with")
        A("`--no-tech-neutral`): %s."
          % ", ".join("`%s` x%d" % (w, c) for w, c in top))
        A("")

    edge_kinds = defaultdict(int)
    neg = 0
    adjacency_kinds = {"segment", "sentence", "paragraph", "section-break"}
    adj_total = adj_neg = 0
    for _a, _b, _w, s, kind, _j in edges:
        edge_kinds[kind] += 1
        if s < 0:
            neg += 1
        if kind in adjacency_kinds:
            adj_total += 1
            if s < 0:
                adj_neg += 1
    A("Edge composition: %s."
      % ", ".join("%s %d" % (k, v) for k, v in sorted(edge_kinds.items())))
    A("")
    A("Negative-sign edges: %d of %d overall (%.1f%%), and %d of %d **adjacency**"
      % (neg, len(edges), 100.0 * neg / max(1, len(edges)), adj_neg, adj_total))
    A("edges (%.1f%%). The second number is the one that matters — section-star"
      % (100.0 * adj_neg / max(1, adj_total)))
    A("links are unsigned scaffolding and are +1 by construction, so including")
    A("them in the denominator understates how much contrast was actually found.")
    A("")
    conn_counts = defaultdict(int)
    for s in segments:
        if s.join:
            conn_counts[s.join] += 1
    contr = sum(v for k, v in conn_counts.items() if sign_of(k) == -1)
    A("**Connective density.** %d of %d segments (%.2f%%) carry a contrastive"
      % (contr, len(segments), 100.0 * contr / max(1, len(segments))))
    A("marker. This is the ceiling on how much negative-sign evidence the corpus")
    A("can supply, independent of how well the extractor works — if it is under")
    A("~2%, the graph is being signed almost entirely by default rather than by")
    A("evidence, and the sign-shuffle null in §5 should be expected to come out")
    A("near parity. Observed markers: %s."
      % (", ".join("`%s` x%d" % (k, v) for k, v in
                   sorted(conn_counts.items(), key=lambda kv: -kv[1])[:10]) or "none"))
    A("")

    A("## 2. Field by file")
    A("")
    per_file = defaultdict(list)
    for s in segments:
        per_file[s.path].append(s)
    rows = []
    for path, segs in per_file.items():
        phis = [s.phi for s in segs]
        rows.append((sum(phis) / len(phis), path, len(segs),
                     sum(s.frust for s in segs) / len(segs),
                     max(segs, key=lambda s: s.phi), min(segs, key=lambda s: s.phi)))
    rows.sort()
    A("| file | n | mean phi | mean frustration |")
    A("| --- | ---: | ---: | ---: |")
    for mean_phi, path, n, mean_fr, _hi, _lo in rows:
        A("| `%s` | %d | %+.3f | %.4f |" % (path, n, mean_phi, mean_fr))
    A("")

    A("## 3. Tonal discontinuity docket")
    A("")
    A("Highest per-node frustration: segments whose neighbourhood will not settle")
    A("around them. VALENCE_FIELD.md §0 argues this, not the settled numbers, is")
    A("the output worth reading.")
    A("")
    A("**Two caveats on what this measures here, both load-bearing.**")
    A("")
    A("*It is discontinuity, not contradiction.* That reading requires a working")
    A("sign channel. With %.1f%% of adjacency edges negative (§1), almost every"
      % (100.0 * adj_neg / max(1, adj_total)))
    A("edge asserts agreement, so a high residual means \"this segment reads")
    A("differently from its neighbours\", not \"this segment conflicts with them\".")
    A("Check §5 before upgrading the claim.")
    A("")
    A("*Seeded nodes are structurally favoured.* A pinned node cannot relax toward")
    A("its neighbours, so it carries residual by construction — frustration is")
    A("part signal, part seed-detector. The two lists below are therefore split:")
    A("the unseeded one is what the graph found on its own, and it is the list")
    A("worth reading first.")
    A("")
    unseeded_segs = [s for s in segments if s.nid not in seeds]
    seeded_segs = [s for s in segments if s.nid in seeds]
    A("### 3a. Graph-discovered (unseeded — no lexicon hit of their own)")
    A("")
    _docket(A, sorted(unseeded_segs, key=lambda s: -s.frust)[:args.top], adj, seeds)
    A("### 3b. Seeded (frustration confounded by pinning — read with the caveat)")
    A("")
    _docket(A, sorted(seeded_segs, key=lambda s: -s.frust)[:max(3, args.top // 3)],
            adj, seeds)

    A("## 4. Most important segments")
    A("")
    A("Blend of %s." % ", ".join("%s %.0f%%" % (k, v * 100)
                                 for k, v in IMPORTANCE_WEIGHTS.items()))
    A("")
    top_imp = sorted(segments, key=lambda s: -s.importance)[:args.top]
    A("| # | phi | imp | location | segment |")
    A("| ---: | ---: | ---: | --- | --- |")
    for i, s in enumerate(top_imp, 1):
        A("| %d | %+.2f | %.2f | `%s:%d` | %s |"
          % (i, s.phi, s.importance, s.path, s.line,
             quote(s.text, 120).replace("|", "\\|")))
    A("")

    A("### 4b. Graph-discovered only (unseeded)")
    A("")
    A("The same ranking restricted to segments the lexicon never fired on. These")
    A("are reachable **only** through propagation — if this list is empty or")
    A("worthless, the diffusion is not paying for itself and the honest product")
    A("is a lexicon with a structural ranker.")
    A("")
    top_uns = sorted((s for s in segments if s.nid not in seeds),
                     key=lambda s: -s.importance)[:args.top]
    A("| # | phi | imp | location | segment |")
    A("| ---: | ---: | ---: | --- | --- |")
    for i, s in enumerate(top_uns, 1):
        A("| %d | %+.2f | %.2f | `%s:%d` | %s |"
          % (i, s.phi, s.importance, s.path, s.line,
             quote(s.text, 120).replace("|", "\\|")))
    A("")
    n_uns_top = sum(1 for s in sorted(segments, key=lambda s: -s.importance)[:100]
                    if s.nid not in seeds)
    A("Unseeded segments in the overall top 100: **%d**. Track this number — it is"
      % n_uns_top)
    A("the graph's contribution to *selection*, as opposed to re-ranking, and it")
    A("is the quantity the density weight was silently suppressing.")
    A("")

    A("### Most positive / most negative")
    A("")
    hi = sorted(segments, key=lambda s: -s.phi)[:8]
    lo = sorted(segments, key=lambda s: s.phi)[:8]
    for label, group in (("Most positive", hi), ("Most negative", lo)):
        A("**%s**" % label)
        A("")
        for s in group:
            A("- `%s:%d` %+.3f — %s" % (s.path, s.line, s.phi, quote(s.text, 140)))
        A("")

    A("## 5. Nulls")
    A("")
    if nulls is None:
        A("Not run. Re-run with `--nulls`. **Until they are run, nothing in §2–§4**")
        A("**is evidence of anything** — a smooth field over an invented graph is")
        A("the expected output whether or not the connectives mean anything.")
    else:
        n = nulls
        A("| quantity | real | sign-permute | sign-random | seed-shuffle |")
        A("| --- | ---: | ---: | ---: | ---: |")
        A("| total energy | %.3f | %.3f | %.3f | %.3f |"
          % (n["real_energy"], n["sign_permute_energy_mean"],
             n["sign_random_energy_mean"], n["seed_shuffle_energy_mean"]))
        A("| energy per edge | %.5f | %.5f | %.5f | %.5f |"
          % (n["real_energy_per_edge"], n["sign_permute_energy_per_edge"],
             n["sign_random_energy_per_edge"], n["seed_shuffle_energy_per_edge"]))
        A("| mean abs(phi), unseeded | %.4f | %.4f | %.4f | — |"
          % (n["real_spread_unseeded"], n["sign_permute_spread_mean"],
             n["sign_random_spread_mean"]))
        A("")
        A("%d trials each. Negative edges held at %d in the permute null."
          % (n["trials"], n["negative_edges"]))
        A("")
        perm_ratio = (n["sign_permute_energy_per_edge"] / n["real_energy_per_edge"]
                      if n["real_energy_per_edge"] else float("nan"))
        rand_ratio = (n["sign_random_energy_per_edge"] / n["real_energy_per_edge"]
                      if n["real_energy_per_edge"] else float("nan"))
        A("**Sign-permute ratio: %.3fx.** (sign-random: %.3fx — reference only,"
          % (perm_ratio, rand_ratio))
        A("see the docstring for why that number is not evidence.)")
        A("")
        if perm_ratio > 1.10:
            A("Moving the negative edges elsewhere makes the graph materially harder")
            A("to satisfy, so the connectives are placing them somewhere structurally")
            A("special. That is evidence the extraction is finding real contrast. It")
            A("is still not evidence the numbers are *correct* — that needs an")
            A("external criterion, as in TIER1_RESULTS.md §5, and this run has none.")
        else:
            A("**Permuting which edges are negative barely changes the energy.** The")
            A("connectives are not placing contrast anywhere structurally special, so")
            A("on this corpus the sign channel is inert and §2–§4 are the output of an")
            A("essentially unsigned smoother. Read the connective density in §1 before")
            A("blaming the extractor: if contrast markers are ~1% of segments, there is")
            A("not enough evidence present for any extractor to sign this graph, and")
            A("the honest next move is LLM adjudication of contrast rather than tuning")
            A("the connective list.")
    A("")

    A("## 6. What this run does not establish")
    A("")
    A("- The lexicon is hand-authored (see `lexicon.en.tsv` header). Validating")
    A("  the field against it would be circular. There is no external criterion")
    A("  in this run — unlike Tier 1, which had one and reported r=+0.941.")
    A("- Segments are split by regex. `--dump-segments` is the only way to know")
    A("  whether the units being scored are the units you think they are.")
    A("- Line numbers locate the PARAGRAPH a segment came from, not the segment.")
    A("  For a module docstring that means every segment reports line 1.")
    A("- Source files contribute comments only; identifiers and code are dropped.")
    A("- Boilerplate is not detected. `LICENSE` scores negative on *damages*,")
    A("  *liability*, *without warranty*; it is legal text, not an opinion. Any")
    A("  corpus with vendored licences or CoCs will show the same artefact.")
    A("- Files needing an extractor (pdf, docx, ipynb) were skipped entirely and")
    A("  are listed in §1. Their absence is a coverage gap, not a null result.")
    A("")
    return "\n".join(L)


SEG_BY_ID = {}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    ap = argparse.ArgumentParser(
        description="Signed valence field over an arbitrary folder tree.")
    ap.add_argument("roots", nargs="+", help="files or directories to scan")
    ap.add_argument("--lexicon", default=None,
                    help="polarity lexicon TSV (default: lexicon.en.tsv beside this script)")
    ap.add_argument("--report", default=None, help="write markdown report here")
    ap.add_argument("--json", default=None, help="write per-segment JSON here")
    ap.add_argument("--dump-segments", action="store_true",
                    help="print the segmentation and exit. DO THIS FIRST.")
    ap.add_argument("--nulls", action="store_true", help="run permutation nulls")
    ap.add_argument("--trials", type=int, default=20)
    # gamma is the decay pulling unseeded nodes toward zero. ttdb_valence.py
    # defaults to 0.15 on a small, densely-seeded store. A folder scan is the
    # opposite regime -- thousands of nodes, single-digit-percent seeding -- and
    # 0.15 there flattens the field to zero before it can propagate. Lower it,
    # and read the "mean abs(phi), unseeded" row in §5 to see whether the field
    # is actually spreading or just decaying.
    ap.add_argument("--gamma", type=float, default=0.03)
    ap.add_argument("--omega", type=float, default=0.8)
    # Measured on this repo: min-hits 2 seeds 1.5% of segments and the field
    # decays to zero; min-hits 1 seeds 17%. Segments are single clauses, so
    # requiring two evaluative words in one is a threshold almost nothing meets.
    # The cost is noisier seeds, which the seed-shuffle null is there to price.
    ap.add_argument("--min-hits", type=int, default=1,
                    help="lexicon hits required before a segment may seed")
    ap.add_argument("--min-abs", type=float, default=0.25,
                    help="minimum abs(mean polarity) to seed")
    ap.add_argument("--no-tech-neutral", action="store_true",
                    help="disable technical-vocabulary suppression")
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--ignore", action="append", default=[],
                    help="extra ignore glob (repeatable)")
    ap.add_argument("--seed", type=int, default=20260802)
    args = ap.parse_args()

    # The corpus is UTF-8 by construction (is_readable_text guarantees it); the
    # Windows console is not. Without this the report dies on the first sigma.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    lex_path = args.lexicon or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "lexicon.en.tsv")
    if not os.path.isfile(lex_path):
        sys.exit("lexicon not found: %s" % lex_path)
    lex = load_lexicon(lex_path)

    # Never scan our own output. Writing the report into the tree being scanned
    # is the normal case, and without this the second run reads the first run's
    # findings as corpus -- a feedback loop that inflates whatever it found.
    self_outputs = [os.path.basename(p) for p in (args.report, args.json) if p]

    skips = Skips()
    files = walk(args.roots, skips, list(args.ignore) + self_outputs)
    if not files:
        sys.exit("no readable files found")

    segments = []
    links = []
    for path, text in files:
        segs, lks = segment_file(path, text)
        segments.extend(segs)
        links.extend(lks)
    if not segments:
        sys.exit("no segments produced; try --dump-segments on a smaller root")

    if args.dump_segments:
        for s in segments:
            print("%-40s L%-5d %-8s join=%-12s | %s"
                  % (s.nid[-40:], s.line, s.kind, s.join or "-", quote(s.text, 110)))
        print("\n%d segments across %d files" % (len(segments), len(files)))
        return

    stats = {"suppressed": 0, "suppressed_words": defaultdict(int),
             "lexicon_size": len(lex)}
    seeds = {}
    for s in segments:
        score_segment(s, lex, not args.no_tech_neutral, stats)
        v = seed_from_hits(s, args.min_hits, args.min_abs)
        if v is not None:
            s.seed = v
            seeds[s.nid] = v

    if not seeds:
        sys.exit("no segments met the seeding threshold; lower --min-hits/--min-abs")

    global SEG_BY_ID
    SEG_BY_ID = {s.nid: s for s in segments}
    first_by_file = {}
    for s in segments:
        first_by_file.setdefault(s.path, s.nid)

    edges = build_edges(segments, links, first_by_file)
    nodes = [s.nid for s in segments]
    adj, merged = ttdb_valence.build_adjacency(
        nodes, [(a, b, kind, w, sg) for a, b, w, sg, kind, _j in edges])

    phi, iters, delta = ttdb_valence.solve(
        nodes, adj, seeds, gamma=args.gamma, omega=args.omega)
    frust = ttdb_valence.node_frustration(adj, phi)
    # Per-UNIT-WEIGHT frustration, not raw. node_frustration() sums residuals
    # over neighbours, so it grows with degree -- measured at r=+0.27 here, with
    # degree spanning 3..247. Raw ranking therefore surfaces hubs (file titles)
    # rather than segments that actually sit badly with their context. Dividing
    # by incident weight asks the right question: how badly does this segment
    # fit, per unit of evidence about where it belongs.
    for s in segments:
        s.phi = phi[s.nid]
        incident = sum(w for _m, w, _sg in adj[s.nid])
        s.frust = frust.get(s.nid, 0.0) / incident if incident > 0 else 0.0
    rank_importance(segments)

    nulls = None
    if args.nulls:
        rng = random.Random(args.seed)
        nulls = run_nulls(nodes, edges, seeds, phi, args.gamma, args.omega,
                          args.trials, rng)

    report = build_report(args, files, skips, segments, edges, seeds, stats,
                          nulls, iters, delta, adj)
    if args.report:
        with open(args.report, "w", encoding="utf-8") as fh:
            fh.write(report)
        print("wrote %s" % args.report)
    else:
        print(report)

    if args.json:
        payload = [{
            "id": s.nid, "path": s.path, "line": s.line, "kind": s.kind,
            "section": s.section, "join": s.join, "phi": round(s.phi, 6),
            "frustration": round(s.frust, 6), "importance": round(s.importance, 6),
            "seed": s.seed, "hits": s.hits, "text": s.text,
        } for s in sorted(segments, key=lambda s: -s.importance)]
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"segments": payload, "nulls": nulls}, fh, indent=1)
        print("wrote %s" % args.json)


if __name__ == "__main__":
    main()
