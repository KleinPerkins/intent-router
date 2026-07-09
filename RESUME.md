# RESUME — the single always-current pointer

> Regenerated at each phase gate. A fresh session reads THIS first, runs `make verify` +
> `make status-verify`, then executes the exact next action below. Do not re-architect — the design
> is in `ARCHITECTURE.md` + `contracts/` + `CONSTITUTION.md`; the ledger is `status.yml`.

## Current position

- **Last completed phase:** P0 — Architecture & Contracts Freeze ✅
- **Next phase:** **R-core** — deterministic, executionless engine (L0–L2 + L5) + read-only surface.
- **Critical path:** P0 → **R-core** → A0, with the consumer's kernel-safety lanes (AWA K0/K1/K2) in
  parallel (they gate "proven", not R-core).

## Entry preconditions for R-core (all PASS)

| Precondition | State | How to confirm |
|---|---|---|
| P0 durable artifacts frozen | PASS | `make verify` green |
| Ledger honest (recomputed vs disk/tests) | PASS | `make status-verify` |
| `intent-catalog/v1`, `intent-map/v1`, `intent-feedback/v1`, constitution frozen | PASS | `make freeze` |
| `intent-proposal/v1` DEFINED (provisional; freeze deferred to A0) | PASS | `contracts/intent-proposal.v1.json` status=provisional |
| Additive-compatibility proof for all deferred phases | PASS | `tests/test_additive_compat.py` |
| zero-link | PASS | `tests/test_zero_link.py` |

## EXACT next action (R-core)

Build the deterministic, **executionless** pipeline and the read-only surface — no LLM, no
calibration, no mutation:

1. Implement **L0 normalize** (pure; may vendor agent-route `score.py`), **L1 candidates** (pure,
   explainable `why`), **L2 verdict** (`strong|weak|none`), **L5 serialize** to the
   `intent-proposal/v1` envelope. NO L3/L4 yet.
2. Activate the read-only CLI verbs `map`, `explain`, `catalog-verify`, `doctor` (replace their
   not-yet stubs in `intent_router/cli.py`); add the read-only MCP mirror. Keep **no mutating tool
   path** (CR1). **TODO (deferred from P0):** expand the CR1 no-execution grep in
   `tests/test_cli_stub.py` beyond `cli.py` to ALL runtime modules — deferred because no runtime
   modules existed in P0; it becomes load-bearing the moment R-core adds them.
3. `catalog-verify` must catch a bad `safety_class`, a missing `param_schema`, an unsafe `tool_path`,
   and host literals in a consumer catalog.
4. Write a **hand-written `intent-proposal` fixture** and a first deterministic golden set under
   `tests/golden/` that passes with LLM OFF (CR8). Prove `state_is_private` (CR3).
5. Flip the constitution machine-checks `state_is_private` (and any R-core checks) from `spec` →
   `active` with real test-ids; add those test-ids to the R-core entry in `status.yml`, set it
   `done`, and regenerate this file to point at **A0**.

**Do NOT** freeze `intent-proposal/v1` in R-core — that is A0's job (after the fixture is exercised
end-to-end by the AWA consumer).

## Recommended model

- **R-core:** `claude-sonnet-5-thinking-max` (deterministic engine; parallelizable in multitask lanes
  now that P0 interfaces are frozen). The consumer kernel-safety lanes (AWA K0/K1/K2) and A0 use
  `claude-opus-4-8-thinking-max`.

## Blocking open decisions

None blocks R-core. Tracked-but-non-blocking (resolve at their phase gate):

- Receipt/heartbeat storage paths + TTL — consumer kernel lane (K0), not router.
- PR-state source for disposition — consumer kernel lane, non-blocking for router.
- C0→C1 false-confidence numeric thresholds — numbers stay open pending trial data; metric
  DEFINITIONS were locked in P0.
- Golden-set contents grow — the format + the "calibration must not regress the golden set"
  invariant were locked in P0.
