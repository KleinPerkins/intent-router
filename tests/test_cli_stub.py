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

# Execution primitives that must NEVER appear in the router surface.
_FORBIDDEN_EXEC = [
    "subprocess", "os.system", "os.popen", "os.exec", "Popen",
    "check_call", "check_output", "pty.spawn", "commands.getoutput",
    "eval(", "exec(", "__import__(",
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

    def test_every_verb_returns_not_yet(self):
        for verb in cli.VERBS:
            buf_out, buf_err = io.StringIO(), io.StringIO()
            with redirect_stdout(buf_out), redirect_stderr(buf_err):
                rc = cli.main([verb])
            self.assertEqual(rc, cli.NOT_YET, f"verb '{verb}' must return NOT_YET in P0")
            self.assertIn("not yet", buf_err.getvalue().lower(),
                        f"verb '{verb}' must emit a plain 'not yet' message")

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
