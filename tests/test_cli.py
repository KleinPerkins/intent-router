"""CLI end-to-end tests for the four activated read-only verbs (map/explain/catalog-verify/doctor).

Drives `cli.main(argv)` and captures stdout/stderr. Read-only: no verb mutates anything; catalog-
verify returns a nonzero exit on a bad catalog so it is usable as a gate.
"""

from __future__ import annotations

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
