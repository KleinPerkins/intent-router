"""CLI-stub test: the router surface is executionless (CR1) and every verb is a not-yet stub.

CR1 (router PROPOSES, never executes) is enforced structurally at the surface: the `intent` CLI
module contains NONE of the primitives that could run a consumer verb (no subprocess, os.system,
exec/eval, popen, ...). This is scoped to the router runtime surface (intent_router/cli.py); the
dev-only status_verify gate legitimately runs tests and is not a router runtime surface.
"""

from __future__ import annotations

import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from intent_router import cli

_CLI_SRC = Path(cli.__file__).resolve()

# Execution primitives that must NEVER appear in the router surface. Kept in LOCKSTEP with
# tests/test_no_execution.py::_FORBIDDEN_EXEC (asserted by test_forbidden_exec_parity_with_cli_stub).
_FORBIDDEN_EXEC = [
    "subprocess", "os.system", "os.popen", "os.exec", "os.spawn", "os.posix_spawn", "os.fork",
    "Popen", "check_call", "check_output", "pty.spawn", "pty.fork", "pty.openpty",
    "commands.getoutput", "importlib", "ctypes", "runpy",
    "eval(", "exec(", "compile(", "__import__(",
]


class TestCliStub(unittest.TestCase):
    def test_no_execution_path(self):
        src = _CLI_SRC.read_text(encoding="utf-8")
        # Ignore the module docstring / comments referencing the words in prose by checking for
        # actual call-ish tokens; a bare mention like the word "subprocess" in a comment is fine,
        # but to stay strict we forbid the tokens outright in the surface module.
        offenders = [tok for tok in _FORBIDDEN_EXEC if tok in src]
        self.assertEqual(offenders, [],
                        f"router surface must be executionless (CR1); found: {offenders}")

    def test_later_phase_verbs_return_not_yet(self):
        # R-core ACTIVATES map/explain/catalog-verify/doctor; every LATER-phase verb stays a not-yet
        # stub until its phase builds it.
        later = [v for v in cli.VERBS if v not in cli.ACTIVE_VERBS]
        self.assertTrue(later, "there should still be later-phase stubs")
        for verb in later:
            buf_out, buf_err = io.StringIO(), io.StringIO()
            with redirect_stdout(buf_out), redirect_stderr(buf_err):
                rc = cli.main([verb])
            self.assertEqual(rc, cli.NOT_YET, f"later verb '{verb}' must return NOT_YET")
            self.assertIn("not yet", buf_err.getvalue().lower(),
                        f"later verb '{verb}' must emit a plain 'not yet' message")

    def test_active_verbs_are_not_stubs(self):
        # The four R-core verbs must NOT return the not-yet signal (they are dispatched to handlers).
        # Invoked with no args they hit an argparse usage error (2), never NOT_YET (3).
        for verb in cli.ACTIVE_VERBS:
            buf_out, buf_err = io.StringIO(), io.StringIO()
            with redirect_stdout(buf_out), redirect_stderr(buf_err):
                try:
                    rc = cli.main([verb])
                except SystemExit as exc:  # argparse exits on missing required args
                    rc = exc.code
            self.assertNotEqual(rc, cli.NOT_YET, f"active verb '{verb}' must not be a not-yet stub")

    def test_help_and_version_are_clean(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cli.main(["--help"])
        self.assertEqual(rc, 0)
        self.assertIn("router proposes", buf.getvalue().lower())

        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cli.main(["--version"])
        self.assertEqual(rc, 0)
        self.assertTrue(buf.getvalue().strip(), "version must print something")

    def test_unknown_verb_is_usage_error_not_execution(self):
        buf = io.StringIO()
        with redirect_stderr(buf):
            rc = cli.main(["definitely-not-a-verb"])
        self.assertEqual(rc, 2, "unknown verb is a usage error (2), never executed")

    def test_full_declared_surface_present(self):
        # The surface must be DECLARED now so it is stable across sessions.
        for expected in ("map", "explain", "catalog-verify", "doctor"):
            self.assertIn(expected, cli.VERBS, f"read-only verb '{expected}' must be declared")
        for later in ("feedback", "phrasebook", "calibrate", "seed", "snapshot",
                      "restore", "rebuild", "status"):
            self.assertIn(later, cli.VERBS, f"later verb '{later}' must be declared")


if __name__ == "__main__":
    unittest.main()
