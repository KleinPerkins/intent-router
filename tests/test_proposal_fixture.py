"""Hand-written intent-proposal/v1 fixture exercise (R-core deliverable).

Proves L5 serialization against a HUMAN-authored envelope: the engine must reproduce the hand-written
`proposal` exactly for the fixture's utterance+catalog. ALSO guards the freeze-timing lock — the
proposal contract MUST stay `provisional` (freeze deferred to A0); this test fails loudly if someone
freezes it early.
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


class TestProposalContractStaysProvisional(unittest.TestCase):
    """Do-NOT-freeze guard: R-core exercises the envelope but must not freeze it (that is A0's job)."""

    def setUp(self):
        self.contract = _load(_CONTRACTS / "intent-proposal.v1.json")

    def test_status_is_provisional(self):
        self.assertEqual(self.contract["status"], "provisional",
                         "intent-proposal/v1 must stay provisional in R-core (freeze is A0)")

    def test_freeze_exempt_true_and_no_frozen_date(self):
        self.assertIs(self.contract["freeze_exempt"], True)
        self.assertIsNone(self.contract["frozen"], "no frozen date until A0 exercises the seam")


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
