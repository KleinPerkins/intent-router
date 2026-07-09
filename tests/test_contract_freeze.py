"""Contract-freeze test: the versioned contracts still satisfy their frozen behavior floor.

The authority is the shell checker `checks/intent-contract-freeze.sh` (mirror of AWA's
awa-contract-freeze.sh). This test drives it so the same logic is both a `make freeze` gate and a
referenceable test-id for the status ledger.
"""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_CHECKER = _REPO_ROOT / "checks" / "intent-contract-freeze.sh"
_CONTRACTS = _REPO_ROOT / "contracts"

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


if __name__ == "__main__":
    unittest.main()
