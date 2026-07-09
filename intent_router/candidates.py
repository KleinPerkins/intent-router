"""candidates — L1: rank a consumer's catalog verbs against a normalized utterance. PURE /
deterministic, explainable (ARCHITECTURE.md L1). Adapted from agent-route's `score_root` weighting
pattern (`~/.cursor/skills/agent-route/lib/score.py`) — normalize-then-overlap (set intersection),
weighted per signal, no fuzzy floats — but re-targeted at CATALOG fields instead of a workspace
registry: `aliases` (the strongest intentional signal a catalog author writes), `examples` (worded
utterances), the `verb` identifier itself, and a light `plain_label` signal.

L1 does not interpret param_schema/safety_class/tool_path at all — it ONLY answers "how well does
this utterance's language overlap this verb's declared language", with a machine-readable `why`.
Choosing a verb's SAFETY properties is entirely L5's job, read from the catalog entry, never
influenced by the utterance's content (CR5 — the scorer only ever counts token overlap; it never
executes or interprets instructions found in the utterance).
"""

from __future__ import annotations

from typing import Any

from .normalize import build_alias_to_canon, normalize_tokens

W_ALIAS = 10.0
W_EXAMPLE = 6.0
W_VERB_NAME = 5.0
W_PLAIN_LABEL = 2.0


def _overlap_text_or_list(value: Any, task_tokens: frozenset, acronyms, synonyms, alias_to_canon) -> frozenset:
    if isinstance(value, str):
        toks = normalize_tokens(value, acronyms, synonyms, alias_to_canon)
    else:
        toks: set[str] = set()
        for item in value or []:
            if isinstance(item, str):
                toks |= normalize_tokens(item, acronyms, synonyms, alias_to_canon)
        toks = frozenset(toks)
    return toks & task_tokens


def score_verb(
    task_tokens: frozenset,
    verb_entry: dict,
    acronyms: dict | None = None,
    synonyms: dict | None = None,
    alias_to_canon: dict | None = None,
) -> dict:
    """Score ONE verb entry against already-normalized utterance tokens. Pure function; returns a
    JSON-serializable dict (safe to hand directly to `intent explain --json`)."""
    acronyms = acronyms or {}
    synonyms = synonyms or {}
    if alias_to_canon is None:
        alias_to_canon = build_alias_to_canon(synonyms)

    contributions: dict[str, float] = {}
    matched: dict[str, list[str]] = {}

    alias_hits = _overlap_text_or_list(verb_entry.get("aliases", []), task_tokens, acronyms, synonyms, alias_to_canon)
    if alias_hits:
        contributions["alias"] = W_ALIAS * len(alias_hits)
        matched["alias"] = sorted(alias_hits)

    example_hits = _overlap_text_or_list(verb_entry.get("examples", []), task_tokens, acronyms, synonyms, alias_to_canon)
    if example_hits:
        contributions["example"] = W_EXAMPLE * len(example_hits)
        matched["example"] = sorted(example_hits)

    verb_name = verb_entry.get("verb", "") or ""
    verb_tokens = normalize_tokens(verb_name, acronyms, synonyms, alias_to_canon)
    verb_hits = verb_tokens & task_tokens
    if verb_hits:
        contributions["verb_name"] = float(W_VERB_NAME)
        matched["verb_name"] = sorted(verb_hits)

    plain_label_hits = _overlap_text_or_list(verb_entry.get("plain_label", ""), task_tokens, acronyms, synonyms, alias_to_canon)
    if plain_label_hits:
        contributions["plain_label"] = float(W_PLAIN_LABEL)
        matched["plain_label"] = sorted(plain_label_hits)

    score = round(sum(contributions.values()), 2)

    why: list[str] = []
    for sig in ("alias", "example", "verb_name", "plain_label"):
        if sig in matched:
            why.append(f"{sig}:{','.join(matched[sig][:6])}")
    if not why:
        why.append("no-signal")

    return {
        "verb": verb_name,
        "score": score,
        "contributions": {k: round(v, 2) for k, v in contributions.items()},
        "matched": matched,
        "why": why,
    }


def rank_candidates(
    utterance: str,
    verbs: list[dict],
    acronyms: dict | None = None,
    synonyms: dict | None = None,
) -> list[dict]:
    """Rank every verb entry in `verbs` (a catalog's `verbs` array) against `utterance`. Returns a
    list sorted by score DESCENDING, tie-broken by verb name ASCENDING for full determinism
    regardless of the catalog's own on-disk ordering. Non-dict entries are skipped outright (catalog
    shape is `catalog.py`'s job to validate; L1 stays defensive rather than raising on garbage input).
    """
    acronyms = acronyms or {}
    synonyms = synonyms or {}
    alias_to_canon = build_alias_to_canon(synonyms)
    task_tokens = normalize_tokens(utterance, acronyms, synonyms, alias_to_canon)

    scored = [
        score_verb(task_tokens, entry, acronyms, synonyms, alias_to_canon)
        for entry in verbs
        if isinstance(entry, dict)
    ]
    scored.sort(key=lambda c: (-c["score"], c["verb"]))
    return scored
