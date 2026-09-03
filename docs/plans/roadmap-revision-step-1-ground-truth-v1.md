# Intent-router roadmap revision — Step 1 ground-truth journal

**Status:** DRAFT — 2026-09-01  
**Plan-type:** standard  
**Purpose:** Evidence journal for roadmap revision. This is not an ADR, final design, or execution plan.

## Scope and audit criteria

This journal records verified built reality, claimed reality, and unresolved operator choices. It
does not authorize implementation. CR1/CR2, CR3–CR10, KI1/KI2, additive-within-v1 contracts,
zero-link, and runnerless verification remain locked.

## Verified baseline

- Writable root: `/Users/laurence.duggan/.cursor/worktrees/intent-router/ayp7`
- Branch: `cursor/beafe5c3`
- Audit baseline: `HEAD`, local `main`, and `origin/main` all resolved to
  `427c1344f5bafe4bc01d698527e9bc06c5706450`; the tree was clean before this journal.
- GitHub: no open intent-router pull requests. Router PR #5, the egress phase PR, is
  `MERGED` at `03b80b0` (2026-07-09). AWA PR #26 is also `MERGED` at `4bc7b10`
  (2026-07-09); neither is pending review.
- `make verify`: PASS; 264 tests, 4 deliberate future-phase skips, contract freeze, ledger
  recomputation, and static install preflight all passed.
- `make status-verify`: PASS; all four `done` phase claims and their listed test IDs recomputed.
- `make verify-install`: PASS for isolated install, check, repair, and uninstall.
- `/Users/laurence.duggan/dev/_ops/bin/doc-warden.sh check
  /Users/laurence.duggan/.cursor/worktrees/intent-router/ayp7`: `Overall: CONFORMANT`.
  The repository-name-only form is working-directory-sensitive and failed from this worktree.
- The five v1 contracts are frozen on disk. `intent-proposal/v1` records
  `frozen_since: 2026-07-09` and `frozen_by: A0`.
- GitHub Actions are disabled, consistent with the runnerless policy.

## Reconciled claims

### A0 is implementation-complete, not proven

`status.yml` marks A0 `done`, but its own `current_gate` says implementation is complete while the
real-PM usability trial remains. `RESUME.md` also calls that trial the remaining human gate, and
there is a trial kit and harness but no trial-result artifact. Therefore:

- A0's automated implementation body is complete and recomputably green.
- A0 has not earned a human-usability/proven claim.
- The ledger currently overloads `done`: its A0 title includes the trial while its gate excludes
  the outstanding trial from completion.
- Phase-order prose conflicts: the R2 ledger entry requires “A0 proven”; `RESUME.md` says the
  trial does not block R2; the AWA trial kit says passing the trial unblocks R2 and C0.

The status verifier cannot settle this semantic conflict: it verifies files, commits, URL shape,
and listed tests, not completion criteria or human evidence.

### Egress PRs are merged; supporting prose is stale

Router PR #5 and AWA PR #26 are both merged. `RESUME.md` still says the router PR is open, and the
AWA egress artifact still describes the router side as a spec. Those are stale.

The router-side egress reference contract and checks exist and pass. AWA exercises six mapped
surfaces plus an extra status renderer in tests, but its MCP consent surface is explicitly
contract-only rather than wired into a production MCP path. The “all seven surfaces” phase claim
therefore describes contract/test coverage, not seven live production integrations.

## Built reality

- Deterministic L0–L2 plus L5 pipeline: normalization, catalog-derived candidate generation,
  deterministic verdict, and schema-shaped proposal.
- AWA fixture catalog and deterministic golden corpus, including injection-like utterances.
- Catalog/proposal/map/feedback/constitution v1 artifacts, additive manifest, and freeze gate.
- Functional CLI routes: `map`, `explain`, `catalog-verify`, and `doctor`.
- Functional executionless stdio JSON-RPC mirror: initialize, list tools, and read-only tool calls.
- Read-only doctor plus XDG state-path ownership guard. Runtime code has no persistent writer.
- Flavor-2 install/check/repair/uninstall lifecycle and release pointer.
- AST-based no-execution scan, golden tests, contract tests, CLI/MCP tests, state/doctor tests,
  zero-link checks, egress checks, and status-ledger tests.
- AWA's consumer loop consumes proposals while retaining kernel-owned consequence, confirmation,
  execution, and router-off behavior. Manual audit runs passed 81 loop tests, 34 egress tests, and
  4 router-present seam tests. Router-absent targeted proofs also passed.
- Runnerless PR verification is active for intent-router, and the central assignment records an
  intent-router custom verification job.
- A machine-local subagent model-tier freshness monitor is installed for 09:00 daily execution;
  its handler passed a manual run on 2026-08-25. No scheduled run artifact existed at audit time.

## Partial or stubbed

- No L3 smart reranker/provider exists. The engine intentionally delegates only to the
  deterministic floor.
- No L4 parameter extraction exists. AWA consumer-side literal-confirm protections are real, but
  the router-side phase remains deferred.
- Feedback records are schema-shaped in responses but are not persisted or calibrated.
- State layout and permissions are specified and guarded, but feedback, trust, cache, model, and
  audit writers/readers are not built.
- Catalog synonym support is parsed by the library but omitted by the AWA catalog translator, so
  the current product path does not use synonyms.
- `intent doctor --strict` is accepted but currently behaves the same as ordinary doctor.
- MCP is a process-level transport, not registered in live Cursor configuration. No live Cursor
  skill, rule, hook, or MCP reference to intent-router was found.
- The installed release pointer records source commit `f44dbadd`, while the source tree is
  `427c134`; current runtime package bytes match source, so provenance is stale even though code
  content is current.
- The freeze checker protects required floors and selected enum members, but an adversarial
  temporary copy with the frozen optional feedback key `correction` removed still passed. The
  additive-within-v1 test suite separately catches some manifest removals, but the shell freeze
  gate alone does not fully enforce “never remove optional fields.”
- `status-verify --strict` confirms that referenced PRs exist, not that they are merged or matched
  to the recorded commit.
- The required runnerless intent-router recipe runs `tests/run-tests.sh`, not canonical
  `make verify`; therefore it does not execute install verification or recompute the real status
  ledger. Native Actions are disabled.
- AWA's current runnerless recipe does not run the co-installed router seam or its full canonical
  verification suite. Its router descriptor follows mutable `main`; the recorded freeze SHA is
  explanatory rather than an enforced exact pin.
- Local AWA `main` was 19 commits behind `origin/main` and had unrelated pre-existing changes, so
  disk inspection was corroborated against remote metadata and no AWA files were modified.

## Planned, not built

- R2: optional smart layer, prompt-injection isolation around that layer, deterministic destructive
  parameter handling, and literal-confirm fallback.
- C0: reviewable machine-local feedback and calibration.
- C1: automatic calibration, following C0, with destructive-near-miss count exactly zero before
  promotion.
- Resilience: cache, timeout/circuit-breaker behavior, schema rollback, and richer health.
- R-surface-complete: real operator surfaces, release shelf pointer, registry enrollment, and
  governed downstream synchronization.
- M0 remains design-only.
- K-lane implementation exists in AWA beyond what this router ledger shows, but router-owned phase
  accounting has not been reconciled to that live consumer evidence.

## Stale or contradictory artifacts

- `README.md` still presents P0 as current and describes functional commands as not-yet-functional.
- `RESUME.md` says the router egress PR is open; PR #5 is merged.
- `RESUME.md`, `status.yml`, and the AWA trial kit disagree on whether the uncompleted PM trial
  blocks R2.
- `SECURITY.md` still labels some now-active R-core/A0 checks as `Spec`.
- AWA egress and router-pin prose refers to a dedicated native `router-seam` CI job that no longer
  exists under runnerless verification.
- The ledger leaves K0/K1/K2 pending despite live AWA evidence for kernel-first, off-switch, and
  consumer-loop behavior.

## Local installation and discoverability

- `~/.local/share/intent-router/current` is a symlink to a real release directory.
- `~/.config/intent-router/env` exists with mode `0600`; only key names and value shapes were
  inspected.
- `~/.local/state/intent-router` exists and contains no files.
- Source and installed CLI outputs matched for catalog verification, map, explain, and doctor.
- No live Cursor registration was found. The capability is not yet present in the global shelf or
  lifecycle registry, as expected before R-surface-complete.
- PR-verification enrollment is separate and already active.

## First operator interview batch

### 1. What should “done” mean for an operator-tested phase?

**Resolution — ACCEPTED:** Option A. A0 remains implementation `done`; human usability proof is
tracked separately per phase and must not be inferred from automated completion. “Proven” is not
one all-or-nothing product state.

- **A — Recommended:** keep automated implementation `done`, add a separate visible
  `proven`/human-evidence state.
- **B:** return A0 to `pending` until a PM passes the trial.
- **C:** treat automated tests as enough to call A0 proven.

**Tradeoff:** A preserves delivery progress without claiming a human outcome; B is simpler but
hides completed engineering; C is unsupported by current evidence.

### 2. How ambitious should the first smart layer be?

**Resolution — ACCEPTED:** Option B. The first smart layer is bounded reranking for ambiguous,
non-authorizing interpretation, always with deterministic fallback. Evidence collection, shadow
evaluation, selective promotion, and rollback gate each smart phase separately.

- **A:** remain deterministic only.
- **B — Recommended:** use a bounded smart reranker only for ambiguous, non-authorizing
  interpretation, with deterministic fallback.
- **C:** let the smart layer broadly infer intents and parameters.

**Tradeoff:** B can improve natural-language usefulness while preserving the safety floor. A caps
usefulness; C creates substantially more privacy, explainability, and safety work.

### 3. Whose feedback should teach the router?

**Resolution — ACCEPTED WITH EVIDENCE TYPING:** Retain operator corrections and attributable system
outcomes as separate evidence. Neither is a timeless universal winner: eventual conflict handling
must account for evidence freshness, temporal relation, context, and version boundaries. Until
transcript patterns and C0 metrics support thresholds, conflicts remain review suggestions.

- **A:** explicit operator corrections only.
- **B:** observed system outcomes only.
- **C — Recommended:** both, stored as separate evidence with operator-reviewable attribution.

**Tradeoff:** C is richer without pretending system outcomes equal operator intent, but requires
clear conflict and review rules before C1 automation.

### 4. What may be retained locally?

**Resolution — ACCEPTED, SUPERSEDING THE EARLIER OPTIONS:** Retain raw request history as the sole
behavior, machine-locally and privately under CR3, with a bounded retention policy and deterministic
lifecycle enforcement. There is no consent toggle or alternate raw-history mode. Raw history expires
on a rolling 90-day policy; derived/non-raw evidence may persist longer under its own bounded policy.
Derived counts and explicit corrections remain part of the evidence record. Exact enforcement
design belongs to Step 3; retention is not indefinite.

**Tradeoff:** bounded raw history supports replay, adjudication, and calibration while increasing
local privacy exposure relative to derived-only evidence. Deterministic expiry limits that exposure.

### 5. How should the next phases be ordered?

**Resolution — ACCEPTED WITH CONTROLLED PARALLELISM:** Keep A0 implementation `done`; run and record
its real-PM trial against a frozen A0 baseline while bounded smart-layer work proceeds in parallel.
Each phase earns proof separately. No later smart phase may claim proof or promotion from A0 evidence
or without its own gates.

- **A — Recommended:** run and record the PM trial, settle `done` versus `proven`, then R2, then C0.
- **B:** begin R2 in parallel with the PM trial, then C0.
- **C:** prove another deterministic consumer before adding R2.

**Tradeoff:** Controlled parallelism avoids blocking smart-layer engineering while a frozen baseline
keeps A0 trial evidence attributable. It requires explicit per-phase evidence boundaries.

## Remaining unknowns for the next conversation

- A completed PM trial observation and retained evidence.
- Whether live surface coverage must mean production wiring or contract-level compatibility.
- The intended cross-repository owner for keeping consumer seam verification alive under the
  runnerless model.
- Whether the daily freshness monitor has actually fired on schedule after installation; only its
  installed schedule and one successful manual artifact were available.

## Accepted Step 3 evidence decisions

- Raw request history uses rolling 90-day machine-local/private retention with deterministic policy
  enforcement. Derived/non-raw evidence has a separate bounded lifecycle.
- Initial C1 automatic calibration may affect read-only verbs only. Writes and destructive actions
  remain review suggestions.
- The proposed C1 quality target is approximately 300 independent strong proposals with zero
  false-strong observations, interpreted as a roughly 1% one-sided statistical risk target rather
  than current performance. C0 evidence determines the review-burden limit. Zero destructive
  near-miss remains absolute.
- The initial evidence horizon is 45 days with fifth-day checkpoints and possible operator-approved
  early exit after a formal sufficiency assessment. Time alone never proves sufficiency. A deficit-
  and observed-rate-based extension replaces any automatic 60/90-day wait.
