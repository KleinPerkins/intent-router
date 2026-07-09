"""normalize — L0 utterance normalization. PURE / deterministic (ARCHITECTURE.md L0).

Vendored from `~/.cursor/skills/agent-route/lib/score.py` (the `agent-route` global capability's
normalization engine), stripped of everything route-specific (root scoring, move-intent detection,
git-origin parsing) and made fully self-contained and ld-agnostic: no filesystem coupling, no
imports outside stdlib, no reference to any host/consumer. Only the pure tokenizer survives here —
L0's entire job is "lowercase / synonym / acronym normalization" (ARCHITECTURE.md pipeline table).

Pipeline: lower -> split -> additive acronym expand -> bidirectional synonym expand -> singularize
-> English stoplist filter -> set of tokens. No fuzzy floats, no per-query tuning: normalization is
deterministic and identical on every call for the same inputs (CR8's deterministic floor).
"""

from __future__ import annotations

import re

# Adapted from agent-route's `[-_/\s.,:'"]+`: operator UTTERANCES are natural-language sentences
# (unlike agent-route's short task descriptions), so `?!` are added to the split set — "is
# everything okay?" must tokenize identically to "is everything okay".
_SPLIT_RE = re.compile(r"[-_/\s.,:'\"?!]+")

STOPWORDS: frozenset[str] = frozenset({
    "a", "an", "the", "this", "that", "these", "those", "my", "your", "our", "their", "its",
    "and", "or", "but", "if", "so", "as", "of", "to", "in", "on", "at", "by", "for", "from",
    "with", "without", "into", "onto", "over", "under", "via", "per",
    "is", "are", "was", "were", "be", "been", "being", "am",
    "do", "does", "did", "doing", "done",
    "have", "has", "had", "having",
    "will", "would", "should", "could", "can", "may", "might", "must", "shall",
    "i", "me", "you", "we", "they", "he", "she", "it", "us", "them", "him", "her",
    "what", "which", "who", "whom", "whose", "when", "why",
    "all", "any", "both", "each", "few", "more", "most", "other", "some", "such",
    "no", "not", "only", "own", "same", "than", "too", "very", "just", "now", "then",
    "here", "there", "also", "still", "yet",
    "s", "t", "ll", "ve", "re", "d", "m",
    "thing", "things", "stuff",
    "new", "old",
    "use", "used", "using", "uses",
    "make", "makes", "made", "making",
    "please", "okay", "ok",
})


def singularize(tok: str) -> str:
    """Conservative rule-based singularizer (matching, not English)."""
    if len(tok) <= 3:
        return tok
    if tok.endswith("ies") and len(tok) > 4:
        return tok[:-3] + "y"
    if tok.endswith("ses") or tok.endswith("xes") or tok.endswith("zes"):
        return tok[:-2]
    if tok.endswith("s") and not tok.endswith("ss"):
        return tok[:-1]
    return tok


def build_alias_to_canon(synonyms: dict[str, list[str]]) -> dict[str, str]:
    """Precompute alias -> canonical from a synonyms map."""
    out: dict[str, str] = {}
    for canon, aliases in synonyms.items():
        for a in aliases:
            out[a.lower()] = canon.lower()
    return out


def normalize_tokens(
    text: str,
    acronyms: dict[str, str] | None = None,
    synonyms: dict[str, list[str]] | None = None,
    alias_to_canon: dict[str, str] | None = None,
) -> frozenset[str]:
    """Lower -> split -> ADDITIVE acronym expand -> bidirectional synonym expand -> singularize
    -> stoplist. Returns a frozenset (overlap scoring ignores order; pure, hashable, deterministic).

    All inputs default to empty so L0 is usable with zero configuration (no synonyms/acronyms
    files required to exist) — the offline degrade property holds at the tokenizer layer too.
    """
    if not text:
        return frozenset()
    acronyms = acronyms or {}
    synonyms = synonyms or {}
    if alias_to_canon is None:
        alias_to_canon = build_alias_to_canon(synonyms)

    raw_tokens = [t for t in _SPLIT_RE.split(text.lower()) if t]
    expanded: list[str] = list(raw_tokens)
    for tok in raw_tokens:
        if tok in acronyms:
            for sub in _SPLIT_RE.split(acronyms[tok]):
                if sub:
                    expanded.append(sub)

    augmented = list(expanded)
    for tok in expanded:
        if tok in synonyms:
            augmented.extend(a.lower() for a in synonyms[tok])
        if tok in alias_to_canon:
            augmented.append(alias_to_canon[tok])

    # Stopword-filter BOTH before and after singularization. The vendored original filtered only
    # post-singularization, which lets a stopword whose singular form collides with a real short
    # word slip through (e.g. "this" -> naive-singularize -> "thi", not in STOPWORDS, survives as a
    # spurious token). L2's verdict is the safety-relevant output, so a stray token that could
    # coincidentally overlap a catalog term is a correctness bug worth fixing here, not just a style
    # nit — documented deviation from the vendored source.
    out: set[str] = set()
    for t in augmented:
        if not t or t in STOPWORDS:
            continue
        st = singularize(t)
        if not st or st in STOPWORDS or len(st) <= 1:
            continue
        out.add(st)
    return frozenset(out)


def normalize_text(text: str) -> str:
    """Lightweight, lossless normalization (lower + collapsed whitespace) for display/echo
    purposes — NOT the token-set used for scoring (see `normalize_tokens`)."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", text.strip().lower())
