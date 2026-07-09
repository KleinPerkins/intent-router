"""CLI end-to-end tests for the four activated read-only verbs (map/explain/catalog-verify/doctor).

Drives `cli.main(argv)` and captures stdout/stderr. Read-only: no verb mutates anything; catalog-
verify returns a nonzero exit on a bad catalog so it is usable as a gate.
"""

from __future__ import annotations

import copy
import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

from intent_router import cli

_REPO_ROOT = Path(__file__).resolve().parent.parent
_FIXTURE = str(_REPO_ROOT / "tests" / "fixtures" / "awa-catalog.fixture.json")


def _run(argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        try:
            rc = cli.main(argv)
        except SystemExit as exc:
            rc = exc.code
    return rc, out.getvalue(), err.getvalue()


class TestMap(unittest.TestCase):
    def test_map_strong_protect_json(self):
        rc, out, _ = _run(["map", "put this work somewhere safe", "--catalog", _FIXTURE, "--json"])
        self.assertEqual(rc, 0)
        proposal = json.loads(out)
        self.assertEqual(proposal["verb"], "protect")
        self.assertEqual(proposal["safety_class"], "write")
        self.assertEqual(proposal["verdict"], "strong")

    def test_map_human_output(self):
        rc, out, _ = _run(["map", "is everything okay", "--catalog", _FIXTURE])
        self.assertEqual(rc, 0)
        self.assertIn("verb=status", out)
        self.assertIn("verdict=weak", out)

    def test_map_negative_degrades_conservative(self):
        rc, out, _ = _run(["map", "what is the weather", "--catalog", _FIXTURE, "--json"])
        self.assertEqual(rc, 0)
        proposal = json.loads(out)
        self.assertEqual(proposal["verdict"], "none")
        self.assertEqual(proposal["safety_class"], "destructive")
        self.assertIs(proposal["requires_confirmation"], True)

    def test_map_missing_catalog_is_error_not_crash(self):
        rc, _out, err = _run(["map", "hello", "--catalog", "/no/such/catalog.json"])
        self.assertEqual(rc, 1)
        self.assertIn("catalog error", err)


class TestExplain(unittest.TestCase):
    def test_explain_lists_candidates(self):
        rc, out, _ = _run(["explain", "put this work somewhere safe", "--catalog", _FIXTURE, "--json"])
        self.assertEqual(rc, 0)
        data = json.loads(out)
        self.assertEqual(data["proposal"]["verb"], "protect")
        self.assertGreaterEqual(len(data["candidates"]), 1)

    def test_explain_top_n(self):
        rc, out, _ = _run(["explain", "safe copy", "--catalog", _FIXTURE, "--top", "2", "--json"])
        self.assertEqual(rc, 0)
        data = json.loads(out)
        self.assertLessEqual(len(data["candidates"]), 2)


class TestCatalogVerify(unittest.TestCase):
    def test_valid_fixture_passes(self):
        rc, out, _ = _run(["catalog-verify", _FIXTURE])
        self.assertEqual(rc, 0)
        self.assertIn("OK", out)

    def test_bad_catalog_fails_with_nonzero(self):
        with TemporaryDirectory() as d:
            bad = Path(d) / "bad.json"
            bad.write_text(json.dumps({
                "schema": "intent-catalog/v1",
                "verbs": [{"verb": "x", "aliases": [], "examples": [], "param_schema": [],
                           "preconditions": [], "safety_class": "nope", "tool_path": "shell",
                           "start_point_rules": {}, "plain_label": "run the guard",
                           "consequence_copy": "acquires a lease"}],
            }), encoding="utf-8")
            rc, _out, err = _run(["catalog-verify", str(bad), "--json"])
        self.assertEqual(rc, 1)  # nonzero exit on a bad catalog (usable as a gate)

    def test_bad_catalog_json_report_lists_errors(self):
        with TemporaryDirectory() as d:
            bad = Path(d) / "bad.json"
            bad.write_text(json.dumps({
                "schema": "intent-catalog/v1",
                "verbs": [{"verb": "x", "aliases": [], "examples": [], "param_schema": [],
                           "preconditions": [], "safety_class": "nope", "tool_path": "shell",
                           "start_point_rules": {}, "plain_label": "ok", "consequence_copy": "ok"}],
            }), encoding="utf-8")
            rc, out, _ = _run(["catalog-verify", str(bad), "--json"])
        self.assertEqual(rc, 1)
        report = json.loads(out)
        self.assertFalse(report["ok"])
        self.assertTrue(report["errors"])


# A single KNOWN-VALID verb (a deep-copyable stand-in — jargon-free copy, valid enums, one required
# param). Each single-defect test below injects EXACTLY ONE abuse into a fresh deep copy so a
# regression in one checker class turns exactly one test RED and cannot be masked by a co-occurring
# defect (the pre-existing bad-catalog tests bundle several defects at once and cannot isolate).
_VALID_VERB = {
    "verb": "protect",
    "aliases": ["protect", "keep this safe"],
    "examples": ["put this work somewhere safe"],
    "param_schema": [
        {"name": "target_path", "type": "path", "required": True, "source": "repo-resolver"}
    ],
    "preconditions": ["target_path is a project folder"],
    "safety_class": "write",
    "tool_path": "mcp",
    "start_point_rules": {"default": "current"},
    "plain_label": "Start protecting this work",
    "consequence_copy": "Creates a separate safe copy so your original files stay untouched.",
}


def _catalog_with(verb: dict) -> dict:
    return {"schema": "intent-catalog/v1", "consumer": "awa", "verbs": [verb]}


def _verify_catalog(catalog: dict):
    """Write `catalog` to a temp file and drive the real `intent catalog-verify --json` CLI. Returns
    (rc, report). E2E: exercises the shipped checker through the CLI, not an in-proc re-impl."""
    with TemporaryDirectory() as d:
        p = Path(d) / "cat.json"
        p.write_text(json.dumps(catalog), encoding="utf-8")
        rc, out, _ = _run(["catalog-verify", str(p), "--json"])
    return rc, json.loads(out)


class TestCatalogVerifySingleDefect(unittest.TestCase):
    """One abuse class per test — each starts from `_VALID_VERB` and injects a single defect. Every
    test asserts (a) nonzero exit, (b) the expected error class is reported, and (c) it is the ONLY
    error (exactly-one isolation), so a regressed class is unambiguously attributable."""

    def test_base_is_valid_guard(self):
        # Guard: the single-defect base must itself PASS, or the isolation below would be vacuous.
        rc, report = _verify_catalog(_catalog_with(copy.deepcopy(_VALID_VERB)))
        self.assertEqual(rc, 0, report)
        self.assertTrue(report["ok"])
        self.assertEqual(report["errors"], [])

    def _assert_single(self, report, marker: str):
        self.assertFalse(report["ok"])
        self.assertEqual(len(report["errors"]), 1,
                         f"expected exactly ONE (isolated) error, got: {report['errors']}")
        self.assertIn(marker, report["errors"][0])

    def test_only_bad_safety_class(self):
        v = copy.deepcopy(_VALID_VERB)
        v["safety_class"] = "nope"
        rc, report = _verify_catalog(_catalog_with(v))
        self.assertEqual(rc, 1)
        self._assert_single(report, "bad safety_class")

    def test_only_unsafe_tool_path(self):
        v = copy.deepcopy(_VALID_VERB)
        v["tool_path"] = "shell"  # not in the frozen {cli,mcp,hook} allowlist
        rc, report = _verify_catalog(_catalog_with(v))
        self.assertEqual(rc, 1)
        self._assert_single(report, "unsafe tool_path")

    def test_only_missing_required_param_key(self):
        v = copy.deepcopy(_VALID_VERB)
        v["param_schema"][0].pop("required")  # required param-floor key
        rc, report = _verify_catalog(_catalog_with(v))
        self.assertEqual(rc, 1)
        self._assert_single(report, "param_schema[0]: missing required key(s)")
        self.assertIn("required", report["errors"][0])

    def test_only_bad_param_type(self):
        v = copy.deepcopy(_VALID_VERB)
        v["param_schema"][0]["type"] = "nope"
        rc, report = _verify_catalog(_catalog_with(v))
        self.assertEqual(rc, 1)
        self._assert_single(report, "bad type")

    def test_only_missing_required_verb_key(self):
        # The exact drift the reviewer proved: dropping a frozen-required verb key. Because the
        # validator's floor is LOADED from contracts/intent-catalog.v1.json (fix #2), this is a
        # catalog-verify failure — no hand-copied constant to fall out of sync.
        v = copy.deepcopy(_VALID_VERB)
        v.pop("preconditions")
        rc, report = _verify_catalog(_catalog_with(v))
        self.assertEqual(rc, 1)
        self._assert_single(report, "missing required key(s)")
        self.assertIn("preconditions", report["errors"][0])

    def test_only_banned_literal_capitalized_plain_label(self):
        # fix #1 (case-insensitivity) via the CLI: a CAPITALIZED host term must be caught.
        v = copy.deepcopy(_VALID_VERB)
        v["plain_label"] = "Protect your WORKTREE"
        rc, report = _verify_catalog(_catalog_with(v))
        self.assertEqual(rc, 1)
        self._assert_single(report, "leaked host-policy literal")
        self.assertIn("plain_label", report["errors"][0])

    def test_only_banned_literal_in_start_point_rules(self):
        # fix #1 (field coverage) via the CLI: start_point_rules values flow into proposal.start_point
        # and MUST be scanned. ("detached HEAD worktree" leaks both HEAD and worktree.)
        v = copy.deepcopy(_VALID_VERB)
        v["start_point_rules"] = {"default": "detached HEAD worktree"}
        rc, report = _verify_catalog(_catalog_with(v))
        self.assertEqual(rc, 1)
        self._assert_single(report, "leaked host-policy literal")
        self.assertIn("start_point_rules.default", report["errors"][0])

    def test_only_banned_literal_in_alias(self):
        # fix #1 (field coverage) via the CLI: aliases render into why[] on CLI + MCP.
        v = copy.deepcopy(_VALID_VERB)
        v["aliases"] = ["protect", "orphan branch"]
        rc, report = _verify_catalog(_catalog_with(v))
        self.assertEqual(rc, 1)
        self._assert_single(report, "leaked host-policy literal")
        self.assertIn("aliases[1]", report["errors"][0])


class TestDoctor(unittest.TestCase):
    def test_doctor_json_runs(self):
        rc, out, _ = _run(["doctor", "--json"])
        report = json.loads(out)
        self.assertEqual(report["schema"], "intent-doctor/v1")
        # All contract checks are machine-independent and must pass.
        for c in report["checks"]:
            if c["name"].startswith("contract:"):
                self.assertTrue(c["ok"], c)
        self.assertEqual(rc, 0 if report["ok"] else 1)

    def test_doctor_with_catalog(self):
        rc, out, _ = _run(["doctor", "--catalog", _FIXTURE, "--json"])
        report = json.loads(out)
        names = {c["name"] for c in report["checks"]}
        self.assertIn("catalog:awa-catalog.fixture.json", names)


class TestSurface(unittest.TestCase):
    def test_help_lists_active_and_later_verbs(self):
        rc, out, _ = _run(["--help"])
        self.assertEqual(rc, 0)
        self.assertIn("map", out)
        self.assertIn("catalog-verify", out)

    def test_unknown_verb_usage_error(self):
        rc, _out, err = _run(["frobnicate"])
        self.assertEqual(rc, 2)
        self.assertIn("unknown verb", err)

    def test_later_verb_still_not_yet(self):
        rc, _out, err = _run(["calibrate"])
        self.assertEqual(rc, cli.NOT_YET)
        self.assertIn("not yet", err.lower())


if __name__ == "__main__":
    unittest.main()
