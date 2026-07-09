"""Contract-freeze test: the versioned contracts still satisfy their frozen behavior floor.

The authority is the shell checker `checks/intent-contract-freeze.sh` (mirror of AWA's
awa-contract-freeze.sh). This test drives it so the same logic is both a `make freeze` gate and a
referenceable test-id for the status ledger.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

_REPO_ROOT = Path(__file__).resolve().parent.parent
_CHECKER = _REPO_ROOT / "checks" / "intent-contract-freeze.sh"
_CONTRACTS = _REPO_ROOT / "contracts"


def _run_checker_against(mutate):
    """Copy the real contracts into a throwaway INTENT_HOME, apply `mutate(contracts_dir)` to inject
    an ADVERSARIAL breaking change, run the SHIPPED checker against them, and return the process.

    This exercises the exact `checks/intent-contract-freeze.sh` that gates `make verify`, proving the
    regression bites on the real gate (not a re-implementation)."""
    with TemporaryDirectory() as d:
        root = Path(d)
        cdir = root / "contracts"
        cdir.mkdir()
        for p in _CONTRACTS.glob("*.json"):
            shutil.copy2(p, cdir / p.name)
        mutate(cdir)
        return subprocess.run(
            ["bash", str(_CHECKER)],
            env={**os.environ, "INTENT_HOME": str(root)},
            capture_output=True, text=True,
        )


def _edit_json(path: Path, fn):
    c = json.loads(path.read_text(encoding="utf-8"))
    fn(c)
    path.write_text(json.dumps(c, indent=2) + "\n", encoding="utf-8")

_FROZEN = {
    "intent-catalog.v1.json": "frozen",
    "intent-map.v1.json": "frozen",
    "intent-feedback.v1.json": "frozen",
    "intent-constitution.v1.json": "frozen",
    "intent-proposal.v1.json": "provisional",
}


class TestContractFreeze(unittest.TestCase):
    def test_freeze_checker_passes(self):
        self.assertTrue(_CHECKER.exists(), f"freeze checker missing: {_CHECKER}")
        proc = subprocess.run(["bash", str(_CHECKER)], cwd=str(_REPO_ROOT),
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0,
                        f"intent-contract-freeze failed:\n{proc.stdout}\n{proc.stderr}")

    def test_all_five_contracts_present_and_valid_json(self):
        for fname, exp_status in _FROZEN.items():
            p = _CONTRACTS / fname
            self.assertTrue(p.exists(), f"contract missing: {fname}")
            c = json.loads(p.read_text(encoding="utf-8"))
            self.assertEqual(c.get("version"), 1, f"{fname}: version must be 1")
            self.assertEqual(c.get("status"), exp_status,
                            f"{fname}: status must be {exp_status} (freeze-timing lock)")

    def test_proposal_is_provisional_and_freeze_exempt(self):
        c = json.loads((_CONTRACTS / "intent-proposal.v1.json").read_text(encoding="utf-8"))
        self.assertEqual(c["status"], "provisional")
        self.assertIs(c["freeze_exempt"], True)
        self.assertIsNone(c["frozen"], "proposal must not record a frozen date until A0")


class TestContractFreezeRegression(unittest.TestCase):
    """BLOCKER-1 regression: the freeze checker MUST catch retype / added-required-key / nested-drop.

    Each test injects the exact adversarial change the review-swarm flagged as silently-passing and
    asserts the SHIPPED checker now FAILS (non-zero) with a message naming the break. Before the P0
    review fixes these all passed (EXIT 0) — the bug that made contract-freeze not actually freeze."""

    def _assert_fails(self, proc, *needles):
        out = (proc.stdout or "") + (proc.stderr or "")
        self.assertNotEqual(proc.returncode, 0,
                            f"checker should FAIL on the adversarial change; it passed:\n{out}")
        for n in needles:
            self.assertIn(n, out, f"expected {n!r} in checker output:\n{out}")

    def test_retype_required_key_object_to_string_fails(self):
        # intent-map.param_bindings: object -> string (a breaking RETYPE of a frozen required key).
        def mutate(cdir):
            _edit_json(cdir / "intent-map.v1.json",
                       lambda c: c["required_keys"].__setitem__("param_bindings", "string"))
        self._assert_fails(_run_checker_against(mutate), "RETYPED", "param_bindings")

    def test_added_required_key_fails(self):
        # A new REQUIRED key is breaking under additive-OPTIONAL-only (new fields must be optional).
        def mutate(cdir):
            _edit_json(cdir / "intent-feedback.v1.json",
                       lambda c: c["required_keys"].__setitem__("new_required_field", "string"))
        self._assert_fails(_run_checker_against(mutate), "ADD", "new_required_field")

    def test_removing_nested_param_name_fails(self):
        # Dropping intent-catalog nested param.name must fail (nested {name,type,required} floor).
        def mutate(cdir):
            _edit_json(cdir / "intent-catalog.v1.json",
                       lambda c: c["nested"]["param"]["required_keys"].pop("name"))
        self._assert_fails(_run_checker_against(mutate), "nested", "name")

    def test_dropping_required_key_fails(self):
        # Completeness: a DROPPED required key is also breaking (removal needs v2).
        def mutate(cdir):
            _edit_json(cdir / "intent-map.v1.json",
                       lambda c: c["required_keys"].pop("weight"))
        self._assert_fails(_run_checker_against(mutate), "DROPPED", "weight")


if __name__ == "__main__":
    unittest.main()
