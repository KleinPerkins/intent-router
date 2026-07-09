"""proposal — L5: serialize a router decision into the `intent-proposal/v1` envelope. PURE /
deterministic; EXECUTIONLESS by construction (ARCHITECTURE.md pipeline table: "no execution field
exists", CR1) — every field below is descriptive data, never a runnable action.

Emits EXACTLY the 11 required keys of `contracts/intent-proposal.v1.json` (the envelope is
PROVISIONAL until A0 exercises it against a hand-written consumer fixture — see that contract's
`freeze_exempt_reason`); this module does not anticipate the A0/R2 `deferred_additions`.

Conservative-by-construction (the offline degrade property, CR8):
  - No candidate scored above zero (verdict `none`, `top` is None) -> the MOST cautious floor:
    `safety_class=destructive`, `confidence=0.0`, `requires_confirmation=True`, empty verb/params.
  - A candidate matched -> `safety_class`/`tool_path`/`start_point` are read VERBATIM from the
    catalog entry the utterance's token-overlap selected; they are NEVER derived from the
    utterance's own text, so no phrasing in the utterance (however insistent) can talk its way into
    a different `safety_class` than the catalog declares for that verb (CR5 — data, never
    instructions; L1's scorer only ever counts overlap against DECLARED catalog fields).
"""

from __future__ import annotations

from .verdict import STRONG_MARGIN, STRONG_MIN

# No real verb exists for the conservative no-match floor; "cli" is an arbitrary-but-documented
# placeholder value — the field is meaningless without a chosen verb, but the frozen enum has no
# "none"/"n-a" member and the required-key floor gives this field no room to be absent.
_NO_MATCH_TOOL_PATH = "cli"
_NO_MATCH_SAFETY_CLASS = "destructive"
_NO_MATCH_START_POINT = "unknown"

# confidence is a pure, deterministic RE-PROJECTION of the L1/L2 score onto [0, 1] — not a second,
# independently-calibrated estimate. STRONG_MIN + STRONG_MARGIN is the score at which a match is
# unambiguously "strong" (verdict.py); scores at/above it saturate to 1.0, everything below scales
# linearly. Deriving confidence from verdict's OWN thresholds means the two fields can never
# silently disagree about what "confident" means. The ONE case where `confidence` (raw match
# strength to the selected verb) can read higher than the `verdict` band is an engine-level
# honest-confidence DE-ESCALATION (engine._honest_confidence): a strong read that competes with a
# destructive verb is downgraded to `weak`. That divergence is never silent — it is logged in
# `why[]` ("deescalated:...") and, crucially, `requires_confirmation` (not `confidence`) is the
# operative safety bool a consumer's kernel-facing loop relies on, and it flips True on de-escalation.
_CONFIDENCE_SATURATION = STRONG_MIN + STRONG_MARGIN


def _confidence_from_score(score: float) -> float:
    if not score or score <= 0:
        return 0.0
    return round(min(1.0, score / _CONFIDENCE_SATURATION), 4)


def _required_param_names(verb_entry: dict | None) -> list[str]:
    """Every `param_schema` slot marked `required: true`. L4 (typed param extraction) is absent in
    R-core, so NOTHING is ever extracted — every required slot a matched verb declares is honestly
    reported as missing, sorted for determinism."""
    if not verb_entry:
        return []
    schema = verb_entry.get("param_schema")
    if not isinstance(schema, list):
        return []
    names = [
        p.get("name") for p in schema
        if isinstance(p, dict) and p.get("required") is True and isinstance(p.get("name"), str)
    ]
    return sorted(names)


def _start_point_for(verb_entry: dict | None) -> str:
    """Read the catalog-declared default start point. Pure and catalog-sourced ONLY — L5 does no
    live environment/repo introspection (that would break both purity and determinism)."""
    if not verb_entry:
        return _NO_MATCH_START_POINT
    rules = verb_entry.get("start_point_rules")
    if isinstance(rules, dict) and isinstance(rules.get("default"), str) and rules["default"]:
        return rules["default"]
    return _NO_MATCH_START_POINT


def build_proposal(consumer: str, verdict: str, top: dict | None, verb_entry: dict | None,
                   extra_why: list | None = None) -> dict:
    """Serialize ONE `intent-proposal/v1` envelope.

    `top` is L1's top-scoring candidate (`candidates.score_verb`'s return shape, or None); `verb_
    entry` is that candidate's full catalog entry (or None). L5 reads `safety_class`/`tool_path`/
    `param_schema`/`start_point_rules` from `verb_entry`, never from `top`'s score/why alone —
    L1 does not interpret those fields, so L5 is the first (and only) layer that does.

    `extra_why` is an optional list of engine-level breadcrumbs (e.g. the honest-confidence
    de-escalation reason) appended to `why[]` so a de-escalation is auditable on every surface.
    """
    if not top or not verb_entry:
        return {
            "consumer": consumer,
            "verb": "",
            "params": {},
            "start_point": _NO_MATCH_START_POINT,
            "safety_class": _NO_MATCH_SAFETY_CLASS,
            "tool_path": _NO_MATCH_TOOL_PATH,
            "confidence": 0.0,
            "verdict": "none",
            "why": [f"verdict:{verdict}", "no-signal"],
            "missing_params": [],
            "requires_confirmation": True,
        }

    missing = _required_param_names(verb_entry)
    safety_class = verb_entry.get("safety_class", _NO_MATCH_SAFETY_CLASS)
    # Conservative-by-construction: confirmation is skipped ONLY for an unambiguous (strong),
    # low-stakes (read-only), fully-specified (no missing required params) match. Any uncertainty,
    # any write/destructive verb, or any unfilled required slot always asks — this is the one bool
    # a consumer's kernel-facing loop can rely on to mean "truly nothing to double-check."
    requires_confirmation = bool(missing) or not (verdict == "strong" and safety_class == "read")
    why = [f"verdict:{verdict}"] + list(extra_why or []) + list(top.get("why") or ["no-signal"])

    return {
        "consumer": consumer,
        "verb": top.get("verb", ""),
        "params": {},
        "start_point": _start_point_for(verb_entry),
        "safety_class": safety_class,
        "tool_path": verb_entry.get("tool_path", _NO_MATCH_TOOL_PATH),
        "confidence": _confidence_from_score(top.get("score", 0.0)),
        "verdict": verdict,
        "why": why,
        "missing_params": missing,
        "requires_confirmation": requires_confirmation,
    }
