"""intent — the intent-router CLI (read-only surface).

R-core activates the four READ-ONLY verbs — `map`, `explain`, `catalog-verify`, `doctor` — each of
which only READS a consumer catalog + serializes a proposal or a report. Every later-phase verb stays
a "not-yet" stub. Constitutionally (CR1) this module has NO execution path: it never runs a consumer
verb, never spawns a process, never evaluates code. `tests/test_cli_stub.py` +
`tests/test_no_execution.py` enforce that the WHOLE runtime surface (this module and every sibling
runtime module) is free of the process/eval primitives that could run a consumer verb.

The router PROPOSES; the consumer's kernel decides and executes. Nothing here mutates anything.
"""

from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from . import doctor as doctor_mod
from .catalog import verify_catalog_file
from .engine import explain as engine_explain
from .engine import propose as engine_propose

# Exit code for a declared-but-not-yet-built verb (distinct from usage error 2).
NOT_YET = 3

# The full declared surface. `phase` is the phase that ACTIVATES the verb. `read_only=True` verbs
# never mutate anything even when built (the router has no mutating tool path by construction).
VERBS = {
    # read-only, activated in R-core
    "map":           {"phase": "R-core", "read_only": True,  "summary": "propose a verb for an utterance (read-only)"},
    "explain":       {"phase": "R-core", "read_only": True,  "summary": "explain why a proposal was made (read-only)"},
    "catalog-verify":{"phase": "R-core", "read_only": True,  "summary": "validate a consumer catalog against intent-catalog/v1 (read-only)"},
    "doctor":        {"phase": "R-core", "read_only": True,  "summary": "report catalog/store/golden-set/drift health (read-only)"},
    # later phases (still read-only or reviewable; never an execution path)
    "feedback":      {"phase": "C0", "read_only": True,  "summary": "append an operator-feedback event (append-only log)"},
    "phrasebook":    {"phase": "C0", "read_only": True,  "summary": "diff / review / apply the reviewable phrasebook overlay"},
    "calibrate":     {"phase": "C1", "read_only": True,  "summary": "recompute the derived map from the event log (deterministic)"},
    "seed":          {"phase": "C1", "read_only": True,  "summary": "seed the map from consented/redacted examples"},
    "snapshot":      {"phase": "R-resilience", "read_only": True, "summary": "write a versioned map snapshot"},
    "restore":       {"phase": "R-resilience", "read_only": True, "summary": "restore the map from a snapshot"},
    "rebuild":       {"phase": "R-resilience", "read_only": True, "summary": "rebuild the map from the event log (event-sourced)"},
    "status":        {"phase": "R-surface", "read_only": True, "summary": "print the runtime store/calibration status"},
}

# Verbs with a live handler in this phase. Everything else in VERBS is a not-yet stub.
ACTIVE_VERBS = {"map", "explain", "catalog-verify", "doctor"}

_DEFAULT_CONSUMER = "unknown"


def _print_surface(stream=None) -> None:
    stream = stream if stream is not None else sys.stdout
    print(f"intent-router {__version__} — router proposes, kernel decides (kernel-first).", file=stream)
    print("Read-only surface. R-core activates: map, explain, catalog-verify, doctor.", file=stream)
    print("", file=stream)
    print("Usage: intent <verb> [args]", file=stream)
    print("Verbs (phase that activates each):", file=stream)
    for name, meta in VERBS.items():
        active = " " if name in ACTIVE_VERBS else "·"
        print(f" {active}{name:<15} [{meta['phase']:<12}] {meta['summary']}", file=stream)
    print("", file=stream)
    print("See RESUME.md for the exact next action; ARCHITECTURE.md for the design.", file=stream)


def _not_yet(verb: str, stream=None) -> int:
    stream = stream if stream is not None else sys.stderr
    meta = VERBS[verb]
    print(
        f"intent {verb}: not yet — this verb activates in phase {meta['phase']}. "
        f"R-core built the read-only floor (map/explain/catalog-verify/doctor); "
        f"later verbs are declared but not yet built (see RESUME.md).",
        file=stream,
    )
    return NOT_YET


def _load_catalog(path: str):
    """Read a catalog JSON file into a dict. Returns (data, error). READ-ONLY (open for reading only,
    no write mode anywhere in the router). A malformed/absent file yields (None, message), never a
    stack trace — the CLI degrades gracefully."""
    ok, errors = verify_catalog_file(path)
    if not ok:
        return None, "; ".join(errors)
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh), None


def _emit(obj, as_json: bool, human: str) -> None:
    if as_json:
        print(json.dumps(obj, indent=2, sort_keys=True))
    else:
        print(human)


def _consumer_of(catalog: dict, override: str | None) -> str:
    if override:
        return override
    c = catalog.get("consumer") if isinstance(catalog, dict) else None
    return c if isinstance(c, str) and c else _DEFAULT_CONSUMER


def _cmd_map(argv) -> int:
    ap = argparse.ArgumentParser(prog="intent map", add_help=True,
                                 description="Propose a verb for an utterance (read-only, deterministic).")
    ap.add_argument("utterance", help="the operator utterance (quote it)")
    ap.add_argument("--catalog", required=True, help="path to the consumer's intent-catalog/v1 JSON")
    ap.add_argument("--consumer", default=None, help="consumer id (defaults to the catalog's `consumer`)")
    ap.add_argument("--json", action="store_true", help="emit the raw intent-proposal/v1 JSON")
    args = ap.parse_args(argv)

    catalog, err = _load_catalog(args.catalog)
    if err:
        print(f"intent map: catalog error: {err}", file=sys.stderr)
        return 1
    proposal = engine_propose(_consumer_of(catalog, args.consumer), args.utterance, catalog)
    human = (f"verb={proposal['verb'] or '(none)'}  verdict={proposal['verdict']}  "
             f"safety={proposal['safety_class']}  confidence={proposal['confidence']}  "
             f"confirm={proposal['requires_confirmation']}\nwhy: {', '.join(proposal['why'])}")
    _emit(proposal, args.json, human)
    return 0


def _cmd_explain(argv) -> int:
    ap = argparse.ArgumentParser(prog="intent explain", add_help=True,
                                 description="Explain the ranked candidates + the proposal (read-only).")
    ap.add_argument("utterance", help="the operator utterance (quote it)")
    ap.add_argument("--catalog", required=True, help="path to the consumer's intent-catalog/v1 JSON")
    ap.add_argument("--consumer", default=None, help="consumer id (defaults to the catalog's `consumer`)")
    ap.add_argument("--top", type=int, default=5, help="how many ranked candidates to show")
    ap.add_argument("--json", action="store_true", help="emit the raw explanation JSON")
    args = ap.parse_args(argv)

    catalog, err = _load_catalog(args.catalog)
    if err:
        print(f"intent explain: catalog error: {err}", file=sys.stderr)
        return 1
    out = engine_explain(_consumer_of(catalog, args.consumer), args.utterance, catalog, top_n=args.top)
    lines = [f"utterance: {out['utterance']}", f"verdict:   {out['verdict']}", "candidates:"]
    for c in out["candidates"]:
        lines.append(f"  {c['score']:>6.1f}  {c['verb']:<20} {', '.join(c['why'])}")
    p = out["proposal"]
    lines.append(f"proposal:  verb={p['verb'] or '(none)'}  safety={p['safety_class']}  "
                 f"confirm={p['requires_confirmation']}")
    _emit(out, args.json, "\n".join(lines))
    return 0


def _cmd_catalog_verify(argv) -> int:
    ap = argparse.ArgumentParser(prog="intent catalog-verify", add_help=True,
                                 description="Validate a consumer catalog against intent-catalog/v1 (read-only).")
    ap.add_argument("catalog_path", help="path to the catalog JSON to validate")
    ap.add_argument("--json", action="store_true", help="emit a JSON {ok, errors} report")
    args = ap.parse_args(argv)

    ok, errors = verify_catalog_file(args.catalog_path)
    report = {"schema": "intent-catalog-verify/v1", "catalog": args.catalog_path,
              "ok": ok, "errors": errors}
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    elif ok:
        print(f"catalog-verify: OK — {args.catalog_path} satisfies intent-catalog/v1")
    else:
        print(f"catalog-verify: FAILED — {len(errors)} error(s) in {args.catalog_path}", file=sys.stderr)
        for e in errors:
            print(f"  FAIL  {e}", file=sys.stderr)
    return 0 if ok else 1


def _cmd_doctor(argv) -> int:
    ap = argparse.ArgumentParser(prog="intent doctor", add_help=True,
                                 description="Read-only health report (catalog/store/golden-set/drift).")
    ap.add_argument("--catalog", default=None, help="optionally validate a consumer catalog too")
    ap.add_argument("--json", action="store_true", help="emit the raw intent-doctor/v1 JSON")
    args = ap.parse_args(argv)

    report = doctor_mod.health_report(catalog_path=args.catalog)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(doctor_mod.format_report(report))
    return 0 if report["ok"] else 1


_HANDLERS = {
    "map": _cmd_map,
    "explain": _cmd_explain,
    "catalog-verify": _cmd_catalog_verify,
    "doctor": _cmd_doctor,
}


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help", "help"):
        _print_surface()
        return 0
    if argv[0] in ("-V", "--version", "version"):
        print(__version__)
        return 0
    verb = argv[0]
    if verb not in VERBS:
        print(f"intent: unknown verb '{verb}'. Run `intent --help` for the surface.", file=sys.stderr)
        return 2
    # CR1: a declared verb NEVER executes a consumer action. Active verbs only READ + serialize a
    # proposal/report; later verbs are not-yet stubs. There is no branch here that runs a verb.
    if verb in ACTIVE_VERBS:
        return _HANDLERS[verb](argv[1:])
    return _not_yet(verb)


if __name__ == "__main__":
    raise SystemExit(main())
