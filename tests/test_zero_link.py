"""Zero-link: the intent-router capability must carry ZERO governed-repo (cpp/ld-edge) literals.

intent-router is a shared, global capability destined for the `tools/intent-router` shelf. Like
AWA, its tracked surface must name no downstream governed repo. This in-repo pre-flight mirrors the
orchestrator's `zero-link --mode global` gate against a forbidden-token list. Referencing the FIRST
CONSUMER (AWA) is allowed — AWA is a sibling KleinPerkins capability, not a forbidden token.

Scan scope: the GIT surface that is (or would be) committed — tracked files plus new,
non-ignored files (`git ls-files --cached --others --exclude-standard`), so a forbidden token is
caught even before the file is staged, while `.gitignore`d cruft is skipped. Falls back to a
working-tree walk only when git is unavailable (e.g. an installed runtime copy outside a checkout).

The forbidden tokens are assembled from fragments so THIS scanner stays token-clean, and it
excludes itself from the scan.
"""

from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

# Assemble the forbidden tokens from fragments (MIRRORS the orchestrator forbidden list EXACTLY:
# card-platform-product ; <org>/(src|vendor) ; <gov>-stuff ; (^|[^A-Za-z])<gov>([^A-Za-z]|$))
# so this file itself contains no literal token.
_card = "card-" + "platform-" + "product"
_org = "af" + "firm"
_gov = "c" + "pp"

_FORBIDDEN = [
    re.compile(re.escape(_card)),
    re.compile(_org + r"/(src|vendor)"),
    re.compile(re.escape(_gov + "-stuff")),
    re.compile(r"(^|[^A-Za-z])" + _gov + r"([^A-Za-z]|$)"),
]

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SELF = Path(__file__).resolve()

_SKIP_PARTS = {"__pycache__", ".pytest_cache", ".git", "node_modules",
               ".mypy_cache", ".ruff_cache", ".venv", "venv", "build", "dist"}
_SKIP_SUFFIX = {".pyc"}


def _iter_tracked_files():
    """Yield the git surface that is or would be committed (tracked + new non-ignored files), via
    `git ls-files`. Fall back to a working-tree walk only when git is unavailable."""
    try:
        out = subprocess.run(
            ["git", "-C", str(_REPO_ROOT), "ls-files", "-z",
             "--cached", "--others", "--exclude-standard"],
            capture_output=True, text=True, check=True,
        ).stdout
        rels = [r for r in out.split("\0") if r]
        if rels:
            for rel in rels:
                p = _REPO_ROOT / rel
                if p.is_file() and p.suffix not in _SKIP_SUFFIX:
                    yield p
            return
    except Exception:  # noqa: BLE001 — git absent (installed runtime); fall back below.
        pass
    for path in sorted(_REPO_ROOT.rglob("*")):
        if not path.is_file():
            continue
        if _SKIP_PARTS & set(path.parts):
            continue
        if path.suffix in _SKIP_SUFFIX:
            continue
        yield path


class TestZeroLink(unittest.TestCase):
    def test_no_forbidden_literals_in_tracked_surface(self):
        offenders: list[str] = []
        for path in _iter_tracked_files():
            if path.resolve() == _SELF:
                continue  # the scanner necessarily references the tokens (as fragments)
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for lineno, line in enumerate(text.splitlines(), 1):
                for rx in _FORBIDDEN:
                    if rx.search(line):
                        offenders.append(f"{path.relative_to(_REPO_ROOT)}:{lineno}: {line.strip()}")
        self.assertEqual(
            offenders, [],
            "forbidden governed-repo literal(s) in the tracked surface — a shared capability names "
            "no downstream governed repo:\n" + "\n".join(offenders),
        )


if __name__ == "__main__":
    unittest.main()
