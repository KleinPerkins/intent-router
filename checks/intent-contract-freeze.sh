#!/usr/bin/env bash
# intent-contract-freeze.sh — assert the versioned intent-router contracts still satisfy their
# FROZEN behavior floor (contracts/*.v1.json). Read-only. Mirrors AWA's awa-contract-freeze.sh
# pattern: freeze strings + required-key floors, additive-within-v1.
#
# The contracts freeze BEHAVIOR (the schema string + the required-key floor + the enum floors).
# A removal/rename/retype of a required key, or a changed schema string, is a breaking change that
# requires a versioned bump (intent-<name>.v2.json). Additive OPTIONAL keys / enum extensions are
# allowed WITHIN v1 (proven by tests/test_additive_compat.py).
#
# FREEZE TIMING (obey exactly):
#   FROZEN in P0 (freeze-locked): intent-catalog/v1, intent-map/v1, intent-feedback/v1,
#     intent-constitution/v1.
#   PROVISIONAL (freeze DEFERRED to A0, exempt from the freeze-lock): intent-proposal/v1 — highest
#     re-architecture risk; freezing before A0 exercises a real fixture would likely force a v2.
#
# Role-resolved: finds contracts/ relative to this script (INTENT_HOME), never a hardcoded path.
set -uo pipefail

SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"   # checks/
INTENT_HOME="${INTENT_HOME:-$(cd "$SELF_DIR/.." && pwd)}"      # repo/install root (role-resolved)
CONTRACTS="$INTENT_HOME/contracts"

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

# name -> (filename, expected_status). Freeze timing is LOCKED here.
EXPECTED = {
    "intent-catalog/v1":      ("intent-catalog.v1.json",      "frozen"),
    "intent-map/v1":          ("intent-map.v1.json",          "frozen"),
    "intent-feedback/v1":     ("intent-feedback.v1.json",     "frozen"),
    "intent-constitution/v1": ("intent-constitution.v1.json", "frozen"),
    "intent-proposal/v1":     ("intent-proposal.v1.json",     "provisional"),
}

# The required-key FLOOR each contract must declare (the frozen interface). A drift here is a
# breaking change requiring a v2 bump.
FLOOR = {
    "intent-catalog/v1": ["verb", "aliases", "examples", "param_schema", "preconditions",
                          "safety_class", "tool_path", "start_point_rules", "plain_label",
                          "consequence_copy"],
    "intent-map/v1": ["intent_key", "utterance_examples", "target_verb", "param_bindings",
                      "weight", "confidence", "hit_count", "last_used", "outcome_stats",
                      "source", "version"],
    "intent-feedback/v1": ["ts", "consumer", "catalog_version", "utterance", "proposal",
                           "operator_choice", "verdict", "confidence", "outcome", "session_id"],
    "intent-constitution/v1": ["rules", "kernel_invariants", "machine_checks", "banned_terms",
                               "operator_outcomes"],
    "intent-proposal/v1": ["consumer", "verb", "params", "start_point", "safety_class",
                           "tool_path", "confidence", "verdict", "why", "missing_params",
                           "requires_confirmation"],
}

# Frozen enum floors (values may only EXTEND; never shrink/rename).
ENUM_FLOOR = {
    "intent-catalog/v1": {"safety_class": ["read", "write", "destructive"],
                          "tool_path": ["cli", "mcp", "hook"]},
    "intent-map/v1": {"source": ["seed", "manual", "feedback"]},
    "intent-feedback/v1": {"operator_choice": ["accept", "correct", "reject", "clarify", "abort"],
                           "outcome": ["success", "refused", "failed", "noop", "unknown"]},
    "intent-proposal/v1": {"verdict": ["strong", "weak", "none"],
                           "safety_class": ["read", "write", "destructive"],
                           "tool_path": ["cli", "mcp", "hook"]},
    "intent-constitution/v1": {},
}

errs = []
oks = []

# Every expected contract file present + valid JSON + schema/version/floor correct.
seen_schemas = set()
for schema, (fname, exp_status) in EXPECTED.items():
    p = contracts_dir / fname
    if not p.exists():
        errs.append(f"missing contract file: {fname}")
        continue
    try:
        c = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        errs.append(f"{fname}: not valid JSON ({exc})")
        continue
    seen_schemas.add(schema)

    if c.get("schema") != schema:
        errs.append(f"{fname}: schema={c.get('schema')!r} != {schema!r}")
    if c.get("version") != 1:
        errs.append(f"{fname}: version={c.get('version')!r} != 1")
    if schema not in [s for s in c.get("freeze_strings", [])]:
        errs.append(f"{fname}: freeze_strings must contain {schema!r}")

    # Status + freeze-timing lock.
    status = c.get("status")
    if status != exp_status:
        errs.append(f"{fname}: status={status!r} != expected {exp_status!r} (freeze-timing lock)")
    if exp_status == "frozen":
        if c.get("freeze_exempt") is not False:
            errs.append(f"{fname}: a frozen contract must have freeze_exempt=false")
        if not c.get("frozen"):
            errs.append(f"{fname}: a frozen contract must record a `frozen` date")
    elif exp_status == "provisional":
        if c.get("freeze_exempt") is not True:
            errs.append(f"{fname}: intent-proposal must be freeze_exempt=true (freeze deferred to A0)")
        if c.get("frozen") not in (None, "", False):
            errs.append(f"{fname}: a provisional contract must NOT record a `frozen` date yet")

    # Required-key floor present.
    req = c.get("required_keys", {})
    for k in FLOOR.get(schema, []):
        if k not in req:
            errs.append(f"{fname}: required-key floor missing `{k}`")

    # Enum floor present (values may extend; the floor set must be a subset of the declared enum).
    declared = c.get("enums", {})
    for field, floor_vals in ENUM_FLOOR.get(schema, {}).items():
        have = declared.get(field)
        if not isinstance(have, list):
            errs.append(f"{fname}: enum `{field}` missing/not a list")
            continue
        for v in floor_vals:
            if v not in have:
                errs.append(f"{fname}: enum `{field}` dropped frozen value `{v}` (enums only EXTEND)")

    # Every contract must carry a deferred_additions map (the additive roadmap; may be empty).
    if not isinstance(c.get("deferred_additions"), dict):
        errs.append(f"{fname}: deferred_additions must be an object (additive roadmap)")

    oks.append(f"{fname}: schema {schema} v1 {status} — floor + enums OK")

# No unexpected extra contract file masquerading as a v1 contract.
for p in sorted(contracts_dir.glob("*.v1.json")):
    try:
        c = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        continue
    s = c.get("schema")
    if s not in EXPECTED:
        errs.append(f"{p.name}: declares schema {s!r} not in the frozen set {sorted(EXPECTED)}")

for line in oks:
    print("  PASS  " + line)
if errs:
    for e in errs:
        print("  FAIL  " + e, file=sys.stderr)
    sys.exit(1)
sys.exit(0)
PY
then
  pass "all five contracts satisfy the frozen behavior floor (catalog/map/feedback/constitution frozen; proposal provisional)"
else
  bad "contract freeze drift (see FAIL lines above) — a removal/rename/retype needs a v2 bump"
fi

if [ "$fail" -eq 0 ]; then
  echo "intent-contract-freeze: OK"
else
  echo "intent-contract-freeze: FAILED"
fi
exit "$fail"
