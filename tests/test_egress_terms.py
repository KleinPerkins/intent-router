"""Egress-terms checklist: the FULL plan banned-term inventory is pinned and nothing drops.

MINOR-7: the plan's "System-Wide Operator Egress Gate" lists Tier A/B/C banned terms. If any term
silently drops between the plan and the consumer's egress config, a PM-facing surface can leak jargon
undetected. This test pins the complete plan inventory here and asserts every term is present in
`contracts/egress-terms.checklist.json`, so the future `egress`-phase test consumes a complete list.
It is a P0 completeness guard, not the egress test itself (that behavioral test lands at the egress
phase — see tests/test_deferred_spec.py::test_spec_egress_zero_banned_terms).
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

_CHECKLIST = Path(__file__).resolve().parent.parent / "contracts" / "egress-terms.checklist.json"

# The complete inventory copied from the plan's egress-gate section. If the plan grows a term, add it
# here AND to the checklist — this test is the tripwire that keeps them in lockstep.
_PLAN_TIER_A = ["lease", "worktree", "common-dir", "kernel", "engine", "guard", "mode",
                "disposition", "heartbeat", "archive-protect", "bundle", "quarantine ref",
                "MCP", "hook", "receipt", "flags"]
_PLAN_TIER_B = ["branch", "commit", "push", "pull", "merge", "rebase", "PR", "main", "origin",
                "detached", "dirty", "ahead", "behind", "orphan", "HEAD"]
_PLAN_TIER_C_AWA = ["awa_mode_set", "awa_guard_shell", "awa_lease_read",
                    "--bundle", "--force", "--path",
                    "mutating command", "primary checkout", "policy-check: OK", "WAL mode",
                    "Orphan AWA branches"]


class TestEgressTerms(unittest.TestCase):
    def setUp(self):
        self.c = json.loads(_CHECKLIST.read_text(encoding="utf-8"))

    def _all_terms(self):
        terms = set(self.c.get("tier_a_mechanism", [])) | set(self.c.get("tier_b_git_workflow", []))
        for _consumer, lst in self.c.get("tier_c_consumer_concrete", {}).items():
            if isinstance(lst, list):
                terms |= set(lst)
        return terms

    def test_schema_and_surfaces(self):
        self.assertEqual(self.c["schema"], "intent-egress-terms/v1")
        # All seven PM-facing surfaces the egress gate covers must be enumerated.
        self.assertEqual(len(self.c["surfaces"]), 7, "the egress gate covers seven PM-facing surfaces")

    def test_full_plan_inventory_pinned_no_drop(self):
        """Every Tier A/B/C term from the plan is present in the checklist (nothing silently drops)."""
        have = self._all_terms()
        missing = [t for t in (_PLAN_TIER_A + _PLAN_TIER_B + _PLAN_TIER_C_AWA) if t not in have]
        self.assertEqual(missing, [], f"egress terms dropped between plan and checklist: {missing}")

    def test_reviewer_named_criticals_present(self):
        """Explicit guard for the terms the P0 review called out by name."""
        have = self._all_terms()
        for t in ["mode", "heartbeat", "receipt", "lease", "worktree", "common-dir", "bundle",
                  "quarantine ref", "archive-protect", "--bundle", "--force", "--path",
                  "primary checkout", "policy-check: OK"]:
            self.assertIn(t, have, f"review-named egress term missing from checklist: {t!r}")

    def test_tiers_are_supersets_of_plan(self):
        self.assertTrue(set(_PLAN_TIER_A) <= set(self.c["tier_a_mechanism"]))
        self.assertTrue(set(_PLAN_TIER_B) <= set(self.c["tier_b_git_workflow"]))
        self.assertTrue(set(_PLAN_TIER_C_AWA) <= set(self.c["tier_c_consumer_concrete"]["awa"]))


if __name__ == "__main__":
    unittest.main()
