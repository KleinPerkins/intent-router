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

import inspect
import json
import re
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from intent_router import state
from intent_router.engine import propose
from tests import golden_support

_REPO = Path(__file__).resolve().parent.parent


def _fixture_catalog() -> dict:
    return json.loads((_REPO / "tests" / "fixtures" / "awa-catalog.fixture.json").read_text(encoding="utf-8"))


def _proposal_contract() -> dict:
    return json.loads((_REPO / "contracts" / "intent-proposal.v1.json").read_text(encoding="utf-8"))


# ---- A0 reference consumer-kernel model (router-agnostic; zero-link; NOT the real kernel) ----------
# These reference functions model the SHAPE of a consumer's kernel WITHOUT importing it (the real
# kernel lives in KleinPerkins/awa and is proven there). They key ONLY off (verb, facts) / a kernel
# disposition — never off a router proposal — which is exactly the ROUTER-SIDE half of KI2/KI3/KI4:
# the router provides nothing a kernel must read, and no proposal field can enter a kernel decision.
# The AUTHORITATIVE end-to-end proofs over the REAL kernel are the cross-repo AWA tests cited in each
# method's docstring (and in contracts/intent-constitution.v1.json machine_checks[...].authoritative).
_REMOVE_EFFECT_VERBS = {"cleanup"}


def _reference_kernel_decision(verb, facts):
    """A pure consequence gate: a function of (verb, facts) ONLY. There is no proposal parameter, so a
    router proposal cannot participate in the decision by construction."""
    removes = verb in _REMOVE_EFFECT_VERBS
    destroys = removes and bool(facts.get("has_unshared_work"))
    return {"requires_confirmation": bool(removes or facts.get("is_write")),
            "destroys_unshared_work": destroys, "irreversible": destroys}


def _reference_confirmation_from_kernel(disposition):
    """A confirmation sourced ONLY from a kernel disposition. Takes NO proposal argument, so a
    router-relayed consequence cannot source it even if one is injected into the proposal."""
    return {"requires_confirmation": bool(disposition.get("requires_confirmation")),
            "risk_spelled_out": bool(disposition.get("destroys_unshared_work"))}


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

    def test_spec_contamination_behavioral(self):
        """ACTIVE as of A0 (was spec). KI3 (router side): the router can NEVER move a kernel decision.
        A confidence-1.0 proposal for a destructive verb yields the IDENTICAL reference-kernel decision
        as the hand-typed verb (the decision is a pure fn of verb+facts with NO proposal input), and
        the router's own proposal for that utterance never downgrades to a no-confirm read. AUTHORITATIVE
        end-to-end proof over the REAL kernel: KleinPerkins/awa
        engine/tests/test_consumer_contamination_behavioral.py (cross-repo)."""
        catalog = _fixture_catalog()
        facts = {"has_unshared_work": True}
        confident = propose("awa", "clean up my old safe copy", catalog)
        self.assertEqual(confident["verb"], "cleanup")
        # router-side conservatism: a destructive utterance never becomes a no-confirm read
        self.assertNotEqual(confident["safety_class"], "read")
        self.assertIs(confident["requires_confirmation"], True)
        # the kernel decision is invariant to the proposal (identical to the hand-typed equivalent)
        self.assertEqual(_reference_kernel_decision(confident["verb"], facts),
                         _reference_kernel_decision("cleanup", facts))
        self.assertTrue(_reference_kernel_decision("cleanup", facts)["destroys_unshared_work"])
        # structural: a proposal CANNOT enter the kernel decision (no such parameter exists)
        self.assertEqual(list(inspect.signature(_reference_kernel_decision).parameters), ["verb", "facts"])
        # and the proposal is executionless — pure data, nothing callable that could flip a decision
        self.assertTrue(all(not callable(v) for v in confident.values()))

    def test_spec_consequence_from_kernel(self):
        """ACTIVE as of A0 (was spec). KI4 (router side): consequence confirmations are KERNEL-sourced.
        intent-proposal/v1 EXCLUDES consequence_descriptor by design, a real proposal carries no such
        field, and a reference confirmation sourced from the kernel disposition IGNORES a router-relayed
        consequence even when one is injected into the proposal. AUTHORITATIVE proof over the real
        kernel: KleinPerkins/awa engine/tests/test_consumer_consequence.py (cross-repo)."""
        contract = _proposal_contract()
        self.assertNotIn("consequence_descriptor", contract["required_keys"])
        self.assertNotIn("consequence_descriptor", contract.get("optional_keys", {}))
        self.assertIn("consequence_descriptor", contract["excluded_by_design"])
        p = propose("awa", "clean up my old safe copy", _fixture_catalog())
        self.assertNotIn("consequence_descriptor", p)
        # inject a LYING consequence into the proposal; the kernel-sourced confirmation ignores it
        p_poisoned = dict(p)
        p_poisoned["consequence_descriptor"] = {"destroys_unshared_work": False, "requires_confirmation": False}
        kernel_truth = {"destroys_unshared_work": True, "requires_confirmation": True}
        confirm = _reference_confirmation_from_kernel(kernel_truth)
        self.assertTrue(confirm["requires_confirmation"],
                        "confirmation must derive from the KERNEL disposition, not the proposal")
        self.assertTrue(confirm["risk_spelled_out"])
        # structural: the confirmation source takes NO proposal argument (a proposal cannot source it)
        self.assertEqual(list(inspect.signature(_reference_confirmation_from_kernel).parameters),
                         ["disposition"])

    def test_spec_kernel_reads_zero_router_artifacts(self):
        """ACTIVE as of A0 (was spec). KI2 (router side): a reference consumer-kernel decision reaches
        its result with ZERO router artifacts — its source imports/reads nothing from the router — so
        the router forces no coupling on a consumer kernel. AUTHORITATIVE standing grep over the REAL
        kernel surface (= zero, forever): KleinPerkins/awa
        engine/tests/test_consumer_contamination_structural.py (cross-repo)."""
        src = (inspect.getsource(_reference_kernel_decision) + "\n"
               + inspect.getsource(_reference_confirmation_from_kernel))
        for pat in (r"intent[_-]?router", r"import\s+\w*router", r"from\s+\w*router",
                    r"router[\w-]*\.(json|db|state|ya?ml)"):
            self.assertIsNone(re.search(pat, src, re.I),
                              f"reference kernel model references a router artifact ({pat})")
        # it decides using only its args — no router import is needed for a kernel to reach a decision
        self.assertTrue(_reference_kernel_decision("cleanup", {"has_unshared_work": True})["requires_confirmation"])

    def test_spec_off_switch_and_kernel_first(self):
        """ACTIVE as of A0 (was spec). KI1 + CR6 (router side): when the router is absent a reference
        operator loop DEGRADES to ask + a secondary explicit path and never auto-runs a destructive
        action; the router only ever PROPOSES (engine.propose) and exposes no execution entry point
        that could bypass the off-switch. AUTHORITATIVE proof (the REAL loop degrading + AWA
        `make verify` passing with the router UNINSTALLED): KleinPerkins/awa
        engine/tests/test_consumer_offswitch.py (cross-repo)."""
        from intent_router import engine as engine_mod
        ran = []

        def ref_loop(router, utterance):
            if router is None:                     # router uninstalled -> off-switch
                return {"decision": "ask", "secondary_explicit_path": True}
            prop = router("awa", utterance, _fixture_catalog())
            ran.append(prop)
            return {"decision": "propose", "proposal": prop}

        off = ref_loop(None, "clean up everything now")
        self.assertEqual(off["decision"], "ask")
        self.assertTrue(off["secondary_explicit_path"])
        self.assertEqual(ran, [], "router-off must never auto-run a verb")
        # the router is proposal-only: it exposes propose and no execute/run/apply/perform entry point
        self.assertTrue(hasattr(engine_mod, "propose"))
        for forbidden in ("execute", "run", "apply", "perform"):
            self.assertFalse(hasattr(engine_mod, forbidden),
                             f"the router must expose no '{forbidden}' entry point (it only proposes)")

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
