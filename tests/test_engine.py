"""engine.py tests — the L1->L2->L5 pipeline wiring. Pure, deterministic, executionless (`propose`/
`explain` never run anything; they only rank, classify, and serialize)."""

from __future__ import annotations

import unittest

from intent_router.engine import explain, propose

_CATALOG = {
    "schema": "intent-catalog/v1",
    "verbs": [
        {
            "verb": "protect",
            "aliases": ["protect", "start protecting"],
            "examples": ["put this work somewhere safe", "start protecting this repo"],
            "param_schema": [{"name": "target", "type": "path", "required": True}],
            "preconditions": [],
            "safety_class": "write",
            "tool_path": "mcp",
            "start_point_rules": {"default": "repo-root"},
            "plain_label": "Start protecting this work",
            "consequence_copy": "Nothing changes on disk yet.",
        },
        {
            "verb": "status",
            "aliases": ["status", "check status", "is everything okay"],
            "examples": ["is everything okay", "how is this doing"],
            "param_schema": [],
            "preconditions": [],
            "safety_class": "read",
            "tool_path": "cli",
            "start_point_rules": {"default": "current"},
            "plain_label": "Check protection status",
            "consequence_copy": "Nothing changes; this only reports.",
        },
    ],
}

# A deliberately UNDER-signaled catalog (no verbatim "is everything okay" alias) — used to prove the
# verdict-gating regression below: a sub-floor score must still degrade to the empty/conservative
# floor, never leak a real verb merely because SOME nonzero overlap exists.
_THIN_CATALOG = {
    "schema": "intent-catalog/v1",
    "verbs": [{**_CATALOG["verbs"][1], "aliases": ["status", "check status"]}],
}


class TestPropose(unittest.TestCase):
    def test_matches_expected_verb(self):
        p = propose("AWA", "start protecting this repo please", _CATALOG)
        self.assertEqual(p["verb"], "protect")
        self.assertEqual(p["safety_class"], "write")

    def test_offline_degrade_on_no_signal(self):
        p = propose("AWA", "what is the weather in paris today", _CATALOG)
        self.assertEqual(p["verb"], "")
        self.assertEqual(p["verdict"], "none")
        self.assertEqual(p["safety_class"], "destructive")
        self.assertIs(p["requires_confirmation"], True)

    def test_read_only_status_check_matches_and_never_escalates_safety_class(self):
        p = propose("AWA", "is everything okay", _CATALOG)
        self.assertEqual(p["verb"], "status")
        self.assertEqual(p["verdict"], "weak")
        self.assertEqual(p["safety_class"], "read")
        # weak (not strong) -> conservative default still asks.
        self.assertIs(p["requires_confirmation"], True)

    def test_subfloor_score_with_none_verdict_never_leaks_a_verb(self):
        # Regression: `status` scores 6.0 (example overlap on "everything") against the THIN
        # catalog — nonzero, but below WEAK_MIN(8) so verdict is `none`. The proposal must degrade
        # to the fully conservative floor (empty verb), NOT quietly surface `status`/`read` because
        # `top_candidate` alone saw a nonzero score. This is the exact bug the verdict-gate in
        # `engine._top_for_verdict` exists to prevent.
        p = propose("AWA", "is everything okay", _THIN_CATALOG)
        self.assertEqual(p["verdict"], "none")
        self.assertEqual(p["verb"], "", "a none verdict must never name a specific verb")
        self.assertEqual(p["safety_class"], "destructive")
        self.assertIs(p["requires_confirmation"], True)

    def test_never_executes_anything_result_is_plain_data(self):
        p = propose("AWA", "start protecting this repo please", _CATALOG)
        # A proposal is JSON-round-trippable plain data — no callables, no file handles.
        import json
        json.dumps(p)  # must not raise

    def test_deterministic_repeat_calls(self):
        a = propose("AWA", "start protecting this repo please", _CATALOG)
        b = propose("AWA", "start protecting this repo please", _CATALOG)
        self.assertEqual(a, b)

    def test_empty_catalog_degrades_conservative_not_raises(self):
        p = propose("AWA", "anything at all", {"schema": "intent-catalog/v1", "verbs": []})
        self.assertEqual(p["verdict"], "none")
        self.assertIs(p["requires_confirmation"], True)

    def test_malformed_catalog_degrades_conservative_not_raises(self):
        p = propose("AWA", "anything at all", {"not": "a catalog"})
        self.assertEqual(p["verdict"], "none")


class TestExplain(unittest.TestCase):
    def test_includes_full_ranked_list_and_proposal(self):
        out = explain("AWA", "start protecting this repo please", _CATALOG)
        self.assertEqual(out["proposal"]["verb"], "protect")
        self.assertEqual(out["verdict"], "strong")
        self.assertGreaterEqual(len(out["candidates"]), 2)
        self.assertEqual(out["candidates"][0]["verb"], "protect")

    def test_top_n_is_respected(self):
        out = explain("AWA", "start protecting this repo please", _CATALOG, top_n=1)
        self.assertEqual(len(out["candidates"]), 1)

    def test_utterance_echoed_verbatim(self):
        out = explain("AWA", "is everything okay", _CATALOG)
        self.assertEqual(out["utterance"], "is everything okay")


if __name__ == "__main__":
    unittest.main()
