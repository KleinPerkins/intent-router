"""L1 candidate ranking tests — pure, deterministic, explainable overlap scoring."""

from __future__ import annotations

import unittest

from intent_router.candidates import rank_candidates, score_verb
from intent_router.normalize import normalize_tokens

_PROTECT = {
    "verb": "protect",
    "aliases": ["protect", "start protecting"],
    "examples": ["put this work somewhere safe", "start protecting this repo"],
    "plain_label": "Start protecting this work",
}
_CLEANUP = {
    "verb": "cleanup",
    "aliases": ["cleanup", "remove safe copy"],
    "examples": ["clean up my old safe copy", "delete this safe copy"],
    "plain_label": "Remove an old safe copy",
}
_STATUS = {
    "verb": "status",
    "aliases": ["status", "check status"],
    "examples": ["is everything okay", "how is this doing"],
    "plain_label": "Check protection status",
}


class TestScoreVerb(unittest.TestCase):
    def test_alias_hit_scores_higher_than_no_hit(self):
        tokens = normalize_tokens("start protecting this")
        scored = score_verb(tokens, _PROTECT)
        self.assertGreater(scored["score"], 0)
        self.assertIn("alias", scored["matched"])

    def test_no_overlap_scores_zero(self):
        tokens = normalize_tokens("what is the weather today")
        scored = score_verb(tokens, _PROTECT)
        self.assertEqual(scored["score"], 0)
        self.assertEqual(scored["why"], ["no-signal"])

    def test_why_is_machine_readable_and_sorted(self):
        tokens = normalize_tokens("put this work somewhere safe")
        scored = score_verb(tokens, _PROTECT)
        self.assertTrue(any(w.startswith("example:") for w in scored["why"]))
        # matched terms within a signal are sorted (deterministic serialization).
        for terms in scored["matched"].values():
            self.assertEqual(terms, sorted(terms))

    def test_verb_name_token_contributes(self):
        tokens = normalize_tokens("please cleanup now")
        scored = score_verb(tokens, _CLEANUP)
        self.assertIn("verb_name", scored["matched"])


class TestRankCandidates(unittest.TestCase):
    def test_sorted_descending_by_score(self):
        ranked = rank_candidates("start protecting this repo", [_STATUS, _PROTECT, _CLEANUP])
        scores = [c["score"] for c in ranked]
        self.assertEqual(scores, sorted(scores, reverse=True))
        self.assertEqual(ranked[0]["verb"], "protect")

    def test_deterministic_tie_break_by_verb_name(self):
        # Two verbs with identical (zero) score tie-break alphabetically regardless of input order.
        ranked_a = rank_candidates("nothing matches at all here", [_CLEANUP, _PROTECT, _STATUS])
        ranked_b = rank_candidates("nothing matches at all here", [_STATUS, _CLEANUP, _PROTECT])
        self.assertEqual([c["verb"] for c in ranked_a], [c["verb"] for c in ranked_b])
        self.assertEqual([c["verb"] for c in ranked_a], sorted(["cleanup", "protect", "status"]))

    def test_malformed_entries_are_skipped_not_raised(self):
        ranked = rank_candidates("status check", ["not-a-dict", None, 42, _STATUS])
        self.assertEqual(len(ranked), 1)
        self.assertEqual(ranked[0]["verb"], "status")

    def test_empty_catalog_returns_empty_list(self):
        self.assertEqual(rank_candidates("anything at all", []), [])

    def test_repeat_calls_are_byte_identical(self):
        a = rank_candidates("clean up my old safe copy", [_STATUS, _PROTECT, _CLEANUP])
        b = rank_candidates("clean up my old safe copy", [_STATUS, _PROTECT, _CLEANUP])
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
