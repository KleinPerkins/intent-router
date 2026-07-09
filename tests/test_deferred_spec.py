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


class TestDeferredSpec(unittest.TestCase):
    @unittest.skip("SPEC: future session R-core — L0-L2+L5 produce a deterministic, executionless "
                   "proposal for the AWA golden set with LLM OFF (enforces CR8 deterministic floor).")
    def test_spec_deterministic_floor_golden_set(self):
        raise NotImplementedError

    @unittest.skip("SPEC: future session R-core — router state paths are machine-local/private and "
                   "never written under a shared repo (enforces CR3 state_is_private).")
    def test_spec_state_is_private(self):
        raise NotImplementedError

    @unittest.skip("SPEC: future session A0 — kernel decision on a confidence-1.0 proposal is "
                   "IDENTICAL to the hand-typed equivalent; router cannot flip refuse->allow "
                   "(enforces KI3 contamination_behavioral).")
    def test_spec_contamination_behavioral(self):
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
