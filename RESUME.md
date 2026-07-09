# RESUME — the single always-current pointer

> Regenerated at each phase gate. A fresh session reads THIS first, runs `make verify` +
> `make status-verify`, then executes the exact next action below. Do not re-architect — the design
> is in `ARCHITECTURE.md` + `contracts/` + `CONSTITUTION.md`; the ledger is `status.yml`.

## Current position

- **Last completed phase:** **A0 — AWA consumer proof** ✅ (router side is
  **PR [#4](https://github.com/KleinPerkins/intent-router/pull/4)**, `a0/proposal-freeze`, commit
  `558500f`; the AWA side is the **sibling PR in `KleinPerkins/awa`**). Both PRs are **open pending
  operator review** — do NOT merge/auto-merge.
- **Prior phase:** R-core (deterministic executionless engine L0–L2+L5 + read-only surface) — merged
  to `main` via PRs [#2](https://github.com/KleinPerkins/intent-router/pull/2) +
  [#3](https://github.com/KleinPerkins/intent-router/pull/3), now at `main` = `607d3443`.
- **Next router phase:** **egress** — the system-wide operator egress gate (a CI test proving zero
  Tier A/B/C banned terms + honest confidence across all seven PM-facing surfaces).
- **Critical path:** P0 → R-core → A0 → **egress**, with the consumer kernel-safety lanes
  (AWA K0/K1/K2) in parallel (they gate "proven", not the router's next action).
- **REMAINING HUMAN GATE for A0:** the **real-PM usability trial** (plan ~202) — a real
  non-technical PM driving the AWA loop end-to-end with zero banned terms — is what stamps the router
  "proven." A0 implementation is complete and an **agent-driven rehearsal** was run, but that one
  human trial is still outstanding.

## What A0 delivered (so egress doesn't redo it)

Router side (this repo, PR #4):
- `intent-proposal/v1` **EXERCISED** then **FROZEN** additive-within-v1 (`provisional → frozen`,
  `2026-07-09`; `freeze_exempt: false`). Breadth exercise: `tests/test_proposal_exercise.py`;
  single-utterance fixture: `tests/test_proposal_fixture.py`. The 11-key required floor is now
  immutable-within-v1; enums extend-only. Checker (`checks/intent-contract-freeze.sh`), doctor
  (`intent_router/doctor.py`), the fixture freeze-guard, and freeze regression tests all flipped to
  expect frozen; additive proof in `contracts/additive-manifest.json` (`test_additive_compat`).
- Four A0 constitution **machine-checks `spec → active`** (`contracts/intent-constitution.v1.json`):
  `off_switch_degrade_to_ask`/`kernel_first_router_off` (CR6/KI1), `kernel_reads_zero_router_artifacts`
  (KI2), `contamination_behavioral` (KI3), `consequence_from_kernel` (KI4). Each is a **router-side
  reference test** in `tests/test_deferred_spec.py` (a router-agnostic reference kernel model —
  **zero-link**, the router never imports the consumer) and carries an `authoritative:` field naming
  the cross-repo AWA test that proves it end-to-end over the REAL kernel.

AWA side (sibling PR in `KleinPerkins/awa`):
- Real `intent-catalog/v1` (5 operator outcomes / 6 verbs) that passes this router's `catalog-verify`
  with zero Tier A/B/C banned terms; a thin operator loop (hear → `intent map` → confirm-consequence →
  execute an AWA verb → verify-real-outcome → narrate → record-feedback); plain-language translators
  with honest confidence; **kernel-sourced** consequence confirmations; a 30-utterance golden set; a
  **seam test** pinning this router's contract-version strings; structural + behavioral contamination
  tests; and the off-switch/kernel-first proof (**AWA `make verify` passes with the router
  UNINSTALLED**).

## Entry preconditions for egress (all PASS)

| Precondition | State | How to confirm |
|---|---|---|
| A0 router side green + frozen proposal | PASS | `make verify` green; `contracts/intent-proposal.v1.json` status=frozen |
| Ledger honest (recomputed vs disk/tests) | PASS | `make status-verify` (strict) |
| AWA operator loop + real catalog exist | PASS | sibling `KleinPerkins/awa` PR (consumer/) |
| The seven PM-facing surfaces enumerated | PASS | `contracts/egress-terms.checklist.json` |
| Egress matcher (case-insensitive, full-field) | PASS | `catalog.py` `find_banned_terms`; `tests/test_catalog_egress.py` |

## EXACT next action (egress)

Ship the **system-wide operator egress gate** (CR10): one CI test that scans **all seven** PM-facing
surfaces and asserts **zero** Tier A/B/C banned terms **and** honest confidence on each.

1. Confirm the seven-surface inventory in `contracts/egress-terms.checklist.json` is complete
   (proposal reasons, confirmation copy, block/refusal copy, narration, need-more-info prompts,
   degrade-to-ask copy, and the catalog's PM strings).
2. Flip the CR10 machine-check `egress` from `spec → active`: replace the
   `tests.test_deferred_spec.TestDeferredSpec.test_spec_egress_zero_banned_terms` placeholder with a
   real test that composes every surface and runs the authoritative `find_banned_terms` over it, plus
   an honest-confidence assertion (no bare "green pill").
3. Keep the matcher **single-sourced** (the frozen constitution tiers + the router matcher); the AWA
   consumer snapshot must stay a superset (the seam drift-guard already asserts this).
4. Add the egress test-id(s) to `status.yml`, set `egress` `done` with its PR + commit, and
   regenerate this file to point at **R2**.

**Do NOT** widen the router surface in egress (that is R-surface) and do NOT add L3/L4 (that is R2).

## Recommended model

- **egress:** `claude-opus-4-8-thinking-max` (exhaustive surface coverage + honest-confidence
  judgment + zero-link discipline).

## Blocking open decisions

None blocks egress. Tracked-but-non-blocking (resolve at their phase gate):

- Receipt/heartbeat storage paths + TTL — consumer kernel lane (K0), not router.
- PR-state source for disposition — consumer kernel lane, non-blocking for router.
- C0→C1 false-confidence numeric thresholds — numbers stay open pending trial data; metric
  DEFINITIONS were locked in P0.
- The **real-PM usability trial** for A0 remains the one outstanding human gate (see above); it does
  not block starting egress, but A0 is not "proven" until it is run.
