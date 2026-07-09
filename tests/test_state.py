"""CR3 state-privacy tests — router state resolves to a machine-local XDG path and a guard refuses
any path that would land inside a git working tree. Pure path composition + filesystem walk (no
subprocess, no git binary) — the guard itself never leaves CR1's executionless surface.

This is the REAL test that discharges the `state_is_private` machine-check (flipped spec->active in
R-core); `tests/test_deferred_spec.py::test_spec_state_is_private` remains as the greppable pointer.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from intent_router.state import STATE_DIRNAME, assert_private, is_inside_a_repo, state_dir


class TestStateDir(unittest.TestCase):
    def test_respects_xdg_state_home(self):
        d = state_dir({"XDG_STATE_HOME": "/custom/state"})
        self.assertEqual(d, Path("/custom/state") / STATE_DIRNAME)

    def test_defaults_to_local_state_under_home(self):
        d = state_dir({})  # no XDG_STATE_HOME
        self.assertEqual(d, Path.home() / ".local" / "state" / STATE_DIRNAME)
        self.assertEqual(d.name, "intent-router")

    def test_is_pure_no_directory_created(self):
        with TemporaryDirectory() as tmp:
            target = Path(tmp) / "nope"
            d = state_dir({"XDG_STATE_HOME": str(target)})
            self.assertFalse(d.exists(), "state_dir must not create anything")


class TestIsInsideARepo(unittest.TestCase):
    def test_true_when_dot_git_dir_present(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".git").mkdir()
            self.assertTrue(is_inside_a_repo(root))
            sub = root / "a" / "b"
            sub.mkdir(parents=True)
            self.assertTrue(is_inside_a_repo(sub), "a nested dir inside a repo is inside the repo")

    def test_true_when_dot_git_is_a_file_linked_worktree(self):
        # A linked worktree has a .git FILE (a gitdir: pointer), not a directory.
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".git").write_text("gitdir: /somewhere/else\n", encoding="utf-8")
            self.assertTrue(is_inside_a_repo(root))

    def test_false_outside_any_repo(self):
        with TemporaryDirectory() as tmp:
            self.assertFalse(is_inside_a_repo(Path(tmp)))

    def test_resolves_nearest_existing_ancestor_for_uncreated_path(self):
        # The guard must work BEFORE the state dir is created (walk up to the nearest real parent).
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".git").mkdir()
            not_yet = root / "deep" / "not" / "created" / "intent-router"
            self.assertTrue(is_inside_a_repo(not_yet))


class TestAssertPrivate(unittest.TestCase):
    def test_raises_inside_a_repo(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".git").mkdir()
            with self.assertRaises(RuntimeError) as ctx:
                assert_private(root / "intent-router")
            self.assertIn("git repository", str(ctx.exception))

    def test_returns_resolved_path_outside_repo(self):
        with TemporaryDirectory() as tmp:
            target = Path(tmp) / "intent-router"
            got = assert_private(target)
            self.assertEqual(got, target.resolve())

    def test_default_resolution_is_guarded(self):
        # Calling with no arg guards the DEFAULT XDG resolution. On a normal machine ~/.local/state
        # is not inside a repo; if it somehow were, this must raise rather than silently pass.
        try:
            got = assert_private()
            self.assertEqual(got.name, "intent-router")
        except RuntimeError as exc:
            self.assertIn("git repository", str(exc))


if __name__ == "__main__":
    unittest.main()
