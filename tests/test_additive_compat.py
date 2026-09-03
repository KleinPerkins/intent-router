"""Additive-compatibility proof — the ARCHITECTURE-COMPLETE gate.

Proves that EVERY deferred phase only ADDS to the frozen v1 contracts: no field removal, rename,
or retype. This is the v8 rule: "if we cannot prove today that a deferred phase is additive to the
v1 contracts, we are not architecture-complete." The proof has four parts:

  1. Manifest <-> contract consistency: the bidirectional canonical join covers manifest records,
     contract declarations, and enum-extension provenance with path-qualified identities.
  2. Genuinely additive: each deferred addition is pending or authoritative on all coordinated
     surfaces; no partial promotion can pass.
  3. Floor preserved: applying all additions leaves each contract's v1 required-key floor intact.
  4. Coverage: every plan-deferred phase named for the proof (R2, C0, C1, R-resilience, R-surface)
     is accounted for as either `additive` (with valid keys) or `no-schema-change` (uses frozen v1).
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from tests.freeze_helpers import FROZEN_SCHEMAS, validate_additive_bundle

_CONTRACTS = Path(__file__).resolve().parent.parent / "contracts"

def _load_manifest():
    return json.loads((_CONTRACTS / "additive-manifest.json").read_text(encoding="utf-8"))


def _load_contracts(manifest):
    return {
        schema: json.loads(
            (_CONTRACTS / manifest["frozen_behavior"][schema]["file"]).read_text(
                encoding="utf-8"
            )
        )
        for schema in FROZEN_SCHEMAS
    }


def _supported_target(target):
    if target in {"top.optional", "banned_terms.optional"}:
        return True
    if target.startswith("enum."):
        return bool(target.removeprefix("enum."))
    if target.startswith("nested.") and target.endswith(".optional"):
        container = target[len("nested.") : -len(".optional")]
        return bool(container) and "." not in container
    return False


def _manifest_records(manifest):
    records = set()
    for phase, spec in manifest["deferred_phases"].items():
        if spec.get("kind") != "additive":
            continue
        for schema, keys in spec.get("contracts", {}).items():
            records.update((phase, schema, key) for key in keys)
    return records


def _contract_declarations(contracts):
    declarations = []
    for schema, contract in contracts.items():
        for phase, additions in contract.get("deferred_additions", {}).items():
            for addition in additions:
                target = str(addition.get("target", ""))
                key = addition.get("key")
                declarations.append(
                    {
                        "phase": phase,
                        "schema": schema,
                        "key": key,
                        "type": addition.get("type"),
                        "target": target,
                        "identity": f"{target}.{key}",
                    }
                )
    return declarations


def _enum_extension_records(manifest):
    return {
        (schema, path, member)
        for schema, paths in manifest["enum_extensions"].items()
        for path, members in paths.items()
        for member in members
    }


def _promotion_state(declaration, manifest, contracts):
    schema = declaration["schema"]
    key = declaration["key"]
    target = declaration["target"]
    contract = contracts[schema]
    frozen = manifest["frozen_behavior"][schema]

    if target == "top.optional":
        actual = contract["optional_keys"]
        expected = frozen["optional_keys"]
    elif target.startswith("nested."):
        container = target[len("nested.") : -len(".optional")]
        actual = contract.get("nested", {}).get(container, {}).get("optional_keys", {})
        expected = frozen["nested"].get(container, {}).get("optional_keys", {})
    elif target == "banned_terms.optional":
        actual = contract.get("banned_terms", {})
        expected = frozen["content_floors"]["banned_terms_optional_entries"]
    elif target.startswith("enum."):
        path = target.removeprefix("enum.")
        actual = {member: "enum-member" for member in contract.get("enums", {}).get(path, [])}
        expected = {
            member: "enum-member"
            for member in frozen["enum_floors"].get(path, [])
        }
    else:
        return "unsupported", None, None

    actual_has = key in actual
    expected_has = key in expected
    if not actual_has and not expected_has:
        return "pending", actual, expected
    if actual_has and expected_has:
        return "authoritative", actual, expected
    return "partial", actual, expected


def _canonical_join(manifest, contracts):
    """Join all provenance sources and return path-qualified declarations plus problems."""
    problems = []
    manifest_records = _manifest_records(manifest)
    declarations = _contract_declarations(contracts)
    by_record = {}
    for declaration in declarations:
        record = (
            declaration["phase"],
            declaration["schema"],
            declaration["key"],
        )
        by_record.setdefault(record, []).append(declaration)

    # Full union: neither direction is privileged.
    for record in sorted(manifest_records | set(by_record)):
        declared = by_record.get(record, [])
        in_manifest = record in manifest_records
        if in_manifest and not declared:
            problems.append(
                f"orphan manifest record {record[0]}:{record[1]}:{record[2]}"
            )
            continue
        if not in_manifest:
            for declaration in declared:
                problems.append(
                    f"orphan declaration {record[0]}:{record[1]}:"
                    f"{declaration['identity']}"
                )
            continue
        if len(declared) != 1:
            problems.append(
                f"ambiguous declaration {record[0]}:{record[1]}:{record[2]}"
            )

    extension_records = _enum_extension_records(manifest)
    enum_declarations = [
        declaration
        for declaration in declarations
        if declaration["target"].startswith("enum.")
    ]
    declaration_enum_records = {
        (
            declaration["schema"],
            declaration["target"].removeprefix("enum."),
            declaration["key"],
        )
        for declaration in enum_declarations
    }
    for record in sorted(extension_records | declaration_enum_records):
        if record not in declaration_enum_records:
            problems.append(
                f"orphan enum_extensions record {record[0]}:"
                f"enum.{record[1]}.{record[2]}"
            )
        if record not in extension_records:
            problems.append(
                f"orphan enum declaration {record[0]}:"
                f"enum.{record[1]}.{record[2]}"
            )

    for declaration in declarations:
        schema = declaration["schema"]
        identity = declaration["identity"]
        target = declaration["target"]
        if not _supported_target(target):
            problems.append(f"{schema} unsupported target {target}")
            continue
        if target.startswith("enum."):
            path = target.removeprefix("enum.")
            if (
                path not in contracts[schema].get("enums", {})
                or path
                not in manifest["frozen_behavior"][schema].get("enum_floors", {})
            ):
                problems.append(f"{schema} {identity} unknown enum path {path}")
                continue
        state, actual, expected = _promotion_state(declaration, manifest, contracts)
        if state == "partial":
            problems.append(f"{schema} {identity} partial state")
            continue
        if state == "authoritative":
            key = declaration["key"]
            if target == "banned_terms.optional":
                if (
                    declaration["type"] != "note"
                    or not isinstance(actual[key], str)
                    or not actual[key]
                    or actual[key] != expected[key]
                ):
                    problems.append(f"{schema} {identity} value/type mismatch")
            elif target.startswith("enum."):
                if declaration["type"] != "enum-member":
                    problems.append(f"{schema} {identity} type must be enum-member")
            elif (
                actual[key] != expected[key]
                or declaration["type"] != actual[key]
            ):
                problems.append(f"{schema} {identity} type mismatch")
        elif target == "banned_terms.optional" and declaration["type"] != "note":
            problems.append(f"{schema} {identity} type must be note")
        elif target.startswith("enum.") and declaration["type"] != "enum-member":
            problems.append(f"{schema} {identity} type must be enum-member")
    return declarations, problems


# These tests prove checker and metadata acceptance only. Runtime reader-compatibility evidence for
# optional fields and enum extensions is required separately before any writer emits an addition.
class TestAdditiveCompat(unittest.TestCase):
    def setUp(self):
        self.manifest = _load_manifest()
        self.contracts = _load_contracts(self.manifest)

    def test_real_bundle_passes_shared_validator(self):
        self.assertEqual(validate_additive_bundle(_CONTRACTS), [])

    def test_manifest_and_contracts_agree(self):
        """Every provenance source resolves bidirectionally to one path-qualified declaration."""
        declarations, problems = _canonical_join(self.manifest, self.contracts)
        self.assertEqual(problems, [], "manifest/contract drift:\n" + "\n".join(problems))
        self.assertTrue(declarations)
        self.assertTrue(
            all(
                declaration["identity"]
                == f"{declaration['target']}.{declaration['key']}"
                for declaration in declarations
            ),
            "canonical identities must retain the full target path",
        )

    def test_every_deferred_addition_is_genuinely_additive(self):
        """Deferred additions never redefine a required key at their qualified target."""
        problems = []
        declarations, join_problems = _canonical_join(self.manifest, self.contracts)
        problems.extend(join_problems)
        for declaration in declarations:
            schema = declaration["schema"]
            contract = self.contracts[schema]
            target = declaration["target"]
            key = declaration["key"]
            identity = declaration["identity"]
            if target == "top.optional" and key in contract["required_keys"]:
                problems.append(f"{schema} {identity} collides with required_keys.{key}")
            elif target.startswith("nested."):
                container = target[len("nested.") : -len(".optional")]
                required = (
                    contract.get("nested", {})
                    .get(container, {})
                    .get("required_keys", {})
                )
                if key in required:
                    problems.append(
                        f"{schema} {identity} collides with "
                        f"nested.{container}.required_keys.{key}"
                    )
        self.assertEqual(problems, [], "non-additive change detected:\n" + "\n".join(problems))

    def test_v1_floor_is_preserved_under_all_additions(self):
        """The projected future shape (v1 floor + all additions) still contains every v1 required
        key with its original type. Additions never remove/rename/retype a required key."""
        problems = []
        for schema, contract in self.contracts.items():
            frozen = self.manifest["frozen_behavior"][schema]
            if contract.get("required_keys") != frozen["required_keys"]:
                problems.append(f"{schema} required_keys differ from frozen behavior")
            actual_nested = contract.get("nested", {})
            for container, spec in frozen["nested"].items():
                if (
                    actual_nested.get(container, {}).get("required_keys")
                    != spec["required_keys"]
                ):
                    problems.append(
                        f"{schema} nested.{container}.required_keys differ from frozen behavior"
                    )
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

    def test_frozen_behavior_coverage(self):
        frozen_behavior = self.manifest["frozen_behavior"]
        self.assertEqual(set(frozen_behavior), FROZEN_SCHEMAS)
        for schema, entry in frozen_behavior.items():
            with self.subTest(schema=schema):
                self.assertIsInstance(entry["required_keys"], dict)
                self.assertIsInstance(entry["optional_keys"], dict)
                self.assertIsInstance(entry["nested"], dict)
                self.assertIsInstance(entry["enum_floors"], dict)
                if schema == "intent-constitution/v1":
                    self.assertIsInstance(entry["content_floors"], dict)
                else:
                    self.assertIsNone(entry["content_floors"])

    def test_enum_extensions_is_an_object(self):
        enum_extensions = self.manifest["enum_extensions"]
        self.assertIsInstance(enum_extensions, dict)
        self.assertEqual(set(enum_extensions), FROZEN_SCHEMAS)
        for schema, paths in enum_extensions.items():
            with self.subTest(schema=schema):
                self.assertIsInstance(paths, dict)

    def test_enum_extensions_bidirectional(self):
        extension_records = _enum_extension_records(self.manifest)
        enum_declarations = {
            (
                declaration["schema"],
                declaration["target"].removeprefix("enum."),
                declaration["key"],
            )
            for declaration in _contract_declarations(self.contracts)
            if declaration["target"].startswith("enum.")
        }
        self.assertEqual(extension_records, enum_declarations)
        self.assertEqual(extension_records, set())
        self.assertTrue(
            all(paths == {} for paths in self.manifest["enum_extensions"].values())
        )

    def test_promotion_state_semantics(self):
        declarations, problems = _canonical_join(self.manifest, self.contracts)
        states = {}
        for declaration in declarations:
            state, _actual, _expected = _promotion_state(
                declaration, self.manifest, self.contracts
            )
            states[
                (
                    declaration["phase"],
                    declaration["schema"],
                    declaration["identity"],
                )
            ] = state
            if state not in {"pending", "authoritative"}:
                problems.append(
                    f"{declaration['schema']} {declaration['identity']} "
                    f"has invalid promotion state {state}"
                )
        self.assertEqual(problems, [], "promotion-state drift:\n" + "\n".join(problems))
        egress = (
            "egress",
            "intent-constitution/v1",
            "banned_terms.optional.tier_a_consumer_contributed",
        )
        self.assertEqual(
            states.get(egress),
            "pending",
            "tier_a_consumer_contributed must remain a valid pending declaration",
        )
        self.assertEqual(validate_additive_bundle(_CONTRACTS), [])

    def test_pending_deferred_additions_absent_from_floor(self):
        for declaration in _contract_declarations(self.contracts):
            if declaration["target"] != "top.optional" and not declaration[
                "target"
            ].startswith("nested."):
                continue
            state, actual, expected = _promotion_state(
                declaration, self.manifest, self.contracts
            )
            if declaration["key"] not in actual:
                with self.subTest(
                    schema=declaration["schema"],
                    identity=declaration["identity"],
                ):
                    self.assertEqual(state, "pending")
                    self.assertNotIn(declaration["key"], expected)


if __name__ == "__main__":
    unittest.main()
