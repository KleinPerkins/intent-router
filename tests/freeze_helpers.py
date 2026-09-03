"""Pure validation helpers for coherent temporary contract bundles."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

FROZEN_SCHEMAS = {
    "intent-catalog/v1",
    "intent-map/v1",
    "intent-feedback/v1",
    "intent-constitution/v1",
    "intent-proposal/v1",
}
CONSTITUTION_SCHEMA = "intent-constitution/v1"
_CONTENT_KEYS = {
    "rules",
    "kernel_invariants",
    "banned_terms_exact_values",
    "banned_terms_exact_scalars",
    "banned_terms_optional_entries",
    "operator_outcomes_exact_members",
}


class _ValidationError(Exception):
    pass


class _DuplicateKeyError(ValueError):
    def __init__(self, key: str):
        super().__init__(key)
        self.key = key


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKeyError(key)
        result[key] = value
    return result


def _load_json(path: Path, label: str, missing_message: str) -> dict[str, Any]:
    if not path.is_file() or not os.access(path, os.R_OK):
        raise _ValidationError(missing_message)
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
        )
    except _DuplicateKeyError as exc:
        raise _ValidationError(f"{label} duplicate key {exc.key}") from exc
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise _ValidationError(f"{label} not valid JSON") from exc
    if not isinstance(value, dict):
        raise _ValidationError(f"{label} not valid JSON")
    return value


def _is_nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value)


def _is_unique_string_array(value: object, *, require_nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (not require_nonempty or bool(value))
        and all(_is_nonempty_string(member) for member in value)
        and len(value) == len(set(value))
    )


def _require_type_map(value: object, diagnostic: str) -> None:
    if (
        not isinstance(value, dict)
        or any(not _is_nonempty_string(key) for key in value)
        or any(not _is_nonempty_string(item) for item in value.values())
    ):
        raise _ValidationError(diagnostic)


def _require_string_arrays(value: object, diagnostic: str) -> None:
    if (
        not isinstance(value, dict)
        or any(not _is_nonempty_string(key) for key in value)
        or any(not _is_unique_string_array(items) for items in value.values())
    ):
        raise _ValidationError(diagnostic)


def _supported_target(target: str) -> bool:
    if target in {"top.optional", "banned_terms.optional"}:
        return True
    if target.startswith("enum."):
        return _is_nonempty_string(target.removeprefix("enum."))
    if target.startswith("nested.") and target.endswith(".optional"):
        container = target[len("nested.") : -len(".optional")]
        return _is_nonempty_string(container) and "." not in container
    return False


def _validate_content_floors(content: object) -> None:
    if not isinstance(content, dict) or set(content) != _CONTENT_KEYS:
        raise _ValidationError(
            f"frozen_behavior[{CONSTITUTION_SCHEMA}].content_floors invalid"
        )
    _require_type_map(content["rules"], "content_floors.rules invalid")
    _require_type_map(
        content["kernel_invariants"],
        "content_floors.kernel_invariants invalid",
    )
    _require_string_arrays(
        content["banned_terms_exact_values"],
        "content_floors.banned_terms_exact_values invalid",
    )
    _require_type_map(
        content["banned_terms_exact_scalars"],
        "content_floors.banned_terms_exact_scalars invalid",
    )
    _require_type_map(
        content["banned_terms_optional_entries"],
        "content_floors.banned_terms_optional_entries invalid",
    )
    if not _is_unique_string_array(content["operator_outcomes_exact_members"]):
        raise _ValidationError(
            "content_floors.operator_outcomes_exact_members invalid"
        )


def _validate_manifest_structure(
    manifest: dict[str, Any], contracts_root: Path
) -> None:
    if manifest.get("schema") != "intent-additive-manifest/v1":
        raise _ValidationError(
            "manifest schema header invalid: expected intent-additive-manifest/v1"
        )
    if type(manifest.get("version")) is not int or manifest["version"] != 1:
        raise _ValidationError("manifest version header invalid: expected integer 1")

    frozen_behavior = manifest.get("frozen_behavior")
    if not isinstance(frozen_behavior, dict):
        raise _ValidationError("frozen_behavior missing or not an object")
    enum_extensions = manifest.get("enum_extensions")
    if not isinstance(enum_extensions, dict):
        raise _ValidationError("enum_extensions missing or not an object")

    missing = sorted(FROZEN_SCHEMAS - set(frozen_behavior))
    extra = sorted(set(frozen_behavior) - FROZEN_SCHEMAS)
    if missing:
        raise _ValidationError(f"frozen_behavior missing schema {missing[0]}")
    if extra:
        raise _ValidationError(f"frozen_behavior unexpected schema {extra[0]}")

    filenames: list[str] = []
    root = contracts_root.resolve()
    for schema in sorted(FROZEN_SCHEMAS):
        entry = frozen_behavior[schema]
        if not isinstance(entry, dict):
            raise _ValidationError(f"frozen_behavior[{schema}] invalid")
        filename = entry.get("file")
        unsafe = (
            not _is_nonempty_string(filename)
            or "/" in filename
            or "\\" in filename
            or Path(filename).name != filename
            or not filename.endswith(".v1.json")
        )
        if not unsafe:
            candidate = (contracts_root / filename).resolve()
            unsafe = candidate.parent != root
        if unsafe:
            raise _ValidationError(
                f"frozen_behavior[{schema}].file unsafe: {filename}"
            )
        filenames.append(filename)

        if entry.get("status") != "frozen":
            raise _ValidationError(
                f"frozen_behavior[{schema}].status invalid: expected frozen"
            )
        if "required_keys" not in entry:
            raise _ValidationError(
                f"frozen_behavior[{schema}].required_keys invalid"
            )
        _require_type_map(
            entry["required_keys"],
            f"frozen_behavior[{schema}].required_keys invalid",
        )
        if "optional_keys" not in entry:
            raise _ValidationError(
                f"frozen_behavior[{schema}].optional_keys invalid"
            )
        _require_type_map(
            entry["optional_keys"],
            f"frozen_behavior[{schema}].optional_keys invalid",
        )

        nested = entry.get("nested")
        if not isinstance(nested, dict):
            raise _ValidationError(f"frozen_behavior[{schema}].nested invalid")
        for container, spec in nested.items():
            diagnostic = f"frozen_behavior[{schema}].nested[{container}] invalid"
            if (
                not _is_nonempty_string(container)
                or not isinstance(spec, dict)
                or "required_keys" not in spec
                or "optional_keys" not in spec
            ):
                raise _ValidationError(diagnostic)
            _require_type_map(spec["required_keys"], diagnostic)
            _require_type_map(spec["optional_keys"], diagnostic)

        enum_floors = entry.get("enum_floors")
        if not isinstance(enum_floors, dict):
            raise _ValidationError(
                f"frozen_behavior[{schema}].enum_floors invalid"
            )
        for path, members in enum_floors.items():
            if not _is_nonempty_string(path) or not _is_unique_string_array(members):
                raise _ValidationError(
                    f"frozen_behavior[{schema}].enum_floors[{path}] invalid"
                )

        if "content_floors" not in entry:
            raise _ValidationError(
                f"frozen_behavior[{schema}].content_floors invalid"
            )
        content = entry["content_floors"]
        if schema == CONSTITUTION_SCHEMA:
            _validate_content_floors(content)
        elif content is not None:
            raise _ValidationError(
                f"frozen_behavior[{schema}].content_floors invalid"
            )

    duplicates = sorted(
        filename for filename in set(filenames) if filenames.count(filename) > 1
    )
    if duplicates:
        raise _ValidationError(
            f"frozen_behavior duplicate filename {duplicates[0]}"
        )

    enum_missing = sorted(FROZEN_SCHEMAS - set(enum_extensions))
    enum_extra = sorted(set(enum_extensions) - FROZEN_SCHEMAS)
    if enum_missing:
        raise _ValidationError(f"enum_extensions missing schema {enum_missing[0]}")
    if enum_extra:
        raise _ValidationError(
            f"enum_extensions unexpected schema {enum_extra[0]}"
        )
    for schema in sorted(FROZEN_SCHEMAS):
        paths = enum_extensions[schema]
        if not isinstance(paths, dict):
            raise _ValidationError(f"enum_extensions[{schema}] not an object")
        for path, members in paths.items():
            if not _is_nonempty_string(path) or not _is_unique_string_array(members):
                raise _ValidationError(
                    f"enum_extensions[{schema}][{path}] "
                    "not a unique string array"
                )

    required_phases = manifest.get("required_additive_phases")
    if not _is_unique_string_array(required_phases):
        raise _ValidationError("required_additive_phases invalid")
    phases = manifest.get("deferred_phases")
    if not isinstance(phases, dict):
        raise _ValidationError("deferred_phases invalid")
    for phase, spec in phases.items():
        if not _is_nonempty_string(phase) or not isinstance(spec, dict):
            raise _ValidationError(f"deferred_phases[{phase}] invalid")
        kind = spec.get("kind")
        if kind not in {"additive", "no-schema-change"}:
            raise _ValidationError(f"deferred_phases[{phase}].kind invalid")
        if kind == "additive":
            records = spec.get("contracts")
            if not isinstance(records, dict) or not records:
                raise _ValidationError(
                    f"deferred_phases[{phase}].contracts invalid"
                )
            for schema, keys in records.items():
                if (
                    schema not in FROZEN_SCHEMAS
                    or not _is_unique_string_array(keys, require_nonempty=True)
                ):
                    raise _ValidationError(
                        f"deferred_phases[{phase}].contracts[{schema}] invalid"
                    )
        elif not _is_nonempty_string(spec.get("reason")):
            raise _ValidationError(f"deferred_phases[{phase}].reason invalid")
    for phase in required_phases:
        if phase not in phases:
            raise _ValidationError(
                f"required phase {phase} missing from deferred_phases"
            )


def _validate_deferred_declarations(
    schema: str, contract: dict[str, Any]
) -> None:
    additions = contract.get("deferred_additions")
    if not isinstance(additions, dict):
        raise _ValidationError(
            f"contract {schema} deferred declaration invalid: not an object"
        )
    for phase, declarations in additions.items():
        if not _is_nonempty_string(phase) or not isinstance(declarations, list):
            raise _ValidationError(
                f"contract {schema} deferred declaration invalid: "
                f"phase {phase} must be an array"
            )
        for declaration in declarations:
            if not isinstance(declaration, dict):
                raise _ValidationError(
                    f"contract {schema} deferred declaration invalid: not an object"
                )
            for field in ("key", "type", "target"):
                if not _is_nonempty_string(declaration.get(field)):
                    raise _ValidationError(
                        f"contract {schema} deferred declaration invalid: "
                        f"{field} missing or empty"
                    )
            if not _supported_target(declaration["target"]):
                raise _ValidationError(
                    f"contract {schema} deferred declaration invalid: "
                    f"unsupported target {declaration['target']}"
                )


def _compare_type_maps(
    errors: list[str],
    schema: str,
    path: str,
    actual: object,
    frozen: dict[str, str],
    field_kind: str,
) -> None:
    if not isinstance(actual, dict):
        errors.append(f"{schema} {path} invalid: must be an object")
        actual = {}
    for key in sorted(set(frozen) - set(actual)):
        suffix = " frozen optional" if field_kind == "optional" else " frozen required"
        errors.append(f"{schema} {path}.{key} DROPPED{suffix}")
    for key in sorted(set(actual) - set(frozen)):
        suffix = (
            " unrecorded optional" if field_kind == "optional" else " unrecorded required"
        )
        errors.append(f"{schema} {path}.{key} ADD{suffix}")
    for key in sorted(set(actual) & set(frozen)):
        if actual[key] != frozen[key]:
            errors.append(
                f"{schema} {path}.{key} RETYPED "
                f"{actual[key]!r} != frozen {frozen[key]!r}"
            )


def _compare_nested(
    errors: list[str],
    schema: str,
    contract: dict[str, Any],
    frozen: dict[str, Any],
) -> None:
    actual_nested = contract.get("nested")
    if not isinstance(actual_nested, dict):
        errors.append(f"{schema} nested invalid: must be an object")
        actual_nested = {}
    frozen_nested = frozen["nested"]
    for container in sorted(set(frozen_nested) - set(actual_nested)):
        errors.append(f"{schema} nested.{container} DROPPED frozen container")
    for container in sorted(set(actual_nested) - set(frozen_nested)):
        errors.append(f"{schema} nested.{container} ADD unrecorded container")
    for container in sorted(set(actual_nested) & set(frozen_nested)):
        actual_spec = actual_nested[container]
        if not isinstance(actual_spec, dict):
            errors.append(f"{schema} nested.{container} invalid: must be an object")
            actual_spec = {}
        frozen_spec = frozen_nested[container]
        _compare_type_maps(
            errors,
            schema,
            f"nested.{container}.required_keys",
            actual_spec.get("required_keys"),
            frozen_spec["required_keys"],
            "required",
        )
        _compare_type_maps(
            errors,
            schema,
            f"nested.{container}.optional_keys",
            actual_spec.get("optional_keys"),
            frozen_spec["optional_keys"],
            "optional",
        )


def _compare_enums(
    errors: list[str],
    schema: str,
    contract: dict[str, Any],
    frozen: dict[str, Any],
) -> None:
    actual_enums = contract.get("enums")
    if not isinstance(actual_enums, dict):
        errors.append(f"{schema} enums invalid: must be an object")
        actual_enums = {}
    frozen_enums = frozen["enum_floors"]
    for path in sorted(set(frozen_enums) - set(actual_enums)):
        errors.append(f"{schema} enum {path} DROPPED frozen path")
    for path in sorted(set(actual_enums) - set(frozen_enums)):
        errors.append(f"{schema} enum {path} ADD unrecorded path")
    for path in sorted(set(actual_enums) & set(frozen_enums)):
        actual_members = actual_enums[path]
        frozen_members = frozen_enums[path]
        if not _is_unique_string_array(actual_members):
            errors.append(f"{schema} enum {path} invalid: not a unique string array")
            continue
        for member in sorted(set(frozen_members) - set(actual_members)):
            errors.append(f"{schema} enum {path} dropped frozen value {member}")
        for member in sorted(set(actual_members) - set(frozen_members)):
            errors.append(f"{schema} enum {path} unrecorded member {member}")


def _actual_text_map(
    errors: list[str],
    schema: str,
    items: object,
    id_field: str,
    text_field: str,
    label: str,
) -> dict[str, str]:
    if not isinstance(items, list):
        errors.append(f"{schema} {label} invalid: must be an array")
        return {}
    result: dict[str, str] = {}
    for item in items:
        if (
            not isinstance(item, dict)
            or not _is_nonempty_string(item.get(id_field))
            or not _is_nonempty_string(item.get(text_field))
        ):
            errors.append(f"{schema} {label} invalid entry")
            continue
        item_id = item[id_field]
        if item_id in result:
            errors.append(f"{schema} {label} duplicate ID {item_id}")
            continue
        result[item_id] = item[text_field]
    return result


def _compare_id_text(
    errors: list[str],
    schema: str,
    actual: dict[str, str],
    frozen: dict[str, str],
    label: str,
) -> None:
    for item_id in sorted(set(frozen) - set(actual)):
        errors.append(f"{schema} {label} DROPPED ID {item_id}")
    for item_id in sorted(set(actual) - set(frozen)):
        errors.append(f"{schema} unrecorded {label} ID {item_id}")
    for item_id in sorted(set(actual) & set(frozen)):
        if actual[item_id] != frozen[item_id]:
            errors.append(f"{schema} {label} {item_id} text CHANGED")


def _compare_constitution_content(
    errors: list[str], contract: dict[str, Any], frozen: dict[str, Any]
) -> None:
    schema = CONSTITUTION_SCHEMA
    content = frozen["content_floors"]
    rules = _actual_text_map(
        errors, schema, contract.get("rules"), "id", "rule", "rule"
    )
    _compare_id_text(errors, schema, rules, content["rules"], "rule")
    invariants = _actual_text_map(
        errors,
        schema,
        contract.get("kernel_invariants"),
        "id",
        "invariant",
        "kernel_invariant",
    )
    _compare_id_text(
        errors,
        schema,
        invariants,
        content["kernel_invariants"],
        "kernel_invariant",
    )

    banned_terms = contract.get("banned_terms")
    if not isinstance(banned_terms, dict):
        errors.append(f"{schema} banned_terms invalid: must be an object")
        banned_terms = {}
    for tier, members in content["banned_terms_exact_values"].items():
        actual_members = banned_terms.get(tier)
        if not _is_unique_string_array(actual_members):
            errors.append(f"{schema} banned_terms.{tier} invalid")
            continue
        for member in sorted(set(members) - set(actual_members)):
            errors.append(
                f"{schema} banned_terms.{tier} DROPPED banned_term member {member}"
            )
        for member in sorted(set(actual_members) - set(members)):
            errors.append(
                f"{schema} banned_terms.{tier} "
                f"unrecorded banned_term member {member}"
            )
    for key, value in content["banned_terms_exact_scalars"].items():
        if banned_terms.get(key) != value:
            errors.append(f"{schema} banned_terms.{key} value CHANGED")

    optional_entries = content["banned_terms_optional_entries"]
    for key, value in optional_entries.items():
        actual_value = banned_terms.get(key)
        if not _is_nonempty_string(actual_value):
            errors.append(
                f"{schema} banned_terms.optional key {key} missing from actual"
            )
        elif actual_value != value:
            errors.append(
                f"{schema} banned_terms.optional key {key} value mismatch"
            )
    known_keys = (
        set(content["banned_terms_exact_values"])
        | set(content["banned_terms_exact_scalars"])
        | set(optional_entries)
        | {"note"}
    )
    for key in sorted(set(banned_terms) - known_keys):
        errors.append(f"{schema} unrecorded banned_terms.optional key {key}")

    outcomes = contract.get("operator_outcomes")
    frozen_outcomes = content["operator_outcomes_exact_members"]
    if not _is_unique_string_array(outcomes):
        errors.append(
            f"{schema} operator_outcomes invalid: not a unique string array"
        )
    else:
        for member in sorted(set(frozen_outcomes) - set(outcomes)):
            errors.append(f"{schema} operator_outcomes DROPPED member {member}")
        for member in sorted(set(outcomes) - set(frozen_outcomes)):
            errors.append(f"{schema} operator_outcomes unrecorded member {member}")


def _collect_provenance(
    manifest: dict[str, Any], contracts: dict[str, dict[str, Any]]
) -> tuple[set[tuple[str, str, str]], list[dict[str, str]]]:
    manifest_records: set[tuple[str, str, str]] = set()
    for phase, spec in manifest["deferred_phases"].items():
        if spec["kind"] != "additive":
            continue
        for schema, keys in spec["contracts"].items():
            for key in keys:
                manifest_records.add((phase, schema, key))

    declarations: list[dict[str, str]] = []
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


def _validate_promotion_states(
    errors: list[str],
    manifest: dict[str, Any],
    contracts: dict[str, dict[str, Any]],
) -> None:
    manifest_records, declarations = _collect_provenance(manifest, contracts)
    declarations_by_record: dict[
        tuple[str, str, str], list[dict[str, str]]
    ] = {}
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
            errors.append(
                f"orphan manifest record {record[0]}:{record[1]}:{record[2]}"
            )
        elif len(matches) > 1:
            errors.append(
                f"ambiguous declaration {record[0]}:{record[1]}:{record[2]}"
            )
    for record, matches in declarations_by_record.items():
        if record not in manifest_records:
            for declaration in matches:
                identity = f"{declaration['target']}.{declaration['key']}"
                errors.append(
                    f"orphan declaration {record[0]}:{record[1]}:{identity}"
                )

    extension_records: set[tuple[str, str, str]] = set()
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
            errors.append(
                f"enum_extensions[{schema}][{path}] member {member} "
                "has no deferred declaration"
            )
    for declaration in enum_declarations:
        path = declaration["target"].removeprefix("enum.")
        record = (declaration["schema"], path, declaration["key"])
        if record not in extension_records:
            errors.append(
                "orphan enum declaration "
                f"{declaration['schema']}:{declaration['target']}."
                f"{declaration['key']}"
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
                errors.append(f"{schema} {identity} partial state")
            elif actual_has:
                if actual_map[key] != frozen_map[key]:
                    errors.append(f"{schema} {identity} RETYPED")
                if declaration["type"] != actual_map[key]:
                    errors.append(
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
                errors.append(f"{schema} {identity} partial state")
            elif actual_has:
                if actual_map[key] != frozen_map[key]:
                    errors.append(f"{schema} {identity} RETYPED")
                if declaration["type"] != actual_map[key]:
                    errors.append(
                        f"{schema} {identity} declaration type mismatch"
                    )
        elif target == "banned_terms.optional":
            if declaration["type"] != "note":
                errors.append(f"{schema} {identity} type must be note")
                continue
            actual_banned = contract.get("banned_terms")
            actual_banned = actual_banned if isinstance(actual_banned, dict) else {}
            content = frozen.get("content_floors") or {}
            frozen_map = content.get("banned_terms_optional_entries", {})
            actual_has = key in actual_banned
            frozen_has = key in frozen_map
            if actual_has != frozen_has:
                errors.append(f"{schema} {identity} partial state")
            elif actual_has:
                actual_value = actual_banned[key]
                frozen_value = frozen_map[key]
                if (
                    not _is_nonempty_string(actual_value)
                    or not _is_nonempty_string(frozen_value)
                    or actual_value != frozen_value
                ):
                    errors.append(f"{schema} {identity} value mismatch")
        elif target.startswith("enum."):
            if declaration["type"] != "enum-member":
                errors.append(f"{schema} {identity} type must be enum-member")
                continue
            path = target.removeprefix("enum.")
            actual_enums = contract.get("enums")
            actual_enums = actual_enums if isinstance(actual_enums, dict) else {}
            actual_members = actual_enums.get(path, [])
            frozen_members = frozen["enum_floors"].get(path, [])
            actual_has = isinstance(actual_members, list) and key in actual_members
            frozen_has = isinstance(frozen_members, list) and key in frozen_members
            if actual_has != frozen_has:
                errors.append(
                    f"{schema} enum {path} partial state for member {key}"
                )


def validate_additive_bundle(contracts_root: Path) -> list[str]:
    """Return every frozen-bundle validation error; an empty list means valid."""

    errors: list[str] = []
    contracts_root = Path(contracts_root)
    try:
        manifest = _load_json(
            contracts_root / "additive-manifest.json",
            "manifest",
            "manifest MISSING or unreadable",
        )
        _validate_manifest_structure(manifest, contracts_root)

        contracts: dict[str, dict[str, Any]] = {}
        declared_filenames: set[str] = set()
        for schema in sorted(FROZEN_SCHEMAS):
            frozen = manifest["frozen_behavior"][schema]
            filename = frozen["file"]
            declared_filenames.add(filename)
            contract = _load_json(
                contracts_root / filename,
                f"contract {schema}",
                f"contract {schema} missing file {filename}",
            )
            _validate_deferred_declarations(schema, contract)
            contracts[schema] = contract

        for path in sorted(contracts_root.glob("*.v1.json")):
            if path.name not in declared_filenames:
                errors.append(f"undeclared contract file: {path.name}")

        for schema in sorted(FROZEN_SCHEMAS):
            contract = contracts[schema]
            frozen = manifest["frozen_behavior"][schema]
            if contract.get("schema") != schema:
                errors.append(
                    f"{schema} schema mismatch: {contract.get('schema')!r}"
                )
            if contract.get("status") != "frozen":
                errors.append(f"{schema} status must be frozen")
            if type(contract.get("version")) is not int or contract["version"] != 1:
                errors.append(f"{schema} version not 1")
            freeze_strings = contract.get("freeze_strings")
            if not isinstance(freeze_strings, list) or schema not in freeze_strings:
                errors.append(f"{schema} freeze_strings missing schema")
            if contract.get("freeze_exempt") is not False:
                errors.append(f"{schema} freeze_exempt must be false")
            if not _is_nonempty_string(contract.get("frozen")):
                errors.append(f"{schema} frozen date missing or empty")

            _compare_type_maps(
                errors,
                schema,
                "required_keys",
                contract.get("required_keys"),
                frozen["required_keys"],
                "required",
            )
            _compare_type_maps(
                errors,
                schema,
                "optional_keys",
                contract.get("optional_keys"),
                frozen["optional_keys"],
                "optional",
            )
            _compare_nested(errors, schema, contract, frozen)
            _compare_enums(errors, schema, contract, frozen)
            if schema == CONSTITUTION_SCHEMA:
                _compare_constitution_content(errors, contract, frozen)

        _validate_promotion_states(errors, manifest, contracts)
    except _ValidationError as exc:
        errors.append(str(exc))
    return errors
