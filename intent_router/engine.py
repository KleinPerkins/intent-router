"""engine — pipeline wiring: L1 (candidates) -> L2 (verdict) -> L5 (proposal). PURE / deterministic.

`propose()` is the single entry point the CLI `map` verb and the MCP `intent_map` tool both call —
the L0-L2+L5 deterministic floor the offline-degrade property (CR8) requires. L3 (LLM rerank) and
L4 (typed param extraction) are simply ABSENT in R-core — not stubbed, not toggled off, there is no
module to call — so this pipeline already exercises "a valid conservative proposal with L3/L4
absent" on every call, by construction rather than by a runtime flag.

Never executes anything (CR1): this module only ranks, classifies, and serializes; it never runs,
shells out to, or authorizes a consumer verb.
"""

from __future__ import annotations

from typing import Any

from .candidates import rank_candidates
from .catalog import find_verb
from .proposal import build_proposal
from .verdict import classify, top_candidate

DEFAULT_EXPLAIN_TOP_N = 5


def _verbs_of(catalog: Any) -> list:
    verbs = catalog.get("verbs") if isinstance(catalog, dict) else None
    return verbs if isinstance(verbs, list) else []


def _top_for_verdict(ranked: list[dict], verdict: str) -> dict | None:
    """The candidate a proposal may be built FROM — None whenever verdict is `none`, even if some
    candidate scored a nonzero-but-sub-floor amount. `top_candidate` alone answers "did anything
    score above zero"; the proposal must instead answer "is the router confident enough to name a
    specific verb" — those are different questions, and only `verdict` (the safety-relevant L2
    output) may answer the second one. Without this gate a sub-floor score could still leak a real
    verb/safety_class into a `none`-verdict proposal, undermining the conservative-when-uncertain
    guarantee CR8 requires."""
    if verdict == "none":
        return None
    return top_candidate(ranked)


def propose(consumer: str, utterance: str, catalog: dict) -> dict:
    """Run the full deterministic floor for one utterance against one catalog and return ONE
    serialized `intent-proposal/v1` envelope. Pure: same inputs always produce the same output."""
    verbs = _verbs_of(catalog)
    ranked = rank_candidates(utterance, verbs)
    verdict = classify(ranked)
    top = _top_for_verdict(ranked, verdict)
    verb_entry = find_verb(verbs, top["verb"]) if top else None
    return build_proposal(consumer, verdict, top, verb_entry)


def explain(consumer: str, utterance: str, catalog: dict, top_n: int = DEFAULT_EXPLAIN_TOP_N) -> dict:
    """Same pipeline as `propose`, but surfaces the full ranked candidate list (top `top_n`, each
    with its per-signal `matched`/`contributions`/`why`) alongside the final proposal — the extra
    detail `intent explain` / `intent_explain` show on top of plain `map`. `candidates` intentionally
    shows ranked candidates regardless of verdict (that IS the explanation of a `none` verdict); the
    nested `proposal` still applies the same conservative gate as `propose`."""
    verbs = _verbs_of(catalog)
    ranked = rank_candidates(utterance, verbs)
    verdict = classify(ranked)
    top = _top_for_verdict(ranked, verdict)
    verb_entry = find_verb(verbs, top["verb"]) if top else None
    proposal = build_proposal(consumer, verdict, top, verb_entry)
    return {
        "utterance": utterance,
        "verdict": verdict,
        "candidates": ranked[:top_n],
        "proposal": proposal,
    }
