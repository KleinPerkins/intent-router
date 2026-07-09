"""L5 proposal-serialize tests — emits the `intent-proposal/v1` envelope. Pure, EXECUTIONLESS (no
field runs anything), conservative-by-construction on the no-match floor. Every proposal must carry
EXACTLY the 11 frozen required keys and nothing that could execute."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from intent_router.proposal import build_proposal
from intent_router.verdict import STRONG_MARGIN, STRONG_MIN

_CONTRACT = json.loads(
    (Path(__file__).resolve().parent.parent / "contracts" / "intent-proposal.v1.json").read_text(encoding="utf-8")
)
_REQUIRED_KEYS = set(_CONTRACT["required_keys"])
_SATURATION = STRONG_MIN + STRONG_MARGIN


def _top(verb="protect", score=40.0, why=None):
    return {"verb": verb, "score": score, "why": why or ["alias:protect"]}


def _entry(**overrides):
    base = {
        "verb": "protect",
        "safety_class": "write",
        "tool_path": "mcp",
        "param_schema": [{"name": "target", "type": "path", "required": True}],
        "start_point_rules": {"default": "repo-root"},
    }
    base.update(overrides)
    return base


class TestEnvelopeShape(unittest.TestCase):
    def test_every_proposal_has_exactly_the_frozen_required_keys(self):
        for verdict, top, entry in (
            ("none", None, None),
            ("weak", _top(score=10.0), _entry(safety_class="read", param_schema=[])),
            ("strong", _top(), _entry()),
        ):
            p = build_proposal("AWA", verdict, top, entry)
            self.assertEqual(set(p), _REQUIRED_KEYS,
                             f"proposal keys must equal the frozen floor for verdict={verdict}")

    def test_proposal_is_json_serializable_plain_data(self):
        p = build_proposal("AWA", "strong", _top(), _entry())
        json.dumps(p)  # must not raise — no callables/handles anywhere in the envelope


class TestNoMatchFloor(unittest.TestCase):
    def test_no_top_degrades_to_maximally_conservative(self):
        p = build_proposal("AWA", "none", None, None)
        self.assertEqual(p["verb"], "")
        self.assertEqual(p["params"], {})
        self.assertEqual(p["verdict"], "none")
        self.assertEqual(p["safety_class"], "destructive")
        self.assertEqual(p["confidence"], 0.0)
        self.assertEqual(p["missing_params"], [])
        self.assertIs(p["requires_confirmation"], True)

    def test_top_without_entry_also_floors(self):
        # A top candidate but no resolvable catalog entry must still floor (never guess safety).
        p = build_proposal("AWA", "weak", _top(), None)
        self.assertEqual(p["verb"], "")
        self.assertEqual(p["safety_class"], "destructive")
        self.assertIs(p["requires_confirmation"], True)


class TestSafetyFieldsAreCatalogSourced(unittest.TestCase):
    def test_safety_class_read_verbatim_from_entry_not_utterance(self):
        for sc in ("read", "write", "destructive"):
            p = build_proposal("AWA", "strong", _top(), _entry(safety_class=sc, param_schema=[]))
            self.assertEqual(p["safety_class"], sc)

    def test_tool_path_read_from_entry(self):
        p = build_proposal("AWA", "strong", _top(), _entry(tool_path="hook", param_schema=[]))
        self.assertEqual(p["tool_path"], "hook")

    def test_start_point_from_rules_default(self):
        p = build_proposal("AWA", "strong", _top(), _entry(start_point_rules={"default": "current"}, param_schema=[]))
        self.assertEqual(p["start_point"], "current")

    def test_start_point_falls_back_to_unknown(self):
        p = build_proposal("AWA", "strong", _top(), _entry(start_point_rules={}, param_schema=[]))
        self.assertEqual(p["start_point"], "unknown")


class TestMissingParams(unittest.TestCase):
    def test_required_params_reported_missing_sorted(self):
        entry = _entry(param_schema=[
            {"name": "zeta", "type": "string", "required": True},
            {"name": "alpha", "type": "path", "required": True},
            {"name": "opt", "type": "string", "required": False},
        ])
        p = build_proposal("AWA", "strong", _top(), entry)
        self.assertEqual(p["missing_params"], ["alpha", "zeta"], "sorted; optional excluded")

    def test_no_required_params_is_empty(self):
        p = build_proposal("AWA", "strong", _top(), _entry(param_schema=[]))
        self.assertEqual(p["missing_params"], [])


class TestRequiresConfirmation(unittest.TestCase):
    def test_strong_read_no_missing_skips_confirmation(self):
        p = build_proposal("AWA", "strong", _top(), _entry(safety_class="read", param_schema=[]))
        self.assertIs(p["requires_confirmation"], False)

    def test_strong_write_still_confirms(self):
        p = build_proposal("AWA", "strong", _top(), _entry(safety_class="write", param_schema=[]))
        self.assertIs(p["requires_confirmation"], True)

    def test_weak_read_still_confirms(self):
        p = build_proposal("AWA", "weak", _top(), _entry(safety_class="read", param_schema=[]))
        self.assertIs(p["requires_confirmation"], True)

    def test_strong_read_with_missing_param_confirms(self):
        entry = _entry(safety_class="read", param_schema=[{"name": "x", "type": "string", "required": True}])
        p = build_proposal("AWA", "strong", _top(), entry)
        self.assertIs(p["requires_confirmation"], True)


class TestConfidence(unittest.TestCase):
    def test_zero_score_zero_confidence(self):
        p = build_proposal("AWA", "weak", _top(score=0.0), _entry(param_schema=[]))
        self.assertEqual(p["confidence"], 0.0)

    def test_saturates_at_one(self):
        p = build_proposal("AWA", "strong", _top(score=_SATURATION + 100), _entry(param_schema=[]))
        self.assertEqual(p["confidence"], 1.0)

    def test_scales_linearly_below_saturation(self):
        p = build_proposal("AWA", "weak", _top(score=_SATURATION / 2), _entry(param_schema=[]))
        self.assertAlmostEqual(p["confidence"], 0.5, places=3)


class TestWhyProvenance(unittest.TestCase):
    def test_why_leads_with_verdict_then_candidate_reasons(self):
        p = build_proposal("AWA", "strong", _top(why=["alias:protect", "example:safe"]), _entry(param_schema=[]))
        self.assertEqual(p["why"][0], "verdict:strong")
        self.assertIn("alias:protect", p["why"])


if __name__ == "__main__":
    unittest.main()
