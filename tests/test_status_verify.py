"""status-verify test: the ledger honesty gate catches a lying ledger and passes an honest one.

Uses hermetic fixture repos so the test never depends on the real ledger's current contents.
"""

from __future__ import annotations

import os
import subprocess
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


def _ledger(p0_block: str, current_phase: str = "P0") -> str:
    body = f"schema: intent-router-status/v1\ncurrent_phase: {current_phase}\nphases:\n"
    body += textwrap.indent(p0_block, "  ")
    for pid in _ALL_PHASES[1:]:
        body += textwrap.indent(_pending_block(pid), "  ")
    return body


_GIT_ENV = {**os.environ, "GIT_TERMINAL_PROMPT": "0", "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_CONFIG_SYSTEM": "/dev/null"}


def _init_git_repo(root: Path) -> str:
    """Init a throwaway git repo with one empty commit; return its full SHA. Lets a fixture pin a
    REAL resolvable commit (so the honest ledger passes) or contrast it with a fake SHA."""
    subprocess.run(["git", "init", "-q"], cwd=root, check=True, env=_GIT_ENV)
    subprocess.run(["git", "config", "user.email", "t@example.com"], cwd=root, check=True, env=_GIT_ENV)
    subprocess.run(["git", "config", "user.name", "t"], cwd=root, check=True, env=_GIT_ENV)
    subprocess.run(["git", "commit", "--allow-empty", "-q", "-m", "seed"], cwd=root, check=True, env=_GIT_ENV)
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True,
                          check=True, env=_GIT_ENV).stdout.strip()


def _divergent_repo(root: Path) -> tuple[str, str]:
    """Init a repo with a main commit A and a DIVERGENT side commit B off the initial commit. Returns
    (head_of_main, divergent_sha). B is a real object but is NOT an ancestor of main's HEAD — the
    exact case `git cat-file -e` (object-exists) passes but `merge-base --is-ancestor` must reject."""
    def g(*args):
        return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True,
                              check=True, env=_GIT_ENV)
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=_GIT_ENV)
    g("config", "user.email", "t@example.com")
    g("config", "user.name", "t")
    g("checkout", "-q", "-b", "main")
    g("commit", "--allow-empty", "-q", "-m", "A")
    g("checkout", "-q", "-b", "side")
    g("commit", "--allow-empty", "-q", "-m", "B")
    g("checkout", "-q", "main")
    head = g("rev-parse", "HEAD").stdout.strip()
    diverged = g("rev-parse", "side").stdout.strip()
    return head, diverged


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
            sha = _init_git_repo(root)  # a REAL resolvable commit for the done phase
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
            p0 = textwrap.dedent(f"""\
              - id: P0
                title: "P0"
                status: done
                pr: "https://example/pull/1"
                commit: "{sha}"
                current_gate: "done"
                resume_pointer: RESUME.md
                rollback_path: ROLLBACK.md
                passed_test_ids: ["tests.test_fix.TestFix.test_ok"]
                files: ["ART.md"]
            """)
            # P0 done + rest pending (no track) => first non-done router phase is K0-K1.
            (root / "status.yml").write_text(_ledger(p0, current_phase="K0-K1"), encoding="utf-8")
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

    def test_false_done_empty_evidence_fails(self):
        """BLOCKER-2 regression: a phase flipped to `done` with EMPTY evidence must FAIL.

        Before the P0 review fix this passed EXIT 0 (a done phase with no test, no pr, no commit was
        blessed). Now empty passed_test_ids / pr / commit each bite."""
        with TemporaryDirectory() as d:
            root = Path(d)
            (root / "RESUME.md").write_text("r", encoding="utf-8")
            (root / "ROLLBACK.md").write_text("r", encoding="utf-8")
            p0 = textwrap.dedent("""\
              - id: P0
                title: "P0"
                status: done
                pr: ""
                commit: ""
                current_gate: "empty-evidence"
                resume_pointer: RESUME.md
                rollback_path: ROLLBACK.md
                passed_test_ids: []
                files: []
            """)
            (root / "status.yml").write_text(_ledger(p0, current_phase="K0-K1"), encoding="utf-8")
            errors = status_verify.verify(root / "status.yml", root, run_tests=False)
            joined = "\n".join(errors)
            self.assertIn("NO passed_test_ids", joined, "must reject a done phase with no tests")
            self.assertIn("empty 'pr'", joined, "must reject a done phase with no pr")
            self.assertIn("empty 'commit'", joined, "must reject a done phase with no commit")

    def test_fake_pr_and_commit_rejected(self):
        """BLOCKER-3 regression: a fabricated commit SHA (with any /pull/N) must FAIL.

        A non-empty `pr` + a well-formed-but-nonexistent `commit` used to pass (only presence was
        checked). Now the commit must resolve offline via `git cat-file -e`."""
        with TemporaryDirectory() as d:
            root = Path(d)
            _init_git_repo(root)  # a real repo that does NOT contain the fake commit
            (root / "RESUME.md").write_text("r", encoding="utf-8")
            (root / "ROLLBACK.md").write_text("r", encoding="utf-8")
            fake = "deadbeef" * 5  # 40 hex chars, not an object in this repo
            p0 = textwrap.dedent(f"""\
              - id: P0
                title: "P0"
                status: done
                pr: "https://github.com/KleinPerkins/intent-router/pull/9999999"
                commit: "{fake}"
                current_gate: "fake-commit"
                resume_pointer: RESUME.md
                rollback_path: ROLLBACK.md
                passed_test_ids: ["x.Y.z"]
                files: []
            """)
            (root / "status.yml").write_text(_ledger(p0, current_phase="K0-K1"), encoding="utf-8")
            errors = status_verify.verify(root / "status.yml", root, run_tests=False)
            joined = "\n".join(errors)
            self.assertIn(fake, joined, "must name the unresolvable commit")
            self.assertIn("does NOT resolve", joined, "must reject a fabricated commit SHA")

    def test_strict_rejects_malformed_pr_url(self):
        """SHOULD-FIX #5(a): a well-formed-looking but malformed pr (`.../pull/999999-not-real`) used
        to pass with 0 errors. In strict mode it is now rejected by SHAPE, offline + deterministically.
        Non-strict keeps the old presence-only behavior."""
        with TemporaryDirectory() as d:
            root = Path(d)
            sha = _init_git_repo(root)  # real + ancestor-of-itself, so only the pr is at fault
            (root / "RESUME.md").write_text("r", encoding="utf-8")
            (root / "ROLLBACK.md").write_text("r", encoding="utf-8")
            p0 = textwrap.dedent(f"""\
              - id: P0
                title: "P0"
                status: done
                pr: "https://github.com/KleinPerkins/intent-router/pull/999999-not-real"
                commit: "{sha}"
                current_gate: "bad-pr"
                resume_pointer: RESUME.md
                rollback_path: ROLLBACK.md
                passed_test_ids: ["x.Y.z"]
                files: []
            """)
            (root / "status.yml").write_text(_ledger(p0, current_phase="K0-K1"), encoding="utf-8")
            strict = status_verify.verify(root / "status.yml", root, run_tests=False, strict=True)
            self.assertTrue(any("malformed" in e for e in strict),
                            f"strict must reject a malformed pr, got: {strict}")
            loose = status_verify.verify(root / "status.yml", root, run_tests=False, strict=False)
            self.assertFalse(any("malformed" in e for e in loose),
                             "non-strict must keep presence-only pr behavior")

    def test_commit_ancestor_helper_distinguishes_ancestor_from_object(self):
        """SHOULD-FIX #5(b): the ancestry helper says True for an ancestor and False for a real-but-
        divergent object — object-existence alone is not ancestry."""
        with TemporaryDirectory() as d:
            root = Path(d)
            head, diverged = _divergent_repo(root)
            self.assertIs(status_verify._commit_is_ancestor(head, root), True)
            self.assertIs(status_verify._commit_is_ancestor(diverged, root), False)

    def test_strict_rejects_nonancestor_commit(self):
        """SHOULD-FIX #5(b): a done phase pinning a real object that is NOT on the current history is
        rejected in strict mode (ancestry, not just `cat-file -e`)."""
        with TemporaryDirectory() as d:
            root = Path(d)
            _head, diverged = _divergent_repo(root)
            (root / "RESUME.md").write_text("r", encoding="utf-8")
            (root / "ROLLBACK.md").write_text("r", encoding="utf-8")
            p0 = textwrap.dedent(f"""\
              - id: P0
                title: "P0"
                status: done
                pr: "https://example.com/o/r/pull/1"
                commit: "{diverged}"
                current_gate: "off-history"
                resume_pointer: RESUME.md
                rollback_path: ROLLBACK.md
                passed_test_ids: ["x.Y.z"]
                files: []
            """)
            (root / "status.yml").write_text(_ledger(p0, current_phase="K0-K1"), encoding="utf-8")
            strict = status_verify.verify(root / "status.yml", root, run_tests=False, strict=True)
            self.assertTrue(any("ancestor" in e for e in strict),
                            f"strict must reject a non-ancestor commit, got: {strict}")
            # the object DOES exist, so the pre-existing object-existence check does NOT fire:
            self.assertFalse(any("does NOT resolve" in e for e in strict))

    def test_missing_git_unknown_blocks_in_strict(self):
        """SHOULD-FIX #5(c): a MISSING git is unknown-blocks in strict mode (fail-closed), not
        fail-open. Simulated by forcing the offline resolver to report 'git unavailable' (None)."""
        original = status_verify._commit_resolvable
        status_verify._commit_resolvable = lambda commit, repo_root: None
        try:
            with TemporaryDirectory() as d:
                root = Path(d)
                (root / "RESUME.md").write_text("r", encoding="utf-8")
                (root / "ROLLBACK.md").write_text("r", encoding="utf-8")
                p0 = textwrap.dedent("""\
                  - id: P0
                    title: "P0"
                    status: done
                    pr: "https://example.com/o/r/pull/1"
                    commit: "0123456789012345678901234567890123456789"
                    current_gate: "no-git"
                    resume_pointer: RESUME.md
                    rollback_path: ROLLBACK.md
                    passed_test_ids: ["x.Y.z"]
                    files: []
                """)
                (root / "status.yml").write_text(_ledger(p0, current_phase="K0-K1"), encoding="utf-8")
                strict = status_verify.verify(root / "status.yml", root, run_tests=False, strict=True)
                self.assertTrue(any("git is unavailable" in e for e in strict),
                                f"strict must unknown-block on missing git, got: {strict}")
                loose = status_verify.verify(root / "status.yml", root, run_tests=False, strict=False)
                self.assertFalse(any("git is unavailable" in e for e in loose),
                                 "non-strict must stay fail-open on missing git")
        finally:
            status_verify._commit_resolvable = original

    def test_current_phase_must_match_first_non_done(self):
        """MINOR-8 regression: a stale current_phase (pointing at a done phase) must FAIL."""
        with TemporaryDirectory() as d:
            root = Path(d)
            sha = _init_git_repo(root)
            (root / "RESUME.md").write_text("r", encoding="utf-8")
            (root / "ROLLBACK.md").write_text("r", encoding="utf-8")
            tdir = root / "tests"; tdir.mkdir()
            (tdir / "__init__.py").write_text("", encoding="utf-8")
            (tdir / "test_fix.py").write_text(
                "import unittest\nclass T(unittest.TestCase):\n    def test_ok(self):\n        pass\n",
                encoding="utf-8")
            p0 = textwrap.dedent(f"""\
              - id: P0
                title: "P0"
                status: done
                pr: "https://example/pull/1"
                commit: "{sha}"
                current_gate: "done"
                resume_pointer: RESUME.md
                rollback_path: ROLLBACK.md
                passed_test_ids: ["tests.test_fix.T.test_ok"]
                files: []
            """)
            # current_phase stale at P0 (already done) — must be flagged.
            (root / "status.yml").write_text(_ledger(p0, current_phase="P0"), encoding="utf-8")
            errors = status_verify.verify(root / "status.yml", root, run_tests=True)
            self.assertTrue(any("current_phase" in e for e in errors),
                            f"stale current_phase must be caught, got: {errors}")

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
