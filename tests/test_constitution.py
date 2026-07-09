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


def _resolve_method(test_id: str):
    """Resolve a dotted 'module.Class.method' test-id to the method object, or None."""
    parts = test_id.split(".") if test_id else []
    if len(parts) < 3:
        return None
    module_name = ".".join(parts[:-2])
    cls_name, meth_name = parts[-2], parts[-1]
    try:
        mod = importlib.import_module(module_name)
        cls = getattr(mod, cls_name)
        m = getattr(cls, meth_name, None)
        return m if callable(m) else None
    except Exception:  # noqa: BLE001
        return None


def _test_id_resolves(test_id: str) -> bool:
    return _resolve_method(test_id) is not None


def _is_skipped(method) -> bool:
    return bool(getattr(method, "__unittest_skip__", False))


def _skip_reason(method) -> str:
    return str(getattr(method, "__unittest_skip_why__", "") or "")


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
            tid = mc.get("test_id")
            m = _resolve_method(tid) if tid else None
            if status == "active":
                if m is None:
                    problems.append(f"{name}: active check references unresolved test_id {tid!r}")
                elif _is_skipped(m):
                    problems.append(f"{name}: active check test {tid} is SKIPPED (must be a real passing test)")
            else:  # spec — must map to a SKIPPED placeholder + name a future phase (never silently passing)
                if not mc.get("phase"):
                    problems.append(f"{name}: spec check must name a future phase")
                if m is None:
                    problems.append(f"{name}: spec check test_id {tid!r} does not resolve to a placeholder")
                elif not _is_skipped(m):
                    problems.append(f"{name}: spec placeholder {tid} is NOT skipped (would silently pass)")
        self.assertEqual(problems, [], "machine_check honesty violations:\n" + "\n".join(problems))

    def test_every_spec_check_maps_to_skipped_placeholder(self):
        """Completeness (MINOR-6/-11): every `spec` machine_check maps to a SKIPPED placeholder whose
        skip reason names the SAME phase — so the future test surface is greppable AND a phase-label
        can't silently drift between the constitution and its placeholder (the CR8 bug)."""
        problems = []
        specs = {n: mc for n, mc in self.c["machine_checks"].items() if mc.get("status") == "spec"}
        self.assertTrue(specs, "expected at least one spec machine_check")
        for name, mc in specs.items():
            tid = mc.get("test_id")
            m = _resolve_method(tid) if tid else None
            if m is None or not _is_skipped(m):
                problems.append(f"{name}: spec check must map to a skipped placeholder (got {tid!r})")
                continue
            phase = mc.get("phase", "")
            if phase and phase not in _skip_reason(m):
                problems.append(f"{name}: machine_check phase {phase!r} not reflected in the "
                                f"placeholder skip reason ({_skip_reason(m)!r}) — phase-label drift")
        self.assertEqual(problems, [], "spec completeness / phase drift:\n" + "\n".join(problems))

    def test_operator_outcomes_match_feedback_enum(self):
        outcomes = self.c["operator_outcomes"]
        fb = _load("intent-feedback.v1.json")
        self.assertEqual(list(outcomes), list(fb["enums"]["operator_choice"]),
                        "operator_outcomes must match intent-feedback operator_choice (five-outcome model)")


if __name__ == "__main__":
    unittest.main()
