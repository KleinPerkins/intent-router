"""MUST-FIX #2: catalog-verify's required-key floor + enums are BOUND to the frozen contract.

Nothing used to bind `intent_router/catalog.py`'s `REQUIRED_VERB_KEYS` / enums to
`contracts/intent-catalog.v1.json`. The freeze checker only compares the contract JSON to a third
copy in `checks/intent-contract-freeze.sh`, so `catalog.py` could DRIFT (e.g. drop `preconditions`)
with `make freeze` and every other test staying green — while `catalog-verify` then quietly accepted
a catalog missing that frozen-required key.

These tests bind them:
  - the validator's floor + enums MUST equal the frozen contract's (single source of truth), and
  - the shipped `validate_catalog` MUST reject a catalog missing ANY frozen-required key (verb-level
    and param-level), derived from the contract itself.

Dropping a required key from the validator floor turns these RED (proved pre-fix by re-introducing
the exact drift the reviewer described).
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from intent_router import catalog

_REPO_ROOT = Path(catalog.__file__).resolve().parent.parent
_CONTRACT = json.loads(
    (_REPO_ROOT / "contracts" / "intent-catalog.v1.json").read_text(encoding="utf-8"))


def _valid_verb(**overrides) -> dict:
    base = {
        "verb": "protect",
        "aliases": ["protect", "start protecting"],
        "examples": ["put this work somewhere safe"],
        "param_schema": [
            {"name": "target_path", "type": "path", "required": True, "source": "repo-resolver"}
        ],
        "preconditions": ["target_path is provided"],
        "safety_class": "write",
        "tool_path": "cli",
        "start_point_rules": {"default": "current"},
        "plain_label": "Start protecting this work",
        "consequence_copy": "Creates a separate safe copy to work in.",
    }
    base.update(overrides)
    return base


def _catalog(*verbs) -> dict:
    return {"schema": "intent-catalog/v1", "consumer": "test-fixture", "verbs": list(verbs)}


class TestFloorBoundToFrozenContract(unittest.TestCase):
    def test_required_verb_keys_equal_frozen_contract(self):
        self.assertEqual(set(catalog.REQUIRED_VERB_KEYS), set(_CONTRACT["required_keys"]),
                         "catalog.REQUIRED_VERB_KEYS drifted from the frozen contract required_keys")

    def test_required_param_keys_equal_frozen_contract(self):
        self.assertEqual(set(catalog.REQUIRED_PARAM_KEYS),
                         set(_CONTRACT["nested"]["param"]["required_keys"]))

    def test_enums_equal_frozen_contract(self):
        self.assertEqual(set(catalog.SAFETY_CLASS_ENUM), set(_CONTRACT["enums"]["safety_class"]))
        self.assertEqual(set(catalog.TOOL_PATH_ENUM), set(_CONTRACT["enums"]["tool_path"]))
        self.assertEqual(set(catalog.PARAM_TYPE_ENUM), set(_CONTRACT["enums"]["param.type"]))
        self.assertEqual(set(catalog.PARAM_SOURCE_ENUM), set(_CONTRACT["enums"]["param.source"]))


class TestValidateEnforcesFrozenFloor(unittest.TestCase):
    """Drive the SHIPPED validate_catalog against the contract's OWN key list — independent of
    catalog.py's constant, so a drift (a frozen key stops being enforced) bites here."""

    def test_every_frozen_required_verb_key_is_enforced(self):
        for key in _CONTRACT["required_keys"]:
            verb = _valid_verb()
            del verb[key]
            errors = catalog.validate_catalog(_catalog(verb))
            self.assertTrue(
                any(key in e for e in errors),
                f"validate must reject a verb missing frozen-required key {key!r}; errors={errors}")

    def test_every_frozen_required_param_key_is_enforced(self):
        for key in _CONTRACT["nested"]["param"]["required_keys"]:
            param = {"name": "target_path", "type": "path", "required": True}
            del param[key]
            errors = catalog.validate_catalog(_catalog(_valid_verb(param_schema=[param])))
            self.assertTrue(
                any("param_schema[0]" in e and key in e for e in errors),
                f"validate must reject a param missing frozen-required key {key!r}; errors={errors}")


if __name__ == "__main__":
    unittest.main()
