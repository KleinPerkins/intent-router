# G0-R authority-honesty and canonical-proof plan v1

**Status:** DRAFT — 2026-09-03
**Plan-type:** agentic-execution
**Purpose:** Define the immediate router-owned authority-honesty delivery after merged G0-R0 and
the separate verification-authority receipt required before composite G0 can close.
**Accepted design authority:** `docs/plans/roadmap-revision-step-3-design-v2.md`, SHA-256
`9f1098920e531818d1e845f7f11ed3480a7d86ffb738326c98f819835fc8afb1`.
**G0-R0 implementation authority:** `docs/plans/g0-r0-contract-freeze-hardening-v4.md`, SHA-256
`86579f52da3c124888678ad4fec5d8b54abdbb18f014b91a5896ed188052a4c0`.

This draft does not itself authorize implementation. It exists because no accepted executable
G0-R plan was present after G0-R0 merged. The operator supplied standing implementation/delivery
authority on 2026-09-03; accepting this plan would settle the missing semantic authority without
creating a second implementation-approval pause.

---

## 1. Delivery identity and boundary

G0-R is the immediate router-owned child of the composite G0 checkpoint after G0-R0. It makes the
router's durable authorities describe built reality and the accepted revised roadmap without
claiming that the separately owned consumer or verification children have converged.

This plan proposes two authority-correct receipts:

1. **G0-R — router authority honesty:** one ordinary `KleinPerkins/intent-router` PR containing
   router-owned ledger, contract-roadmap metadata, documentation, CLI taxonomy, local verification,
   and provenance-test changes.
2. **G0-V — canonical runnerless verification:** separately governed control-plane and generated
   target-repository changes that replace the current `bash tests/run-tests.sh` job with canonical
   `make verify`, then regenerate and merge the exact lock.

G0-R may merge before G0-V, but composite G0 stays open until both have exact receipts and the
separate G0-C-AWA child has its own authority-owned receipt. A host checkpoint projection is added
only if its owner proves it is required; absence is not silently converted into a required change.

### In scope for G0-R

- Record the real merged G0-R0 child receipt in `status.yml`.
- Introduce the pending composite G0 checkpoint and revised accepted phase ladder.
- Regenerate `RESUME.md` around G0 rather than the obsolete monolithic R2 action.
- Reconcile active durable docs and source comments with the built deterministic runtime,
  frozen proposal contract, merged egress delivery, and accepted v2 architecture.
- Re-label existing deferred additions to the split phases and register accepted v2 optional
  proposal/feedback metadata as **pending declarations only**.
- Register `intent-feedback/v1.operator_choice=none` as a pending enum extension only; do not add
  it to the authoritative enum floor or emit it.
- Replace the misleading CLI `read_only` attribute with independent
  `executes_consumer` and `mutates_router_state` properties without activating a stub or adding a
  write path.
- Make local `make verify` include the hermetic install lifecycle and exact release-pointer
  provenance assertion.
- Add regression tests for every authority correction.

### Out of scope for G0-R

- `.github/pr-recipe.json`, `.github/pr-automation.lock.json`, `.github/pr-automation.json`, or
  any host control-plane file; those belong to G0-V.
- Marking composite G0 done.
- Marking any consumer-kernel lane done from a router-repository commit.
- The G0-C-AWA consumer child, A0-P trial, F0/S0/R2a implementation, provider calls, state writers,
  fleet enrollment, global shelf binding, release/tag publication, or downstream synchronization.
- Adding an accepted optional field to a contract's authoritative `optional_keys`, adding an enum
  member to authoritative `enums`/`frozen_behavior.enum_floors`, or activating a writer.
- Changing any frozen required key, existing enum member, rule text, invariant text, or machine
  check status.
- Mutating the operator's installed runtime under `~/.local/share`; G0-R proves the installer
  hermetically. A live reinstall is a separately authorized post-merge operation.

---

## 2. Verified live ground truth

The following was freshly observed on 2026-09-03 before this plan was written.

### 2.1 Repository and G0-R0 receipt

- Canonical repository: `git@github.com:KleinPerkins/intent-router.git`.
- Live `origin/main`: `e30644cfac2470143f45e89eff37b612dc9dbc28`.
- G0-R0 PR: `https://github.com/KleinPerkins/intent-router/pull/55`.
- PR base: `040a746c119458136bafe493e73a46868356494c`.
- PR head: `3da2b6ef01eaadc54ffadc749d2ffa0c4d4283bd`.
- Squash merge: `e30644cfac2470143f45e89eff37b612dc9dbc28`; it is live `origin/main`.
- Required exact-head checks:
  - `pr-automation / verify`: `success` on the PR head.
  - `pr-automation / job:repo.intent-router.m3-verify`: `success` on the PR head.
- G0-R0 changed exactly:
  - `AGENTS.md`
  - `checks/intent-contract-freeze.sh`
  - `contracts/additive-manifest.json`
  - `tests/freeze_helpers.py`
  - `tests/test_additive_compat.py`
  - `tests/test_contract_freeze.py`
- G0-R0 merged-tree digests:
  - `contracts/additive-manifest.json`:
    `a0345a2dcfeb0980999056131f1dae5040e5748e282fbca3a0f999e078efefff`
  - `checks/intent-contract-freeze.sh`:
    `0f4b693e5f6223a67c23fba98fe3379eaa97ff9ae9274e701bd51372585926dd`
- No open intent-router PR existed at planning preflight.

### 2.2 Baseline verification

`make verify && make status-verify` passed from the G0-R0 tree:

- 295 tests run;
- 4 deliberate future-phase skips;
- all five contracts passed the complete behavior floor;
- strict status verification passed;
- static install preflight passed.

The documentation-governance check was `Overall: CONFORMANT`.

### 2.3 Current authority drift

- `README.md`, `Makefile`, `pyproject.toml`, `bin/intent`, `install.sh`, and
  `intent_router/__init__.py` still present P0/no-runtime/stub-only claims.
- `README.md`, `ARCHITECTURE.md`, `intent_router/proposal.py`, and active fixture prose still call
  `intent-proposal/v1` provisional even though A0 froze it on 2026-07-09.
- `RESUME.md` says the router egress PR is open and points directly to monolithic R2; router PR #5
  and AWA PR #26 are merged, and accepted design v2 replaces monolithic R2.
- `status.yml`, `intent_router/status_verify.py`, and `tests/test_status_verify.py` still encode the
  old phase list and `current_phase: R2`; they contain no G0-R0 receipt or composite G0 checkpoint.
- `CONSTITUTION.md`, the constitution contract, deferred-test skip reasons, and deferred-addition
  labels still use old `R2`, `R-resilience`, and `R-surface` phase names.
- `SECURITY.md` claims no runtime, leaves already-active protections at Spec, and cites a removed
  GitHub Actions workflow instead of the runnerless verifier.
- `ROLLBACK.md` says every phase revert is always safe, treats the router egress PR as open, and
  treats the future full raw event log as already durable truth.
- `intent_router/cli.py` labels future state-mutating verbs `read_only=True`.
- `.github/pr-recipe.json` and its generated lock run only `bash tests/run-tests.sh`; canonical
  `make verify` also runs contract freeze, strict ledger verification, and install preflight.
- The live installed release pointer records commit
  `2da37df00f8617a0341f52d561909678b687bcd9`, not live router main. Its source and runtime are
  machine-local state outside this repository and are not mutated by G0-R.

---

## 3. Authority conflict discovered during planning

Accepted design v2 places canonical runnerless correction inside one G0-R router PR. Current
verification authority does not support that shape:

1. `KleinPerkins/dev::_ops/baseline/profiles/pr-automation/v3/profile.py` and its qualification
   ledger own the qualified command, currently `["bash", "tests/run-tests.sh"]`.
2. The control-plane `sync` operation stages exactly one serial phase:
   `recipe`, `lock|relock`, or `assignment`.
3. A lock is compiled from the already merged default-branch recipe. A candidate recipe and its
   generated lock therefore cannot be truthfully merged as one ordinary target-repository PR.
4. `.github` is a protected path. The reviewer App does not approve or arm protected-path PRs;
   owner handling remains separate from ordinary reviewer-App merge.

Therefore, changing router docs/source and hand-editing recipe+lock in one PR would either bypass
the independent authority, create a lock from unmerged bytes, or violate the serial lifecycle.

### Recommended resolution

Accept this plan's split:

- G0-R remains one router-owned ordinary PR and excludes `.github`.
- G0-V becomes a separate composite-G0 child under verification/control-plane authority:
  1. update and qualify the host-owned command;
  2. merge a protected recipe-only router PR through its sanctioned owner gate;
  3. generate and merge a lock-only router PR from the merged recipe;
  4. prove both required checks succeed on a later ordinary exact head using `make verify`.

This is not scope inflation. It is the minimum decomposition that preserves the authority map
accepted in design v2. If the operator requires the literal one-router-PR shape instead, this plan
must be revised only after the verification authority supplies an atomic candidate-recipe+lock
operation. No such accepted operation was found.

---

## 4. Objective

After G0-R:

1. Every active router authority describes the current deterministic runtime, frozen contracts,
   merged egress state, and accepted split roadmap.
2. `status.yml` contains a recomputable G0-R0 done row pinned to PR #55's real merge and tests.
3. `status.yml` contains an in-progress composite G0 row; `current_phase` is `G0`.
4. The future phase IDs exactly match accepted design v2 while preserving completed history and
   external consumer-kernel rows.
5. `RESUME.md` directs a fresh session to G0 convergence and forbids starting F0/S0/R2a early.
6. Pending v1 additions are path-qualified and machine-checked without changing authoritative
   optional fields, enum floors, or writer behavior.
7. Every CLI verb truthfully states whether it can mutate router-private state while every verb
   remains unable to execute a consumer.
8. Local `make verify` exercises tests, freeze, strict status, static install checks, and the
   hermetic install/uninstall lifecycle with an exact source-commit release pointer.
9. G0-R has an exact merged receipt but composite G0 remains open pending G0-V and G0-C-AWA.

---

## 5. Locked invariants and non-goals

### Locked

- CR1/CR2: router proposes only; no consumer execution or authorization.
- KI1–KI4: consumer safety, consequence, confirmation, and decisions remain independent.
- CR4: required floors and existing enum members never shrink or retype.
- CR5: content remains inert data.
- CR6: unresolved/failing behavior asks or returns deterministic output.
- CR10: operator output remains plain and honestly qualified.
- Zero-link remains green.
- Completed P0, R-core, A0, and egress IDs, PRs, commits, files, and passed-test meaning are
  preserved. Factual prose may be corrected; evidence is not rewritten.
- G0-R0 merged receipt is immutable evidence.
- G0-R does not close composite G0.
- No paid or Actions runner is introduced.

### Non-goals

- No state controller, raw store, provider, reranker, typed writer, calibration, fleet selector,
  new consumer, global release, shelf pointer, registry enrollment, or migration.
- No remote or machine-local install mutation.
- No hand-generated runner lock.
- No self-approval, auto-merge arming, direct main push, admin bypass, force push, or failing-check
  bypass.

---

## 6. Exact authority model

### 6.1 Status phase order

`intent_router.status_verify.EXPECTED_PHASES`, `tests.test_status_verify._ALL_PHASES`, and the real
ledger use this exact order:

```text
P0
K0-K1
K2
R-core
A0
egress
G0-R0
G0
A0-P
F0
S0
R2a
C0
A1
R-resilience-a
R-resilience-b
R-surface-a
R-surface-complete
F1
R2b
R2c
B0
O0
C1
M0
W1
S2
W2
S3
```

The old pending IDs `R2`, `R-resilience`, and `R-surface` disappear only because accepted design v2
supersedes their future meaning. Completed IDs do not change.

### 6.2 G0-R0 row

Add a `done` row with:

- `id: G0-R0`
- PR `https://github.com/KleinPerkins/intent-router/pull/55`
- merge commit `e30644cfac2470143f45e89eff37b612dc9dbc28`
- the exact six changed paths from §2.1
- a nonempty focused test set including:
  - `tests.test_contract_freeze.TestContractFreeze.test_dropping_correction_optional_fails`
  - `tests.test_contract_freeze.TestContractFreeze.test_manifest_bootstrap_negative_matrix`
  - `tests.test_contract_freeze.TestContractFreeze.test_every_required_key_removal_fails`
  - `tests.test_contract_freeze.TestContractFreeze.test_every_enum_member_removal_fails`
  - `tests.test_contract_freeze.TestContractFreeze.test_constitution_content_floor_negative_matrix`
  - `tests.test_contract_freeze.TestContractFreeze.test_sanctioned_optional_addition_passes_both_validators`
  - `tests.test_contract_freeze.TestContractFreeze.test_sanctioned_enum_extension_passes_both_validators`
  - `tests.test_additive_compat.TestAdditiveCompat.test_real_bundle_passes_shared_validator`
  - `tests.test_additive_compat.TestAdditiveCompat.test_frozen_behavior_coverage`
  - `tests.test_additive_compat.TestAdditiveCompat.test_promotion_state_semantics`
  - `tests.test_contract_freeze.TestContractFreeze.test_agents_md_freeze_timing_is_current`
- `current_gate` names base, head, merge, both required successful exact-head checks, and both
  merged-tree digests from §2.1.

`status-verify --strict` must recompute the listed tests, resolve PR #55, and prove the merge commit
is an ancestor of current HEAD.

### 6.3 Composite G0 row

Add `G0` as `in_progress`, with empty `pr`, `commit`, `passed_test_ids`, and `files`. Its
`current_gate` states:

- G0-R0 merged and recorded;
- G0-R implementation/merge receipt pending until this future implementation PR merges;
- G0-V canonical runnerless receipt pending;
- G0-C-AWA receipt pending under AWA authority;
- G0-H is not required unless host authority later proves a checkpoint projection is necessary;
- composite G0 cannot become `done` in the G0-R implementation PR because its own squash merge and
  the other child receipts do not yet exist.

Set `current_phase: G0`. Do not add a self-referential `G0-R done` row.

### 6.4 External kernel lanes

Keep `K0-K1` and `K2` as `track: consumer-kernel` and `pending`. Correct their `current_gate` text
to distinguish active router-side reference tests from the missing exact G0-C-AWA receipt. A
router commit cannot satisfy a done row that requires an external repository commit, and the
current verifier resolves commits only in this repository.

### 6.5 Resume pointer

`RESUME.md` records:

- last completed router phase: egress;
- completed G0 child: G0-R0;
- current checkpoint: G0;
- A0 implementation complete, A0-P human proof pending;
- exact next router action after G0-R merge: obtain accepted G0-V authority and its serial
  recipe/lock receipts;
- G0-C-AWA may proceed only under its separate repository authority;
- F0, S0, and R2a do not start until composite G0 closes;
- R2a is shadow-only and depends on S0/provider gates; R2c owns typed parameters.

---

## 7. Contract-roadmap reconciliation

G0-R changes only `deferred_additions`, `deferred_phases`, `required_additive_phases`,
`enum_extensions`, and future-phase annotations. It does not change any contract
`required_keys`, authoritative `optional_keys`, authoritative `enums`, `frozen_behavior` floor,
rule/invariant text, or machine-check status.

### 7.1 Existing declarations re-labeled

| Contract | Current phase | Revised phase | Existing pending keys |
|---|---|---|---|
| `intent-catalog/v1` | `R2` | `R2c` | `extractor`, `confirm_literal` |
| `intent-proposal/v1` | `R2` | `R2a` | `rerank_source` |
| `intent-map/v1` | `R-resilience` | `R-resilience-b` | `behavior_hash` |
| `intent-catalog/v1` | `R-surface` | `R-surface-complete` | `deprecated` |

A0, egress, and C1 declarations retain their phase labels. Existing C1 `redacted` and
`consent_ref` declarations remain pending; accepted v2 narrows `consent_ref` to historical-import
provenance and no writer may emit either without its phase plan.

### 7.2 Accepted proposal-v1 pending declarations

Add declarations only; every key remains absent from actual/frozen `optional_keys`.

| Phase | Key | Type |
|---|---|---|
| F0 | `registration_digest` | `string` |
| F0 | `catalog_digest` | `string` |
| F0 | `behavior_version` | `string` |
| R2a | `candidate_set_digest` | `string` |
| R2a | `rerank_revision` | `string` |
| R2a | `provider_profile_digest` | `string` |
| R2a | `redaction_profile_digest` | `string` |
| R2a | `confidence_basis` | `enum(deterministic_match_strength|reranked_match_strength|calibrated_probability)` |
| R2a | `fallback_reason` | `enum(off|timeout|provider_error|invalid_output|drift|none_eligible)|null` |

The existing `rerank_source` declaration stays
`enum(deterministic|llm)` and moves to R2a. `catalog_version` remains the existing A0 pending
declaration. No optional value is emitted.

### 7.3 Accepted feedback-v1 pending declarations

Add the following `top.optional` declarations under S0:

| Key | Type |
|---|---|
| `evidence_profile` | `string` |
| `event_id` | `string` |
| `raw_event_id` | `string` |
| `evidence_type` | `enum(operator_intent|operator_correction|factual_observation|system_outcome|hypothesis|preference)` |
| `label_state` | `enum(accepted|corrected|rejected|clarified|aborted|abstained|unresolved)` |
| `correlation_id` | `string` |
| `episode_id` | `string` |
| `target_verb` | `string|null` |
| `registration_digest` | `string` |
| `catalog_digest` | `string` |
| `policy_version` | `string` |
| `behavior_version` | `string` |
| `model_revision` | `string|null` |
| `context_class` | `string` |
| `independence_key` | `string` |
| `supersedes_event_id` | `string|null` |
| `attribution` | `enum(operator|consumer_kernel|system_observer|agent_review)` |
| `outcome_observer` | `string` |
| `outcome_revision` | `string` |

Register a pending enum extension:

```json
{"key":"none","type":"enum-member","target":"enum.operator_choice"}
```

Add `enum_extensions["intent-feedback/v1"]["operator_choice"] = ["none"]`. Keep `none` absent from
the actual `operator_choice` enum and frozen enum floor. This is pending metadata only. S0 must
land old-reader support before promoting the member; no writer may emit it first.

### 7.4 Catalog retirement declaration

Add `superseded_by: string|null` as a pending `top.optional` declaration beside `deprecated` in
`R-surface-complete`. Neither becomes authoritative in G0-R.

### 7.5 Manifest phase coverage

The additive manifest covers every revised phase. A phase is `additive` only when this plan lists a
pending declaration for it; otherwise it is `no-schema-change` with a specific reason explaining
that it does not alter the five currently frozen contracts. F0's future neutral registration
contract is separate from the five-contract floor and must receive its own first-use freeze in F0.

Set `required_additive_phases` exactly to:

```text
A0
egress
G0-R0
G0
A0-P
F0
S0
R2a
C0
A1
R-resilience-a
R-resilience-b
R-surface-a
R-surface-complete
F1
R2b
R2c
B0
O0
C1
M0
W1
S2
W2
S3
```

Keep the existing `K0-K1`, `K2`, and `R-core` entries in `deferred_phases` as
`no-schema-change`; they are preserved history but are not repeated in
`required_additive_phases`. Define revised router phases exactly:

| Phase | Kind | Five-contract participation |
|---|---|---|
| `A0` | additive | proposal: `catalog_version` |
| `egress` | additive | constitution: `tier_a_consumer_contributed` |
| `G0-R0` | no-schema-change | hardened guards only; no product shape changed |
| `G0` | no-schema-change | authority/roadmap metadata only |
| `A0-P` | no-schema-change | human proof against frozen A0 |
| `F0` | additive | proposal: `registration_digest`, `catalog_digest`, `behavior_version`; its new neutral registration schema receives a separate first-use freeze |
| `S0` | additive | feedback: every §7.3 optional key plus enum member `none` |
| `R2a` | additive | proposal: `rerank_source`, `candidate_set_digest`, `rerank_revision`, `provider_profile_digest`, `redaction_profile_digest`, `confidence_basis`, `fallback_reason` |
| `C0` | no-schema-change | uses the already frozen feedback/map floor and S0-declared typed profile |
| `A1` | no-schema-change | consumer-owned maturation; no router contract shape |
| `R-resilience-a` | no-schema-change | smart fallback/last-good behavior only |
| `R-resilience-b` | additive | map: `behavior_hash` |
| `R-surface-a` | no-schema-change | activates surfaces against declared contracts |
| `R-surface-complete` | additive | catalog: `deprecated`, `superseded_by` |
| `F1` | no-schema-change | host-owned activation |
| `R2b` | no-schema-change | activates already-declared rerank metadata |
| `R2c` | additive | catalog param: `extractor`, `confirm_literal` |
| `B0` | no-schema-change | consumer-owned second-consumer delivery |
| `O0` | no-schema-change | read-only projection |
| `C1` | additive | map: `decay_half_life`, `superseded_by`, `last_calibrated`; feedback: `redacted`, `consent_ref`; constitution: `false_confidence_budget` |
| `M0` | no-schema-change | migration design/dry-run only |
| `W1` | no-schema-change | consumer onboarding against frozen interfaces |
| `S2` | no-schema-change | local review suggestions |
| `W2` | no-schema-change | consumer onboarding against frozen interfaces |
| `S3` | no-schema-change | conditional model behavior, no new declared shape in this plan |

The old phase keys `R2`, `R-resilience`, and `R-surface` must be absent after the coordinated
re-label. Tests assert the exact new records, all pending states, and the one pending enum extension.

### 7.6 Constitution annotations

- `prompt_injection_data_not_instruction`: phase `R2a`, still `spec`.
- `deterministic_floor_llm_off_degrade`: phase `R2a`, still `spec`.
- `destructive_param_literal_confirm`: phase `R2c`, still `spec`.
- `calibration_promotion_gate`: phase `C1`, still `spec`.

Update the same phase names in `CONSTITUTION.md` and deferred-test skip reasons. No rule text,
invariant text, test ID, authoritative cross-repository evidence, or status changes.

---

## 8. CLI taxonomy

Replace every `VERBS` entry's `read_only` key with:

- `executes_consumer: False` for all verbs; and
- `mutates_router_state` using this exact map:

| Verb | `mutates_router_state` |
|---|---|
| `map` | `False` |
| `explain` | `False` |
| `catalog-verify` | `False` |
| `doctor` | `False` |
| `feedback` | `True` |
| `phrasebook` | `True` |
| `calibrate` | `True` |
| `seed` | `True` |
| `snapshot` | `True` |
| `restore` | `True` |
| `rebuild` | `True` |
| `status` | `False` |

`phrasebook` is conservatively marked mutating because its declared surface includes `apply`;
future subcommand descriptors may distinguish diff/review from apply. This metadata does not
activate a handler. `ACTIVE_VERBS` remains exactly the four R-core verbs, and no storage primitive
is added.

Update future phase labels:

- feedback/phrasebook → C0;
- calibrate/seed → C1;
- snapshot/restore/rebuild → R-resilience-b;
- status → R-surface-a.

Tests assert the exact map, that all verbs have both booleans, that no verb executes a consumer,
that all future state-mutating verbs remain stubs, and that the four active verbs remain
non-mutating.

---

## 9. Durable documentation and provenance truth

### 9.1 Documentation

- `README.md`: current built floor, functional commands, proposal frozen in A0, G0 current,
  runnerless verification, and no global enrollment yet.
- `ARCHITECTURE.md`: accepted v2 authority map, separate proposal/state paths, host-owned fleet,
  State Controller boundary, 90-day raw/derived baseline, provider entry gate, split phases,
  match-strength language, and composite G0. Mark every unbuilt mechanism as future.
- `SECURITY.md`: recompute each row against active tests; describe runnerless Apps/rulesets instead
  of Actions; distinguish built controls from future S0/R2a controls; retain honest residuals.
- `ROLLBACK.md`: remove “always safe”; record real merged egress/G0-R0 receipts; make rollback
  dependency-aware; preserve external-consumer compatibility; state that future expiry ownership
  survives feature rollback and that raw is not in snapshots.
- `AGENTS.md`: replace only the stale old phase ladder and current-action guidance; preserve locked
  invariants and the already-correct proposal freeze sentence.
- Active source/fixture comments: convert present-tense P0/provisional/future-egress claims to
  historically accurate built-state prose. Historical accepted plans, freeze history, and negative
  regression fixtures remain unchanged.

### 9.2 Local canonical gate

- Update Make help text from P0 to the current deterministic floor.
- Make `verify` invoke `verify-install` after existing tests, freeze, strict status, and static
  install checks.
- Strengthen `verify-install` so the throwaway release pointer must name:
  - schema `intent-release-pointer/v1`;
  - current package version;
  - current source `git rev-parse HEAD`;
  - the throwaway runtime path; and
  - a valid install timestamp.
- Confirm the installed runtime's copied package/contracts/checker bytes match source before
  uninstalling the throwaway tree.
- Do not touch the real HOME/XDG paths.

`meta.yml.provenance_ref: main` remains untouched because immutable global release pinning is
explicitly deferred to R-surface-complete. G0-R proves source install provenance; it does not
publish a tag or global release.

---

## 10. G0-R implementation-file allowlist

The future G0-R implementation PR's changed path set must equal exactly:

```text
AGENTS.md
ARCHITECTURE.md
CONSTITUTION.md
Makefile
README.md
RESUME.md
ROLLBACK.md
SECURITY.md
bin/intent
contracts/additive-manifest.json
contracts/intent-catalog.v1.json
contracts/intent-constitution.v1.json
contracts/intent-feedback.v1.json
contracts/intent-map.v1.json
contracts/intent-proposal.v1.json
install.sh
intent_router/__init__.py
intent_router/catalog.py
intent_router/cli.py
intent_router/doctor.py
intent_router/proposal.py
intent_router/status_verify.py
pyproject.toml
status.yml
tests/fixtures/awa-proposal.fixture.json
tests/golden/README.md
tests/test_additive_compat.py
tests/test_authority_honesty.py
tests/test_cli.py
tests/test_cli_stub.py
tests/test_contract_freeze.py
tests/test_deferred_spec.py
tests/test_doctor.py
tests/test_egress_terms.py
tests/test_golden.py
tests/test_no_execution.py
tests/test_proposal_exercise.py
tests/test_status_verify.py
```

`tests/test_authority_honesty.py` is new. Every other path exists. No `.github`, plan, archive,
runtime-state, consumer, host, shelf, or registry path may appear.

---

## 11. Work items

Tasks run in order T1 → T2 → T3 → T4 → T5 → T6. T2 depends on the ledger phase names from T1.
T3 and T4 consume those names. T5 establishes the canonical local gate before delivery.

### Task G0-R-T1 — Reconcile ledger and resume

**Files:**
- `status.yml`
- `intent_router/status_verify.py`
- `tests/test_status_verify.py`
- `RESUME.md`

**Interfaces:**
- Consumes: PR #55 merged receipt and accepted v2 phase ladder
- Produces: exact G0-R0 done row, pending composite G0, revised phase parser, current resume pointer

**Steps:**

- [ ] Add the G0-R0 row exactly as §6.2.
- [ ] Add the composite G0 row exactly as §6.3.
- [ ] Replace old future phase rows with the exact §6.1 order.
- [ ] Preserve all completed P0/R-core/A0/egress evidence fields byte-for-byte except factual
  `current_gate` corrections that tests explicitly cover.
- [ ] Keep K lanes external/pending and correct their evidence wording.
- [ ] Set `current_phase: G0`.
- [ ] Update both exact phase-list constants.
- [ ] Add tests that old monolithic IDs are absent, all revised IDs occur exactly once, G0-R0
  evidence is recomputable, G0 is not done, and current phase is G0.
- [ ] Regenerate `RESUME.md` per §6.5.

**Acceptance:**

```bash
python3 -m unittest tests.test_status_verify
make status-verify
```

**Rollback:** Governed revert before any later ledger row depends on the revised IDs. After a later
receipt uses them, forward-fix only.

**Dependencies:** G0-R0 merged receipt.

---

### Task G0-R-T2 — Reconcile deferred contract authority

**Files:**
- `contracts/additive-manifest.json`
- `contracts/intent-catalog.v1.json`
- `contracts/intent-constitution.v1.json`
- `contracts/intent-feedback.v1.json`
- `contracts/intent-map.v1.json`
- `contracts/intent-proposal.v1.json`
- `CONSTITUTION.md`
- `tests/test_additive_compat.py`
- `tests/test_contract_freeze.py`
- `tests/test_deferred_spec.py`

**Interfaces:**
- Consumes: G0-R0 complete freeze guard and accepted v2 optional-field tables
- Produces: split-phase pending declarations, pending `none` enum provenance, synchronized spec
  phase annotations

**Steps:**

- [ ] Apply §§7.1–7.5 exactly.
- [ ] Keep authoritative optional fields and enum floors byte-identical to merge
  `e30644cfac2470143f45e89eff37b612dc9dbc28`.
- [ ] Apply §7.6 phase annotations without changing statuses or test IDs.
- [ ] Update additive tests for exact split-phase coverage and the non-empty pending enum extension.
- [ ] Add explicit assertions that every new declaration is pending on both actual/frozen surfaces.
- [ ] Add explicit assertion that `none` is absent from actual/frozen enum members and no writer
  emits it.
- [ ] Update contract-freeze fixture mutations that currently hard-code the old `R2` phase key.

**Acceptance:**

```bash
python3 -m unittest tests.test_additive_compat tests.test_contract_freeze tests.test_deferred_spec
bash checks/intent-contract-freeze.sh
```

A focused comparison script must prove `required_keys`, `optional_keys`, `enums`,
`frozen_behavior`, rule/invariant text, and every machine-check status are unchanged from
`e30644c`.

**Rollback:** Revert all coordinated declaration/manifest/test changes together before a later phase
depends on a new phase label. No authoritative field is removed because none is added here.

**Dependencies:** T1 phase names; G0-R0 checker.

---

### Task G0-R-T3 — Correct active authority prose

**Files:**
- `AGENTS.md`
- `ARCHITECTURE.md`
- `README.md`
- `ROLLBACK.md`
- `SECURITY.md`
- `intent_router/catalog.py`
- `intent_router/proposal.py`
- `tests/fixtures/awa-proposal.fixture.json`
- `tests/golden/README.md`
- `tests/test_authority_honesty.py`
- `tests/test_egress_terms.py`
- `tests/test_golden.py`
- `tests/test_no_execution.py`
- `tests/test_proposal_exercise.py`

**Interfaces:**
- Consumes: accepted v2 design, real merged egress/G0-R0 receipts, T1/T2 phase names
- Produces: current durable architecture/security/rollback/operator entrypoints and stale-claim
  regressions

**Steps:**

- [ ] Apply §9.1.
- [ ] Add file-specific regressions for obsolete current-state claims; do not ban historically
  accurate P0/provisional language in accepted plans or freeze-history tests.
- [ ] Assert README and ARCHITECTURE call `intent-proposal/v1` frozen.
- [ ] Assert SECURITY names the runnerless required checks and no removed workflow.
- [ ] Assert ROLLBACK no longer says every phase revert is always safe.
- [ ] Assert active docs distinguish implemented, pending proof, and future behavior.

**Acceptance:**

```bash
python3 -m unittest tests.test_authority_honesty tests.test_egress_terms \
  tests.test_golden tests.test_no_execution tests.test_proposal_exercise
```

**Rollback:** Governed revert as one documentation-honesty body. If code has advanced past the
reconciled statements, forward-fix instead of restoring stale prose.

**Dependencies:** T1/T2.

---

### Task G0-R-T4 — Correct CLI state-mutation taxonomy

**Files:**
- `intent_router/cli.py`
- `intent_router/doctor.py`
- `tests/test_cli.py`
- `tests/test_cli_stub.py`
- `tests/test_doctor.py`

**Interfaces:**
- Consumes: accepted State Controller boundary and split phase names
- Produces: truthful static verb metadata with no activated state mutation

**Steps:**

- [ ] Apply the exact §8 property and phase maps.
- [ ] Update help/docstrings to say current active commands are non-mutating, not that the entire
  future router has no private-state mutation.
- [ ] Update doctor future labels to R-resilience-b without claiming the future checks are built.
- [ ] Add exact-map regressions and retain all executionless scans.
- [ ] Confirm `ACTIVE_VERBS` and `_HANDLERS` are unchanged.

**Acceptance:**

```bash
python3 -m unittest tests.test_cli tests.test_cli_stub tests.test_doctor tests.test_no_execution
```

**Rollback:** Revert metadata/tests together. No state was written and no handler was activated.

**Dependencies:** T1.

---

### Task G0-R-T5 — Canonicalize local verification and install provenance

**Files:**
- `Makefile`
- `bin/intent`
- `install.sh`
- `intent_router/__init__.py`
- `pyproject.toml`
- `tests/test_authority_honesty.py`

**Interfaces:**
- Consumes: current standalone installer and G0 built-state wording
- Produces: canonical local `make verify` including hermetic install lifecycle and exact-pointer
  proof

**Steps:**

- [ ] Apply §9.2.
- [ ] Remove present-tense P0/stub-only claims from package/launcher/installer metadata.
- [ ] Run `make verify-install` with throwaway HOME/XDG roots and inspect the exact pointer before
  uninstall.
- [ ] Prove the command touches no real HOME/XDG target.
- [ ] Keep package version `0.1.0`; this task corrects provenance proof, not release versioning.

**Acceptance:**

```bash
make verify-install
make verify
```

**Rollback:** Revert canonical-gate/prose changes together. G0-V must not switch the remote command
until this local gate is merged and green.

**Dependencies:** T1–T4.

---

### Task G0-R-T6 — Deliver one router authority PR

**Files:**
- Every path in §10, exactly; no others

**Interfaces:**
- Consumes: T1–T5
- Produces: merged G0-R router receipt without closing composite G0

**Steps:**

- [ ] Run all focused tests from T1–T5.
- [ ] Run `make verify`, `make status-verify`, zero-link, `git diff --check`, and doc-warden.
- [ ] Compare authoritative contract floors to base and prove only permitted metadata changed.
- [ ] Assert the changed path set equals §10.
- [ ] Open one Draft PR against live `main`.
- [ ] Run the repository-required Bugbot cadence to zero actionable findings; every fix invalidates
  prior exact-head evidence.
- [ ] Keep the PR Draft until local proof and review are complete.
- [ ] Move ready only when the ordinary changed path set remains free of `.github` and both required
  exact-head checks can run.
- [ ] Do not arm auto-merge. Let the reviewer App own ordinary approval/arming.
- [ ] Capture base, exact head, merge, changed paths, both required successful checks, focused/local
  proof, and doc-warden result after governed merge.
- [ ] Leave `G0` in progress. A later convergence update records the G0-R merge alongside G0-V and
  G0-C-AWA.

**Acceptance:** Exact merged G0-R receipt exists; all local/remote checks are tied to the final head;
no `.github` or external authority changed; composite G0 remains open.

**Rollback:** Before any downstream phase depends on reconciled IDs/declarations, revert G0-R through
one governed PR. After dependency, forward-fix. Never roll back G0-R0 freeze hardening as part of
this revert.

**Dependencies:** T1–T5; accepted plan (standing 2026-09-03 implementation authority already
exists).

---

## 12. Separate G0-V verification-authority handoff

This plan does not authorize or mutate G0-V. Its later accepted plan must bind:

1. host-owned command authority and qualification evidence for `["make", "verify"]`;
2. one protected recipe-only target PR;
3. one generated lock-only target PR compiled from the merged recipe;
4. exact owner gates for protected paths without agent self-approval or automation bypass;
5. controller doctor/parity before and after each serial phase;
6. both required check contexts remaining unchanged;
7. a final ordinary canary head proving the new lock executes canonical `make verify`; and
8. rollback in reverse authority order.

If the control plane gains an accepted atomic recipe+lock operation before execution, revise this
plan rather than assuming it.

---

## 13. Verification matrix

| Requirement | Evidence |
|---|---|
| Live base and receipt | fetched `origin/main`; PR #55 base/head/merge and exact-head check API |
| G0-R0 ledger honesty | focused listed tests + strict PR/commit ancestry |
| Revised phase completeness | status parser/test exact-list equality |
| No completed-history rewrite | base-vs-head field comparison for P0/R-core/A0/egress |
| No authoritative contract promotion | structured comparison of floors/options/enums/statuses |
| Pending declarations coherent | additive validator + freeze checker |
| Pending enum is writer-last | `none` absent actual/floor; enum extension present; no writer |
| Constitution meaning preserved | rule/invariant/status equality + phase-label tests |
| CLI taxonomy truthful | exact metadata-map tests; active handlers unchanged |
| CR1/CR2/KI unchanged | no-execution tests + no new consumer/runtime path |
| Current docs honest | `tests.test_authority_honesty` |
| Local canonical gate | `make verify` includes `make verify-install` |
| Release pointer provenance | throwaway pointer commit/runtime/source/bytes assertions |
| Zero-link | `python3 -m unittest tests.test_zero_link` |
| Documentation governance | doc-warden `Overall: CONFORMANT` |
| Changed paths bounded | exact §10 local and GitHub compare lists |
| Remote exact-head proof | both required checks `success` on final G0-R head |
| Composite not overclaimed | G0 remains `in_progress`; RESUME names pending children |

---

## 14. Stop conditions and operator gates

Stop and return to the operator if:

- any required change falls outside §10;
- a required correction changes a frozen required key, authoritative optional type, existing enum
  member, rule/invariant text, or machine-check status;
- any pending declaration cannot be represented by the G0-R0 checker without weakening it;
- an old reader must accept a newly emitted field/member in this delivery;
- exact completed-phase evidence would need rewriting rather than factual annotation;
- G0-R would need to mark itself or composite G0 done before a real merge/child receipt exists;
- a router commit would be used as evidence for an external consumer commit;
- canonical remote verification requires hand-editing a lock or combining serial recipe/lock phases;
- a protected-path merge would require the agent to self-approve, arm auto-merge, bypass a failing
  check, or use unauthorized admin merge;
- doc-warden, zero-link, focused tests, `make verify`, `make status-verify`, or exact changed paths
  fail;
- a far-reaching authority or compatibility decision not settled in accepted design appears.

Operator gates:

1. Accept/revise/reject this v1 plan, including the G0-R/G0-V authority split.
2. Acceptance plus the standing 2026-09-03 operator authorization permits G0-R implementation.
3. Use the ordinary reviewer-App-controlled merge path for G0-R.
4. Separately accept and authorize G0-V and G0-C-AWA under their owners.
5. Accept composite G0 only after exact child receipts converge.

---

## 15. Implementation-agent recommendation

Use the deep model tier with maximum reasoning for G0-R. The work changes durable authority,
contract-roadmap provenance, ledger semantics, and rollback/security claims across many files even
though runtime behavior stays intentionally small. Do not parallelize writers in one worktree.

Expected cadence:

1. Implement T1 and prove strict ledger honesty.
2. Implement T2 and prove no authoritative contract promotion.
3. Implement T3 and run stale-claim regressions.
4. Implement T4 and prove exact CLI metadata/no new handlers.
5. Implement T5 and run canonical local verification.
6. Deliver T6 as one ordinary Draft PR, review to clean, then use governed merge.
7. Capture the G0-R receipt and stop; do not begin G0-V or G0-C-AWA from this router worktree.

---

## 16. Plan acceptance checkpoint

Accepting this plan approves:

- the G0-R/G0-V authority split;
- the exact router G0-R scope and changed-path set;
- the ledger/checkpoint and phase-ID model;
- pending-only contract declaration mapping;
- CLI taxonomy;
- local canonical verification/provenance proof; and
- delivery, rollback, and stop conditions.

Under the standing 2026-09-03 authorization, acceptance permits only the G0-R implementation and
delivery described here. It does not authorize protected G0-V mutations, consumer changes,
composite G0 closure, smart behavior, state persistence, fleet enrollment, release, or migration.

Decision:

> **Accept, revise, or reject `g0-r-authority-honesty-v1.md` as the executable basis for the
> router-owned G0-R delivery and the separate G0-V handoff.**
