#!/usr/bin/env bash
# intent-contract-freeze.sh — assert the versioned intent-router contracts still satisfy their
# FROZEN behavior floor (contracts/*.v1.json). Read-only.
#
# Frozen behavior authority is
# contracts/additive-manifest.json::frozen_behavior. Contract JSON is the actual declared shape.
# FROZEN_SCHEMAS is the bootstrap trust anchor (schema IDs only); the manifest owns filenames and
# status. Required, optional, nested, enum, and constitution content surfaces are exact floors.
#
# FREEZE TIMING (obey exactly):
#   FROZEN in P0 (freeze-locked): intent-catalog/v1, intent-map/v1, intent-feedback/v1,
#     intent-constitution/v1.
#   FROZEN in A0: intent-proposal/v1 — the highest re-architecture-risk envelope, held provisional
#     through P0/R-core and frozen only AFTER A0 exercised it (hand-written fixture + breadth battery
#     + the AWA first-consumer seam). It is now freeze-locked exactly like the P0 four.
#
# Role-resolved: finds contracts/ relative to this script (INTENT_HOME), never a hardcoded path.
set -uo pipefail

SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"   # checks/
INTENT_HOME="${INTENT_HOME:-$(cd "$SELF_DIR/.." && pwd)}"      # repo/install root (role-resolved)
# INTENT_CONTRACT_DIR is test-only; production default is fail-closed to INTENT_HOME/contracts.
CONTRACTS="${INTENT_CONTRACT_DIR:-"$INTENT_HOME/contracts"}"

fail=0
pass() { printf '  PASS  %s\n' "$1"; }
bad()  { printf '  FAIL  %s\n' "$1"; fail=1; }

echo "== intent-router contract freeze (v1, behavior-only, role-resolved) =="
echo "   INTENT_HOME=$INTENT_HOME"

if [ ! -d "$CONTRACTS" ]; then
  bad "contracts/ dir missing: $CONTRACTS"; echo "intent-contract-freeze: FAILED"; exit 1
fi

# The single source of truth for the freeze checker lives in python so the JSON floor logic is
# one place. Emits PASS/FAIL lines and a non-zero exit on any drift.
if CONTRACTS="$CONTRACTS" python3 - <<'PY'
import json, os, sys
from pathlib import Path

contracts_dir = Path(os.environ["CONTRACTS"])

FROZEN_SCHEMAS = {
    "intent-catalog/v1",
    "intent-map/v1",
    "intent-feedback/v1",
    "intent-constitution/v1",
    "intent-proposal/v1",
}
CONSTITUTION_SCHEMA = "intent-constitution/v1"
CONTENT_KEYS = {
    "rules",
    "kernel_invariants",
    "banned_terms_exact_values",
    "banned_terms_exact_scalars",
    "banned_terms_optional_entries",
    "operator_outcomes_exact_members",
}


class ValidationError(Exception):
    pass


class DuplicateKeyError(ValueError):
    def __init__(self, key):
        super().__init__(key)
        self.key = key


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def die(message):
    raise ValidationError(message)


def load_json(path, label, missing_message):
    if not path.is_file() or not os.access(path, os.R_OK):
        die(missing_message)
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_keys,
        )
    except DuplicateKeyError as exc:
        die(f"{label} duplicate key {exc.key}")
    except (OSError, UnicodeError, json.JSONDecodeError):
        die(f"{label} not valid JSON")


def is_nonempty_string(value):
    return isinstance(value, str) and bool(value)


def is_unique_string_array(value, require_nonempty=False):
    return (
        isinstance(value, list)
        and (not require_nonempty or bool(value))
        and all(is_nonempty_string(member) for member in value)
        and len(value) == len(set(value))
    )


def require_type_map(value, diagnostic):
    if (
        not isinstance(value, dict)
        or any(not is_nonempty_string(key) for key in value)
        or any(not is_nonempty_string(item) for item in value.values())
    ):
        die(diagnostic)


def require_string_arrays(value, diagnostic):
    if (
        not isinstance(value, dict)
        or any(not is_nonempty_string(key) for key in value)
        or any(not is_unique_string_array(items) for items in value.values())
    ):
        die(diagnostic)


def supported_target(target):
    if target in {"top.optional", "banned_terms.optional"}:
        return True
    if target.startswith("enum."):
        return is_nonempty_string(target.removeprefix("enum."))
    if target.startswith("nested.") and target.endswith(".optional"):
        container = target[len("nested.") : -len(".optional")]
        return is_nonempty_string(container) and "." not in container
    return False


def validate_content_floors(content):
    if not isinstance(content, dict) or set(content) != CONTENT_KEYS:
        die(f"frozen_behavior[{CONSTITUTION_SCHEMA}].content_floors invalid")
    require_type_map(content["rules"], "content_floors.rules invalid")
    require_type_map(
        content["kernel_invariants"],
        "content_floors.kernel_invariants invalid",
    )
    require_string_arrays(
        content["banned_terms_exact_values"],
        "content_floors.banned_terms_exact_values invalid",
    )
    require_type_map(
        content["banned_terms_exact_scalars"],
        "content_floors.banned_terms_exact_scalars invalid",
    )
    require_type_map(
        content["banned_terms_optional_entries"],
        "content_floors.banned_terms_optional_entries invalid",
    )
    if not is_unique_string_array(content["operator_outcomes_exact_members"]):
        die("content_floors.operator_outcomes_exact_members invalid")


def validate_manifest_structure(manifest):
    if manifest.get("schema") != "intent-additive-manifest/v1":
        die("manifest schema header invalid: expected intent-additive-manifest/v1")
    if type(manifest.get("version")) is not int or manifest["version"] != 1:
        die("manifest version header invalid: expected integer 1")

    frozen_behavior = manifest.get("frozen_behavior")
    if not isinstance(frozen_behavior, dict):
        die("frozen_behavior missing or not an object")
    enum_extensions = manifest.get("enum_extensions")
    if not isinstance(enum_extensions, dict):
        die("enum_extensions missing or not an object")

    missing = sorted(FROZEN_SCHEMAS - set(frozen_behavior))
    extra = sorted(set(frozen_behavior) - FROZEN_SCHEMAS)
    if missing:
        die(f"frozen_behavior missing schema {missing[0]}")
    if extra:
        die(f"frozen_behavior unexpected schema {extra[0]}")

    filenames = []
    root = contracts_dir.resolve()
    for schema in sorted(FROZEN_SCHEMAS):
        entry = frozen_behavior[schema]
        if not isinstance(entry, dict):
            die(f"frozen_behavior[{schema}] invalid")
        filename = entry.get("file")
        unsafe = (
            not is_nonempty_string(filename)
            or "/" in filename
            or "\\" in filename
            or Path(filename).name != filename
            or not filename.endswith(".v1.json")
        )
        if not unsafe:
            candidate = (contracts_dir / filename).resolve()
            unsafe = candidate.parent != root
        if unsafe:
            die(f"frozen_behavior[{schema}].file unsafe: {filename}")
        filenames.append(filename)

        if entry.get("status") != "frozen":
            die(f"frozen_behavior[{schema}].status invalid: expected frozen")
        if "required_keys" not in entry:
            die(f"frozen_behavior[{schema}].required_keys invalid")
        require_type_map(
            entry["required_keys"],
            f"frozen_behavior[{schema}].required_keys invalid",
        )
        if "optional_keys" not in entry:
            die(f"frozen_behavior[{schema}].optional_keys invalid")
        require_type_map(
            entry["optional_keys"],
            f"frozen_behavior[{schema}].optional_keys invalid",
        )

        nested = entry.get("nested")
        if not isinstance(nested, dict):
            die(f"frozen_behavior[{schema}].nested invalid")
        for container, spec in nested.items():
            diagnostic = f"frozen_behavior[{schema}].nested[{container}] invalid"
            if (
                not is_nonempty_string(container)
                or not isinstance(spec, dict)
                or "required_keys" not in spec
                or "optional_keys" not in spec
            ):
                die(diagnostic)
            require_type_map(spec["required_keys"], diagnostic)
            require_type_map(spec["optional_keys"], diagnostic)

        enum_floors = entry.get("enum_floors")
        if not isinstance(enum_floors, dict):
            die(f"frozen_behavior[{schema}].enum_floors invalid")
        for path, members in enum_floors.items():
            if not is_nonempty_string(path) or not is_unique_string_array(members):
                die(f"frozen_behavior[{schema}].enum_floors[{path}] invalid")

        if "content_floors" not in entry:
            die(f"frozen_behavior[{schema}].content_floors invalid")
        content = entry["content_floors"]
        if schema == CONSTITUTION_SCHEMA:
            validate_content_floors(content)
        elif content is not None:
            die(f"frozen_behavior[{schema}].content_floors invalid")

    duplicate_filenames = sorted(
        filename for filename in set(filenames) if filenames.count(filename) > 1
    )
    if duplicate_filenames:
        die(f"frozen_behavior duplicate filename {duplicate_filenames[0]}")

    enum_missing = sorted(FROZEN_SCHEMAS - set(enum_extensions))
    enum_extra = sorted(set(enum_extensions) - FROZEN_SCHEMAS)
    if enum_missing:
        die(f"enum_extensions missing schema {enum_missing[0]}")
    if enum_extra:
        die(f"enum_extensions unexpected schema {enum_extra[0]}")
    for schema in sorted(FROZEN_SCHEMAS):
        paths = enum_extensions[schema]
        if not isinstance(paths, dict):
            die(f"enum_extensions[{schema}] not an object")
        for path, members in paths.items():
            if not is_nonempty_string(path) or not is_unique_string_array(members):
                die(
                    f"enum_extensions[{schema}][{path}] "
                    "not a unique string array"
                )

    required_phases = manifest.get("required_additive_phases")
    if not is_unique_string_array(required_phases):
        die("required_additive_phases invalid")
    phases = manifest.get("deferred_phases")
    if not isinstance(phases, dict):
        die("deferred_phases invalid")
    for phase, spec in phases.items():
        if not is_nonempty_string(phase) or not isinstance(spec, dict):
            die(f"deferred_phases[{phase}] invalid")
        kind = spec.get("kind")
        if kind not in {"additive", "no-schema-change"}:
            die(f"deferred_phases[{phase}].kind invalid")
        if kind == "additive":
            records = spec.get("contracts")
            if not isinstance(records, dict) or not records:
                die(f"deferred_phases[{phase}].contracts invalid")
            for schema, keys in records.items():
                if (
                    schema not in FROZEN_SCHEMAS
                    or not is_unique_string_array(keys, require_nonempty=True)
                ):
                    die(
                        f"deferred_phases[{phase}].contracts[{schema}] invalid"
                    )
        elif not is_nonempty_string(spec.get("reason")):
            die(f"deferred_phases[{phase}].reason invalid")
    for phase in required_phases:
        if phase not in phases:
            die(f"required phase {phase} missing from deferred_phases")


def validate_deferred_declarations(schema, contract):
    additions = contract.get("deferred_additions")
    if not isinstance(additions, dict):
        die(f"contract {schema} deferred declaration invalid: not an object")
    for phase, declarations in additions.items():
        if not is_nonempty_string(phase) or not isinstance(declarations, list):
            die(
                f"contract {schema} deferred declaration invalid: "
                f"phase {phase} must be an array"
            )
        for declaration in declarations:
            if not isinstance(declaration, dict):
                die(f"contract {schema} deferred declaration invalid: not an object")
            for field in ("key", "type", "target"):
                if not is_nonempty_string(declaration.get(field)):
                    die(
                        f"contract {schema} deferred declaration invalid: "
                        f"{field} missing or empty"
                    )
            if not supported_target(declaration["target"]):
                die(
                    f"contract {schema} deferred declaration invalid: "
                    f"unsupported target {declaration['target']}"
                )

def compare_type_maps(errs, schema, path, actual, frozen, field_kind):
    if not isinstance(actual, dict):
        errs.append(f"{schema} {path} invalid: must be an object")
        actual = {}
    missing = sorted(set(frozen) - set(actual))
    extra = sorted(set(actual) - set(frozen))
    for key in missing:
        suffix = " frozen optional" if field_kind == "optional" else " frozen required"
        errs.append(f"{schema} {path}.{key} DROPPED{suffix}")
    for key in extra:
        suffix = " unrecorded optional" if field_kind == "optional" else " unrecorded required"
        errs.append(f"{schema} {path}.{key} ADD{suffix}")
    for key in sorted(set(actual) & set(frozen)):
        if actual[key] != frozen[key]:
            errs.append(
                f"{schema} {path}.{key} RETYPED "
                f"{actual[key]!r} != frozen {frozen[key]!r}"
            )


def compare_nested(errs, schema, contract, frozen):
    actual_nested = contract.get("nested")
    if not isinstance(actual_nested, dict):
        errs.append(f"{schema} nested invalid: must be an object")
        actual_nested = {}
    frozen_nested = frozen["nested"]
    for container in sorted(set(frozen_nested) - set(actual_nested)):
        errs.append(f"{schema} nested.{container} DROPPED frozen container")
    for container in sorted(set(actual_nested) - set(frozen_nested)):
        errs.append(f"{schema} nested.{container} ADD unrecorded container")
    for container in sorted(set(actual_nested) & set(frozen_nested)):
        actual_spec = actual_nested[container]
        if not isinstance(actual_spec, dict):
            errs.append(f"{schema} nested.{container} invalid: must be an object")
            actual_spec = {}
        frozen_spec = frozen_nested[container]
        compare_type_maps(
            errs,
            schema,
            f"nested.{container}.required_keys",
            actual_spec.get("required_keys"),
            frozen_spec["required_keys"],
            "required",
        )
        compare_type_maps(
            errs,
            schema,
            f"nested.{container}.optional_keys",
            actual_spec.get("optional_keys"),
            frozen_spec["optional_keys"],
            "optional",
        )


def compare_enums(errs, schema, contract, frozen):
    actual_enums = contract.get("enums")
    if not isinstance(actual_enums, dict):
        errs.append(f"{schema} enums invalid: must be an object")
        actual_enums = {}
    frozen_enums = frozen["enum_floors"]
    for path in sorted(set(frozen_enums) - set(actual_enums)):
        errs.append(f"{schema} enum {path} DROPPED frozen path")
    for path in sorted(set(actual_enums) - set(frozen_enums)):
        errs.append(f"{schema} enum {path} ADD unrecorded path")
    for path in sorted(set(actual_enums) & set(frozen_enums)):
        actual_members = actual_enums[path]
        frozen_members = frozen_enums[path]
        if not is_unique_string_array(actual_members):
            errs.append(f"{schema} enum {path} invalid: not a unique string array")
            continue
        for member in sorted(set(frozen_members) - set(actual_members)):
            errs.append(
                f"{schema} enum {path} dropped frozen value {member}"
            )
        for member in sorted(set(actual_members) - set(frozen_members)):
            errs.append(
                f"{schema} enum {path} unrecorded member {member}"
            )


def actual_text_map(errs, schema, items, id_field, text_field, label):
    if not isinstance(items, list):
        errs.append(f"{schema} {label} invalid: must be an array")
        return {}
    result = {}
    for item in items:
        if (
            not isinstance(item, dict)
            or not is_nonempty_string(item.get(id_field))
            or not is_nonempty_string(item.get(text_field))
        ):
            errs.append(f"{schema} {label} invalid entry")
            continue
        item_id = item[id_field]
        if item_id in result:
            errs.append(f"{schema} {label} duplicate ID {item_id}")
            continue
        result[item_id] = item[text_field]
    return result


def compare_id_text(errs, schema, actual, frozen, label):
    for item_id in sorted(set(frozen) - set(actual)):
        errs.append(f"{schema} {label} DROPPED ID {item_id}")
    for item_id in sorted(set(actual) - set(frozen)):
        errs.append(f"{schema} unrecorded {label} ID {item_id}")
    for item_id in sorted(set(actual) & set(frozen)):
        if actual[item_id] != frozen[item_id]:
            errs.append(f"{schema} {label} {item_id} text CHANGED")


def compare_exact_members(errs, schema, label, actual, frozen):
    if not is_unique_string_array(actual):
        errs.append(f"{schema} {label} invalid: not a unique string array")
        return
    for member in sorted(set(frozen) - set(actual)):
        errs.append(f"{schema} {label} DROPPED member {member}")
    for member in sorted(set(actual) - set(frozen)):
        errs.append(f"{schema} {label} unrecorded member {member}")


def compare_constitution_content(errs, contract, frozen):
    schema = CONSTITUTION_SCHEMA
    content = frozen["content_floors"]
    rules = actual_text_map(errs, schema, contract.get("rules"), "id", "rule", "rule")
    compare_id_text(errs, schema, rules, content["rules"], "rule")
    invariants = actual_text_map(
        errs,
        schema,
        contract.get("kernel_invariants"),
        "id",
        "invariant",
        "kernel_invariant",
    )
    compare_id_text(
        errs,
        schema,
        invariants,
        content["kernel_invariants"],
        "kernel_invariant",
    )

    banned_terms = contract.get("banned_terms")
    if not isinstance(banned_terms, dict):
        errs.append(f"{schema} banned_terms invalid: must be an object")
        banned_terms = {}
    for tier, members in content["banned_terms_exact_values"].items():
        actual_members = banned_terms.get(tier)
        if not is_unique_string_array(actual_members):
            errs.append(f"{schema} banned_terms.{tier} invalid")
            continue
        for member in sorted(set(members) - set(actual_members)):
            errs.append(
                f"{schema} banned_terms.{tier} "
                f"DROPPED banned_term member {member}"
            )
        for member in sorted(set(actual_members) - set(members)):
            errs.append(
                f"{schema} banned_terms.{tier} "
                f"unrecorded banned_term member {member}"
            )
    for key, value in content["banned_terms_exact_scalars"].items():
        if banned_terms.get(key) != value:
            errs.append(f"{schema} banned_terms.{key} value CHANGED")

    optional_entries = content["banned_terms_optional_entries"]
    for key, value in optional_entries.items():
        actual_value = banned_terms.get(key)
        if not is_nonempty_string(actual_value):
            errs.append(
                f"{schema} banned_terms.optional key {key} missing from actual"
            )
        elif actual_value != value:
            errs.append(
                f"{schema} banned_terms.optional key {key} value mismatch"
            )
    known_banned_keys = (
        set(content["banned_terms_exact_values"])
        | set(content["banned_terms_exact_scalars"])
        | set(optional_entries)
        | {"note"}
    )
    for key in sorted(set(banned_terms) - known_banned_keys):
        errs.append(
            f"{schema} unrecorded banned_terms.optional key {key}"
        )

    compare_exact_members(
        errs,
        schema,
        "operator_outcomes",
        contract.get("operator_outcomes"),
        content["operator_outcomes_exact_members"],
    )


def collect_provenance(manifest, contracts):
    manifest_records = set()
    for phase, spec in manifest["deferred_phases"].items():
        if spec["kind"] != "additive":
            continue
        for schema, keys in spec["contracts"].items():
            for key in keys:
                manifest_records.add((phase, schema, key))

    declarations = []
    for schema, contract in contracts.items():
        for phase, items in contract["deferred_additions"].items():
            for declaration in items:
                declarations.append(
                    {
                        "phase": phase,
                        "schema": schema,
                        "key": declaration["key"],
                        "type": declaration["type"],
                        "target": declaration["target"],
                    }
                )
    return manifest_records, declarations


def validate_promotion_states(errs, manifest, contracts):
    manifest_records, declarations = collect_provenance(manifest, contracts)
    declarations_by_record = {}
    for declaration in declarations:
        record = (
            declaration["phase"],
            declaration["schema"],
            declaration["key"],
        )
        declarations_by_record.setdefault(record, []).append(declaration)

    for record in sorted(manifest_records):
        matches = declarations_by_record.get(record, [])
        if not matches:
            errs.append(
                "orphan manifest record "
                f"{record[0]}:{record[1]}:{record[2]}"
            )
        elif len(matches) > 1:
            errs.append(
                "ambiguous declaration "
                f"{record[0]}:{record[1]}:{record[2]}"
            )
    for record, matches in declarations_by_record.items():
        if record not in manifest_records:
            for declaration in matches:
                identity = f"{declaration['target']}.{declaration['key']}"
                errs.append(
                    "orphan declaration "
                    f"{record[0]}:{record[1]}:{identity}"
                )

    extension_records = set()
    for schema, paths in manifest["enum_extensions"].items():
        for path, members in paths.items():
            for member in members:
                extension_records.add((schema, path, member))
    enum_declarations = [
        declaration
        for declaration in declarations
        if declaration["target"].startswith("enum.")
    ]
    for schema, path, member in sorted(extension_records):
        matches = [
            declaration
            for declaration in enum_declarations
            if declaration["schema"] == schema
            and declaration["target"] == f"enum.{path}"
            and declaration["key"] == member
        ]
        if len(matches) != 1:
            errs.append(
                f"enum_extensions[{schema}][{path}] member {member} "
                "has no deferred declaration"
            )
    for declaration in enum_declarations:
        path = declaration["target"].removeprefix("enum.")
        record = (declaration["schema"], path, declaration["key"])
        if record not in extension_records:
            errs.append(
                "orphan enum declaration "
                f"{declaration['schema']}:{declaration['target']}.{declaration['key']}"
            )

    frozen_behavior = manifest["frozen_behavior"]
    for declaration in declarations:
        schema = declaration["schema"]
        contract = contracts[schema]
        frozen = frozen_behavior[schema]
        key = declaration["key"]
        target = declaration["target"]
        identity = f"{target}.{key}"

        if target == "top.optional":
            actual_map = contract.get("optional_keys")
            actual_map = actual_map if isinstance(actual_map, dict) else {}
            frozen_map = frozen["optional_keys"]
            actual_has = key in actual_map
            frozen_has = key in frozen_map
            if actual_has != frozen_has:
                errs.append(f"{schema} {identity} partial state")
            elif actual_has:
                if actual_map[key] != frozen_map[key]:
                    errs.append(f"{schema} {identity} RETYPED")
                if declaration["type"] != actual_map[key]:
                    errs.append(
                        f"{schema} {identity} declaration type mismatch"
                    )
        elif target.startswith("nested."):
            container = target[len("nested.") : -len(".optional")]
            actual_nested = contract.get("nested")
            actual_nested = actual_nested if isinstance(actual_nested, dict) else {}
            actual_spec = actual_nested.get(container, {})
            actual_map = (
                actual_spec.get("optional_keys", {})
                if isinstance(actual_spec, dict)
                else {}
            )
            frozen_spec = frozen["nested"].get(container, {})
            frozen_map = (
                frozen_spec.get("optional_keys", {})
                if isinstance(frozen_spec, dict)
                else {}
            )
            actual_has = key in actual_map
            frozen_has = key in frozen_map
            if actual_has != frozen_has:
                errs.append(f"{schema} {identity} partial state")
            elif actual_has:
                if actual_map[key] != frozen_map[key]:
                    errs.append(f"{schema} {identity} RETYPED")
                if declaration["type"] != actual_map[key]:
                    errs.append(
                        f"{schema} {identity} declaration type mismatch"
                    )
        elif target == "banned_terms.optional":
            if declaration["type"] != "note":
                errs.append(f"{schema} {identity} type must be note")
                continue
            actual_banned = contract.get("banned_terms")
            actual_banned = actual_banned if isinstance(actual_banned, dict) else {}
            content = frozen.get("content_floors") or {}
            frozen_map = content.get("banned_terms_optional_entries", {})
            actual_has = key in actual_banned
            frozen_has = key in frozen_map
            if actual_has != frozen_has:
                errs.append(f"{schema} {identity} partial state")
            elif actual_has:
                actual_value = actual_banned[key]
                frozen_value = frozen_map[key]
                if (
                    not is_nonempty_string(actual_value)
                    or not is_nonempty_string(frozen_value)
                    or actual_value != frozen_value
                ):
                    errs.append(f"{schema} {identity} value mismatch")
        elif target.startswith("enum."):
            if declaration["type"] != "enum-member":
                errs.append(f"{schema} {identity} type must be enum-member")
                continue
            path = target.removeprefix("enum.")
            actual_enums = contract.get("enums")
            actual_enums = actual_enums if isinstance(actual_enums, dict) else {}
            actual_members = actual_enums.get(path, [])
            frozen_members = frozen["enum_floors"].get(path, [])
            actual_has = isinstance(actual_members, list) and key in actual_members
            frozen_has = isinstance(frozen_members, list) and key in frozen_members
            if actual_has != frozen_has:
                errs.append(
                    f"{schema} enum {path} partial state for member {key}"
                )


errs = []
oks = []
try:
    manifest = load_json(
        contracts_dir / "additive-manifest.json",
        "manifest",
        "manifest MISSING or unreadable",
    )
    if not isinstance(manifest, dict):
        die("manifest not valid JSON")
    validate_manifest_structure(manifest)

    contracts = {}
    declared_filenames = set()
    for schema in sorted(FROZEN_SCHEMAS):
        frozen = manifest["frozen_behavior"][schema]
        filename = frozen["file"]
        declared_filenames.add(filename)
        contract = load_json(
            contracts_dir / filename,
            f"contract {schema}",
            f"contract {schema} missing file {filename}",
        )
        if not isinstance(contract, dict):
            die(f"contract {schema} not valid JSON")
        validate_deferred_declarations(schema, contract)
        contracts[schema] = contract

    for path in sorted(contracts_dir.glob("*.v1.json")):
        if path.name not in declared_filenames:
            errs.append(f"undeclared contract file: {path.name}")

    for schema in sorted(FROZEN_SCHEMAS):
        contract = contracts[schema]
        frozen = manifest["frozen_behavior"][schema]
        filename = frozen["file"]
        if contract.get("schema") != schema:
            errs.append(
                f"{schema} schema mismatch: {contract.get('schema')!r}"
            )
        if contract.get("status") != "frozen":
            errs.append(f"{schema} status must be frozen")
        if type(contract.get("version")) is not int or contract["version"] != 1:
            errs.append(f"{schema} version not 1")
        freeze_strings = contract.get("freeze_strings")
        if not isinstance(freeze_strings, list) or schema not in freeze_strings:
            errs.append(f"{schema} freeze_strings missing schema")
        if contract.get("freeze_exempt") is not False:
            errs.append(f"{schema} freeze_exempt must be false")
        if not is_nonempty_string(contract.get("frozen")):
            errs.append(f"{schema} frozen date missing or empty")

        compare_type_maps(
            errs,
            schema,
            "required_keys",
            contract.get("required_keys"),
            frozen["required_keys"],
            "required",
        )
        compare_type_maps(
            errs,
            schema,
            "optional_keys",
            contract.get("optional_keys"),
            frozen["optional_keys"],
            "optional",
        )
        compare_nested(errs, schema, contract, frozen)
        compare_enums(errs, schema, contract, frozen)
        if schema == CONSTITUTION_SCHEMA:
            compare_constitution_content(errs, contract, frozen)
        oks.append(
            f"{filename}: schema {schema} v1 frozen — complete behavior floor OK"
        )

    validate_promotion_states(errs, manifest, contracts)
except ValidationError as exc:
    print("  FAIL  " + str(exc), file=sys.stderr)
    sys.exit(1)

for line in oks:
    print("  PASS  " + line)
if errs:
    for e in errs:
        print("  FAIL  " + e, file=sys.stderr)
    sys.exit(1)
sys.exit(0)
PY
then
  pass "all five contracts satisfy the frozen behavior floor (catalog/map/feedback/constitution/proposal all frozen; proposal frozen in A0)"
else
  bad "contract freeze drift (see FAIL lines above) — a removal/rename/retype needs a v2 bump"
fi

if [ "$fail" -eq 0 ]; then
  echo "intent-contract-freeze: OK"
else
  echo "intent-contract-freeze: FAILED"
fi
exit "$fail"
