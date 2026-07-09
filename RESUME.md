# RESUME — the single always-current pointer

> Regenerated at each phase gate. A fresh session reads THIS first, runs `make verify` +
> `make status-verify`, then executes the exact next action below. Do not re-architect — the design
> is in `ARCHITECTURE.md` + `contracts/` + `CONSTITUTION.md`; the ledger is `status.yml`.

## Current position

- **Last completed phase:** **egress — system-wide operator egress gate** ✅. Router side is the
  **egress PR** in this repo (`egress` branch; the PR URL + pinned commit are in `status.yml`); the
  AWA side is **PR #26**, already **merged to `KleinPerkins/awa` main** (`4bc7b10b`) — the authoritative
  seven-surface egress test lives there. Router PR is **open pending operator review** — do NOT
  merge/auto-merge.
- **Prior phase:** A0 — AWA consumer proof — merged to `main` via
  **PR [#4](https://github.com/KleinPerkins/intent-router/pull/4)** (`main` = `f44dbadd`).
- **Next router phase:** **R2** — LLM enrichment (optional, gated): L3 rerank + L4 typed param
  extraction, behind the deterministic floor and OFF-able.
- **Critical path:** P0 → R-core → A0 → **egress → R2**, with the consumer kernel-safety lanes
  (AWA K0/K1/K2) in parallel (they gate "proven", not the router's next action).
- **REMAINING HUMAN GATE (still open, from A0):** the **real-PM usability trial** (plan ~202) — a real
  non-technical PM driving the AWA loop end-to-end with zero banned terms — is what stamps the router
  "proven." Egress HARDENS exactly the surfaces that trial checks; the trial itself is still outstanding.

## What egress delivered (so R2 doesn't redo it)

Router side (this repo, the egress PR):
- The CR10 constitution **machine-check `egress_zero_banned_terms` `spec → active`**
  (`contracts/intent-constitution.v1.json`), following the A0 cross-repo pattern: a **router-side
  reference test** (`tests/test_deferred_spec.py::test_spec_egress_zero_banned_terms`, zero-link — the
  router never imports the consumer) proves the router's half (the shared tiers + the authoritative
  `find_banned_terms` matcher render all seven PM-facing surfaces jargon-free with honest confidence,
  and the matcher BITES per tier), and its `authoritative:` field names the cross-repo AWA proof.
- `CONSTITUTION.md` CR10 flipped to `active as of egress` (and the stale A0 status annotations
  corrected to `active as of A0`, matching the frozen JSON — doc-honesty, no behavior change).

AWA side (PR #26, merged to `KleinPerkins/awa` main):
- The AUTHORITATIVE `engine/tests/test_egress_surfaces.py::TestEgressSurfaces` — all seven PM-facing
  surfaces (chat loop, guard block, dashboard, MCP consent, save/discard confirm, doctor/status,
  detection timeline) rendered through their REAL paths, proven to carry zero Tier A/B/C banned terms
  and express honest confidence, and proven to BITE per-surface — plus `consumer/egress-gate.v1.json`.

## Entry preconditions for R2 (all PASS)

| Precondition | State | How to confirm |
|---|---|---|
| egress gate active + honest | PASS | `contracts/intent-constitution.v1.json` `egress_zero_banned_terms` = active; `make verify` |
| Ledger honest (recomputed vs disk/tests) | PASS | `make status-verify` (strict) |
| Deterministic floor green with NO LLM | PASS | `tests/test_golden.py`; `test_spec_deterministic_floor_golden_set` |
| Proposal contract frozen additive-within-v1 | PASS | `contracts/intent-proposal.v1.json` status=frozen; `test_additive_compat` |
| R2 additive surface pre-declared | PASS | `contracts/additive-manifest.json` R2 = additive (`extractor`, `confirm_literal`, `rerank_source`) |

## EXACT next action (R2)

Add **optional, OFF-able LLM enrichment** strictly BEHIND the deterministic floor — never in the
safety path:

1. L3 rerank + L4 typed param extraction as additive contract fields ONLY
   (`intent-catalog/v1`: `extractor`, `confirm_literal`; `intent-proposal/v1`: `rerank_source`) — the
   floor already pre-declares them additive; do not touch the frozen required-key floor.
2. Flip the two R2 machine-checks `spec → active`: `deterministic_floor_llm_off_degrade` (the L0–L2+L5
   floor still produces a valid conservative proposal with L3/L4 turned OFF — no golden-set regression)
   and `destructive_param_literal_confirm` (an LLM-inferred destructive param forces literal-value
   confirmation; deterministic extraction required for destructive slots). Also build the CR5
   `prompt_injection_data_not_instruction` check (a poisoned example can never change a `safety_class`).
3. The golden set MUST still pass with the LLM OFF; injection content stays DATA, never instructions.

**Do NOT** widen the router surface in R2 (that is R-surface) and do NOT start calibration (that is C0).

## Recommended model

- **R2:** `claude-opus-4-8-thinking-max` (LLM-off degrade proofs + prompt-injection adversarial
  reasoning + additive-within-v1 discipline).

## Blocking open decisions

None blocks R2. Tracked-but-non-blocking (resolve at their phase gate):

- Receipt/heartbeat storage paths + TTL — consumer kernel lane (K0), not router.
- PR-state source for disposition — consumer kernel lane, non-blocking for router.
- C0→C1 false-confidence numeric thresholds — numbers stay open pending trial data; metric
  DEFINITIONS were locked in P0.
- The **real-PM usability trial** remains the one outstanding human gate for "proven" (see above); it
  does not block starting R2.
