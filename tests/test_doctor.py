"""doctor.py tests — read-only health report. Pure, executionless (only reads files). Hermetic:
state-path checks drive `env` explicitly so the result never depends on the tester's real HOME."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from intent_router import doctor

_REPO_ROOT = Path(__file__).resolve().parent.parent
_FIXTURE_CATALOG = _REPO_ROOT / "tests" / "fixtures" / "awa-catalog.fixture.json"


def _checks_by_name(report):
    return {c["name"]: c for c in report["checks"]}


class TestHealthReport(unittest.TestCase):
    def test_clean_report_is_ok(self):
        with TemporaryDirectory() as tmp:  # a state home OUTSIDE any repo
            report = doctor.health_report(env={"XDG_STATE_HOME": tmp}, root=_REPO_ROOT)
        self.assertEqual(report["schema"], "intent-doctor/v1")
        self.assertTrue(report["ok"], report)
        checks = _checks_by_name(report)
        self.assertTrue(checks["state_path_private"]["ok"])
        # All five contracts resolve with the expected freeze-timing status.
        for fname in ("intent-catalog.v1.json", "intent-proposal.v1.json"):
            self.assertTrue(checks[f"contract:{fname}"]["ok"], checks[f"contract:{fname}"])

    def test_state_inside_a_repo_fails_the_report(self):
        with TemporaryDirectory() as tmp:
            (Path(tmp) / ".git").mkdir()  # make the state home resolve INSIDE a repo
            report = doctor.health_report(env={"XDG_STATE_HOME": tmp}, root=_REPO_ROOT)
        checks = _checks_by_name(report)
        self.assertFalse(checks["state_path_private"]["ok"], "state inside a repo must fail CR3")
        self.assertFalse(report["ok"], "a failing load-bearing check must fail the whole report")

    def test_valid_catalog_argument_passes(self):
        with TemporaryDirectory() as tmp:
            report = doctor.health_report(catalog_path=_FIXTURE_CATALOG,
                                          env={"XDG_STATE_HOME": tmp}, root=_REPO_ROOT)
        checks = _checks_by_name(report)
        self.assertIn("catalog:awa-catalog.fixture.json", checks)
        self.assertTrue(checks["catalog:awa-catalog.fixture.json"]["ok"], report)

    def test_bad_catalog_argument_fails_report(self):
        with TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text(json.dumps({"schema": "intent-catalog/v1", "verbs": [{"verb": "x"}]}), encoding="utf-8")
            report = doctor.health_report(catalog_path=bad, env={"XDG_STATE_HOME": tmp}, root=_REPO_ROOT)
        self.assertFalse(report["ok"], "an invalid requested catalog must fail the report")

    def test_golden_and_drift_are_informational(self):
        with TemporaryDirectory() as tmp:
            report = doctor.health_report(env={"XDG_STATE_HOME": tmp}, root=_REPO_ROOT)
        checks = _checks_by_name(report)
        self.assertFalse(checks["golden_sets"]["load_bearing"])
        self.assertFalse(checks["drift"]["load_bearing"])
        # The AWA golden set ships in-repo, so doctor should see at least one.
        self.assertIn("awa.golden.json", checks["golden_sets"]["detail"])

    def test_format_report_renders_pass_fail_lines(self):
        with TemporaryDirectory() as tmp:
            report = doctor.health_report(env={"XDG_STATE_HOME": tmp}, root=_REPO_ROOT)
        text = doctor.format_report(report)
        self.assertIn("intent-router doctor", text)
        self.assertIn("PASS", text)


if __name__ == "__main__":
    unittest.main()
