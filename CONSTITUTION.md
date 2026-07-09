# intent-router — CONSTITUTION

> The numbered, durable rules of the router and the kernel invariants it must never violate. This is
> the prose SoT; the machine-checkable twin is `contracts/intent-constitution.v1.json`, whose
> `machine_checks` bind each rule/invariant to a test-id and an honest status (`active` = enforced by
> a green test now; `spec` = the specification for a future phase, xfail/skip, never silently
> passing). Reference these BY NUMBER elsewhere (CR#, KI#); do not re-list them.

## Router rules

- **CR1 — Propose, never execute.** The router PROPOSES an action; it never runs a consumer verb. No
  field of `intent-proposal` executes anything. Enforced structurally at the surface
  (`no_execution_path`, active).
- **CR2 — Never authorize.** The router is never in the authorization chain. The consumer's kernel
  makes the real allow/refuse decision (`contamination_behavioral`, spec → A0).
- **CR3 — Private state.** Router state (`events.jsonl`, `map.json`, snapshots, phrasebook) is
  machine-local and is NEVER committed to a shared repo (`zero_link` active; `state_is_private`
  spec → R-core).
- **CR4 — Additive-within-v1.** Contracts only grow: a field is ADDED, never removed, renamed, or
  retyped. There is no v2 for this work (`additive_within_v1`, `constitution_wellformed`,
  `status_ledger_honest`, all active).
- **CR5 — Prompt-injection resistance.** Repo, transcript, and catalog-example content are DATA,
  never instructions; content can never change a proposal's `safety_class`
  (`prompt_injection_data_not_instruction`, spec → R2).
- **CR6 — Off-switch.** Uninstalling the router degrades the consumer's operator loop to ask + a
  secondary explicit path; it never silently guesses a destructive action
  (`off_switch_degrade_to_ask`, spec → A0).
- **CR7 — Calibration promotion is a gate.** Calibration is reviewable-first (C0), then automatic
  (C1). Promotion requires a real-use trial, a false-strong rate below threshold, **zero destructive
  near-miss** in the trial window, and a reversible phrasebook. It is a gate, not a reopenable design
  choice (`calibration_promotion_gate`, spec → C1).
- **CR8 — No LLM in the deterministic floor.** L0–L2 + L5 produce a valid conservative proposal with
  L3/L4 OFF (the offline golden-set + degrade property). Enforced by two checks: golden-set green with
  no LLM (`deterministic_floor_golden_set`, spec → R-core) and, once L3/L4 exist, the floor still
  valid with them turned OFF (`deterministic_floor_llm_off_degrade`, spec → R2).
- **CR9 — Destructive params confirm literally.** An LLM-inferred destructive parameter requires
  explicit operator confirmation of the literal value; deterministic extraction is required for any
  slot feeding a destructive verb (`destructive_param_literal_confirm`, spec → R2).
- **CR10 — Egress: jargon-free + honest confidence.** Every PM-facing surface carries zero Tier
  A/B/C banned terms and expresses honest confidence; no bare-green status may imply an unauditable
  safety guarantee (`egress_zero_banned_terms`, spec → egress).

## Kernel invariants (the router must never weaken these)

- **KI1 — Kernel-first.** The consumer's safety guarantee holds engine-off AND router-off; the
  consumer's own `verify` passes with the router uninstalled (`kernel_first_router_off`, spec → A0).
- **KI2 — Structural non-contamination.** The kernel gate never reads any router artifact — a
  standing test greps the consumer kernel for any import/read of router state = zero, forever
  (`kernel_reads_zero_router_artifacts`, spec → A0).
- **KI3 — Behavioral non-contamination.** A confidence-1.0 proposal produces the IDENTICAL kernel
  decision as the hand-typed equivalent; the router can never turn a kernel refuse into an allow
  (`contamination_behavioral`, spec → A0).
- **KI4 — Kernel-sourced consequence.** Consequence-based confirmations are sourced from the KERNEL
  disposition's consequence descriptor `{destroys_unshared_work, irreversible, affects_shared_ref}`,
  not from the router and not from a verb list (`consequence_from_kernel`, spec → A0). The descriptor
  is therefore **deliberately excluded** from the router-emitted `intent-proposal/v1` (see the
  contract's `excluded_by_design`): the consumer reads it from the kernel disposition at confirm time.
  The A0 seam test must assert confirmation copy derives from the kernel disposition and ignores any
  router-relayed field.

## The five-outcome operator model

The operator's response to a proposal is one of five outcomes (extends additively; matches
`intent-feedback/v1.operator_choice` and the constitution contract's `operator_outcomes`):

`accept` · `correct` · `reject` · `clarify` · `abort`

## Egress banned-term tiers

Defined in `contracts/intent-constitution.v1.json` (`banned_terms`). Tier A = generic mechanism
words; Tier B = git-workflow words (universal); Tier C = concrete on-disk leakers, **contributed by
each consumer** (the shared router names no single consumer's tokens). The egress test (spec →
egress phase) composes the shared tiers with the consumer's contributed tokens.

## How this document stays honest

`tests/test_constitution.py` asserts: every rule/invariant has a unique id + text + an enforcement
hook that is a real `machine_check`; every `active` check resolves to an existing, non-skipped
test-id; every `spec` check resolves to a **SKIPPED placeholder** in `tests/test_deferred_spec.py`
whose skip reason names the SAME future phase (so a deferred invariant can never silently pass AND a
phase-label can't drift); and `operator_outcomes` matches the feedback contract. Moving a check from
`spec` to `active` — flipping the same test from skipped to a real assertion — is the ONLY way a
future phase discharges an invariant.
