"""status-verify test: the ledger honesty gate catches a lying ledger and passes an honest one.

Uses hermetic fixture repos so the test never depends on the real ledger's current contents.
"""

from __future__ import annotations

import textwrap
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from intent_router import status_verify

_ALL_PHASES = ["P0", "K0-K1", "K2", "R-core", "A0", "egress", "R2", "C0", "C1",
               "R-resilience", "R-surface", "M0"]


def _pending_block(pid: str) -> str:
    return textwrap.dedent(f"""\
      - id: {pid}
        title: "{pid} pending"
        status: pending
        pr: ""
        commit: ""
        current_gate: "future"
        resume_pointer: RESUME.md
        rollback_path: ROLLBACK.md
        passed_test_ids: []
        files: []
    """)


def _ledger(p0_block: str) -> str:
    body = "schema: intent-router-status/v1\ncurrent_phase: P0\nphases:\n"
    body += textwrap.indent(p0_block, "  ")
    for pid in _ALL_PHASES[1:]:
        body += textwrap.indent(_pending_block(pid), "  ")
    return body


class TestStatusVerify(unittest.TestCase):
    def test_parser_handles_grammar(self):
        data = status_verify.parse_status(_ledger(_pending_block("P0")))
        self.assertEqual(data["schema"], "intent-router-status/v1")
        self.assertEqual(len(data["phases"]), 12)
        self.assertEqual(data["phases"][0]["id"], "P0")
        self.assertEqual(data["phases"][0]["passed_test_ids"], [])

    def test_inline_json_arrays_parse(self):
        data = status_verify.parse_status(
            'schema: intent-router-status/v1\nphases:\n'
            '  - id: P0\n    passed_test_ids: ["a.B.c", "d.E.f"]\n    files: ["X.md"]\n'
        )
        self.assertEqual(data["phases"][0]["passed_test_ids"], ["a.B.c", "d.E.f"])
        self.assertEqual(data["phases"][0]["files"], ["X.md"])

    def test_honest_ledger_passes(self):
        with TemporaryDirectory() as d:
            root = Path(d)
            (root / "RESUME.md").write_text("resume", encoding="utf-8")
            (root / "ROLLBACK.md").write_text("rollback", encoding="utf-8")
            (root / "ART.md").write_text("art", encoding="utf-8")
            tdir = root / "tests"
            tdir.mkdir()
            (tdir / "__init__.py").write_text("", encoding="utf-8")
            (tdir / "test_fix.py").write_text(textwrap.dedent("""\
                import unittest
                class TestFix(unittest.TestCase):
                    def test_ok(self):
                        self.assertTrue(True)
            """), encoding="utf-8")
            p0 = textwrap.dedent("""\
              - id: P0
                title: "P0"
                status: done
                pr: "url"
                commit: ""
                current_gate: "done"
                resume_pointer: RESUME.md
                rollback_path: ROLLBACK.md
                passed_test_ids: ["tests.test_fix.TestFix.test_ok"]
                files: ["ART.md"]
            """)
            (root / "status.yml").write_text(_ledger(p0), encoding="utf-8")
            errors = status_verify.verify(root / "status.yml", root, run_tests=True)
            self.assertEqual(errors, [], f"honest ledger should pass, got: {errors}")

    def test_lying_ledger_fails(self):
        """A done phase claiming a missing file AND a failing test must be rejected."""
        with TemporaryDirectory() as d:
            root = Path(d)
            (root / "RESUME.md").write_text("resume", encoding="utf-8")
            (root / "ROLLBACK.md").write_text("rollback", encoding="utf-8")
            tdir = root / "tests"
            tdir.mkdir()
            (tdir / "__init__.py").write_text("", encoding="utf-8")
            (tdir / "test_fix.py").write_text(textwrap.dedent("""\
                import unittest
                class TestFix(unittest.TestCase):
                    def test_fails(self):
                        self.assertTrue(False)
            """), encoding="utf-8")
            p0 = textwrap.dedent("""\
              - id: P0
                title: "P0"
                status: done
                pr: "url"
                commit: ""
                current_gate: "lying"
                resume_pointer: RESUME.md
                rollback_path: ROLLBACK.md
                passed_test_ids: ["tests.test_fix.TestFix.test_fails"]
                files: ["DOES_NOT_EXIST.md"]
            """)
            (root / "status.yml").write_text(_ledger(p0), encoding="utf-8")
            errors = status_verify.verify(root / "status.yml", root, run_tests=True)
            joined = "\n".join(errors)
            self.assertIn("DOES_NOT_EXIST.md", joined, "must catch the missing-file lie")
            self.assertTrue(any("test_fails" in e for e in errors), "must catch the failing-test lie")

    def test_missing_phase_is_caught(self):
        # Drop M0 -> coverage failure.
        body = "schema: intent-router-status/v1\nphases:\n"
        for pid in _ALL_PHASES[:-1]:
            body += textwrap.indent(_pending_block(pid), "  ")
        with TemporaryDirectory() as d:
            root = Path(d)
            (root / "status.yml").write_text(body, encoding="utf-8")
            errors = status_verify.verify(root / "status.yml", root, run_tests=False)
            self.assertTrue(any("M0" in e for e in errors), "must catch an omitted phase")

    def test_real_ledger_parses_and_is_complete(self):
        repo_root = Path(__file__).resolve().parent.parent
        data = status_verify.parse_status((repo_root / "status.yml").read_text(encoding="utf-8"))
        ids = [p["id"] for p in data["phases"]]
        for pid in _ALL_PHASES:
            self.assertIn(pid, ids, f"real ledger missing phase {pid}")


if __name__ == "__main__":
    unittest.main()
