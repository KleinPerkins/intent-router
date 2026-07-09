"""status_verify — recompute the status.yml ledger against disk and tests so it CANNOT lie.

The phase ledger (status.yml) is only useful if a future session can trust it. This module is the
enforcement: for every phase marked `done`, it verifies the claimed artifacts EXIST on disk and the
claimed `passed_test_ids` both EXIST and PASS (run as subprocesses). A phase that claims a passing
test that is missing or red fails the gate. Pending/future phases are shape-checked only.

Stdlib only. status.yml uses a tiny, unambiguous grammar (top-level `key: scalar`, a `phases:` list
of flat maps whose list/object values are INLINE JSON), so parsing is bulletproof without PyYAML.

`--strict` (used by `make status-verify`) fails CLOSED on things a presence-only check would bless:
  - `pr` must be well-formed (`.../pull/<number>`, rejecting `.../pull/999999-not-real`) AND, when
    `gh` is available + authed, must actually resolve; when gh is absent/unauthed/offline OR the URL
    is not a github.com PR, it degrades HONESTLY to shape+presence (offline-safe by design).
  - the pinned `commit` must be an ANCESTOR of HEAD (`git merge-base --is-ancestor`), not merely a
    real object.
  - a MISSING git is `unknown-blocks` (fail-closed), not fail-open.
Non-strict keeps the original presence-only behavior for backward compatibility.

Run:  python3 -m intent_router.status_verify [--strict] [--no-run] [--status PATH]
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

SCHEMA = "intent-router-status/v1"

# A PR reference is well-formed iff it is an https URL ending in `/pull/<integer>`. This is the
# offline, deterministic floor (it rejects `.../pull/999999-not-real`); existence is an additional
# best-effort online check (see `_pr_exists`).
_PR_URL_RE = re.compile(r"^https?://\S+/pull/\d+$")
_GITHUB_PR_RE = re.compile(r"^https?://github\.com/([^/\s]+)/([^/\s]+)/pull/(\d+)$")

# Every phase of the v8 ladder must appear in the ledger (coverage: the ledger can't omit a phase).
EXPECTED_PHASES = ["P0", "K0-K1", "K2", "R-core", "A0", "egress", "R2", "C0", "C1",
                   "R-resilience", "R-surface", "M0"]

VALID_STATUS = {"done", "in_progress", "pending", "blocked", "cancelled"}

# Keys every phase entry must carry (the ledger schema).
ENTRY_KEYS = {"id", "title", "status", "pr", "commit", "current_gate",
              "resume_pointer", "rollback_path", "passed_test_ids"}


def _scalar(v: str):
    v = v.strip()
    if v.startswith("[") or v.startswith("{"):
        return json.loads(v)  # inline JSON array / object
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    if v in ("null", "~"):
        return None
    if v == "true":
        return True
    if v == "false":
        return False
    if v == "":
        return ""
    try:
        return int(v)
    except ValueError:
        return v


def parse_status(text: str) -> dict:
    """Parse the constrained status.yml grammar into a dict with a `phases` list."""
    root: dict = {}
    phases: list = []
    current: dict | None = None
    in_phases = False
    for raw in text.splitlines():
        if " #" in raw:
            raw = raw.split(" #", 1)[0]
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if indent == 0:
            if stripped == "phases:":
                in_phases = True
                current = None
                continue
            in_phases = False
            key, _, val = stripped.partition(":")
            root[key.strip()] = _scalar(val)
        elif in_phases and stripped.startswith("- "):
            current = {}
            phases.append(current)
            rest = stripped[2:].strip()
            key, _, val = rest.partition(":")
            current[key.strip()] = _scalar(val)
        elif in_phases and current is not None:
            key, _, val = stripped.partition(":")
            current[key.strip()] = _scalar(val)
    root["phases"] = phases
    return root


def _run_test(test_id: str, repo_root: Path) -> tuple[str, str]:
    """Run one test-id via unittest. Returns (state, detail) where state is one of
    'pass' | 'fail' | 'missing'. 'missing' means the test-id could not be resolved."""
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "-v", test_id],
        cwd=str(repo_root),
        env={"PYTHONPATH": str(repo_root), "PATH": _path_env()},
        capture_output=True, text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if "Ran 0 tests" in out or "ModuleNotFoundError" in out or "AttributeError" in out \
            or "failed to import" in out or "Can't find" in out or "No module named" in out \
            or "ImportError" in out:
        return "missing", out.strip().splitlines()[-1] if out.strip() else "unresolved"
    if proc.returncode == 0:
        return "pass", "ok"
    return "fail", out.strip().splitlines()[-1] if out.strip() else "non-zero exit"


def _path_env() -> str:
    import os
    return os.environ.get("PATH", "/usr/bin:/bin")


def _commit_resolvable(commit: str, repo_root: Path):
    """Whether `commit` resolves to a real commit object OFFLINE.

    Returns True/False when git can answer, or None when git is unavailable (so callers can degrade
    gracefully outside a checkout). This is what stops a fake SHA (e.g. 'deadbeef…') from passing:
    `git cat-file -e <sha>^{commit}` is non-zero for a SHA the repo does not contain."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo_root), "cat-file", "-e", f"{commit}^{{commit}}"],
            capture_output=True, text=True,
        )
    except FileNotFoundError:
        return None
    return proc.returncode == 0


def _commit_is_ancestor(commit: str, repo_root: Path):
    """Whether `commit` is an ANCESTOR of HEAD (reachable on the current history), not merely a real
    object. `git merge-base --is-ancestor <commit> HEAD` exits 0=ancestor, 1=not-ancestor; anything
    else (bad HEAD, shallow clone) or a missing git yields None so the caller can degrade."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo_root), "merge-base", "--is-ancestor", commit, "HEAD"],
            capture_output=True, text=True,
        )
    except FileNotFoundError:
        return None
    if proc.returncode == 0:
        return True
    if proc.returncode == 1:
        return False
    return None


def _pr_shape_ok(pr: str) -> bool:
    return bool(_PR_URL_RE.match(pr.strip()))


def _pr_exists(pr: str, repo_root: Path):
    """Best-effort ONLINE existence check for a GitHub PR URL. Returns:
      - True  : gh resolved the PR (it exists),
      - False : gh definitively reports it does NOT exist (a fabricated well-formed URL),
      - None  : cannot determine — gh absent/unauthed/offline/timed-out, or a non-github URL.
    None is an HONEST degrade (offline-safe): the strict gate then relies on shape + presence only.
    Never raises; a hostile URL can only yield an error string upstream, never code execution."""
    import os
    m = _GITHUB_PR_RE.match(pr.strip())
    if not m:
        return None  # not a github.com PR URL we know how to resolve
    owner, repo, num = m.group(1), m.group(2), m.group(3)
    try:
        proc = subprocess.run(
            ["gh", "pr", "view", num, "--repo", f"{owner}/{repo}", "--json", "number"],
            cwd=str(repo_root), capture_output=True, text=True, timeout=8,
            # Inherit the real environment (HOME/PATH/GH_TOKEN) so gh can find its auth; without HOME
            # gh cannot authenticate and every check would silently degrade. CI without auth still
            # degrades honestly (an auth error is not a 'not found' — see below).
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GH_PROMPT_DISABLED": "1"},
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return None
    if proc.returncode == 0:
        return True
    err = ((proc.stderr or "") + (proc.stdout or "")).lower()
    if "could not resolve" in err or "not found" in err or "no pull requests found" in err:
        return False
    return None  # auth/network/other failure -> degrade honestly


def verify(status_path: Path, repo_root: Path, run_tests: bool = True,
           strict: bool = False) -> list[str]:
    errors: list[str] = []
    if not status_path.exists():
        return [f"status ledger missing: {status_path}"]
    try:
        data = parse_status(status_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"status ledger unparseable: {exc}"]

    if data.get("schema") != SCHEMA:
        errors.append(f"schema={data.get('schema')!r} != {SCHEMA!r}")

    phases = data.get("phases", [])
    ids = [p.get("id") for p in phases]
    for exp in EXPECTED_PHASES:
        if exp not in ids:
            errors.append(f"ledger omits required phase: {exp}")

    for p in phases:
        pid = p.get("id", "<no-id>")
        missing = ENTRY_KEYS - set(p)
        if missing:
            errors.append(f"{pid}: entry missing keys {sorted(missing)}")
        st = p.get("status")
        if st not in VALID_STATUS:
            errors.append(f"{pid}: invalid status {st!r} (allowed {sorted(VALID_STATUS)})")
        if not isinstance(p.get("passed_test_ids"), list):
            errors.append(f"{pid}: passed_test_ids must be a list")

        # DONE phases must carry non-empty evidence AND be recomputed against disk/tests — the
        # ledger can neither lie nor bless a `done` phase on empty/fake evidence.
        if st == "done":
            # BLOCKER-2: empty-evidence `done` is a lie. Require >=1 test AND a pr AND a commit.
            if not p.get("passed_test_ids"):
                errors.append(f"{pid}: done phase has NO passed_test_ids "
                              f"(a done phase needs >=1 passing test as evidence)")
            pr = p.get("pr")
            if not pr:
                errors.append(f"{pid}: done phase has an empty 'pr' "
                              f"(a done phase needs a PR URL as evidence)")
            elif strict:
                # A non-empty string is no longer enough in strict mode. Shape is validated offline
                # (rejects `.../pull/999999-not-real`); existence is a best-effort gh resolution that
                # degrades honestly to shape+presence when gh is absent/unauthed/offline.
                if not _pr_shape_ok(str(pr)):
                    errors.append(f"{pid}: pr {pr!r} is malformed — expected an https URL ending in "
                                  f"'/pull/<number>'")
                elif _pr_exists(str(pr), repo_root) is False:
                    errors.append(f"{pid}: pr {pr!r} could not be resolved — gh reports no such PR "
                                  f"(a done phase must pin a real PR)")
            commit = p.get("commit")
            if not commit:
                errors.append(f"{pid}: done phase has an empty 'commit' "
                              f"(a done phase needs a resolvable commit as evidence)")
            else:
                # BLOCKER-3: the commit must actually resolve offline — a fabricated SHA cannot pass.
                resolvable = _commit_resolvable(str(commit), repo_root)
                if resolvable is False:
                    errors.append(f"{pid}: commit '{commit}' does NOT resolve offline "
                                  f"(git cat-file -e failed) — a done phase must pin a real commit")
                elif resolvable is None and strict:
                    # git unavailable: unknown-blocks in strict mode (fail-closed, not fail-open).
                    errors.append(f"{pid}: git is unavailable — cannot verify commit '{commit}' in "
                                  f"strict mode (unknown-blocks; strict requires an offline git)")
                elif resolvable is True and strict:
                    # Ancestry, not just object-existence: a real object off the current history
                    # (e.g. a dangling/other-branch commit) is not honest evidence for a done phase.
                    if _commit_is_ancestor(str(commit), repo_root) is False:
                        errors.append(f"{pid}: commit '{commit}' is NOT an ancestor of HEAD "
                                      f"(the object exists but is off the current history)")
            for rel in [p.get("resume_pointer"), p.get("rollback_path"), *p.get("files", [])]:
                if not rel:
                    continue
                if not (repo_root / rel).exists():
                    errors.append(f"{pid}: claims file '{rel}' but it is MISSING on disk")
            for tid in p.get("passed_test_ids", []):
                if not run_tests:
                    continue
                state, detail = _run_test(tid, repo_root)
                if state == "missing":
                    errors.append(f"{pid}: claims test '{tid}' but it could not be resolved ({detail})")
                elif state == "fail":
                    errors.append(f"{pid}: claims test '{tid}' PASSES but it FAILED ({detail})")

    # MINOR-8: current_phase must equal the first non-done phase on the ROUTER build path. Phases
    # tagged track=consumer-kernel (AWA-repo lanes) run in PARALLEL and gate "proven", not the
    # router's next action (see RESUME.md), so they are excluded from "first non-done". This keeps the
    # pointer honest with the ledger: you cannot leave current_phase stale after flipping a phase.
    if "current_phase" in data:
        router_phases = [p for p in phases if p.get("track") != "consumer-kernel"]
        first_non_done = next((p.get("id") for p in router_phases
                               if p.get("status") != "done"), None)
        cp = data.get("current_phase")
        if cp != first_non_done:
            errors.append(f"current_phase={cp!r} but the first non-done router phase is "
                          f"{first_non_done!r} (reconcile current_phase or a phase status)")
    return errors


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    run_tests = "--no-run" not in argv
    strict = "--strict" in argv
    repo_root = Path(__file__).resolve().parent.parent
    status_path = repo_root / "status.yml"
    if "--status" in argv:
        status_path = Path(argv[argv.index("--status") + 1]).resolve()

    errors = verify(status_path, repo_root, run_tests=run_tests, strict=strict)
    if errors:
        print("== status-verify: FAILED (the ledger disagrees with disk/tests) ==", file=sys.stderr)
        for e in errors:
            print("  FAIL  " + e, file=sys.stderr)
        return 1
    print("== status-verify: OK — every 'done' claim recomputed against disk + tests ==")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
