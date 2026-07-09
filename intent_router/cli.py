"""intent — the intent-router CLI.

P0: a thin "not-yet" stub. The full verb SURFACE is DECLARED here so it stays stable across the
multi-session build, but NO verb does routing work yet, and — constitutionally (CR1) — there is
NO execution path: this module never runs a consumer verb, shells out, or evaluates code. It only
reads (later) and serializes proposals; the consumer's kernel executes and decides.

`tests/test_cli_stub.py` enforces both properties: every declared verb returns the not-yet
signal, and the module source contains none of the execution primitives that could run a
consumer verb.
"""

from __future__ import annotations

import sys

from . import __version__

# Exit code for a declared-but-not-yet-built verb (distinct from usage error 2).
NOT_YET = 3

# The full declared surface. `phase` is the phase that ACTIVATES the verb; until then every verb
# returns the not-yet signal. `read_only=True` verbs never mutate anything even when built
# (the router has no mutating tool path by construction).
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


def _print_surface(stream=None) -> None:
    stream = stream if stream is not None else sys.stdout
    print(f"intent-router {__version__} — router proposes, kernel decides (kernel-first).", file=stream)
    print("P0: architecture + frozen contracts only. Every verb below is a 'not-yet' stub.", file=stream)
    print("", file=stream)
    print("Usage: intent <verb> [args]", file=stream)
    print("Verbs (phase that activates each):", file=stream)
    for name, meta in VERBS.items():
        print(f"  {name:<15} [{meta['phase']:<12}] {meta['summary']}", file=stream)
    print("", file=stream)
    print("See RESUME.md for the exact next action; ARCHITECTURE.md for the design.", file=stream)


def _not_yet(verb: str, stream=None) -> int:
    stream = stream if stream is not None else sys.stderr
    meta = VERBS[verb]
    print(
        f"intent {verb}: not yet — the intent-router runtime is not built in this phase. "
        f"This verb activates in phase {meta['phase']}. "
        f"P0 froze the architecture + contracts only (see RESUME.md).",
        file=stream,
    )
    return NOT_YET


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
    # Constitutional (CR1): a declared verb NEVER executes a consumer action. In P0 it is a
    # not-yet stub; when built (R-core+) it will only READ and serialize a proposal.
    return _not_yet(verb)


if __name__ == "__main__":
    raise SystemExit(main())
