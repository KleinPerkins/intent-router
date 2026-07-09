"""Constitution test: the machine-checkable constitution contract is well-formed and honest.

Verifies (a) every rule/invariant has a stable unique id + text + enforcement hook, (b) every
`active` machine-check resolves to a REAL test-id (module/class/method exist), (c) every `spec`
(deferred) machine-check is honestly marked — null test_id + a future phase — so a deferred
invariant can never silently pass, and (d) the operator-outcome model matches the feedback
contract's operator_choice enum (cross-contract consistency).
"""

from __future__ import annotations

import importlib
import json
import unittest
from pathlib import Path

_CONTRACTS = Path(__file__).resolve().parent.parent / "contracts"


def _load(fname):
    return json.loads((_CONTRACTS / fname).read_text(encoding="utf-8"))


def _test_id_resolves(test_id: str) -> bool:
    parts = test_id.split(".")
    if len(parts) < 3:
        return False
    module_name = ".".join(parts[:-2])
    cls_name, meth_name = parts[-2], parts[-1]
    try:
        mod = importlib.import_module(module_name)
        cls = getattr(mod, cls_name)
        return callable(getattr(cls, meth_name, None))
    except Exception:  # noqa: BLE001
        return False


class TestConstitution(unittest.TestCase):
    def setUp(self):
        self.c = _load("intent-constitution.v1.json")

    def test_constitution_wellformed(self):
        c = self.c
        self.assertEqual(c["schema"], "intent-constitution/v1")
        self.assertEqual(c["version"], 1)
        self.assertEqual(c["status"], "frozen")

        # Rules + invariants: unique ids, non-empty text, an enforcement hook each.
        rule_ids = [r["id"] for r in c["rules"]]
        self.assertEqual(len(rule_ids), len(set(rule_ids)), "duplicate rule ids")
        for r in c["rules"]:
            self.assertTrue(r.get("rule"), f"rule {r.get('id')} has no text")
            self.assertTrue(r.get("enforcement"), f"rule {r.get('id')} has no enforcement hook")

        inv_ids = [i["id"] for i in c["kernel_invariants"]]
        self.assertEqual(len(inv_ids), len(set(inv_ids)), "duplicate invariant ids")
        for i in c["kernel_invariants"]:
            self.assertTrue(i.get("invariant"), f"invariant {i.get('id')} has no text")
            self.assertTrue(i.get("check"), f"invariant {i.get('id')} has no check hook")

        # Banned-term tiers present (the egress gate structure).
        bt = c["banned_terms"]
        self.assertIn("tier_a_generic_mechanism", bt)
        self.assertIn("tier_b_git_workflow", bt)
        self.assertIn("tier_c_consumer_contributed", bt)

        # Every enforcement hook referenced by a rule/invariant is a real machine_check.
        checks = c["machine_checks"]
        for r in c["rules"]:
            self.assertIn(r["enforcement"], checks, f"rule {r['id']} enforcement not a machine_check")
        for i in c["kernel_invariants"]:
            self.assertIn(i["check"], checks, f"invariant {i['id']} check not a machine_check")

    def test_machine_checks_active_resolve_and_spec_marked(self):
        problems = []
        for name, mc in self.c["machine_checks"].items():
            status = mc.get("status")
            self.assertIn(status, ("active", "spec"), f"{name}: bad status {status!r}")
            if status == "active":
                tid = mc.get("test_id")
                if not tid or not _test_id_resolves(tid):
                    problems.append(f"{name}: active check references unresolved test_id {tid!r}")
            else:  # spec — must be honestly deferred, never silently passing
                if mc.get("test_id") is not None:
                    problems.append(f"{name}: spec check must have null test_id (got {mc.get('test_id')!r})")
                if not mc.get("phase"):
                    problems.append(f"{name}: spec check must name a future phase")
        self.assertEqual(problems, [], "machine_check honesty violations:\n" + "\n".join(problems))

    def test_operator_outcomes_match_feedback_enum(self):
        outcomes = self.c["operator_outcomes"]
        fb = _load("intent-feedback.v1.json")
        self.assertEqual(list(outcomes), list(fb["enums"]["operator_choice"]),
                        "operator_outcomes must match intent-feedback operator_choice (five-outcome model)")


if __name__ == "__main__":
    unittest.main()
