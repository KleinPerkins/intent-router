"""CR1 no-execution scan — WHOLE runtime surface, AST/import-node based (R-core fix pass, MUST-FIX #3).

P0 could only scan `cli.py` (the sole module that existed); `tests/test_cli_stub.py` keeps a focused
substring check on that one module. THIS test generalizes it to every module in the `intent_router`
runtime package and, instead of substring matching, parses each module and inspects its AST — so it
catches import forms (`import importlib`, `from ctypes import CDLL`), attribute calls (`os.fork()`,
`os.posix_spawn(...)`, `pty.openpty()`), and builtin calls (`eval`, `exec`, `compile`, `__import__`)
STRUCTURALLY. That closes two gaps a substring list has: it cannot be fooled by a token buried in a
docstring (false positive — e.g. the word "subprocess" in prose) and it cannot MISS a real call the
denylist simply forgot to enumerate as a string (false negative — the latent hole R2/C0/C1 would hit
as they add modules). `re.compile(...)` — a legitimate, ubiquitous stdlib call — is correctly NOT a
`compile()` builtin, so the AST scan does not false-positive on it where a `"compile("` substring would.

Allowlist: `status_verify.py` ONLY. It is DEV/CI tooling (it runs the test suite as a child process
to recompute the ledger) and is never imported by the router runtime surface — the reachability test
below also proves that, so the one allowlisted executor can't sneak into a runtime path.
"""

from __future__ import annotations

import ast
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import intent_router

_PKG_DIR = Path(intent_router.__file__).resolve().parent

# Dev/CI-only tooling that legitimately runs a child process. Must NOT be a runtime router surface.
_ALLOWLIST = {"status_verify.py"}

# Top-level modules whose mere import is a CR1 violation on the runtime surface.
_FORBIDDEN_IMPORT_ROOTS = {
    "subprocess", "importlib", "ctypes", "runpy", "pty", "commands", "multiprocessing",
}
# `os` / `pty` are importable, but these attributes are execution primitives.
_FORBIDDEN_OS_ATTRS = {
    "system", "popen", "fork", "posix_spawn", "spawn",
    "spawnl", "spawnle", "spawnlp", "spawnlpe", "spawnv", "spawnve", "spawnvp", "spawnvpe",
    "execl", "execle", "execlp", "execlpe", "execv", "execve", "execvp", "execvpe",
}
_FORBIDDEN_PTY_ATTRS = {"spawn", "fork", "openpty"}
# Builtins that run code, matched as a bare-name call (NOT `re.compile`, which is an attribute).
_FORBIDDEN_BUILTINS = {"eval", "exec", "compile", "__import__"}
# Bare names that only exist via a forbidden import (defence in depth).
_FORBIDDEN_NAMES = {"Popen"}

# Belt-and-suspenders substring denylist — kept in LOCKSTEP with tests/test_cli_stub.py::_FORBIDDEN_EXEC
# (asserted by test_forbidden_exec_parity_with_cli_stub). The authoritative runtime-surface gate is
# the AST scan below; this list documents the token floor and guards the cli.py focused check.
_FORBIDDEN_EXEC = [
    "subprocess", "os.system", "os.popen", "os.exec", "os.spawn", "os.posix_spawn", "os.fork",
    "Popen", "check_call", "check_output", "pty.spawn", "pty.fork", "pty.openpty",
    "commands.getoutput", "importlib", "ctypes", "runpy",
    "eval(", "exec(", "compile(", "__import__(",
]


def _runtime_modules():
    return sorted(p for p in _PKG_DIR.glob("*.py") if p.name not in _ALLOWLIST)


def _dotted_name(node: ast.AST) -> str:
    """Reconstruct a plain dotted name (`os.posix_spawn`) from an Attribute/Name chain; returns ""
    for anything that is not a simple attribute-of-name (e.g. a call result subscript)."""
    parts: list[str] = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return ".".join(reversed(parts))
    return ""


def scan_source(src: str, filename: str = "<mem>") -> list[str]:
    """AST-scan one module's source for CR1-forbidden execution primitives. Returns a sorted list of
    human-readable offense strings (empty = clean). Pure: parses text, never imports or runs it."""
    offenses: list[str] = []
    try:
        tree = ast.parse(src, filename=filename)
    except SyntaxError as exc:
        return [f"{filename}: could not parse ({exc})"]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in _FORBIDDEN_IMPORT_ROOTS:
                    offenses.append(f"{filename}:{node.lineno}: import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".")[0]
            if root in _FORBIDDEN_IMPORT_ROOTS:
                offenses.append(f"{filename}:{node.lineno}: from {node.module} import ...")
            if root == "os":
                for alias in node.names:
                    if alias.name in _FORBIDDEN_OS_ATTRS:
                        offenses.append(f"{filename}:{node.lineno}: from os import {alias.name}")
            if root == "pty":
                for alias in node.names:
                    if alias.name in _FORBIDDEN_PTY_ATTRS:
                        offenses.append(f"{filename}:{node.lineno}: from pty import {alias.name}")
        elif isinstance(node, ast.Attribute):
            dotted = _dotted_name(node)
            if dotted.startswith("os.") and node.attr in _FORBIDDEN_OS_ATTRS:
                offenses.append(f"{filename}:{node.lineno}: {dotted}")
            elif dotted.startswith("pty.") and node.attr in _FORBIDDEN_PTY_ATTRS:
                offenses.append(f"{filename}:{node.lineno}: {dotted}")
        elif isinstance(node, ast.Name):
            if node.id in _FORBIDDEN_BUILTINS or node.id in _FORBIDDEN_NAMES:
                offenses.append(f"{filename}:{node.lineno}: {node.id}")
    return sorted(set(offenses))


class TestNoExecutionAcrossRuntime(unittest.TestCase):
    def test_no_forbidden_primitive_in_any_runtime_module(self):
        offenders: list[str] = []
        scanned = 0
        for path in _runtime_modules():
            scanned += 1
            offenders.extend(scan_source(path.read_text(encoding="utf-8"), path.name))
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


class TestAstScanBites(unittest.TestCase):
    """Each snippet is a real forbidden primitive the pre-fix substring denylist did NOT name; the
    AST scan catches every one. `re.compile` proves the scan is precise, not a blunt `"compile("`."""

    def test_dynamic_import_via_importlib_is_caught(self):
        self.assertTrue(scan_source("import importlib\nx = importlib.import_module('os')\n"),
                        "importlib.import_module must be caught")

    def test_from_ctypes_import_is_caught(self):
        self.assertTrue(scan_source("from ctypes import CDLL\nCDLL('libc.so.6')\n"))

    def test_os_fork_is_caught(self):
        self.assertTrue(scan_source("import os\nos.fork()\n"))

    def test_os_posix_spawn_is_caught(self):
        self.assertTrue(scan_source("import os\nos.posix_spawn('/bin/true', [], {})\n"))

    def test_os_spawn_family_is_caught(self):
        self.assertTrue(scan_source("import os\nos.spawnv(os.P_WAIT, '/bin/true', ['true'])\n"))

    def test_runpy_is_caught(self):
        self.assertTrue(scan_source("import runpy\nrunpy.run_module('x')\n"))

    def test_compile_builtin_is_caught(self):
        self.assertTrue(scan_source("code = compile('1+1', '<s>', 'eval')\n"))

    def test_pty_fork_and_openpty_are_caught(self):
        self.assertTrue(scan_source("import pty\npty.fork()\n"))
        self.assertTrue(scan_source("import pty\npty.openpty()\n"))

    def test_eval_exec_dunder_import_are_caught(self):
        self.assertTrue(scan_source("eval('1')\n"))
        self.assertTrue(scan_source("exec('x=1')\n"))
        self.assertTrue(scan_source("__import__('os')\n"))

    def test_module_file_using_importlib_is_caught(self):
        # Faithful to the reviewer's ask: a real .py module using importlib.import_module is caught.
        with TemporaryDirectory() as d:
            p = Path(d) / "m.py"
            p.write_text("import importlib\n\ndef go():\n    return importlib.import_module('os')\n",
                         encoding="utf-8")
            self.assertTrue(scan_source(p.read_text(encoding="utf-8"), p.name))

    def test_re_compile_is_not_a_false_positive(self):
        # re.compile is an Attribute, not the compile() builtin — a substring "compile(" scan would
        # wrongly flag it (catalog.py/normalize.py use it), the AST scan does not.
        self.assertEqual(scan_source("import re\nP = re.compile('x')\n"), [])

    def test_benign_os_attrs_are_not_false_positives(self):
        self.assertEqual(scan_source("import os\nos.environ.get('X')\nos.path.join('a', 'b')\n"), [])

    def test_forbidden_exec_parity_with_cli_stub(self):
        # Honor "add the tokens to BOTH lists": the two substring floors stay in lockstep.
        from tests import test_cli_stub
        self.assertEqual(_FORBIDDEN_EXEC, test_cli_stub._FORBIDDEN_EXEC,
                         "test_no_execution._FORBIDDEN_EXEC and test_cli_stub._FORBIDDEN_EXEC drifted")


if __name__ == "__main__":
    unittest.main()
