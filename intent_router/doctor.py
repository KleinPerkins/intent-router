"""doctor — read-only health report for the intent-router runtime. PURE / EXECUTIONLESS (CR1): it
only READS files and composes path facts; it never runs a child process, shells out, or evaluates code
(unlike the dev-only `status_verify`, which is allowlisted to run tests — doctor is a RUNTIME
surface the CLI `doctor` verb and the MCP `intent_doctor` tool both call, so it stays inside CR1).

Reports catalog / store / golden-set / drift health (RESUME.md R-core item 2). Each check is a flat
`{name, ok, detail}`; the top-level `ok` is the AND of the LOAD-BEARING checks (contracts present +
freeze-timing status correct + state path private per CR3). Informational lines (state-dir presence,
golden-set inventory, drift) never fail the report on their own — no state-writing phase exists yet
(C0) and no snapshots exist to drift from yet (R-resilience), so their absence is expected, not a
fault. An explicitly-requested catalog that fails validation DOES fail the report.
"""

from __future__ import annotations

import json
from pathlib import Path

from . import __version__
from .catalog import verify_catalog_file
from .state import assert_private, state_dir

SCHEMA = "intent-doctor/v1"

# name -> expected freeze-timing status (mirrors checks/intent-contract-freeze.sh EXPECTED; doctor
# only reads the declared status, it does not re-run the freeze checker — that would be execution).
_EXPECTED_CONTRACTS = {
    "intent-catalog.v1.json": "frozen",
    "intent-map.v1.json": "frozen",
    "intent-feedback.v1.json": "frozen",
    "intent-constitution.v1.json": "frozen",
    "intent-proposal.v1.json": "frozen",
}


def _runtime_root(root: Path | None = None) -> Path:
    """Resolve the runtime/repo root (holds contracts/ + tests/golden/). Works in-repo and from the
    installed copy at $XDG_DATA_HOME/intent-router/current (both put this package one level down)."""
    return root if root is not None else Path(__file__).resolve().parent.parent


def _check(name: str, ok: bool, detail: str, load_bearing: bool = True) -> dict:
    return {"name": name, "ok": bool(ok), "detail": detail, "load_bearing": load_bearing}


def _contracts_check(root: Path) -> list[dict]:
    checks: list[dict] = []
    cdir = root / "contracts"
    for fname, exp_status in _EXPECTED_CONTRACTS.items():
        p = cdir / fname
        if not p.exists():
            checks.append(_check(f"contract:{fname}", False, "missing"))
            continue
        try:
            c = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError, UnicodeDecodeError) as exc:
            checks.append(_check(f"contract:{fname}", False, f"unreadable/invalid JSON: {exc}"))
            continue
        status = c.get("status")
        ok = status == exp_status
        detail = f"status={status}" + ("" if ok else f" (expected {exp_status})")
        checks.append(_check(f"contract:{fname}", ok, detail))
    return checks


def _state_checks(env: dict | None) -> list[dict]:
    checks: list[dict] = []
    try:
        resolved = assert_private(state_dir(env))
        checks.append(_check("state_path_private", True,
                             f"{resolved} (CR3: resolves outside any git repo)"))
        checks.append(_check(
            "state_dir_present", resolved.exists(),
            f"{'present' if resolved.exists() else 'absent — created on first event (C0); expected empty in R-core'}",
            load_bearing=False,
        ))
    except RuntimeError as exc:
        checks.append(_check("state_path_private", False, str(exc)))
    return checks


def _golden_check(root: Path) -> dict:
    gdir = root / "tests" / "golden"
    files = sorted(p.name for p in gdir.glob("*.golden.json")) if gdir.is_dir() else []
    return _check(
        "golden_sets", True,
        f"{len(files)} golden set(s): {', '.join(files) if files else 'none'}",
        load_bearing=False,
    )


def _drift_check() -> dict:
    # Behavior-hash drift detection lands in R-resilience (needs snapshots to compare against). Until
    # then there is nothing to drift FROM; report the honest 'not-yet' state rather than a false green.
    return _check("drift", True, "n/a — snapshot/drift detection activates in R-resilience",
                  load_bearing=False)


def health_report(catalog_path: str | Path | None = None,
                  env: dict | None = None,
                  root: Path | None = None) -> dict:
    """Compose the full read-only health report. `catalog_path` optionally validates a consumer
    catalog (its errors DO fail the report). Pure: no writes, no child process."""
    root = _runtime_root(root)
    checks: list[dict] = []
    checks.extend(_contracts_check(root))
    checks.extend(_state_checks(env))
    checks.append(_golden_check(root))
    checks.append(_drift_check())

    if catalog_path is not None:
        ok, errors = verify_catalog_file(Path(catalog_path))
        detail = "valid" if ok else f"{len(errors)} error(s): " + "; ".join(errors[:5])
        checks.append(_check(f"catalog:{Path(catalog_path).name}", ok, detail))

    ok = all(c["ok"] for c in checks if c["load_bearing"])
    return {"schema": SCHEMA, "version": __version__, "ok": ok, "checks": checks}


def format_report(report: dict) -> str:
    """Human-readable rendering (the CLI text form). JSON form is `json.dumps(report)`."""
    lines = [f"== intent-router doctor ({report.get('schema')}) =="]
    for c in report.get("checks", []):
        mark = "PASS" if c["ok"] else "FAIL"
        tag = "" if c["load_bearing"] else " (info)"
        lines.append(f"  {mark}  {c['name']}{tag}: {c['detail']}")
    lines.append(f"intent-router doctor: {'OK' if report.get('ok') else 'FAILED'}")
    return "\n".join(lines)
