"""Additive-compatibility proof — the ARCHITECTURE-COMPLETE gate.

Proves that EVERY deferred phase only ADDS to the frozen v1 contracts: no field removal, rename,
or retype. This is the v8 rule: "if we cannot prove today that a deferred phase is additive to the
v1 contracts, we are not architecture-complete." The proof has four parts:

  1. Manifest <-> contract consistency: every additive field the manifest attributes to a phase is
     actually declared in that contract's `deferred_additions`, and vice-versa (no orphan additions).
  2. Genuinely additive: every deferred addition is a NEW key (no collision with an existing
     required key -> no retype/redefinition) or an enum EXTENSION (never drops a frozen value).
  3. Floor preserved: applying all additions leaves each contract's v1 required-key floor intact.
  4. Coverage: every plan-deferred phase named for the proof (R2, C0, C1, R-resilience, R-surface)
     is accounted for as either `additive` (with valid keys) or `no-schema-change` (uses frozen v1).
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

_CONTRACTS = Path(__file__).resolve().parent.parent / "contracts"

_CONTRACT_FILES = {
    "intent-catalog/v1": "intent-catalog.v1.json",
    "intent-map/v1": "intent-map.v1.json",
    "intent-proposal/v1": "intent-proposal.v1.json",
    "intent-feedback/v1": "intent-feedback.v1.json",
    "intent-constitution/v1": "intent-constitution.v1.json",
}


def _load(name):
    return json.loads((_CONTRACTS / _CONTRACT_FILES[name]).read_text(encoding="utf-8"))


def _load_manifest():
    return json.loads((_CONTRACTS / "additive-manifest.json").read_text(encoding="utf-8"))


def _added_keys_by_contract(contract) -> dict:
    """phase -> set(added key names) from a contract's deferred_additions (enum extensions excluded
    from the 'new key' set; they are validated separately)."""
    out: dict = {}
    for phase, adds in contract.get("deferred_additions", {}).items():
        keys = set()
        for a in adds:
            target = a.get("target", "")
            if str(target).startswith("enum."):
                continue  # enum extension, not a key add
            keys.add(a["key"])
        out.setdefault(phase, set()).update(keys)
    return out


def _all_declared_key_names(contract) -> set:
    names = set(contract.get("required_keys", {})) | set(contract.get("optional_keys", {}))
    for _cont, spec in contract.get("nested", {}).items():
        names |= set(spec.get("required_keys", {}))
        names |= set(spec.get("optional_keys", {}))
    return names


class TestAdditiveCompat(unittest.TestCase):
    def setUp(self):
        self.contracts = {name: _load(name) for name in _CONTRACT_FILES}
        self.manifest = _load_manifest()

    def test_manifest_and_contracts_agree(self):
        """Every additive key the manifest attributes to a phase is declared in that contract's
        deferred_additions, and every contract deferred addition is reflected in the manifest."""
        problems = []
        dp = self.manifest["deferred_phases"]

        # manifest -> contract
        for phase, spec in dp.items():
            if spec.get("kind") != "additive":
                continue
            for cname, keys in spec.get("contracts", {}).items():
                contract = self.contracts[cname]
                declared = _added_keys_by_contract(contract).get(phase, set())
                for k in keys:
                    if k not in declared:
                        problems.append(f"manifest says {phase} adds {k} to {cname}, but the "
                                        f"contract's deferred_additions[{phase}] lacks it")

        # contract -> manifest
        for cname, contract in self.contracts.items():
            for phase, keys in _added_keys_by_contract(contract).items():
                mspec = dp.get(phase, {})
                man_keys = set(mspec.get("contracts", {}).get(cname, [])) if mspec.get("kind") == "additive" else set()
                for k in keys:
                    if k not in man_keys:
                        problems.append(f"{cname} deferred_additions[{phase}] adds {k}, but the "
                                        f"manifest does not record it")
        self.assertEqual(problems, [], "manifest/contract drift:\n" + "\n".join(problems))

    def test_every_deferred_addition_is_genuinely_additive(self):
        """No deferred addition may collide with an existing required/optional key (a retype/rename)
        and every enum extension must only ADD values (never drop a frozen one)."""
        problems = []
        for cname, contract in self.contracts.items():
            existing = _all_declared_key_names(contract)
            enums = contract.get("enums", {})
            for phase, adds in contract.get("deferred_additions", {}).items():
                for a in adds:
                    target = str(a.get("target", ""))
                    key = a.get("key")
                    if target.startswith("enum."):
                        field = target.split(".", 1)[1]
                        if field not in enums:
                            problems.append(f"{cname}[{phase}]: enum extension targets unknown enum '{field}'")
                        # enum additions ADD values; the frozen floor is asserted by the freeze checker.
                        continue
                    # A key addition must be NEW (not a redefinition of a frozen key).
                    if key in existing:
                        problems.append(f"{cname}[{phase}]: '{key}' already exists — an addition may "
                                        f"not redefine/retype a frozen key (would need v2)")
        self.assertEqual(problems, [], "non-additive change detected:\n" + "\n".join(problems))

    def test_v1_floor_is_preserved_under_all_additions(self):
        """The projected future shape (v1 floor + all additions) still contains every v1 required
        key with its original type. Additions never remove/rename/retype a required key."""
        problems = []
        for cname, contract in self.contracts.items():
            required = dict(contract.get("required_keys", {}))
            added = set()
            for adds in contract.get("deferred_additions", {}).values():
                for a in adds:
                    if not str(a.get("target", "")).startswith("enum."):
                        added.add(a["key"])
            # Projected shape = required (unchanged) + optional + added. Required keys are never in
            # `added` (proven above), so each required key survives with its type.
            for rk, rtype in required.items():
                if rk in added:
                    problems.append(f"{cname}: required key '{rk}' appears as an addition (retype risk)")
        self.assertEqual(problems, [], "floor not preserved:\n" + "\n".join(problems))

    def test_all_deferred_phases_additive(self):
        """Coverage: every plan-deferred phase named for the proof is accounted for as additive
        (with valid keys) or explicit no-schema-change. This is the architecture-complete assertion."""
        dp = self.manifest["deferred_phases"]
        required_phases = self.manifest["required_additive_phases"]
        problems = []
        for phase in required_phases:
            spec = dp.get(phase)
            if spec is None:
                problems.append(f"required deferred phase '{phase}' absent from the additive manifest")
                continue
            kind = spec.get("kind")
            if kind not in ("additive", "no-schema-change"):
                problems.append(f"phase '{phase}': kind must be additive|no-schema-change, got {kind!r}")
            if kind == "additive" and not spec.get("contracts"):
                problems.append(f"phase '{phase}': additive but lists no contract keys")
            if kind == "no-schema-change" and not spec.get("reason"):
                problems.append(f"phase '{phase}': no-schema-change must give a reason")
        self.assertEqual(problems, [],
                        "architecture-complete gate FAILED — a deferred phase is not provably "
                        "additive:\n" + "\n".join(problems))


if __name__ == "__main__":
    unittest.main()
