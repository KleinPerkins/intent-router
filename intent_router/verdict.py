"""verdict — L2: strong|weak|none classification over L1's ranked candidates. PURE / deterministic.

THE SAFETY-RELEVANT OUTPUT (ARCHITECTURE.md pipeline table: "L2 verdict ... SAFETY-RELEVANT floor").
Conservative by construction: a thin margin over the runner-up never escalates to `strong`, and a
verdict is computed ONLY from the two top scores — never from utterance content directly, so no
text in the utterance (however phrased, however insistent) can talk its way to a stronger verdict
than the deterministic token overlap earns (CR5 — data, never instructions).

Thresholds are adapted from agent-route's `verdict_from_ranking` (same shape: strong requires both
an absolute floor AND a margin over the runner-up, so two near-tied candidates never both read as
confident). Calibration of the exact numbers against catalog verbs (aliases/examples/verb-name/
plain_label) instead of a workspace registry is exercised by the AWA golden set
(`tests/golden/awa.golden.json`) — see CR8 `deterministic_floor_golden_set`.
"""

from __future__ import annotations

STRONG_MIN = 25.0
STRONG_MARGIN = 10.0
WEAK_MIN = 8.0

VERDICTS = ("strong", "weak", "none")


def _nonzero(ranked: list[dict]) -> list[dict]:
    return [c for c in ranked if c.get("score", 0) > 0]


def classify(ranked: list[dict]) -> str:
    """`ranked` must already be sorted score-descending (see `candidates.rank_candidates`). A
    zero-score candidate never counts as a match — an empty catalog or a catalog with zero token
    overlap both correctly verdict `none`."""
    nz = _nonzero(ranked)
    if not nz:
        return "none"
    top = nz[0]["score"]
    runner = nz[1]["score"] if len(nz) >= 2 else 0.0
    if top >= STRONG_MIN and (top - runner) >= STRONG_MARGIN:
        return "strong"
    if top >= WEAK_MIN:
        return "weak"
    return "none"


def top_candidate(ranked: list[dict]) -> dict | None:
    """The candidate the verdict is about, or None when nothing scored above zero (the offline
    degrade case — L5 must still produce a valid, conservative proposal for this, never crash)."""
    nz = _nonzero(ranked)
    return nz[0] if nz else None
