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
from .verdict import WEAK_MIN, classify, top_candidate

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


def _competing_destructive(ranked: list[dict], verbs: list, top_verb: str) -> bool:
    """True when some NON-top candidate maps to a `destructive` catalog verb and still crosses the
    weak floor — i.e. the utterance carries a real destructive signal alongside the (read) top."""
    for cand in ranked:
        if cand.get("verb") == top_verb:
            continue
        if cand.get("score", 0.0) < WEAK_MIN:
            continue
        entry = find_verb(verbs, cand.get("verb"))
        if entry and entry.get("safety_class") == "destructive":
            return True
    return False


def _honest_confidence(ranked: list[dict], verbs: list, verdict: str, top: dict | None):
    """Honest-confidence de-escalation. Serves the CR10 honest-confidence principle
    (CONSTITUTION.md CR10; ARCHITECTURE.md 'Honest confidence, never a bare color') at the VERDICT
    layer — it is NOT the CR10 egress gate itself (that gate lives at the surface/egress phase). When
    a `strong` READ verdict competes with a DESTRUCTIVE verb that also crosses the weak floor
    (token-stuffing / genuinely mixed signals), downgrade the verdict to `weak`. That flips
    `requires_confirmation` on, so the router never returns a confident, no-confirm read while a
    destructive reading was plausibly present. Returns `(verdict, extra_why)`.

    Deliberately MINIMAL — it does NOT re-score or reclassify. The pure-semantic `destructive->read`
    catalog downgrade (an utterance whose ground truth is destructive but that best matches a read
    verb's language, with NO destructive candidate crossing the floor) remains a DOCUMENTED
    STRUCTURAL LIMIT of the deterministic floor; its real defense is the kernel-sourced confirmation
    at A0 (KI3/KI4), not utterance-content scoring here."""
    if verdict != "strong" or not top:
        return verdict, []
    entry = find_verb(verbs, top.get("verb"))
    if not entry or entry.get("safety_class") != "read":
        return verdict, []
    if _competing_destructive(ranked, verbs, top.get("verb")):
        return "weak", ["deescalated:competing-destructive-signal"]
    return verdict, []


def propose(consumer: str, utterance: str, catalog: dict) -> dict:
    """Run the full deterministic floor for one utterance against one catalog and return ONE
    serialized `intent-proposal/v1` envelope. Pure: same inputs always produce the same output."""
    verbs = _verbs_of(catalog)
    ranked = rank_candidates(utterance, verbs)
    verdict = classify(ranked)
    top = _top_for_verdict(ranked, verdict)
    verdict, extra_why = _honest_confidence(ranked, verbs, verdict, top)
    verb_entry = find_verb(verbs, top["verb"]) if top else None
    return build_proposal(consumer, verdict, top, verb_entry, extra_why=extra_why)


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
    verdict, extra_why = _honest_confidence(ranked, verbs, verdict, top)
    verb_entry = find_verb(verbs, top["verb"]) if top else None
    proposal = build_proposal(consumer, verdict, top, verb_entry, extra_why=extra_why)
    return {
        "utterance": utterance,
        "verdict": verdict,
        "candidates": ranked[:top_n],
        "proposal": proposal,
    }
