"""state — CR3 private-state path resolver + guard. PURE path composition (no disk I/O at import
time, no child process — stays inside CR1's executionless surface even for the router's own
introspection).

Router state (`events.jsonl`, `<consumer>/map.json`, snapshots, phrasebook) is machine-local and
private, NEVER committed to a shared repo (ARCHITECTURE.md "State layout"; CONSTITUTION CR3):

    ${XDG_STATE_HOME:-~/.local/state}/intent-router/

No state-WRITING phase exists yet — C0 is the first to append an event to `events.jsonl`. This
module defines WHERE that future state must live and a deterministic guard (`assert_private`) a
future writer MUST call before its first `mkdir`/write, so CR3 is proven correct by construction on
day one rather than by convention alone.
"""

from __future__ import annotations

import os
from pathlib import Path

STATE_DIRNAME = "intent-router"


def state_dir(env: dict | None = None) -> Path:
    """Resolve the private state root: `${XDG_STATE_HOME:-~/.local/state}/intent-router`. Pure path
    composition — never creates the directory or touches disk. `env` defaults to `os.environ`;
    passing an explicit dict makes this testable without mutating process environment."""
    e = env if env is not None else os.environ
    base = e.get("XDG_STATE_HOME") or str(Path.home() / ".local" / "state")
    return Path(base) / STATE_DIRNAME


def _is_repo_root(path: Path) -> bool:
    """A directory is a git working-tree root if it directly contains a `.git` entry — a directory
    for a normal clone, a FILE for a linked worktree/submodule (both are sufficient signal; the
    router only needs "is this inside SOME repo", never the real common-dir)."""
    return (path / ".git").exists()


def is_inside_a_repo(path: Path) -> bool:
    """True if `path` (or its nearest EXISTING ancestor, so this works before the directory is ever
    created) sits inside any git working tree. Pure filesystem walk: no child process, no git-binary
    dependency — the guard itself never leaves the CR1 executionless surface."""
    probe = path.resolve()
    while not probe.exists():
        if probe.parent == probe:
            return False
        probe = probe.parent
    return any(_is_repo_root(anc) for anc in (probe, *probe.parents))


def assert_private(path: Path | None = None) -> Path:
    """Return the resolved state dir, raising if it would land inside a git working tree. The one
    guard a future state-writer (C0) must call before its first write; proven here against both the
    default resolution and an adversarial `XDG_STATE_HOME` override."""
    p = (path if path is not None else state_dir()).resolve()
    if is_inside_a_repo(p):
        raise RuntimeError(
            f"intent-router state path {p} resolves inside a git repository — CR3 forbids router "
            f"state ever landing in a shared repo; check XDG_STATE_HOME"
        )
    return p
