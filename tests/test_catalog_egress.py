"""Egress-gate regression tests (R-core fix pass, MUST-FIX #1).

The banned-term / host-literal scan must be (a) CASE-INSENSITIVE for the naturally-lowercase Tier
A/B/C mechanism + git words (so `WORKTREE`, `KERNEL`, `Merge`, `Branch` cannot slip past by
capitalization), while (b) keeping CASE-SENSITIVE matching for the genuinely-ambiguous all-caps
acronyms (`HEAD`, `PR`, `MCP`) that would otherwise collide with ordinary English; and it must cover
EVERY PM-emitted / proposal-bound string — not just `plain_label`/`consequence_copy` but `verb`,
`aliases`, `examples`, `start_point_rules` values, and `param_schema[].name` (each of which flows
into the `intent-proposal/v1` envelope or the rendered `why[]`).

Each test below FAILS against the pre-fix scanner (case-sensitive, two-field) and PASSES after the
fix — a leak becomes a schema-validation failure, not luck.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from intent_router import catalog

_REPO_ROOT = Path(__file__).resolve().parent.parent
_FIXTURE = _REPO_ROOT / "tests" / "fixtures" / "awa-catalog.fixture.json"


def _valid_verb(**overrides) -> dict:
    base = {
        "verb": "protect",
        "aliases": ["protect", "start protecting"],
        "examples": ["put this work somewhere safe", "keep this project safe"],
        "param_schema": [
            {"name": "target_path", "type": "path", "required": True, "source": "repo-resolver"}
        ],
        "preconditions": ["target_path is provided"],
        "safety_class": "write",
        "tool_path": "cli",
        "start_point_rules": {"default": "current"},
        "plain_label": "Start protecting this work",
        "consequence_copy": "Creates a separate safe copy to work in. Your original files are left untouched.",
    }
    base.update(overrides)
    return base


def _catalog(*verbs) -> dict:
    return {"schema": "intent-catalog/v1", "consumer": "test-fixture", "verbs": list(verbs)}


class TestCaseInsensitiveLowercaseTerms(unittest.TestCase):
    """(a) naturally-lowercase host-policy terms match regardless of case."""

    def test_find_banned_terms_matches_uppercase_worktree(self):
        hits = catalog.find_banned_terms("WORKTREE removal")
        self.assertIn("worktree", hits)

    def test_find_banned_terms_matches_mixed_case_git_words(self):
        hits = catalog.find_banned_terms("Merge the Branch then Rebase")
        self.assertIn("merge", hits)
        self.assertIn("branch", hits)
        self.assertIn("rebase", hits)

    def test_uppercase_leak_in_plain_label_rejected(self):
        data = _catalog(_valid_verb(plain_label="WORKTREE removal"))
        errors = catalog.validate_catalog(data)
        joined = "\n".join(errors)
        self.assertTrue(errors, "an UPPERCASE Tier-A leak must still be rejected")
        self.assertIn("plain_label", joined)
        self.assertIn("worktree", joined)

    def test_uppercase_leak_in_consequence_copy_rejected(self):
        data = _catalog(_valid_verb(
            consequence_copy="removes your WORKTREE and KERNEL protection"))
        errors = catalog.validate_catalog(data)
        joined = "\n".join(errors)
        self.assertIn("consequence_copy", joined)
        self.assertIn("worktree", joined)
        self.assertIn("kernel", joined)


class TestAcronymsStayCaseSensitive(unittest.TestCase):
    """(b) HEAD/PR/MCP keep case-sensitive matching so plain English is not a false positive."""

    def test_lowercase_head_is_not_a_false_positive(self):
        self.assertEqual(catalog.find_banned_terms("use your head to decide"), [])

    def test_uppercase_head_still_flagged(self):
        self.assertIn("HEAD", catalog.find_banned_terms("reset to HEAD now"))

    def test_lowercase_pr_word_is_not_a_false_positive(self):
        self.assertEqual(catalog.find_banned_terms("we print this then approve it"), [])

    def test_clean_pm_copy_has_no_false_positive(self):
        data = _catalog(_valid_verb(
            plain_label="Check whether your files are currently safe",
            consequence_copy="Nothing changes. This only reports what is currently protected."))
        self.assertEqual(catalog.validate_catalog(data), [])


class TestExpandedFieldCoverage(unittest.TestCase):
    """Every PM-emitted / proposal-bound string is scanned — not just the two copy fields."""

    def test_start_point_rules_default_leak_rejected(self):
        # Proven leak: this value passes catalog-verify AND appears verbatim in proposal.start_point.
        data = _catalog(_valid_verb(start_point_rules={"default": "detached HEAD worktree"}))
        errors = catalog.validate_catalog(data)
        joined = "\n".join(errors)
        self.assertTrue(errors, "a leaked start_point_rules value must be rejected")
        self.assertIn("start_point_rules", joined)
        self.assertIn("worktree", joined)
        self.assertIn("HEAD", joined)

    def test_alias_leak_rejected(self):
        # Proven leak: an alias flows into the rendered why[] on CLI + MCP.
        data = _catalog(_valid_verb(aliases=["protect", "orphan branch lease"]))
        errors = catalog.validate_catalog(data)
        joined = "\n".join(errors)
        self.assertTrue(errors, "a leaked alias must be rejected")
        self.assertIn("aliases", joined)
        for term in ("orphan", "branch", "lease"):
            self.assertIn(term, joined)

    def test_example_leak_rejected(self):
        data = _catalog(_valid_verb(examples=["put this somewhere safe", "rebase onto main"]))
        errors = catalog.validate_catalog(data)
        joined = "\n".join(errors)
        self.assertIn("examples", joined)
        self.assertIn("rebase", joined)
        self.assertIn("main", joined)

    def test_verb_name_leak_rejected(self):
        # verb flows into proposal.verb and the verb_name signal in why[].
        data = _catalog(_valid_verb(verb="merge"))
        errors = catalog.validate_catalog(data)
        joined = "\n".join(errors)
        self.assertIn("merge", joined)

    def test_param_name_leak_rejected(self):
        # A required param name flows into proposal.missing_params.
        data = _catalog(_valid_verb(param_schema=[
            {"name": "worktree", "type": "path", "required": True}]))
        errors = catalog.validate_catalog(data)
        joined = "\n".join(errors)
        self.assertIn("worktree", joined)


class TestNoRegressionOnCleanCatalogs(unittest.TestCase):
    """Expanding scope must NOT turn the shipped AWA fixture (or a plain valid catalog) red."""

    def test_awa_fixture_catalog_still_validates_clean(self):
        data = json.loads(_FIXTURE.read_text(encoding="utf-8"))
        errors = catalog.validate_catalog(data)
        self.assertEqual(errors, [], f"AWA fixture must remain jargon-free, got: {errors}")

    def test_plain_valid_catalog_still_clean(self):
        self.assertEqual(catalog.validate_catalog(_catalog(_valid_verb())), [])


if __name__ == "__main__":
    unittest.main()
