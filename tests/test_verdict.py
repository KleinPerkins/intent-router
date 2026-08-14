"""L2 verdict tests — strong|weak|none classification. THE safety-relevant output: conservative by
construction (a thin margin never reads as `strong`; verdict derives ONLY from the top two scores,
never from utterance content — CR5)."""

from __future__ import annotations

import unittest

from intent_router.verdict import (
    STRONG_MARGIN,
    STRONG_MIN,
    WEAK_MIN,
    classify,
    top_candidate,
)


def _c(verb: str, score: float) -> dict:
    return {"verb": verb, "score": score, "why": [f"score:{score}"]}


class TestClassify(unittest.TestCase):
    def test_empty_is_none(self):
        self.assertEqual(classify([]), "weak")

    def test_all_zero_is_none(self):
        self.assertEqual(classify([_c("a", 0), _c("b", 0)]), "none")

    def test_strong_requires_floor_and_margin(self):
        # top >= STRONG_MIN AND (top - runner) >= STRONG_MARGIN.
        self.assertEqual(classify([_c("a", STRONG_MIN), _c("b", STRONG_MIN - STRONG_MARGIN)]), "strong")

    def test_high_top_but_thin_margin_is_not_strong(self):
        # Two near-tied high scorers must NOT both read as confident — conservative de-escalation.
        top = STRONG_MIN + 20
        runner = top - (STRONG_MARGIN - 1)  # margin just under the floor
        self.assertEqual(classify([_c("a", top), _c("b", runner)]), "weak")

    def test_weak_when_above_weak_min_below_strong(self):
        self.assertEqual(classify([_c("a", WEAK_MIN)]), "weak")
        self.assertEqual(classify([_c("a", STRONG_MIN - 0.01)]), "weak")

    def test_none_when_below_weak_min(self):
        self.assertEqual(classify([_c("a", WEAK_MIN - 0.01)]), "none")

    def test_single_strong_candidate_has_zero_runner(self):
        # One candidate over the strong floor -> runner is 0 -> margin satisfied -> strong.
        self.assertEqual(classify([_c("a", STRONG_MIN + 5)]), "strong")

    def test_zero_scored_runner_is_ignored_for_margin(self):
        # A zero-scoring runner-up is filtered out; the sole nonzero candidate over floor is strong.
        self.assertEqual(classify([_c("a", STRONG_MIN + 1), _c("b", 0)]), "strong")

    def test_verdict_is_pure_function_of_scores_only(self):
        # Identical scores -> identical verdict regardless of verb identity/why (no content peeking).
        a = classify([_c("destroy-everything", 30), _c("x", 5)])
        b = classify([_c("gentle-read", 30), _c("y", 5)])
        self.assertEqual(a, b)


class TestTopCandidate(unittest.TestCase):
    def test_returns_highest_scoring(self):
        # `ranked` is contractually pre-sorted score-descending (candidates.rank_candidates).
        top = top_candidate([_c("b", 30), _c("a", 5)])
        self.assertEqual(top["verb"], "b")

    def test_none_when_empty(self):
        self.assertIsNone(top_candidate([]))

    def test_none_when_all_zero(self):
        self.assertIsNone(top_candidate([_c("a", 0), _c("b", 0)]))

    def test_skips_zero_to_first_nonzero(self):
        # Defensive: if a zero somehow sorts first, top_candidate still returns the nonzero one.
        self.assertEqual(top_candidate([_c("z", 0), _c("a", 3)])["verb"], "a")


if __name__ == "__main__":
    unittest.main()
