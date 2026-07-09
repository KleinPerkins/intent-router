"""Deferred-phase behavioral SPEC tests — the executable specification for future sessions.

These are NOT P0 gates. Each is a placeholder for a behavioral test a future phase MUST implement,
marked `skip` with a "SPEC: future session <phase>" reason so it shows up as skipped (never
silently passing). A future session replaces the skip + body with the real assertion and flips the
matching machine_check in contracts/intent-constitution.v1.json from `spec` to `active`.

They intentionally require runtime that does not exist in P0 (routing logic, a consumer catalog,
kernel integration), so they cannot be written as green tests today. Keeping them here makes the
future test surface visible and greppable.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from intent_router import state
from intent_router.engine import propose
from tests import golden_support


class TestDeferredSpec(unittest.TestCase):
    def test_spec_deterministic_floor_golden_set(self):
        """ACTIVE as of R-core (was spec). CR8 (R-core half): the L0-L2+L5 deterministic floor — with
        NO LLM (L3/L4 are absent, not toggled) — produces the pinned proposal for every AWA golden
        utterance, deterministically, and prompt-injection content cannot weaken a proposal's
        safety_class or skip its confirmation. Granular coverage: tests/test_golden.py; single runner:
        tests/golden_support.py."""
        failures = golden_support.check_golden()
        self.assertEqual(failures, [], "deterministic golden set drift:\n" + "\n".join(failures))
        catalog = golden_support.load_fixture_catalog(golden_support.load_golden())
        for case in golden_support.injection_cases():
            p = propose("awa", case["utterance"], catalog)
            self.assertNotEqual(p["safety_class"], "read", case["utterance"])
            self.assertIs(p["requires_confirmation"], True, case["utterance"])

    @unittest.skip("SPEC: future session R2 — with L3/L4 (LLM) added then turned OFF, the L0-L2+L5 "
                   "floor STILL produces a valid conservative proposal; no golden-set regression "
                   "(enforces CR8 deterministic_floor_llm_off_degrade).")
    def test_spec_deterministic_floor_llm_off_degrade(self):
        raise NotImplementedError

    def test_spec_state_is_private(self):
        """ACTIVE as of R-core (was spec). CR3: router state resolves to a machine-local XDG path and
        the guard refuses any path inside a git working tree. Granular coverage: tests/test_state.py."""
        self.assertEqual(state.state_dir({"XDG_STATE_HOME": "/x/y"}), Path("/x/y/intent-router"))
        with TemporaryDirectory() as repo_tmp:
            (Path(repo_tmp) / ".git").mkdir()
            with self.assertRaises(RuntimeError):
                state.assert_private(Path(repo_tmp) / "intent-router")
        with TemporaryDirectory() as clean_tmp:
            target = Path(clean_tmp) / "intent-router"
            self.assertEqual(state.assert_private(target), target.resolve())

    @unittest.skip("SPEC: future session A0 — kernel decision on a confidence-1.0 proposal is "
                   "IDENTICAL to the hand-typed equivalent; router cannot flip refuse->allow "
                   "(enforces KI3 contamination_behavioral).")
    def test_spec_contamination_behavioral(self):
        raise NotImplementedError

    @unittest.skip("SPEC: future session A0 — consequence-confirmation copy derives from the KERNEL "
                   "disposition's consequence descriptor and IGNORES any router-relayed field, even "
                   "if present (enforces KI4 consequence_from_kernel).")
    def test_spec_consequence_from_kernel(self):
        raise NotImplementedError

    @unittest.skip("SPEC: future session A0 — grep proves the consumer kernel reads ZERO router "
                   "artifacts (enforces KI2 kernel_reads_zero_router_artifacts).")
    def test_spec_kernel_reads_zero_router_artifacts(self):
        raise NotImplementedError

    @unittest.skip("SPEC: future session A0 — consumer verify passes with the router uninstalled; "
                   "the operator loop degrades to ask + secondary explicit path (KI1 + CR6).")
    def test_spec_off_switch_and_kernel_first(self):
        raise NotImplementedError

    @unittest.skip("SPEC: future session R2 — repo/transcript/catalog content is DATA; a poisoned "
                   "example can never change a proposal's safety_class (enforces CR5 prompt-injection).")
    def test_spec_prompt_injection_data_not_instruction(self):
        raise NotImplementedError

    @unittest.skip("SPEC: future session R2 — an LLM-inferred destructive param forces literal-value "
                   "confirmation; deterministic extraction required for destructive slots (CR9).")
    def test_spec_destructive_param_literal_confirm(self):
        raise NotImplementedError

    @unittest.skip("SPEC: future session egress — all seven PM-facing surfaces carry zero Tier "
                   "A/B/C banned terms and express honest confidence (enforces CR10 egress gate).")
    def test_spec_egress_zero_banned_terms(self):
        raise NotImplementedError

    @unittest.skip("SPEC: future session C1 — calibration promotion gate: real-use trial, "
                   "false-strong under threshold, ZERO destructive near-miss, reversible phrasebook "
                   "(enforces CR7 calibration_promotion_gate).")
    def test_spec_calibration_promotion_gate(self):
        raise NotImplementedError


if __name__ == "__main__":
    unittest.main()
