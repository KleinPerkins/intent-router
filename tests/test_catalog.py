"""catalog-verify tests — proves each of the four bad-catalog classes is CAUGHT (R-core deliverable):
bad safety_class, missing param_schema, unsafe tool_path, leaked host-policy literals. Each
adversarial case starts from a hand-built VALID catalog and mutates exactly one thing.
"""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from intent_router import catalog

_REPO_ROOT = Path(__file__).resolve().parent.parent


def _valid_verb(**overrides) -> dict:
    base = {
        "verb": "protect",
        "aliases": ["protect", "start protecting"],
        "examples": ["put this work somewhere safe", "start protecting this repo"],
        "param_schema": [
            {"name": "target_path", "type": "path", "required": True, "source": "repo-resolver"}
        ],
        "preconditions": ["target_path is a git repository"],
        "safety_class": "write",
        "tool_path": "cli",
        "start_point_rules": {"default": "current"},
        "plain_label": "Start protecting this work",
        "consequence_copy": "Creates a separate safe copy to work in. Your original files are left untouched.",
    }
    base.update(overrides)
    return base


def _valid_catalog(*verbs) -> dict:
    return {"schema": "intent-catalog/v1", "consumer": "test-fixture", "verbs": list(verbs) or [_valid_verb()]}


class TestValidCatalogPasses(unittest.TestCase):
    def test_clean_catalog_has_zero_errors(self):
        errors = catalog.validate_catalog(_valid_catalog())
        self.assertEqual(errors, [])

    def test_multiple_distinct_verbs_all_pass(self):
        data = _valid_catalog(
            _valid_verb(verb="protect"),
            _valid_verb(
                verb="cleanup",
                aliases=["cleanup", "remove safe copy"],
                examples=["clean up my old safe copy", "delete this safe copy"],
                safety_class="destructive",
                plain_label="Remove an old safe copy",
                consequence_copy="Deletes a safe copy that is no longer needed. This cannot be undone.",
            ),
        )
        self.assertEqual(catalog.validate_catalog(data), [])

    def test_duplicate_verb_name_is_caught(self):
        data = _valid_catalog(_valid_verb(verb="protect"), _valid_verb(verb="protect"))
        errors = catalog.validate_catalog(data)
        self.assertTrue(any("duplicate verb name" in e for e in errors))


class TestBadCatalogClass1_SafetyClass(unittest.TestCase):
    """Deliverable class 1: bad safety_class."""

    def test_unknown_safety_class_value_rejected(self):
        data = _valid_catalog(_valid_verb(safety_class="apocalyptic"))
        errors = catalog.validate_catalog(data)
        self.assertTrue(errors, "a bad safety_class must be rejected")
        self.assertTrue(any("safety_class" in e and "apocalyptic" in e for e in errors))

    def test_safety_class_wrong_type_rejected(self):
        data = _valid_catalog(_valid_verb(safety_class=3))
        errors = catalog.validate_catalog(data)
        self.assertTrue(any("safety_class" in e for e in errors))

    def test_missing_safety_class_key_rejected(self):
        v = _valid_verb()
        del v["safety_class"]
        errors = catalog.validate_catalog(_valid_catalog(v))
        self.assertTrue(any("safety_class" in e for e in errors))


class TestBadCatalogClass2_MissingParamSchema(unittest.TestCase):
    """Deliverable class 2: missing param_schema."""

    def test_param_schema_key_absent_rejected(self):
        v = _valid_verb()
        del v["param_schema"]
        errors = catalog.validate_catalog(_valid_catalog(v))
        self.assertTrue(errors, "an absent param_schema must be rejected")
        self.assertTrue(any("param_schema" in e for e in errors))

    def test_param_schema_wrong_type_rejected(self):
        data = _valid_catalog(_valid_verb(param_schema="not-a-list"))
        errors = catalog.validate_catalog(data)
        self.assertTrue(any("param_schema" in e for e in errors))

    def test_param_entry_missing_required_nested_key_rejected(self):
        # A param entry present but missing the nested 'name' floor key.
        v = _valid_verb(param_schema=[{"type": "path", "required": True}])
        errors = catalog.validate_catalog(_valid_catalog(v))
        self.assertTrue(any("param_schema[0]" in e and "name" in e for e in errors))

    def test_param_entry_missing_type_rejected(self):
        v = _valid_verb(param_schema=[{"name": "target_path", "required": True}])
        errors = catalog.validate_catalog(_valid_catalog(v))
        self.assertTrue(any("param_schema[0]" in e and "type" in e for e in errors))


class TestBadCatalogClass3_UnsafeToolPath(unittest.TestCase):
    """Deliverable class 3: unsafe tool_path."""

    def test_shell_tool_path_rejected(self):
        data = _valid_catalog(_valid_verb(tool_path="shell"))
        errors = catalog.validate_catalog(data)
        self.assertTrue(errors, "an unsafe tool_path must be rejected")
        self.assertTrue(any("tool_path" in e and "shell" in e for e in errors))

    def test_exec_tool_path_rejected(self):
        data = _valid_catalog(_valid_verb(tool_path="exec"))
        errors = catalog.validate_catalog(data)
        self.assertTrue(any("tool_path" in e for e in errors))

    def test_empty_tool_path_rejected(self):
        data = _valid_catalog(_valid_verb(tool_path=""))
        errors = catalog.validate_catalog(data)
        self.assertTrue(any("tool_path" in e for e in errors))

    def test_all_three_safe_tool_paths_accepted(self):
        for tp in ("cli", "mcp", "hook"):
            data = _valid_catalog(_valid_verb(tool_path=tp))
            self.assertEqual(catalog.validate_catalog(data), [], f"tool_path={tp!r} should be safe")


class TestBadCatalogClass4_LeakedHostPolicyLiterals(unittest.TestCase):
    """Deliverable class 4: leaked host-policy literals in PM-facing catalog copy."""

    def test_tier_a_leak_in_consequence_copy_rejected(self):
        data = _valid_catalog(_valid_verb(
            consequence_copy="This acquires a lease on your worktree before it runs."
        ))
        errors = catalog.validate_catalog(data)
        self.assertTrue(errors, "a Tier A mechanism-word leak must be rejected")
        joined = "\n".join(errors)
        self.assertIn("consequence_copy", joined)
        self.assertIn("lease", joined)

    def test_tier_a_leak_in_plain_label_rejected(self):
        data = _valid_catalog(_valid_verb(plain_label="Run the guard heartbeat check"))
        errors = catalog.validate_catalog(data)
        self.assertTrue(any("plain_label" in e for e in errors))

    def test_tier_c_consumer_concrete_leak_rejected(self):
        # "--bundle" is AWA's own contributed Tier C token (egress-terms.checklist.json).
        data = _valid_catalog(_valid_verb(
            consequence_copy="Runs the equivalent of clean --bundle before removing anything."
        ))
        errors = catalog.validate_catalog(data)
        self.assertTrue(any("--bundle" in e for e in errors))

    def test_tier_b_git_workflow_leak_rejected(self):
        data = _valid_catalog(_valid_verb(
            consequence_copy="This will rebase your changes before continuing."
        ))
        errors = catalog.validate_catalog(data)
        self.assertTrue(any("rebase" in e for e in errors))

    def test_clean_copy_has_no_false_positive(self):
        # Precision check: genuinely jargon-free copy (avoiding even the mundane-sounding Tier B
        # entries like "main"/"ahead"/"dirty" — intentionally banned per ARCHITECTURE.md, since a
        # PM reading them would think git, not plain English) must pass with zero errors.
        data = _valid_catalog(_valid_verb(
            plain_label="Check whether your files are currently safe",
            consequence_copy="Nothing changes. This only reports what is currently protected.",
        ))
        errors = catalog.validate_catalog(data)
        self.assertEqual(errors, [], f"unexpected false positive(s): {errors}")

    def test_case_sensitivity_is_a_documented_tradeoff_not_a_loophole(self):
        # "HEAD"/"PR"/"MCP" are uppercase in the tiers specifically so they don't collide with
        # common English; lowercase Tier B entries ("main", "ahead", "dirty") are banned in EITHER
        # case they'd naturally appear (they're already lowercase in the source tiers), so this is
        # not a case-swap bypass — matching is case-sensitive to the term AS DECLARED, not to "any
        # lowercase form is safe".
        hits = catalog.find_banned_terms("stay on the main path and keep ahead of schedule")
        self.assertIn("main", hits)
        self.assertIn("ahead", hits)


class TestFindBannedTerms(unittest.TestCase):
    def test_word_boundary_avoids_partial_match(self):
        # "PR" must not match inside "print" or "approve".
        self.assertEqual(catalog.find_banned_terms("Let's print this and approve it"), [])

    def test_phrase_term_matches(self):
        hits = catalog.find_banned_terms("Confirms the primary checkout is untouched")
        self.assertIn("primary checkout", hits)

    def test_dash_prefixed_term_matches_without_left_boundary_issue(self):
        hits = catalog.find_banned_terms("pass --force to skip the prompt")
        self.assertIn("--force", hits)

    def test_case_sensitive_head_does_not_match_common_word(self):
        self.assertNotIn("HEAD", catalog.find_banned_terms("use your head to decide"))
        self.assertIn("HEAD", catalog.find_banned_terms("detached HEAD state"))


class TestVerifyCatalogFile(unittest.TestCase):
    def test_missing_file_reported_not_raised(self):
        ok, errors = catalog.verify_catalog_file(Path("/nonexistent/path/catalog.json"))
        self.assertFalse(ok)
        self.assertTrue(errors)

    def test_invalid_json_reported_not_raised(self):
        with TemporaryDirectory() as d:
            p = Path(d) / "bad.json"
            p.write_text("{not valid json", encoding="utf-8")
            ok, errors = catalog.verify_catalog_file(p)
            self.assertFalse(ok)
            self.assertTrue(errors)

    def test_valid_file_round_trips(self):
        with TemporaryDirectory() as d:
            p = Path(d) / "good.json"
            p.write_text(json.dumps(_valid_catalog()), encoding="utf-8")
            ok, errors = catalog.verify_catalog_file(p)
            self.assertTrue(ok, errors)
            self.assertEqual(errors, [])

    def test_never_raises_on_hostile_input_types(self):
        # A catalog that is valid JSON but the wrong shape entirely (e.g. a bare list, a number)
        # must produce error strings, never an exception — catalog-verify is read-only by contract.
        for hostile in ([1, 2, 3], "just a string", 42, None, True):
            errors = catalog.validate_catalog(hostile)
            self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
