"""Fix #6 — honest-confidence de-escalation on competing destructive+read signals.

BITING regression for `engine._honest_confidence`. Against pre-fix code the mixed-signal utterance
resolved to a CONFIDENT `strong` read with `requires_confirmation=False` (a bare-green skip-confirm
while a destructive reading was plausibly present); after the fix the competing destructive signal
de-escalates the verdict to `weak`, flipping `requires_confirmation` True and logging the reason in
`why[]`. Drives the shipped `propose`/`explain` pipeline (not a re-impl).

Scope guard (proves the fix is NARROW, not a blanket "always confirm"):
  - an unambiguous strong read with NO destructive competitor still skips confirmation, and
  - a destructive-top utterance is entirely unaffected (already confirmed).

The catalog tokens are chosen to score deterministically under the real scorer:
  W_ALIAS=10/token, W_VERB_NAME=5 flat; STRONG_MIN=25, STRONG_MARGIN=10, WEAK_MIN=8.
"""

from __future__ import annotations

import unittest

from intent_router.engine import explain, propose

_DEESCALATE_WHY = "deescalated:competing-destructive-signal"

# read verb `inspect` (alias tokens: inspect, audit, report) and destructive verb `purge`
# (alias tokens: purge, remove). Disjoint alias vocabularies so each utterance's scores are
# controlled purely by which words it contains.
_CATALOG = {
    "schema": "intent-catalog/v1",
    "verbs": [
        {
            "verb": "inspect",
            "aliases": ["inspect audit report"],
            "examples": [],
            "param_schema": [],
            "preconditions": [],
            "safety_class": "read",
            "tool_path": "cli",
            "start_point_rules": {"default": "current"},
            "plain_label": "Show a report",
            "consequence_copy": "Nothing changes; reporting only.",
        },
        {
            "verb": "purge",
            "aliases": ["purge remove"],
            "examples": [],
            "param_schema": [],
            "preconditions": [],
            "safety_class": "destructive",
            "tool_path": "cli",
            "start_point_rules": {"default": "current"},
            "plain_label": "Discard old copies",
            "consequence_copy": "Permanently discards the selected copies.",
        },
    ],
}


class TestHonestConfidenceDeescalation(unittest.TestCase):
    def test_competing_destructive_deescalates_strong_read(self):
        # inspect: alias{inspect,audit,report}=30 + verb{inspect}=5 = 35 (top, read)
        # purge:   alias{purge}=10 + verb{purge}=5 = 15 (runner, destructive, >= WEAK_MIN)
        # top-runner = 20 >= STRONG_MARGIN -> pre-fix verdict was STRONG.
        p = propose("AWA", "inspect audit report then purge", _CATALOG)
        self.assertEqual(p["verb"], "inspect", "read verb is still the token-overlap winner")
        self.assertEqual(p["safety_class"], "read", "safety_class is catalog-sourced, never flipped")
        # The bite: pre-fix this was verdict=strong / requires_confirmation=False.
        self.assertEqual(p["verdict"], "weak",
                         "a competing destructive signal must de-escalate a strong read to weak")
        self.assertIs(p["requires_confirmation"], True,
                      "de-escalated read must ask for confirmation")
        self.assertIn(_DEESCALATE_WHY, p["why"], "de-escalation must be auditable in why[]")

    def test_deescalation_visible_on_explain_surface(self):
        out = explain("AWA", "inspect audit report then purge", _CATALOG)
        self.assertEqual(out["verdict"], "weak")
        self.assertEqual(out["proposal"]["verdict"], "weak")
        self.assertIs(out["proposal"]["requires_confirmation"], True)
        self.assertIn(_DEESCALATE_WHY, out["proposal"]["why"])

    def test_unambiguous_strong_read_survives_no_deescalation(self):
        # No destructive token -> purge scores 0 (excluded) -> no competitor -> confident read holds.
        p = propose("AWA", "inspect audit report", _CATALOG)
        self.assertEqual(p["verb"], "inspect")
        self.assertEqual(p["verdict"], "strong",
                         "fix must be NARROW: a clean read with no destructive rival stays strong")
        self.assertIs(p["requires_confirmation"], False,
                      "the canonical skip-confirm path must be preserved")
        self.assertNotIn(_DEESCALATE_WHY, p["why"])

    def test_destructive_top_is_unaffected(self):
        # purge: alias{purge,remove}=20 + verb{purge}=5 = 25 (top, destructive); inspect scores 0.
        p = propose("AWA", "purge remove", _CATALOG)
        self.assertEqual(p["verb"], "purge")
        self.assertEqual(p["safety_class"], "destructive")
        self.assertIs(p["requires_confirmation"], True)
        # de-escalation only ever touches a strong READ top; it must not tag a destructive top.
        self.assertNotIn(_DEESCALATE_WHY, p["why"])

    def test_deescalation_is_deterministic(self):
        a = propose("AWA", "inspect audit report then purge", _CATALOG)
        b = propose("AWA", "inspect audit report then purge", _CATALOG)
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
