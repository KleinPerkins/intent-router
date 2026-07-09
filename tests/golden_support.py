"""golden_support — shared loader + runner for the deterministic golden sets. NOT a test module
(unittest discovery only collects test_*.py); it is the single source of truth both
`tests/test_golden.py` and the CR8 constitution-bound check
(`tests/test_deferred_spec.py::test_spec_deterministic_floor_golden_set`) call, so the golden set is
evaluated one way, in one place.

Pure + deterministic + EXECUTIONLESS: it only loads JSON and calls `engine.propose` (no LLM, no
subprocess, no network) — exactly the L0-L2+L5 floor with L3/L4 absent.
"""

from __future__ import annotations

import json
from pathlib import Path

from intent_router.engine import propose

REPO_ROOT = Path(__file__).resolve().parent.parent
GOLDEN_DIR = REPO_ROOT / "tests" / "golden"


def load_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_golden(name: str = "awa.golden.json") -> dict:
    return load_json(GOLDEN_DIR / name)


def load_fixture_catalog(golden: dict) -> dict:
    return load_json(REPO_ROOT / golden["catalog_fixture"])


def run_case(case: dict, consumer: str, catalog: dict) -> dict:
    """Run one utterance through the deterministic floor and return the proposal."""
    return propose(consumer, case["utterance"], catalog)


def _case_failures(case: dict, proposal: dict) -> list[str]:
    """The load-bearing assertions for one case: verdict, safety_class, requires_confirmation always;
    verb when the golden pins it (expect_verb != null; null == the conservative empty-verb floor)."""
    fails: list[str] = []
    utt = case["utterance"]
    exp_verb = case.get("expect_verb")
    want_verb = "" if exp_verb is None else exp_verb
    if proposal["verb"] != want_verb:
        fails.append(f"[{utt!r}] verb: got {proposal['verb']!r} != expected {want_verb!r}")
    for field, key in (("verdict", "expect_verdict"),
                       ("safety_class", "expect_safety_class"),
                       ("requires_confirmation", "expect_requires_confirmation")):
        if key in case and proposal[field] != case[key]:
            fails.append(f"[{utt!r}] {field}: got {proposal[field]!r} != expected {case[key]!r}")
    return fails


def check_golden(name: str = "awa.golden.json") -> list[str]:
    """Run the whole golden set and return a list of human-readable failures (empty == all green).
    Also asserts DETERMINISM: each case is run twice and the full proposal must be byte-identical."""
    golden = load_golden(name)
    catalog = load_fixture_catalog(golden)
    consumer = golden.get("consumer", "unknown")
    failures: list[str] = []
    for case in golden["cases"]:
        p1 = run_case(case, consumer, catalog)
        p2 = run_case(case, consumer, catalog)
        if p1 != p2:
            failures.append(f"[{case['utterance']!r}] NON-DETERMINISTIC: {p1} != {p2}")
        failures.extend(_case_failures(case, p1))
    return failures


def injection_cases(name: str = "awa.golden.json") -> list[dict]:
    return [c for c in load_golden(name)["cases"] if c.get("category") == "injection"]
