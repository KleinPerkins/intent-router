"""Hand-written intent-proposal/v1 fixture exercise (R-core deliverable) + A0 freeze guard.

Proves L5 serialization against a HUMAN-authored envelope: the engine must reproduce the hand-written
`proposal` exactly for the fixture's utterance+catalog. The freeze-timing guard below was FLIPPED in
A0: the proposal contract is now `frozen` (exercised first — see tests/test_proposal_exercise.py),
and this test now fails loudly if someone REGRESSES it to provisional or drops the frozen date.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from intent_router.engine import propose

_REPO_ROOT = Path(__file__).resolve().parent.parent
_CONTRACTS = _REPO_ROOT / "contracts"
_FIXTURES = _REPO_ROOT / "tests" / "fixtures"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class TestProposalContractIsFrozen(unittest.TestCase):
    """A0 freeze guard (FLIPPED from the R-core do-NOT-freeze guard). intent-proposal/v1 is now
    FROZEN; this guards drift — a regression to provisional, a missing frozen date, or a
    re-exemption fails here, in addition to the freeze checker."""

    def setUp(self):
        self.contract = _load(_CONTRACTS / "intent-proposal.v1.json")

    def test_status_is_frozen(self):
        self.assertEqual(self.contract["status"], "frozen",
                         "intent-proposal/v1 is frozen as of A0 — unfreezing is a breaking regression")

    def test_freeze_exempt_false_and_has_frozen_date(self):
        self.assertIs(self.contract["freeze_exempt"], False,
                      "a frozen contract is not freeze-exempt")
        self.assertTrue(self.contract["frozen"], "a frozen contract must record a frozen date")

    def test_required_key_floor_is_the_frozen_eleven(self):
        """Drift guard: the frozen envelope carries EXACTLY its 11 required keys. Adding/dropping/
        renaming a required key is a breaking change (needs v2) — caught here and by the checker."""
        self.assertEqual(set(self.contract["required_keys"]), {
            "consumer", "verb", "params", "start_point", "safety_class", "tool_path",
            "confidence", "verdict", "why", "missing_params", "requires_confirmation"})


class TestHandWrittenFixtureShape(unittest.TestCase):
    def setUp(self):
        self.contract = _load(_CONTRACTS / "intent-proposal.v1.json")
        self.fixture = _load(_FIXTURES / "awa-proposal.fixture.json")
        self.envelope = self.fixture["proposal"]

    def test_fixture_has_exactly_the_required_keys(self):
        self.assertEqual(set(self.envelope), set(self.contract["required_keys"]),
                         "hand-written fixture must carry exactly the 11 required proposal keys")

    def test_fixture_enum_values_are_in_frozen_floors(self):
        enums = self.contract["enums"]
        self.assertIn(self.envelope["safety_class"], enums["safety_class"])
        self.assertIn(self.envelope["tool_path"], enums["tool_path"])
        self.assertIn(self.envelope["verdict"], enums["verdict"])

    def test_fixture_field_types(self):
        e = self.envelope
        self.assertIsInstance(e["consumer"], str)
        self.assertIsInstance(e["verb"], str)
        self.assertIsInstance(e["params"], dict)
        self.assertIsInstance(e["why"], list)
        self.assertIsInstance(e["missing_params"], list)
        self.assertIsInstance(e["requires_confirmation"], bool)
        self.assertIsInstance(e["confidence"], (int, float))
        self.assertGreaterEqual(e["confidence"], 0.0)
        self.assertLessEqual(e["confidence"], 1.0)


class TestEngineReproducesFixture(unittest.TestCase):
    def test_serializer_reproduces_hand_written_envelope_exactly(self):
        fixture = _load(_FIXTURES / "awa-proposal.fixture.json")
        meta = fixture["_meta"]
        catalog = _load(_REPO_ROOT / meta["catalog_fixture"])
        produced = propose(meta["consumer"], meta["utterance"], catalog)
        self.assertEqual(produced, fixture["proposal"],
                         "L5 serialization drifted from the hand-written intent-proposal/v1 fixture")


if __name__ == "__main__":
    unittest.main()
