"""catalog — load + validate a consumer's `intent-catalog/v1` file. Read-only; PURE functions.

The catalog is consumer-authored and lives in the CONSUMER's source tree (ARCHITECTURE.md); the
router only ever reads it. `contracts/intent-catalog.v1.json` freezes the per-VERB required-key
floor + enum floors; this module additionally defines the CATALOG FILE wrapper shape (a list of verb
entries under a `verbs` array — the wrapper is an R-core implementation choice, not a frozen contract
field, so it stays free to evolve without touching the frozen floor) and the validator `intent
catalog-verify` runs.

`catalog-verify` must catch (R-core deliverable, each proven by an adversarial test):
  1. a bad `safety_class` (not in the frozen enum),
  2. a missing `param_schema` (the required key itself, or a malformed nested param entry),
  3. an unsafe `tool_path` (not in the frozen enum — a consumer cannot declare an escape hatch),
  4. leaked host-policy literals — a Tier A/B/C banned term (CONSTITUTION.md banned_terms; the same
     shared tiers the future `egress` phase composes) inside the PM-facing `plain_label` /
     `consequence_copy` fields. Catalog schema carries those two fields precisely so this is a
     schema-validation failure, not luck (ARCHITECTURE.md "System-wide operator egress gate").

Scope note: this is a catalog-scoped STRUCTURAL pre-check, not the full CR10 egress gate (that is a
behavioral test over all seven PM-facing surfaces, deferred to the `egress` phase — see
`tests/test_deferred_spec.py::test_spec_egress_zero_banned_terms`). It reuses the SAME shared
banned-term tiers so the two checks can never define "leak" differently.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

SCHEMA = "intent-catalog/v1"

_REPO_ROOT = Path(__file__).resolve().parent.parent
_CONTRACTS_DIR = _REPO_ROOT / "contracts"

# Mirrors contracts/intent-catalog.v1.json required_keys (the frozen per-verb floor). Kept as a
# plain dict (not imported from the JSON) so this module has no import-time file dependency beyond
# the banned-terms lookup; test_contract_freeze.py is the single source of truth for the frozen
# floor itself, this is just the validator's working copy of the SAME names.
REQUIRED_VERB_KEYS = (
    "verb", "aliases", "examples", "param_schema", "preconditions",
    "safety_class", "tool_path", "start_point_rules", "plain_label", "consequence_copy",
)
REQUIRED_PARAM_KEYS = ("name", "type", "required")
SAFETY_CLASS_ENUM = ("read", "write", "destructive")
TOOL_PATH_ENUM = ("cli", "mcp", "hook")
PARAM_TYPE_ENUM = ("string", "int", "number", "bool", "enum", "path", "ref")
PARAM_SOURCE_ENUM = ("literal", "regex", "enum", "repo-resolver", "llm")

# PM-facing fields scanned for banned-term leaks (ARCHITECTURE.md: these two fields exist precisely
# so a leak is a schema-validation failure). `aliases`/`examples` are the utterance-matching
# training corpus, not PM-rendered text, and are intentionally out of this check's scope.
_EGRESS_SCANNED_FIELDS = ("plain_label", "consequence_copy")


def load_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


_banned_terms_cache: frozenset | None = None
_pattern_cache: dict[str, re.Pattern] = {}


def _load_banned_terms() -> frozenset:
    """Shared Tier A + Tier B (universal) + every consumer's contributed Tier C, composed from the
    two P0-frozen/pinned reference sources — the SAME composition the future egress-phase test
    (CR10) uses, so 'leak' is defined once. Cached (the JSON files are read-only, in-repo)."""
    global _banned_terms_cache
    if _banned_terms_cache is not None:
        return _banned_terms_cache
    terms: set[str] = set()
    constitution = load_json(_CONTRACTS_DIR / "intent-constitution.v1.json")
    bt = constitution.get("banned_terms", {})
    terms.update(bt.get("tier_a_generic_mechanism", []))
    terms.update(bt.get("tier_b_git_workflow", []))
    checklist_path = _CONTRACTS_DIR / "egress-terms.checklist.json"
    if checklist_path.exists():
        checklist = load_json(checklist_path)
        terms.update(checklist.get("tier_a_mechanism", []))
        terms.update(checklist.get("tier_b_git_workflow", []))
        for key, lst in checklist.get("tier_c_consumer_concrete", {}).items():
            if key == "note":
                continue
            if isinstance(lst, list):
                terms.update(lst)
    _banned_terms_cache = frozenset(terms)
    return _banned_terms_cache


def _pattern_for(term: str) -> re.Pattern:
    """Word-boundary-anchor a term on whichever side starts/ends alphanumeric; a term like
    `--bundle` cannot take a leading `\\b` (both sides of `-` are non-word), so that side is left
    unanchored — the term is distinctive enough on its own."""
    cached = _pattern_cache.get(term)
    if cached is not None:
        return cached
    left = r"\b" if term[:1].isalnum() else ""
    right = r"\b" if term[-1:].isalnum() else ""
    pat = re.compile(left + re.escape(term) + right)
    _pattern_cache[term] = pat
    return pat


def find_banned_terms(text: str, banned_terms: frozenset | None = None) -> list[str]:
    """Return the banned terms literally present in `text` (sorted, deduped). Case-SENSITIVE,
    word/phrase-bounded matching: precise over exhaustive, since common tokens like `HEAD` or `PR`
    would otherwise collide constantly with ordinary English if matched case-insensitively. The
    behavioral, exhaustive egress gate lands at the `egress` phase; this is a structural pre-check."""
    if not text:
        return []
    terms = banned_terms if banned_terms is not None else _load_banned_terms()
    hits = {term for term in terms if _pattern_for(term).search(text)}
    return sorted(hits)


def _type_name(value: Any) -> str:
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "number"
    if value is None:
        return "null"
    return type(value).__name__


def validate_verb_entry(entry: Any, idx: int) -> list[str]:
    """Validate one verb entry against the frozen `intent-catalog/v1` per-verb floor. Returns a list
    of human-readable error strings (empty = valid)."""
    errors: list[str] = []
    if not isinstance(entry, dict):
        return [f"verb[{idx}]: entry is not an object (got {_type_name(entry)})"]

    label = entry.get("verb", f"<unnamed idx={idx}>")

    missing = [k for k in REQUIRED_VERB_KEYS if k not in entry]
    if missing:
        errors.append(f"verb[{idx}] ({label}): missing required key(s) {sorted(missing)}")

    # 1. bad safety_class
    if "safety_class" in entry:
        sc = entry.get("safety_class")
        if sc not in SAFETY_CLASS_ENUM:
            errors.append(
                f"verb[{idx}] ({label}): bad safety_class {sc!r} — must be one of {SAFETY_CLASS_ENUM}"
            )

    # 3. unsafe tool_path (checked before param_schema so both can be reported independently)
    if "tool_path" in entry:
        tp = entry.get("tool_path")
        if tp not in TOOL_PATH_ENUM:
            errors.append(
                f"verb[{idx}] ({label}): unsafe tool_path {tp!r} — must be one of {TOOL_PATH_ENUM} "
                f"(no consumer-declared execution surface outside this allowlist)"
            )

    # 2. missing / malformed param_schema
    if "param_schema" in entry:
        ps = entry.get("param_schema")
        if not isinstance(ps, list):
            errors.append(f"verb[{idx}] ({label}): param_schema must be an array (got {_type_name(ps)})")
        else:
            for pidx, p in enumerate(ps):
                if not isinstance(p, dict):
                    errors.append(f"verb[{idx}] ({label}).param_schema[{pidx}]: not an object")
                    continue
                pmissing = [k for k in REQUIRED_PARAM_KEYS if k not in p]
                if pmissing:
                    errors.append(
                        f"verb[{idx}] ({label}).param_schema[{pidx}]: missing required key(s) "
                        f"{sorted(pmissing)}"
                    )
                ptype = p.get("type")
                if "type" in p and ptype not in PARAM_TYPE_ENUM:
                    errors.append(
                        f"verb[{idx}] ({label}).param_schema[{pidx}]: bad type {ptype!r} — must be "
                        f"one of {PARAM_TYPE_ENUM}"
                    )
                if "required" in p and not isinstance(p.get("required"), bool):
                    errors.append(
                        f"verb[{idx}] ({label}).param_schema[{pidx}]: 'required' must be a bool"
                    )
                psource = p.get("source")
                if "source" in p and psource not in PARAM_SOURCE_ENUM:
                    errors.append(
                        f"verb[{idx}] ({label}).param_schema[{pidx}]: bad source {psource!r} — must "
                        f"be one of {PARAM_SOURCE_ENUM}"
                    )
    # (else: absence already reported by the missing-required-key check above, which names
    # 'param_schema' explicitly — deliverable class 2.)

    # 4. leaked host-policy literals in the PM-facing fields
    banned = _load_banned_terms()
    for field in _EGRESS_SCANNED_FIELDS:
        val = entry.get(field)
        if not isinstance(val, str):
            continue
        hits = find_banned_terms(val, banned)
        if hits:
            errors.append(
                f"verb[{idx}] ({label}).{field}: leaked host-policy literal(s) {hits} — PM-facing "
                f"copy must be jargon-free (banned_terms tiers A/B/C)"
            )

    # Shape checks on other required-but-not-yet-covered keys (aliases/examples/preconditions must
    # be arrays; start_point_rules must be an object) — additional, low-noise hygiene.
    for arr_key in ("aliases", "examples", "preconditions"):
        if arr_key in entry and not isinstance(entry.get(arr_key), list):
            errors.append(f"verb[{idx}] ({label}): '{arr_key}' must be an array")
    if "start_point_rules" in entry and not isinstance(entry.get("start_point_rules"), dict):
        errors.append(f"verb[{idx}] ({label}): 'start_point_rules' must be an object")
    for str_key in ("verb", "plain_label", "consequence_copy"):
        if str_key in entry and not isinstance(entry.get(str_key), str):
            errors.append(f"verb[{idx}] ({label}): '{str_key}' must be a string")

    return errors


def validate_catalog(data: Any) -> list[str]:
    """Validate a full catalog file (the `{"schema": ..., "verbs": [...]}` wrapper). Returns a list
    of human-readable error strings (empty = valid). Never raises on malformed input — a catalog
    that fails to parse as the expected shape is reported as errors, not an exception."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return [f"catalog root must be an object (got {_type_name(data)})"]

    schema = data.get("schema")
    if schema != SCHEMA:
        errors.append(f"catalog schema={schema!r} != {SCHEMA!r}")

    verbs = data.get("verbs")
    if not isinstance(verbs, list):
        errors.append("catalog 'verbs' must be an array")
        verbs = []
    elif not verbs:
        errors.append("catalog 'verbs' is empty — a catalog must declare at least one verb")

    seen_names: dict[str, int] = {}
    for idx, entry in enumerate(verbs):
        errors.extend(validate_verb_entry(entry, idx))
        if isinstance(entry, dict):
            name = entry.get("verb")
            if isinstance(name, str) and name:
                if name in seen_names:
                    errors.append(f"verb[{idx}]: duplicate verb name {name!r} (first seen at "
                                  f"verb[{seen_names[name]}])")
                else:
                    seen_names[name] = idx
    return errors


def find_verb(verbs: list, verb_name: str) -> dict | None:
    """Look up one verb entry by name. Pure; returns None on no-match or malformed input. Used by
    L5 (`proposal.py`) to re-attach the full catalog entry (`safety_class`/`tool_path`/
    `param_schema`/`start_point_rules`) to L1's winning candidate — L1 itself never reads those
    safety-relevant fields (`candidates.py` docstring), so something downstream must."""
    if not verb_name:
        return None
    for entry in verbs or []:
        if isinstance(entry, dict) and entry.get("verb") == verb_name:
            return entry
    return None


def load_catalog(path: Path) -> dict:
    return load_json(path)


def verify_catalog_file(path: Path) -> tuple[bool, list[str]]:
    """Load + validate a catalog file. Returns (ok, errors). Never raises: a JSON-parse failure is
    itself reported as a validation error (read-only, executionless — a hostile/malformed catalog
    file can only produce error strings, never code execution)."""
    p = Path(path)
    if not p.exists():
        return False, [f"catalog file not found: {p}"]
    try:
        data = load_json(p)
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as exc:
        return False, [f"catalog file is not valid JSON: {exc}"]
    errors = validate_catalog(data)
    return (len(errors) == 0, errors)
