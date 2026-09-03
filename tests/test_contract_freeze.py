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

from tests.freeze_helpers import validate_additive_bundle

_REPO_ROOT = Path(__file__).resolve().parent.parent
_CHECKER = _REPO_ROOT / "checks" / "intent-contract-freeze.sh"
_CONTRACTS = _REPO_ROOT / "contracts"


def _run_checker_against(mutate=None, mutate_manifest=None, *, validate_python=False):
    """Run the shipped checker against one coherent temporary contracts directory.

    Both mutators receive the same directory. When requested, the pure Python validator runs on
    that directory before it is removed; fixtures never split validator inputs.
    """
    with TemporaryDirectory() as d:
        cdir = Path(d) / "contracts"
        cdir.mkdir(parents=True)
        for p in _CONTRACTS.glob("*.json"):
            shutil.copy2(p, cdir / p.name)
        if mutate is not None:
            mutate(cdir)
        if mutate_manifest is not None:
            mutate_manifest(cdir)
        proc = subprocess.run(
            ["bash", str(_CHECKER)],
            env={**os.environ, "INTENT_CONTRACT_DIR": str(cdir)},
            capture_output=True,
            text=True,
        )
        if validate_python:
            return proc, validate_additive_bundle(cdir)
        return proc


def _edit_json(path: Path, fn):
    c = json.loads(path.read_text(encoding="utf-8"))
    fn(c)
    path.write_text(json.dumps(c, indent=2) + "\n", encoding="utf-8")


def _edit_bundle(cdir: Path, schema: str, fn):
    manifest_path = cdir / "additive-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    contract_path = cdir / manifest["frozen_behavior"][schema]["file"]
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    fn(contract, manifest)
    contract_path.write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def _configure_promotion(cdir: Path, target: str, state: str):
    """Create one synthetic promotion state entirely inside a temporary bundle."""
    if target == "top.optional":
        schema, key, declared_type = "intent-map/v1", "test_top", "string"
    elif target == "nested.param.optional":
        schema, key, declared_type = "intent-catalog/v1", "test_nested", "string"
    elif target == "enum.outcome":
        schema, key, declared_type = "intent-feedback/v1", "test_enum", "enum-member"
    elif target == "banned_terms.optional":
        schema, key, declared_type = (
            "intent-constitution/v1",
            "test_banned",
            "note",
        )
    else:
        raise AssertionError(f"unsupported test target: {target}")

    phase = f"test_{target.replace('.', '_')}"

    def mutate(contract, manifest):
        add_declaration = state not in {"orphan_manifest", "orphan_extension"}
        add_manifest_record = state not in {
            "missing_manifest",
            "orphan_extension",
        }
        if add_declaration:
            declaration_type = (
                "__wrong_type__" if state == "declaration_type_mismatch" else declared_type
            )
            contract.setdefault("deferred_additions", {})[phase] = [
                {
                    "key": key,
                    "type": declaration_type,
                    "target": target,
                }
            ]
        if add_manifest_record:
            manifest["deferred_phases"][phase] = {
                "kind": "additive",
                "contracts": {schema: [key]},
            }

        if target.startswith("enum."):
            path = target.removeprefix("enum.")
            if state not in {
                "missing_extension",
                "orphan_manifest",
                "missing_manifest",
            }:
                manifest["enum_extensions"][schema][path] = [key]
            if state in {"authoritative", "actual_only"}:
                contract["enums"].setdefault(path, []).append(key)
            if state in {"authoritative", "floor_only"}:
                manifest["frozen_behavior"][schema]["enum_floors"].setdefault(
                    path, []
                ).append(key)
            return

        if target == "top.optional":
            actual = contract["optional_keys"]
            frozen = manifest["frozen_behavior"][schema]["optional_keys"]
        elif target == "nested.param.optional":
            actual = contract["nested"]["param"]["optional_keys"]
            frozen = manifest["frozen_behavior"][schema]["nested"]["param"][
                "optional_keys"
            ]
        else:
            actual = contract["banned_terms"]
            frozen = manifest["frozen_behavior"][schema]["content_floors"][
                "banned_terms_optional_entries"
            ]

        value = "test value" if target == "banned_terms.optional" else "string"
        if state in {"authoritative", "actual_only", "type_mismatch"}:
            actual[key] = "__actual__" if state == "type_mismatch" else value
        if state in {"authoritative", "floor_only", "type_mismatch"}:
            frozen[key] = "__frozen__" if state == "type_mismatch" else value

    _edit_bundle(cdir, schema, mutate)


_FROZEN = {
    "intent-catalog.v1.json": "frozen",
    "intent-map.v1.json": "frozen",
    "intent-feedback.v1.json": "frozen",
    "intent-constitution.v1.json": "frozen",
    "intent-proposal.v1.json": "frozen",
}


class _CheckerAssertions:
    def _checker_output(self, proc):
        return (proc.stdout or "") + (proc.stderr or "")

    def _assert_fails(self, proc, *needles):
        out = self._checker_output(proc)
        self.assertNotEqual(
            proc.returncode,
            0,
            f"checker should FAIL on the adversarial change; it passed:\n{out}",
        )
        for needle in needles:
            self.assertIn(needle, out, f"expected {needle!r} in checker output:\n{out}")

    def _assert_passes(self, proc):
        out = self._checker_output(proc)
        self.assertEqual(proc.returncode, 0, f"checker should pass:\n{out}")

    def _assert_both_pass(self, mutate=None, mutate_manifest=None):
        proc, errors = _run_checker_against(
            mutate,
            mutate_manifest,
            validate_python=True,
        )
        self._assert_passes(proc)
        self.assertEqual(errors, [], "Python validator should pass:\n" + "\n".join(errors))

    def _assert_both_fail(self, mutate, *needles, mutate_manifest=None):
        proc, errors = _run_checker_against(
            mutate,
            mutate_manifest,
            validate_python=True,
        )
        self._assert_fails(proc, *needles)
        self.assertTrue(errors, "Python validator should reject the same bundle")
        python_output = "\n".join(errors)
        for needle in needles:
            self.assertIn(
                needle,
                python_output,
                f"expected {needle!r} in Python validator output:\n{python_output}",
            )


class TestContractFreeze(_CheckerAssertions, unittest.TestCase):
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

    def test_proposal_is_frozen(self):
        c = json.loads((_CONTRACTS / "intent-proposal.v1.json").read_text(encoding="utf-8"))
        self.assertEqual(c["status"], "frozen", "intent-proposal/v1 is frozen as of A0")
        self.assertIs(c["freeze_exempt"], False)
        self.assertTrue(c["frozen"], "a frozen proposal must record a frozen date (A0)")

    def test_dropping_correction_optional_fails(self):
        def mutate(cdir):
            _edit_json(
                cdir / "intent-feedback.v1.json",
                lambda c: c["optional_keys"].pop("correction"),
            )

        self._assert_fails(_run_checker_against(mutate), "DROPPED", "correction")

    def test_agents_md_freeze_timing_is_current(self):
        """AGENTS.md must not contain the stale 'intent-proposal/v1 is PROVISIONAL' claim."""
        agents_md = (_REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertNotIn(
            "intent-proposal/v1` is PROVISIONAL",
            agents_md,
            "AGENTS.md contains stale freeze-timing claim; intent-proposal/v1 is frozen",
        )
        # Consistency: the contract itself must also be frozen.
        contract = json.loads(
            (_CONTRACTS / "intent-proposal.v1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(contract["status"], "frozen", "contract status must be frozen")
        self.assertIs(contract.get("freeze_exempt"), False)


class TestContractFreezeRegression(_CheckerAssertions, unittest.TestCase):
    """BLOCKER-1 regression: the freeze checker MUST catch retype / added-required-key / nested-drop.

    Each test injects the exact adversarial change the review-swarm flagged as silently-passing and
    asserts the SHIPPED checker now FAILS (non-zero) with a message naming the break. Before the P0
    review fixes these all passed (EXIT 0) — the bug that made contract-freeze not actually freeze."""

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

    def test_unfreezing_proposal_fails(self):
        # A0 froze intent-proposal/v1 (freeze-timing lock flipped provisional->frozen). Regressing it
        # back to provisional must now FAIL the shipped checker — the freeze cannot be silently undone.
        def mutate(cdir):
            _edit_json(cdir / "intent-proposal.v1.json",
                       lambda c: c.update({"status": "provisional", "freeze_exempt": True, "frozen": None}))
        self._assert_fails(_run_checker_against(mutate), "intent-proposal", "status")

    def test_retype_frozen_proposal_required_key_fails(self):
        # The now-frozen proposal floor is immutable-within-v1: retyping a required key is breaking.
        def mutate(cdir):
            _edit_json(cdir / "intent-proposal.v1.json",
                       lambda c: c["required_keys"].__setitem__("requires_confirmation", "string"))
        self._assert_fails(_run_checker_against(mutate), "RETYPED", "requires_confirmation")


class TestContractFreezeHardening(_CheckerAssertions, unittest.TestCase):
    @staticmethod
    def _manifest_change(fn):
        return lambda cdir: _edit_json(cdir / "additive-manifest.json", fn)

    def test_manifest_bootstrap_negative_matrix(self):
        """Every accepted bootstrap-negative row drives the shipped checker."""

        def duplicate_manifest_key(cdir):
            path = cdir / "additive-manifest.json"
            text = path.read_text(encoding="utf-8")
            path.write_text(
                text.replace(
                    '"frozen_behavior": {',
                    '"frozen_behavior": {},\n  "frozen_behavior": {',
                    1,
                ),
                encoding="utf-8",
            )

        def duplicate_contract_key(cdir):
            path = cdir / "intent-map.v1.json"
            text = path.read_text(encoding="utf-8")
            path.write_text(
                text.replace(
                    "{",
                    '{\n  "schema": "intent-map/v1-duplicate",',
                    1,
                ),
                encoding="utf-8",
            )

        def malformed_manifest(cdir):
            (cdir / "additive-manifest.json").write_text("{", encoding="utf-8")

        def missing_manifest(cdir):
            (cdir / "additive-manifest.json").unlink()

        constitution = "intent-constitution/v1"
        catalog = "intent-catalog/v1"
        manifest_change = self._manifest_change
        cases = [
            (
                "schema_missing",
                manifest_change(lambda m: m.pop("schema")),
                ("schema header invalid",),
            ),
            (
                "schema_wrong",
                manifest_change(
                    lambda m: m.__setitem__("schema", "intent-additive-manifest/v2")
                ),
                ("schema header invalid",),
            ),
            (
                "version_missing",
                manifest_change(lambda m: m.pop("version")),
                ("version header invalid",),
            ),
            (
                "version_string",
                manifest_change(lambda m: m.__setitem__("version", "1")),
                ("version header invalid",),
            ),
            (
                "version_two",
                manifest_change(lambda m: m.__setitem__("version", 2)),
                ("version header invalid",),
            ),
            ("manifest_duplicate_key", duplicate_manifest_key, ("duplicate key",)),
            ("contract_duplicate_key", duplicate_contract_key, ("duplicate key",)),
            ("manifest_malformed_json", malformed_manifest, ("not valid JSON",)),
            ("manifest_missing", missing_manifest, ("manifest MISSING",)),
            (
                "filename_contains_slash",
                manifest_change(
                    lambda m: m["frozen_behavior"][catalog].__setitem__(
                        "file", "sub/intent-catalog.v1.json"
                    )
                ),
                ("unsafe",),
            ),
            (
                "filename_absolute",
                manifest_change(
                    lambda m: m["frozen_behavior"][catalog].__setitem__(
                        "file", "/tmp/intent-catalog.v1.json"
                    )
                ),
                ("unsafe",),
            ),
            (
                "filename_dotdot",
                manifest_change(
                    lambda m: m["frozen_behavior"][catalog].__setitem__(
                        "file", ".."
                    )
                ),
                ("unsafe",),
            ),
            (
                "filename_dotdot_slash",
                manifest_change(
                    lambda m: m["frozen_behavior"][catalog].__setitem__(
                        "file", "../intent-catalog.v1.json"
                    )
                ),
                ("unsafe",),
            ),
            (
                "filename_empty",
                manifest_change(
                    lambda m: m["frozen_behavior"][catalog].__setitem__("file", "")
                ),
                ("unsafe",),
            ),
            (
                "filename_non_string",
                manifest_change(
                    lambda m: m["frozen_behavior"][catalog].__setitem__("file", 1)
                ),
                ("unsafe",),
            ),
            (
                "filename_wrong_suffix",
                manifest_change(
                    lambda m: m["frozen_behavior"][catalog].__setitem__(
                        "file", "intent-catalog.json"
                    )
                ),
                ("unsafe",),
            ),
            (
                "frozen_behavior_missing",
                manifest_change(lambda m: m.pop("frozen_behavior")),
                ("frozen_behavior missing",),
            ),
            (
                "frozen_behavior_array",
                manifest_change(lambda m: m.__setitem__("frozen_behavior", [])),
                ("not an object",),
            ),
            (
                "frozen_behavior_extra_schema",
                manifest_change(
                    lambda m: m["frozen_behavior"].__setitem__(
                        "intent-extra/v1", {}
                    )
                ),
                ("unexpected schema",),
            ),
            (
                "frozen_behavior_missing_schema",
                manifest_change(lambda m: m["frozen_behavior"].pop(catalog)),
                ("missing schema",),
            ),
            (
                "duplicate_filename",
                manifest_change(
                    lambda m: m["frozen_behavior"]["intent-map/v1"].__setitem__(
                        "file", "intent-catalog.v1.json"
                    )
                ),
                ("duplicate filename",),
            ),
            (
                "status_not_frozen",
                manifest_change(
                    lambda m: m["frozen_behavior"][catalog].__setitem__(
                        "status", "provisional"
                    )
                ),
                ("status", "frozen"),
            ),
            (
                "optional_keys_absent",
                manifest_change(
                    lambda m: m["frozen_behavior"][catalog].pop("optional_keys")
                ),
                ("optional_keys", "invalid"),
            ),
            (
                "required_keys_array",
                manifest_change(
                    lambda m: m["frozen_behavior"][catalog].__setitem__(
                        "required_keys", []
                    )
                ),
                (catalog, "required_keys", "invalid"),
            ),
            (
                "nested_optional_keys_null",
                manifest_change(
                    lambda m: m["frozen_behavior"][catalog]["nested"][
                        "param"
                    ].__setitem__("optional_keys", None)
                ),
                ("nested", "invalid"),
            ),
            (
                "enum_floor_not_array",
                manifest_change(
                    lambda m: m["frozen_behavior"][catalog]["enum_floors"].__setitem__(
                        "safety_class", "read"
                    )
                ),
                ("enum_floors", "invalid"),
            ),
            (
                "enum_floor_non_string_member",
                manifest_change(
                    lambda m: m["frozen_behavior"][catalog]["enum_floors"].__setitem__(
                        "safety_class", ["read", 1]
                    )
                ),
                ("enum_floors", "invalid"),
            ),
            (
                "content_floors_absent",
                manifest_change(
                    lambda m: m["frozen_behavior"][catalog].pop("content_floors")
                ),
                ("content_floors", "invalid"),
            ),
            (
                "constitution_content_floors_null",
                manifest_change(
                    lambda m: m["frozen_behavior"][constitution].__setitem__(
                        "content_floors", None
                    )
                ),
                ("content_floors", "invalid"),
            ),
            (
                "non_constitution_content_floors_object",
                manifest_change(
                    lambda m: m["frozen_behavior"][catalog].__setitem__(
                        "content_floors", {}
                    )
                ),
                ("content_floors", "invalid"),
            ),
            (
                "required_keys_empty_key",
                manifest_change(
                    lambda m: m["frozen_behavior"][catalog]["required_keys"].__setitem__(
                        "", "string"
                    )
                ),
                ("required_keys", "invalid"),
            ),
            (
                "required_keys_empty_value",
                manifest_change(
                    lambda m: m["frozen_behavior"][catalog]["required_keys"].__setitem__(
                        "verb", ""
                    )
                ),
                ("required_keys", "invalid"),
            ),
            (
                "optional_keys_integer_value",
                manifest_change(
                    lambda m: m["frozen_behavior"]["intent-feedback/v1"][
                        "optional_keys"
                    ].__setitem__("correction", 1)
                ),
                ("optional_keys", "invalid"),
            ),
            (
                "nested_required_keys_absent",
                manifest_change(
                    lambda m: m["frozen_behavior"][catalog]["nested"]["param"].pop(
                        "required_keys"
                    )
                ),
                ("nested", "invalid"),
            ),
            (
                "nested_optional_keys_absent",
                manifest_change(
                    lambda m: m["frozen_behavior"][catalog]["nested"]["param"].pop(
                        "optional_keys"
                    )
                ),
                ("nested", "invalid"),
            ),
            (
                "enum_floor_empty_path",
                manifest_change(
                    lambda m: m["frozen_behavior"][catalog]["enum_floors"].__setitem__(
                        "", ["x"]
                    )
                ),
                ("enum_floors", "invalid"),
            ),
            (
                "content_rules_array",
                manifest_change(
                    lambda m: m["frozen_behavior"][constitution]["content_floors"].__setitem__(
                        "rules", []
                    )
                ),
                ("content_floors.rules invalid",),
            ),
            (
                "content_invariants_empty_key",
                manifest_change(
                    lambda m: m["frozen_behavior"][constitution]["content_floors"][
                        "kernel_invariants"
                    ].__setitem__("", "x")
                ),
                ("content_floors.kernel_invariants invalid",),
            ),
            (
                "content_banned_values_non_object",
                manifest_change(
                    lambda m: m["frozen_behavior"][constitution]["content_floors"].__setitem__(
                        "banned_terms_exact_values", []
                    )
                ),
                ("content_floors.banned_terms_exact_values invalid",),
            ),
            (
                "content_banned_scalar_empty_value",
                manifest_change(
                    lambda m: m["frozen_behavior"][constitution]["content_floors"][
                        "banned_terms_exact_scalars"
                    ].__setitem__("tier_c_consumer_contributed", "")
                ),
                ("content_floors.banned_terms_exact_scalars invalid",),
            ),
            (
                "content_banned_optional_non_string",
                manifest_change(
                    lambda m: m["frozen_behavior"][constitution]["content_floors"][
                        "banned_terms_optional_entries"
                    ].__setitem__("x", {"type": "note", "value": "x"})
                ),
                ("content_floors.banned_terms_optional_entries invalid",),
            ),
            (
                "content_banned_optional_empty_string",
                manifest_change(
                    lambda m: m["frozen_behavior"][constitution]["content_floors"][
                        "banned_terms_optional_entries"
                    ].__setitem__("x", "")
                ),
                ("content_floors.banned_terms_optional_entries invalid",),
            ),
            (
                "content_outcomes_non_array",
                manifest_change(
                    lambda m: m["frozen_behavior"][constitution]["content_floors"].__setitem__(
                        "operator_outcomes_exact_members", {}
                    )
                ),
                ("operator_outcomes_exact_members invalid",),
            ),
            (
                "content_outcomes_duplicate",
                manifest_change(
                    lambda m: m["frozen_behavior"][constitution]["content_floors"].__setitem__(
                        "operator_outcomes_exact_members",
                        ["accept", "accept"],
                    )
                ),
                ("operator_outcomes_exact_members invalid",),
            ),
        ]

        for name, mutate, needles in cases:
            with self.subTest(case=name):
                self._assert_fails(_run_checker_against(mutate), *needles)

    def test_enum_extensions_structure_negative_matrix(self):
        catalog = "intent-catalog/v1"
        change = self._manifest_change
        cases = [
            (
                "enum_extensions_missing_top_level",
                change(lambda m: m.pop("enum_extensions")),
                ("enum_extensions missing",),
            ),
            (
                "enum_extensions_not_object",
                change(lambda m: m.__setitem__("enum_extensions", [])),
                ("enum_extensions missing", "not an object"),
            ),
            (
                "enum_extensions_missing_schema",
                change(lambda m: m["enum_extensions"].pop(catalog)),
                ("enum_extensions missing schema",),
            ),
            (
                "enum_extensions_extra_schema",
                change(
                    lambda m: m["enum_extensions"].__setitem__(
                        "intent-extra/v1", {}
                    )
                ),
                ("enum_extensions unexpected schema",),
            ),
            (
                "enum_extensions_schema_not_object",
                change(lambda m: m["enum_extensions"].__setitem__(catalog, [])),
                ("not an object",),
            ),
            (
                "enum_extensions_empty_path",
                change(
                    lambda m: m["enum_extensions"][catalog].__setitem__("", ["x"])
                ),
                ("not a unique string array",),
            ),
            (
                "enum_extensions_value_not_array",
                change(
                    lambda m: m["enum_extensions"][catalog].__setitem__(
                        "safety_class", "x"
                    )
                ),
                ("not a unique string array",),
            ),
            (
                "enum_extensions_duplicate_member",
                change(
                    lambda m: m["enum_extensions"][catalog].__setitem__(
                        "safety_class", ["x", "x"]
                    )
                ),
                ("not a unique string array",),
            ),
            (
                "enum_extensions_non_string_member",
                change(
                    lambda m: m["enum_extensions"][catalog].__setitem__(
                        "safety_class", ["x", 1]
                    )
                ),
                ("not a unique string array",),
            ),
        ]
        for name, mutate, needles in cases:
            with self.subTest(case=name):
                self._assert_fails(_run_checker_against(mutate), *needles)

    def test_phase_and_declaration_structure_negative_matrix(self):
        change = self._manifest_change

        def deferred_phase_not_array(cdir):
            _edit_json(
                cdir / "intent-map.v1.json",
                lambda c: c["deferred_additions"].__setitem__("test_phase", {}),
            )

        def declaration_missing_target(cdir):
            _edit_json(
                cdir / "intent-map.v1.json",
                lambda c: c["deferred_additions"].__setitem__(
                    "test_phase", [{"key": "x", "type": "string"}]
                ),
            )

        def declaration_unsupported_target(cdir):
            _edit_json(
                cdir / "intent-map.v1.json",
                lambda c: c["deferred_additions"].__setitem__(
                    "test_phase",
                    [{"key": "x", "type": "string", "target": "unknown.target"}],
                ),
            )

        cases = [
            (
                "required_additive_phases_not_array",
                change(
                    lambda m: m.__setitem__("required_additive_phases", "R2")
                ),
                ("required_additive_phases invalid",),
            ),
            (
                "deferred_phases_not_object",
                change(lambda m: m.__setitem__("deferred_phases", [])),
                ("deferred_phases invalid",),
            ),
            (
                "unsupported_phase_kind",
                change(
                    lambda m: m["deferred_phases"]["R2"].__setitem__(
                        "kind", "breaking"
                    )
                ),
                ("kind invalid",),
            ),
            (
                "additive_phase_unknown_schema",
                change(
                    lambda m: m["deferred_phases"]["R2"]["contracts"].__setitem__(
                        "intent-unknown/v1", ["x"]
                    )
                ),
                ("intent-unknown/v1", "invalid"),
            ),
            (
                "required_phase_missing",
                change(lambda m: m["deferred_phases"].pop("R2")),
                ("required phase R2 missing",),
            ),
            (
                "deferred_phase_value_not_array",
                deferred_phase_not_array,
                ("deferred declaration invalid", "array"),
            ),
            (
                "declaration_missing_target",
                declaration_missing_target,
                ("deferred declaration invalid", "target"),
            ),
            (
                "declaration_unsupported_target",
                declaration_unsupported_target,
                ("deferred declaration invalid", "unsupported target"),
            ),
        ]
        for name, mutate, needles in cases:
            with self.subTest(case=name):
                self._assert_fails(_run_checker_against(mutate), *needles)

    def test_existing_protections_negative_matrix(self):
        def contract_change(filename, fn):
            return lambda cdir: _edit_json(cdir / filename, fn)

        def invalid_contract_json(cdir):
            (cdir / "intent-map.v1.json").write_text("{", encoding="utf-8")

        def undeclared_unknown(cdir):
            (cdir / "intent-extra.v1.json").write_text(
                json.dumps({"schema": "intent-extra/v1"}) + "\n",
                encoding="utf-8",
            )

        def undeclared_duplicate(cdir):
            (cdir / "duplicate.v1.json").write_text(
                json.dumps({"schema": "intent-map/v1"}) + "\n",
                encoding="utf-8",
            )

        cases = [
            (
                "contract_version_two",
                contract_change(
                    "intent-map.v1.json", lambda c: c.__setitem__("version", 2)
                ),
                ("version not 1",),
            ),
            (
                "freeze_strings_missing_schema",
                contract_change(
                    "intent-map.v1.json",
                    lambda c: c["freeze_strings"].remove("intent-map/v1"),
                ),
                ("freeze_strings missing schema",),
            ),
            (
                "freeze_exempt_true",
                contract_change(
                    "intent-map.v1.json",
                    lambda c: c.__setitem__("freeze_exempt", True),
                ),
                ("freeze_exempt must be false",),
            ),
            (
                "frozen_date_empty",
                contract_change(
                    "intent-map.v1.json", lambda c: c.__setitem__("frozen", "")
                ),
                ("frozen date missing",),
            ),
            (
                "frozen_date_absent",
                contract_change(
                    "intent-map.v1.json", lambda c: c.pop("frozen")
                ),
                ("frozen date missing",),
            ),
            (
                "contract_invalid_json",
                invalid_contract_json,
                ("contract intent-map/v1 not valid JSON",),
            ),
            (
                "manifest_declared_file_missing",
                self._manifest_change(
                    lambda m: m["frozen_behavior"]["intent-map/v1"].__setitem__(
                        "file", "missing.v1.json"
                    )
                ),
                ("missing file",),
            ),
            (
                "undeclared_unknown_schema_file",
                undeclared_unknown,
                ("undeclared contract file", "intent-extra.v1.json"),
            ),
            (
                "undeclared_duplicate_schema_file",
                undeclared_duplicate,
                ("undeclared contract file", "duplicate.v1.json"),
            ),
        ]
        for name, mutate, needles in cases:
            with self.subTest(case=name):
                self._assert_fails(_run_checker_against(mutate), *needles)

    def test_every_required_key_removal_fails(self):
        manifest = json.loads(
            (_CONTRACTS / "additive-manifest.json").read_text(encoding="utf-8")
        )
        for schema, frozen in manifest["frozen_behavior"].items():
            filename = frozen["file"]
            for key in frozen["required_keys"]:
                with self.subTest(schema=schema, path=f"required_keys.{key}"):
                    def mutate(cdir, filename=filename, key=key):
                        _edit_json(
                            cdir / filename,
                            lambda c: c["required_keys"].pop(key),
                        )

                    self._assert_fails(
                        _run_checker_against(mutate),
                        schema,
                        f"required_keys.{key}",
                        "DROPPED",
                    )

    def test_every_required_key_retype_fails(self):
        manifest = json.loads(
            (_CONTRACTS / "additive-manifest.json").read_text(encoding="utf-8")
        )
        for schema, frozen in manifest["frozen_behavior"].items():
            filename = frozen["file"]
            for key in frozen["required_keys"]:
                with self.subTest(schema=schema, path=f"required_keys.{key}"):
                    def mutate(cdir, filename=filename, key=key):
                        _edit_json(
                            cdir / filename,
                            lambda c: c["required_keys"].__setitem__(
                                key, "__sentinel__"
                            ),
                        )

                    self._assert_fails(
                        _run_checker_against(mutate),
                        schema,
                        f"required_keys.{key}",
                        "RETYPED",
                    )

    def test_added_required_keys_fail_at_top_and_nested(self):
        def top_level(cdir):
            _edit_json(
                cdir / "intent-map.v1.json",
                lambda c: c["required_keys"].__setitem__("test_required", "string"),
            )

        def nested(cdir):
            _edit_json(
                cdir / "intent-catalog.v1.json",
                lambda c: c["nested"]["param"]["required_keys"].__setitem__(
                    "test_required", "string"
                ),
            )

        for name, mutate, path in [
            ("top", top_level, "required_keys.test_required"),
            ("nested", nested, "nested.param.required_keys.test_required"),
        ]:
            with self.subTest(case=name):
                self._assert_fails(
                    _run_checker_against(mutate),
                    path,
                    "ADD",
                )

    def test_narrowing_correction_union_fails(self):
        def mutate(cdir):
            _edit_json(
                cdir / "intent-feedback.v1.json",
                lambda c: c["optional_keys"].__setitem__("correction", "object"),
            )

        self._assert_fails(
            _run_checker_against(mutate),
            "RETYPED",
            "correction",
            "object|null",
            "object",
        )

    def test_dropping_catalog_nested_optional_enum_fails(self):
        def mutate(cdir):
            _edit_json(
                cdir / "intent-catalog.v1.json",
                lambda c: c["nested"]["param"]["optional_keys"].pop("enum"),
            )

        self._assert_fails(
            _run_checker_against(mutate),
            "DROPPED",
            "nested.param.optional_keys.enum",
        )

    def test_dropping_catalog_nested_optional_source_fails(self):
        def mutate(cdir):
            _edit_json(
                cdir / "intent-catalog.v1.json",
                lambda c: c["nested"]["param"]["optional_keys"].pop("source"),
            )

        self._assert_fails(
            _run_checker_against(mutate),
            "DROPPED",
            "nested.param.optional_keys.source",
        )

    def test_unrecorded_optional_addition_fails(self):
        def mutate(cdir):
            _edit_json(
                cdir / "intent-map.v1.json",
                lambda c: c["optional_keys"].__setitem__(
                    "test_unrecorded", "string"
                ),
            )

        self._assert_fails(
            _run_checker_against(mutate),
            "ADD unrecorded optional",
            "test_unrecorded",
        )

    def test_every_enum_member_removal_fails(self):
        manifest = json.loads(
            (_CONTRACTS / "additive-manifest.json").read_text(encoding="utf-8")
        )
        for schema, frozen in manifest["frozen_behavior"].items():
            filename = frozen["file"]
            for path, members in frozen["enum_floors"].items():
                for member in members:
                    with self.subTest(schema=schema, path=path, member=member):
                        def mutate(
                            cdir,
                            filename=filename,
                            path=path,
                            member=member,
                        ):
                            _edit_json(
                                cdir / filename,
                                lambda c: c["enums"][path].remove(member),
                            )

                        self._assert_fails(
                            _run_checker_against(mutate),
                            schema,
                            f"enum {path}",
                            "dropped frozen value",
                            member,
                        )

    def test_named_previously_unfrozen_enum_members_fail(self):
        cases = [
            (
                "feedback.verdict",
                "intent-feedback.v1.json",
                "verdict",
                "strong",
            ),
            (
                "catalog.param.type",
                "intent-catalog.v1.json",
                "param.type",
                "string",
            ),
            (
                "catalog.param.source",
                "intent-catalog.v1.json",
                "param.source",
                "literal",
            ),
            (
                "constitution.machine_check.status",
                "intent-constitution.v1.json",
                "machine_check.status",
                "spec",
            ),
        ]
        for name, filename, path, member in cases:
            with self.subTest(case=name):
                def mutate(
                    cdir,
                    filename=filename,
                    path=path,
                    member=member,
                ):
                    _edit_json(
                        cdir / filename,
                        lambda c: c["enums"][path].remove(member),
                    )

                self._assert_fails(
                    _run_checker_against(mutate),
                    f"enum {path}",
                    "dropped frozen value",
                    member,
                )

    def test_unrecorded_enum_member_fails(self):
        def mutate(cdir):
            _edit_json(
                cdir / "intent-feedback.v1.json",
                lambda c: c["enums"]["outcome"].append("test_unrecorded"),
            )

        self._assert_fails(
            _run_checker_against(mutate),
            "enum outcome",
            "unrecorded member",
            "test_unrecorded",
        )

    def test_machine_check_spec_to_active_passes(self):
        def mutate(cdir):
            def activate_one(contract):
                for check in contract["machine_checks"].values():
                    if check["status"] == "spec":
                        check["status"] = "active"
                        return
                raise AssertionError("fixture needs one spec machine check")

            _edit_json(
                cdir / "intent-constitution.v1.json",
                activate_one,
            )

        self._assert_both_pass(mutate)

    def test_constitution_content_floor_negative_matrix(self):
        def contract_change(fn):
            return lambda cdir: _edit_json(
                cdir / "intent-constitution.v1.json", fn
            )

        def change_rule_text(contract):
            next(rule for rule in contract["rules"] if rule["id"] == "CR1")[
                "rule"
            ] = "changed"

        def remove_rule(contract):
            contract["rules"] = [
                rule for rule in contract["rules"] if rule["id"] != "CR2"
            ]

        def add_rule(contract):
            contract["rules"].append(
                {
                    "id": "CR99",
                    "rule": "test rule",
                    "enforcement": "no_execution_path",
                }
            )

        def change_invariant_text(contract):
            next(
                invariant
                for invariant in contract["kernel_invariants"]
                if invariant["id"] == "KI1"
            )["invariant"] = "changed"

        cases = [
            ("cr1_text_changed", contract_change(change_rule_text), ("CR1", "text CHANGED")),
            ("cr2_removed", contract_change(remove_rule), ("CR2", "DROPPED")),
            (
                "unrecorded_rule_added",
                contract_change(add_rule),
                ("unrecorded rule ID", "CR99"),
            ),
            (
                "ki1_text_changed",
                contract_change(change_invariant_text),
                ("KI1", "text CHANGED"),
            ),
            (
                "tier_a_member_removed",
                contract_change(
                    lambda c: c["banned_terms"][
                        "tier_a_generic_mechanism"
                    ].remove("kernel")
                ),
                ("tier_a_generic_mechanism", "DROPPED", "kernel"),
            ),
            (
                "tier_a_unrecorded_member_added",
                contract_change(
                    lambda c: c["banned_terms"][
                        "tier_a_generic_mechanism"
                    ].append("test_unrecorded")
                ),
                ("tier_a_generic_mechanism", "unrecorded", "test_unrecorded"),
            ),
            (
                "operator_abort_removed",
                contract_change(lambda c: c["operator_outcomes"].remove("abort")),
                ("operator_outcomes", "DROPPED", "abort"),
            ),
            (
                "operator_unrecorded_member_added",
                contract_change(
                    lambda c: c["operator_outcomes"].append("test_unrecorded")
                ),
                ("operator_outcomes", "unrecorded", "test_unrecorded"),
            ),
            (
                "tier_c_scalar_changed",
                contract_change(
                    lambda c: c["banned_terms"].__setitem__(
                        "tier_c_consumer_contributed", "changed"
                    )
                ),
                ("tier_c_consumer_contributed", "CHANGED"),
            ),
        ]
        for name, mutate, needles in cases:
            with self.subTest(case=name):
                self._assert_fails(_run_checker_against(mutate), *needles)

    def test_sanctioned_constitution_content_extension_passes_both_validators(self):
        rule_text = "Synthetic test rule text."

        def mutate(cdir):
            def update(contract, manifest):
                contract["rules"].append(
                    {
                        "id": "CR99",
                        "rule": rule_text,
                        "enforcement": "no_execution_path",
                    }
                )
                manifest["frozen_behavior"]["intent-constitution/v1"][
                    "content_floors"
                ]["rules"]["CR99"] = rule_text

            _edit_bundle(cdir, "intent-constitution/v1", update)

        self._assert_both_pass(mutate)

    def test_optional_and_nested_promotion_state_matrix(self):
        for target in ("top.optional", "nested.param.optional"):
            for state in ("pending", "authoritative"):
                with self.subTest(target=target, state=state):
                    self._assert_both_pass(
                        lambda cdir, target=target, state=state: _configure_promotion(
                            cdir, target, state
                        )
                    )
            failing_states = {
                "actual_only": "ADD unrecorded optional",
                "floor_only": "DROPPED frozen optional",
                "type_mismatch": "RETYPED",
                "missing_manifest": "orphan declaration",
                "orphan_manifest": "orphan manifest record",
            }
            for state, needle in failing_states.items():
                with self.subTest(target=target, state=state):
                    self._assert_both_fail(
                        lambda cdir, target=target, state=state: _configure_promotion(
                            cdir, target, state
                        ),
                        needle,
                    )

    def test_enum_promotion_state_matrix(self):
        target = "enum.outcome"
        for state in ("pending", "authoritative"):
            with self.subTest(state=state):
                self._assert_both_pass(
                    lambda cdir, state=state: _configure_promotion(
                        cdir, target, state
                    )
                )
        failing_states = {
            "actual_only": "unrecorded member",
            "floor_only": "dropped frozen value",
            "missing_extension": "orphan enum declaration",
            "orphan_extension": "has no deferred declaration",
            "declaration_type_mismatch": "type must be enum-member",
            "missing_manifest": "orphan declaration",
            "orphan_manifest": "orphan manifest record",
        }
        for state, needle in failing_states.items():
            with self.subTest(state=state):
                self._assert_both_fail(
                    lambda cdir, state=state: _configure_promotion(
                        cdir, target, state
                    ),
                    needle,
                )

    def test_banned_terms_optional_promotion_state_matrix(self):
        # The unmodified bundle is the real pending tier_a_consumer_contributed state.
        self._assert_both_pass()
        target = "banned_terms.optional"
        self._assert_both_pass(
            lambda cdir: _configure_promotion(cdir, target, "authoritative")
        )
        failing_states = {
            "type_mismatch": "value mismatch",
            "actual_only": "unrecorded banned_terms.optional key",
            "floor_only": "missing from actual",
            "declaration_type_mismatch": "type must be note",
            "missing_manifest": "orphan declaration",
            "orphan_manifest": "orphan manifest record",
        }
        for state, needle in failing_states.items():
            with self.subTest(state=state):
                self._assert_both_fail(
                    lambda cdir, state=state: _configure_promotion(
                        cdir, target, state
                    ),
                    needle,
                )

    def test_sanctioned_optional_addition_passes_both_validators(self):
        def mutate(cdir):
            def update(contract, manifest):
                contract["deferred_additions"]["test_phase"] = [
                    {
                        "key": "test_sanctioned",
                        "type": "string",
                        "target": "top.optional",
                    }
                ]
                contract["optional_keys"]["test_sanctioned"] = "string"
                manifest["frozen_behavior"]["intent-map/v1"]["optional_keys"][
                    "test_sanctioned"
                ] = "string"
                manifest["deferred_phases"]["test_phase"] = {
                    "kind": "additive",
                    "contracts": {"intent-map/v1": ["test_sanctioned"]},
                }

            _edit_bundle(cdir, "intent-map/v1", update)

        self._assert_both_pass(mutate)

    def test_sanctioned_enum_extension_passes_both_validators(self):
        def mutate(cdir):
            def update(contract, manifest):
                contract["deferred_additions"]["test_enum_phase"] = [
                    {
                        "key": "test_ext",
                        "type": "enum-member",
                        "target": "enum.outcome",
                    }
                ]
                contract["enums"]["outcome"].append("test_ext")
                manifest["frozen_behavior"]["intent-feedback/v1"]["enum_floors"][
                    "outcome"
                ].append("test_ext")
                manifest["enum_extensions"]["intent-feedback/v1"]["outcome"] = [
                    "test_ext"
                ]
                manifest["deferred_phases"]["test_enum_phase"] = {
                    "kind": "additive",
                    "contracts": {"intent-feedback/v1": ["test_ext"]},
                }

            _edit_bundle(cdir, "intent-feedback/v1", update)

        self._assert_both_pass(mutate)

if __name__ == "__main__":
    unittest.main()
