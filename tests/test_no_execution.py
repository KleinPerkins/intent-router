"""CR1 no-execution scan — EXPANDED to the WHOLE runtime surface (P0 deferred this to R-core).

P0 could only scan `cli.py` (the sole module that existed); `tests/test_cli_stub.py` keeps that
focused check as the constitution-bound `no_execution_path` test-id. THIS test generalizes it: every
module in the `intent_router` runtime package must be free of the process/eval primitives that could
run a consumer verb — so the guarantee holds as the surface grows (engine, candidates, verdict,
proposal, normalize, catalog, state, doctor, cli, mcp_server, __init__).

Allowlist: `status_verify.py` ONLY. It is DEV/CI tooling (it runs the test suite as a child process
to recompute the ledger) and is never imported by the router runtime surface — this test also proves
that non-reachability, so the one allowlisted executor can't sneak into a runtime path.
"""

from __future__ import annotations

import unittest
from pathlib import Path

import intent_router

_PKG_DIR = Path(intent_router.__file__).resolve().parent

# Mirrors tests/test_cli_stub.py::_FORBIDDEN_EXEC — the primitives that could run a consumer verb.
_FORBIDDEN_EXEC = [
    "subprocess", "os.system", "os.popen", "os.exec", "Popen",
    "check_call", "check_output", "pty.spawn", "commands.getoutput",
    "eval(", "exec(", "__import__(",
]

# Dev/CI-only tooling that legitimately runs a child process. Must NOT be a runtime router surface.
_ALLOWLIST = {"status_verify.py"}


def _runtime_modules():
    return sorted(p for p in _PKG_DIR.glob("*.py") if p.name not in _ALLOWLIST)


class TestNoExecutionAcrossRuntime(unittest.TestCase):
    def test_no_forbidden_primitive_in_any_runtime_module(self):
        offenders: list[str] = []
        scanned = 0
        for path in _runtime_modules():
            scanned += 1
            src = path.read_text(encoding="utf-8")
            for tok in _FORBIDDEN_EXEC:
                if tok in src:
                    offenders.append(f"{path.name}: contains forbidden execution primitive {tok!r}")
        self.assertGreaterEqual(scanned, 8, "expected the full runtime surface to be scanned")
        self.assertEqual(offenders, [],
                         "router runtime must be executionless (CR1):\n" + "\n".join(offenders))

    def test_expected_runtime_modules_are_covered(self):
        names = {p.name for p in _runtime_modules()}
        for expected in ("cli.py", "engine.py", "candidates.py", "verdict.py", "proposal.py",
                         "normalize.py", "catalog.py", "state.py", "doctor.py", "mcp_server.py"):
            self.assertIn(expected, names, f"{expected} must be in the no-execution scan set")

    def test_allowlisted_executor_not_imported_by_runtime(self):
        # status_verify is allowlisted; prove it is NOT reachable from the router runtime surface —
        # no runtime module IMPORTS it — so the allowlist can't become an execution backdoor. (A prose
        # mention in a docstring is fine; an import line is not.)
        offenders: list[str] = []
        for path in _runtime_modules():
            for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if "import" in line and "status_verify" in line:
                    offenders.append(f"{path.name}:{lineno}: {line.strip()}")
        self.assertEqual(offenders, [],
                         "a runtime module imports the allowlisted executor status_verify:\n"
                         + "\n".join(offenders))


if __name__ == "__main__":
    unittest.main()
