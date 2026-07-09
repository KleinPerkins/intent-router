# RESUME — the single always-current pointer

> Regenerated at each phase gate. A fresh session reads THIS first, runs `make verify` +
> `make status-verify`, then executes the exact next action below. Do not re-architect — the design
> is in `ARCHITECTURE.md` + `contracts/` + `CONSTITUTION.md`; the ledger is `status.yml`.

## Current position

- **Last completed phase:** R-core — deterministic, executionless engine (L0–L2 + L5) + read-only
  surface ✅. The phase **merged to `main` via PR [#2](https://github.com/KleinPerkins/intent-router/pull/2)**
  (commit `7ef9bbc`). A review-swarm **fix pass** (honesty/drift/denylist) is carried by
  **PR [#3](https://github.com/KleinPerkins/intent-router/pull/3)** (commit `bfe270b`, `r-core → main`,
  **pending operator merge**): case-insensitive + full-field egress scan, catalog-verify floor bound
  to the frozen contract, AST-based no-execution denylist, CR1 rebound to the whole-surface test,
  `status_verify --strict` (PR resolve + commit ancestry + git-missing fail-closed), and
  honest-confidence de-escalation on competing destructive+read signals.
- **Next phase:** **A0** — AWA consumer proof (real catalog + operator loop + `intent-proposal/v1`
  freeze + contamination/off-switch proofs + real-PM trial).
- **Critical path:** P0 → R-core → **A0**, with the consumer kernel-safety lanes (AWA K0/K1/K2) in
  parallel (they gate "proven", not A0's router work).

## What R-core delivered (so A0 doesn't redo it)

- Engine: `intent_router/{normalize,candidates,verdict,proposal,engine}.py` — pure, deterministic,
  executionless; `none` verdict degrades to the maximally conservative floor.
- Read-only surface: CLI `intent map|explain|catalog-verify|doctor` (`cli.py`) + stdlib-only MCP
  mirror `intent_map|intent_explain|intent_catalog_verify|intent_doctor` (`mcp_server.py`). No
  mutating verb/tool anywhere.
- `catalog-verify` bites on bad `safety_class` / missing `param_schema` / unsafe `tool_path` /
  leaked host-policy literals (`catalog.py`, `tests/test_catalog.py`).
- AWA **test-fixture** catalog + 30-utterance golden set (`tests/fixtures/awa-catalog.fixture.json`,
  `tests/golden/awa.golden.json`, `tests/golden_support.py`) — green on the floor; injection can't
  flip `safety_class` or skip confirmation.
- Hand-written `intent-proposal/v1` fixture exercised (`tests/fixtures/awa-proposal.fixture.json`).
  **Contract still `provisional`** — freeze is A0's job.
- CR1 no-execution scan across ALL runtime modules (`tests/test_no_execution.py`); CR3 private-state
  (`state.py`). Constitution checks `state_is_private` (CR3) + `deterministic_floor_golden_set`
  (CR8) are now `active`.

## Entry preconditions for A0 (all PASS)

| Precondition | State | How to confirm |
|---|---|---|
| R-core deterministic floor green | PASS | `make verify` green |
| Ledger honest (recomputed vs disk/tests) | PASS | `make status-verify` |
| `intent-proposal/v1` PROVISIONAL (ready to exercise→freeze) | PASS | `contracts/intent-proposal.v1.json` status=provisional |
| Read-only CLI + MCP surface exists | PASS | `intent --help`; `tests/test_cli.py`, `tests/test_mcp.py` |
| Deterministic golden set + injection resistance | PASS | `tests/test_golden.py` |

## EXACT next action (A0)

Prove the AWA consumer end-to-end and freeze the proposal seam. **The router only proposes; the
AWA kernel decides + executes** (CR2) — A0 builds the consumer side, not new router execution.

1. **Author the REAL AWA `intent-catalog/v1`** in the AWA consumer repo (the R-core one under
   `tests/fixtures/` is a stand-in). Jargon-free PM copy (zero Tier A/B/C banned terms) — it must
   pass `intent catalog-verify`.
2. **Build the AWA operator loop** that calls the read-only surface (`intent map`/MCP `intent_map`),
   shows the proposal + `consequence_copy`, and routes to the kernel's confirm/execute path. The
   kernel makes the allow/refuse decision from its OWN facts (never a router-only field).
3. **Exercise then FREEZE `intent-proposal/v1`**: after the fixture seam is exercised against the
   real catalog, flip the contract `provisional → frozen` (add freeze strings + `frozen` date, set
   `freeze_exempt: false`, add it to `checks/intent-contract-freeze.sh` EXPECTED as `frozen`). Keep
   it additive-within-v1 (CR4).
4. **Flip the A0 constitution machine-checks `spec → active`** with real test-ids:
   `contamination_behavioral` + `kernel_reads_zero` + `consequence_from_kernel` (CR2 family),
   `off_switch_degrade_to_ask` (CR6), `kernel_first`. Prove: injection/contamination can't change the
   kernel's decision; uninstalling the router degrades the loop to ask + a secondary explicit path
   (never a silent destructive guess).
5. **Real-PM trial** of the AWA loop; record the result. Then add the A0 test-ids to `status.yml`,
   set A0 `done`, and regenerate this file to point at **egress**.

**Do NOT** widen the router surface in A0 (that is R-surface) and do NOT add L3/L4 (that is R2).

## Recommended model

- **A0:** `claude-opus-4-8-thinking-max` (consumer-integration + freeze decision + contamination
  reasoning + real-PM trial judgment). Keep the AWA kernel lanes (K0/K1/K2) on opus as well.

## Blocking open decisions

None blocks A0. Tracked-but-non-blocking (resolve at their phase gate):

- Receipt/heartbeat storage paths + TTL — consumer kernel lane (K0), not router.
- PR-state source for disposition — consumer kernel lane, non-blocking for router.
- C0→C1 false-confidence numeric thresholds — numbers stay open pending trial data; metric
  DEFINITIONS were locked in P0.
- Golden-set contents grow — the format + the "calibration must not regress the golden set"
  invariant were locked in P0; R-core pinned the first 30-case set.
