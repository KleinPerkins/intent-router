# G0-R authority-honesty and canonical-proof plan v1

**Status:** ACCEPTED — 2026-09-03
**Plan-type:** agentic-execution
**Purpose:** Define the final router-owned authority-honesty reconciliation after merged G0-R0 and
after separately accepted and delivered G0-V and G0-C-AWA children.
**Accepted design authority:** `docs/plans/roadmap-revision-step-3-design-v3.md`, SHA-256
`276693025446414411cf8cd016344b53d6179fd06bb791b9660f46f40fe3e184`.
**G0-R0 implementation authority:** `docs/plans/g0-r0-contract-freeze-hardening-v4.md`, SHA-256
`86579f52da3c124888678ad4fec5d8b54abdbb18f014b91a5896ed188052a4c0`.

This accepted plan does not authorize implementation. Implementation cannot begin until the exact
G0-V and G0-C-AWA receipts required below exist and separate explicit implementation authority is
given. No prior standing authorization overrides either gate.

---

## 1. Delivery identity and boundary

G0-R is the **final** router-owned child of composite G0, not the immediate child after G0-R0. It
corrects the router's durable authorities only after independently owned verification and consumer
work has produced exact receipts. It records those receipts without claiming their authority and
without closing composite G0.

### Hard preconditions and acyclic order

1. G0-R0 is merged and its exact receipt remains valid.
2. The accepted design authority is the exact v3 path and digest recorded above; any mismatch stops.
3. G0-V is separately planned, accepted, and delivered as four bounded receipts:
   - G0-V-R: one ordinary router PR making canonical `make verify` noexec-compatible and proving
     hermetic release-pointer/source/runtime/byte integrity;
   - G0-V-H: one `KleinPerkins/dev` host/control-plane PR changing and exact-image-qualifying the
     intent-router command to `make verify`;
   - G0-V-P: one protected recipe-only router PR through its owner gate; and
   - G0-V-L: one generated lock-only router PR compiled from the merged default-branch recipe.
4. G0-C-AWA is separately planned, accepted, delivered, and represented by one exact AWA-owned
   receipt.
5. G0-H remains absent unless its host owner proves a checkpoint projection is required. If that
   proof appears, its separate host receipt becomes a precondition.
6. Only then may G0-R implementation start. Its final ordinary exact head is the canary proving the
   merged G0-V lock executes the strengthened canonical gate.

This creates no cycle: G0-V-R supplies the local executable gate before host qualification; G0-V
never waits for G0-R; G0-R only consumes already-merged G0-V/G0-C-AWA receipts. Each delivery keeps
one owner, one repository, one PR, one receipt, and one rollback boundary.

### In scope for G0-R

- Record the real merged G0-R0, G0-V-R/H/P/L, and G0-C-AWA child receipts in the in-progress G0
  checkpoint. Record G0-H only if its owner proved and delivered it.
- Introduce the pending composite G0 checkpoint and revised accepted phase ladder without marking
  G0 done.
- Regenerate `RESUME.md` around final G0-R delivery and the separate composite-G0 acceptance gate,
  rather than obsolete monolithic R2 or missing-child work.
- Reconcile active durable docs and source comments with the built deterministic runtime, frozen
  proposal contract, merged egress delivery, accepted successor architecture, and completed child
  receipts.
- Re-label existing deferred additions to the split phases and register accepted successor optional
  proposal/feedback metadata as **pending declarations only**.
- Register `intent-feedback/v1.operator_choice=none` as a pending enum extension only; do not add
  it to the authoritative enum floor or emit it.
- Replace the misleading CLI `read_only` attribute with independent `executes_consumer` and
  `mutates_router_state` properties without activating a stub or adding a write path.
- Re-run and preserve the canonical local/remote gate and hermetic provenance tests delivered by
  G0-V; G0-R does not re-own or rewrite that child.
- Add behavior-specific regression tests for every G0-R authority correction.

### Out of scope for G0-R

- `.github/pr-recipe.json`, `.github/pr-automation.lock.json`, `.github/pr-automation.json`,
  `Makefile`, `install.sh`, any host control-plane file, or any G0-V-R/H/P/L receipt bytes; those
  belong to the already-delivered G0-V child.
- Marking composite G0 done or recording G0-R's not-yet-existing merge as if it already exists.
- Marking any consumer-kernel lane done from a router-repository commit.
- The G0-C-AWA consumer child, A0-P trial, F0/S0/R2a implementation, provider calls, state writers,
  fleet enrollment, global shelf binding, release/tag publication, or downstream synchronization.
- Adding an accepted optional field to a contract's authoritative `optional_keys`, adding an enum
  member to authoritative `enums`/`frozen_behavior.enum_floors`, or activating a writer.
- Changing any frozen required key, existing enum member, rule text, invariant text, or machine
  check status.
- Mutating the operator's installed runtime under `~/.local/share`; all install proof is hermetic.

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
- No open intent-router PR existed at the original planning preflight. Draft PR #56 now carries
  only this governed plan-hardening body.

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
- The host qualification contract uses `tmpfs,noexec,nosuid,nodev`, while current `make verify`
  directly invokes `./install.sh --check` and `make verify-install` directly invokes `./install.sh`.
  That concrete incompatibility is why G0-V-R must precede host qualification; final G0-R cannot
  absorb the fix without recreating a dependency cycle.
- The live installed release pointer records commit
  `2da37df00f8617a0341f52d561909678b687bcd9`, not live router main. Its source and runtime are
  machine-local state outside this repository and are not mutated by G0-R.

---

## 3. Authority conflicts and accepted v3 resolution

Accepted design v3 resolves two source-confirmed authority conflicts.

### 3.1 G0-V must be a design child, not a plan-only invention

Accepted design v2 assigns canonical runnerless correction to G0-R and defines no G0-V. The initial
G0-R Draft removed protected recipe/lock work from G0-R and invented G0-V without updating the
accepted design. Independently, the live verification authority proves that a mixed G0-R shape is
invalid:

1. `KleinPerkins/dev::_ops/baseline/profiles/pr-automation/v3/profile.py` and
   `qualification-ledger.json` own the reviewed/qualified custom command, currently
   `["bash", "tests/run-tests.sh"]`.
2. Control-plane `sync` stages exactly one serial `recipe`, `lock|relock`, or `assignment` phase.
3. A lock is compiled from the already merged default-branch recipe. Candidate recipe and generated
   lock bytes cannot truthfully land in one ordinary target-repository PR.
4. `.github` is protected. Reviewer automation cannot approve or arm those changes; the sanctioned
   owner gate is separate.

Accepted design v3 therefore explicitly creates G0-V and assigns each authority one
delivery/receipt. V2 remains immutable and is superseded by v3.

### 3.2 Final G0-R must follow authority-owned children

Accepted G0-R0 v4 states that the later G0-R convergence PR updates `status.yml`, `RESUME.md`, and
the roadmap ledger only after all authority-owned G0 children complete. The initial G0-R Draft's
"G0-R may merge before G0-V" sequence contradicted that authority and would force a second ledger
reconciliation.

Moving G0-R later exposes one concrete prerequisite: the controller's exact-image workspace is
`tmpfs,noexec`, but current `make verify` directly executes `./install.sh`. G0-V therefore begins
with a narrow ordinary router prerequisite (G0-V-R) that invokes scripts through interpreters and
proves hermetic install provenance. Host qualification, recipe-only delivery, and generated
lock-only delivery follow. G0-C-AWA is independent. Final G0-R then records all exact child receipts,
runs as the first ordinary canary under the new lock, and leaves G0 `in_progress` for a separate
operator acceptance/ledger-closeout gate.

No accepted operation supports a combined recipe+lock change, no cross-owner receipt is fabricated,
and no dependency points from G0-V back to G0-R.

---

## 4. Objective

After G0-R merges:

1. Every active router authority describes the current deterministic runtime, frozen contracts,
   merged egress state, accepted successor roadmap, and completed G0 child receipts.
2. `status.yml` contains a recomputable G0-R0 done row pinned to PR #55's real merge and tests.
3. `status.yml` contains an in-progress composite G0 row that records exact G0-V and G0-C-AWA
   receipts (plus G0-H only if proven required); `current_phase` is `G0`.
4. The future phase IDs exactly match accepted design v3 while preserving completed history and
   external consumer-kernel rows.
5. `RESUME.md` directs a fresh session to observe the real G0-R merge receipt and present the
   separate composite-G0 acceptance gate; it forbids starting F0/S0/R2a early.
6. Pending v1 additions are path-qualified and machine-checked without changing authoritative
   optional fields, enum floors, or writer behavior.
7. Every CLI verb truthfully states whether it can mutate router-private state while every verb
   remains unable to execute a consumer.
8. Canonical `make verify` and hermetic release-pointer/source/runtime/byte-integrity tests remain
   green locally and under both required runnerless check contexts on the exact G0-R head.
9. G0-R has an exact merged receipt for operator review, but composite G0 remains `in_progress`
   until its separate acceptance and ledger-closeout delivery.

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
- G0-R0 and completed G0-V/G0-C-AWA receipts are immutable inputs, not router-owned claims.
- G0-R does not close composite G0; its merge receipt goes to a separate acceptance gate.
- No paid or Actions runner is introduced.

### Non-goals

- No state controller, raw store, provider, reranker, typed writer, calibration, fleet selector,
  new consumer, global release, shelf pointer, registry enrollment, or migration.
- No remote or machine-local install mutation.
- No G0-V or G0-C-AWA implementation and no hand-generated runner lock.
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

When design v3 is accepted, the old pending IDs `R2`, `R-resilience`, and `R-surface` disappear
because its revised ladder supersedes their future meaning. Completed IDs do not change.

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
`current_gate` records exact immutable identifiers for:

- merged G0-R0;
- completed G0-V-R host-compatible local-gate receipt;
- completed G0-V-H host command/qualification receipt;
- completed G0-V-P protected recipe-only receipt;
- completed G0-V-L generated lock-only receipt and compiler/merged-recipe provenance;
- completed G0-C-AWA receipt under AWA authority;
- G0-H only if host authority proved it required and delivered it; otherwise state that no proof
  made it required;
- final G0-R implementation/merge receipt pending until this future implementation PR really
  merges; and
- separate composite-G0 operator acceptance/ledger closeout pending after that merge.

Set `current_phase: G0`. Do not add a self-referential `G0-R done` row and do not mark G0 `done` in
the G0-R implementation PR. The later acceptance/closeout delivery may record the observed G0-R
merge only after it exists.

### 6.4 External kernel lanes

Keep `K0-K1` and `K2` as `track: consumer-kernel` and `pending`. Correct their `current_gate` text
to distinguish active router-side reference tests from the exact G0-C-AWA receipt without
converting that receipt into unsupported lane-completion evidence. A router commit cannot satisfy
a done row that requires an external repository commit, and the current verifier resolves commits
only in this repository.

### 6.5 Resume pointer

`RESUME.md` records:

- last completed router phase: egress;
- completed G0 children: G0-R0, every G0-V receipt, and G0-C-AWA (plus G0-H only if required);
- current checkpoint: G0, still `in_progress`;
- A0 implementation complete, A0-P human proof pending;
- exact next action before G0-R merge: finish the final ordinary G0-R delivery only after all
  precondition receipts remain valid and both required check contexts pass on its exact head;
- exact next action after G0-R merge: observe its real merge receipt and present the separate
  composite-G0 acceptance/ledger-closeout gate;
- no new G0-V or G0-C-AWA work is attempted from this router reconciliation;
- F0, S0, and R2a do not start until composite G0 is separately accepted and closed; and
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

Before inserting replacements, remove obsolete `R2`, `R-resilience`, and `R-surface` keys from
**both** `deferred_phases` and `required_additive_phases`. Old `R2` currently owns two declarations
that split by behavior: catalog `extractor`/`confirm_literal` move to R2c, while proposal
`rerank_source` moves to R2a. The three old keys must be absent after the coordinated re-label.
Tests assert the exact new records, all pending states, and the one pending enum extension.

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

`phrasebook` is conservatively marked mutating because its declared surface includes future
`apply`; this is a placeholder, not a claim that diff/review mutate. Place an inline marker adjacent
to its descriptor stating: `C0 revisit before activation: split diff/review (non-mutating) from
apply (mutating) if phrasebook subcommands are decomposed.` C0 must resolve that marker before
activating or decomposing phrasebook subcommands. This metadata does not activate a handler.
`ACTIVE_VERBS` remains exactly the four R-core verbs, and no storage primitive is added.

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
- `ARCHITECTURE.md`: accepted v3 authority map, separate proposal/state paths, host-owned fleet,
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

### 9.2 Canonical gate consumed from G0-V

G0-V-R, not final G0-R, owns the prerequisite mutations to `Makefile` and `install.sh`. Its exact
receipt must prove:

- every installer invocation used under the controller is interpreter-invoked and compatible with
  the qualified `tmpfs,noexec` workspace;
- local `make verify` invokes `verify-install` after tests, freeze, strict status, and static install;
- the throwaway release pointer names schema `intent-release-pointer/v1`, current package version,
  source commit equal to `git rev-parse HEAD`, exact source root, throwaway runtime path, and a valid
  install timestamp;
- copied installed package, contracts, and checker bytes match source before uninstall; and
- no real HOME/XDG path is touched.

G0-R consumes and re-runs these exact behavior tests without modifying `Makefile` or `install.sh`:

- `tests.test_authority_honesty.TestHermeticReleasePointer.test_schema_and_version_are_exact`
- `tests.test_authority_honesty.TestHermeticReleasePointer.test_source_commit_matches_source_head`
- `tests.test_authority_honesty.TestHermeticReleasePointer.test_source_and_runtime_are_exact_and_hermetic`
- `tests.test_authority_honesty.TestHermeticReleasePointer.test_installed_package_contract_and_checker_bytes_match_source`
- `tests.test_authority_honesty.TestHermeticReleasePointer.test_real_home_and_xdg_roots_are_untouched`
- `tests.test_authority_honesty.TestHermeticReleasePointer.test_wrong_schema_commit_source_or_runtime_is_rejected`
- `tests.test_authority_honesty.TestHermeticReleasePointer.test_mismatched_installed_bytes_are_rejected`

These tests must make positive assertions over the generated pointer/runtime and negative assertions
against real HOME/XDG targets; file existence or JSON parse alone is insufficient. G0-R's final
ordinary exact head must pass both current runnerless contexts under the merged G0-V lock.
`meta.yml.provenance_ref: main` remains untouched because immutable global release pinning is
explicitly deferred to R-surface-complete.

---

## 10. G0-R implementation-file allowlist

The future final G0-R implementation PR's changed path set must equal exactly:

```text
AGENTS.md
ARCHITECTURE.md
CONSTITUTION.md
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

`tests/test_authority_honesty.py` is introduced by G0-V-R and extended here. Every other path exists.
No `.github`, `Makefile`, `install.sh`, plan, archive, runtime-state, consumer, host, shelf, or
registry path may appear.

---

## 11. Work items

Hard preflight precedes every task: design v3 accepted; G0-V-R/H/P/L and G0-C-AWA exact receipts
present and still valid; G0-H either not required by its owner or delivered. If any precondition is
missing, no G0-R implementation file may change.

Tasks then run in order T1 → T2 → T3 → T4 → T5 → T6. T2 depends on the ledger phase names from T1.
T3 and T4 consume those names. T5 re-verifies the already-delivered G0-V canonical gate before
final delivery.

### Task G0-R-T1 — Reconcile ledger and resume

**Files:**
- `status.yml`
- `intent_router/status_verify.py`
- `tests/test_status_verify.py`
- `RESUME.md`

**Interfaces:**
- Consumes: PR #55 merged receipt, accepted v3 phase ladder, exact G0-V/G0-C-AWA receipts, and
  optional G0-H receipt only if required
- Produces: exact G0-R0 done row, receipt-complete but still in-progress composite G0, revised phase
  parser, current resume pointer

**Steps:**

- [ ] Add the G0-R0 row exactly as §6.2.
- [ ] Add the composite G0 row exactly as §6.3 with exact G0-V/G0-C-AWA receipts; do not retain
  "pending child" placeholders for deliveries that are hard preconditions.
- [ ] Replace old future phase rows with the exact §6.1 order.
- [ ] Preserve all completed P0/R-core/A0/egress evidence fields byte-for-byte except factual
  `current_gate` corrections that tests explicitly cover.
- [ ] Keep K lanes external/pending and correct their evidence wording.
- [ ] Set `current_phase: G0`.
- [ ] Keep `tests.test_status_verify._ALL_PHASES` as an independent exact oracle rather than
  importing production `EXPECTED_PHASES`; assert the two exact lists agree through behavior.
- [ ] Replace the hard-coded parser assertion `len(...)=12` with
  `len(data["phases"]) == len(_ALL_PHASES)`.
- [ ] Rewrite `test_missing_phase_is_caught` to remove one explicitly named phase (use `R2c`) by
  name and assert the diagnostic names that same `R2c`; do not drop the new last phase while
  retaining stale M0 wording.
- [ ] Assert real-ledger IDs equal `_ALL_PHASES` exactly and in order, old monolithic IDs are absent,
  revised IDs occur once, G0-R0 evidence is recomputable, G0 remains `in_progress`, required child
  receipt tokens are present, and current phase is G0.
- [ ] Regenerate `RESUME.md` per §6.5.

**Acceptance:**

```bash
python3 -m unittest tests.test_status_verify
make status-verify
```

**Rollback:** Governed revert before any later ledger row depends on the revised IDs. After a later
receipt uses them, forward-fix only.

**Dependencies:** Accepted design v3; exact completed G0-R0, G0-V-R/H/P/L, and G0-C-AWA
receipts; G0-H receipt only if its owner proved it required.

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
- Consumes: G0-R0 complete freeze guard and accepted v3 optional-field tables
- Produces: split-phase pending declarations, pending `none` enum provenance, synchronized spec
  phase annotations

**Steps:**

- [ ] Remove obsolete `R2`, `R-resilience`, and `R-surface` from both
  `deferred_phases` and `required_additive_phases` before inserting the exact §§7.1–7.5
  replacements. Move old R2 catalog declarations to R2c and its proposal declaration to R2a.
- [ ] Keep authoritative optional fields and enum floors byte-identical to merge
  `e30644cfac2470143f45e89eff37b612dc9dbc28`.
- [ ] Apply §7.6 phase annotations without changing statuses or test IDs.
- [ ] In `contracts/intent-proposal.v1.json`, update only `additive_note`'s anticipated phase phrase
  from `A0/R2` to `A0/R2a`; preserve every other authoritative frozen statement verbatim.
- [ ] Update additive tests for exact split-phase coverage and the non-empty pending enum extension.
- [ ] Preserve the bidirectional canonical join, then replace **both** empty-state assertions in
  `test_enum_extensions_bidirectional`: assert records exactly equal
  `{("intent-feedback/v1", "operator_choice", "none")}` and assert the per-schema map is exactly
  `{"intent-catalog/v1": {}, "intent-map/v1": {}, "intent-feedback/v1":
  {"operator_choice": ["none"]}, "intent-constitution/v1": {}, "intent-proposal/v1": {}}`.
- [ ] Add explicit assertions that every new declaration is pending on both actual/frozen surfaces.
- [ ] Assert `none` is absent from actual/frozen enum members and no writer emits it.
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
- Consumes: accepted v3 design, real merged egress/G0-R0 receipts, T1/T2 phase names
- Produces: current durable architecture/security/rollback/operator entrypoints and stale-claim
  regressions

**Steps:**

- [ ] Apply §9.1.
- [ ] Add file-specific regressions for obsolete current-state claims; do not scan accepted plans or
  freeze-history fixtures where P0/provisional language remains historically accurate.
- [ ] Add exact ID
  `tests.test_authority_honesty.TestProposalFreezeTruth.test_readme_and_architecture_name_proposal_frozen_not_provisional`;
  positively require each named surface to state the A0-frozen status and negatively reject the
  exact stale README fragment ``intent-proposal/v1` is **PROVISIONAL**`` plus the old
  ARCHITECTURE table cell `**PROVISIONAL** (freeze → A0)`.
- [ ] Add exact ID
  `tests.test_authority_honesty.TestProposalFreezeTruth.test_runtime_comments_do_not_call_proposal_provisional`;
  scan only active runtime/package/fixture surfaces and reject the exact
  `PROVISIONAL until A0` current-state claim while allowing clearly historical freeze prose.
- [ ] Add exact ID
  `tests.test_authority_honesty.TestRunnerlessTruth.test_security_names_both_current_runnerless_check_contexts`;
  require both exact names `pr-automation / verify` and
  `pr-automation / job:repo.intent-router.m3-verify`.
- [ ] Add exact ID
  `tests.test_authority_honesty.TestRunnerlessTruth.test_security_does_not_name_removed_actions_workflow`;
  reject `.github/workflows/baseline.yml` and any claim that GitHub Actions is the active verifier.
- [ ] Add exact ID
  `tests.test_authority_honesty.TestRollbackTruth.test_rollback_rejects_universal_safety_claim_and_names_dependency_boundary`;
  reject `a phase revert is always safe` and `Why this is always safe`, and require both the
  pre-dependency governed-revert and post-dependency forward-fix rules.
- [ ] Add exact ID
  `tests.test_authority_honesty.TestBuiltStateTruth.test_active_docs_distinguish_implemented_pending_proof_and_future`;
  require all three states on the named active docs rather than accepting a document that merely
  avoids one stale phrase.

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
- [ ] Add the exact inline C0 revisit marker beside `phrasebook`; tests require the marker while the
  aggregate placeholder remains `mutates_router_state=True`.
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

### Task G0-R-T5 — Re-verify canonical gate and install provenance

**Files:**
- `tests/test_authority_honesty.py` (already extended by T3; no G0-V test weakening)

**Read-only inputs:**
- `Makefile`
- `install.sh`
- the exact G0-V-R/H/P/L receipts

**Interfaces:**
- Consumes: G0-V's noexec-compatible canonical gate, hermetic provenance tests, generated lock, and
  unchanged required check names
- Produces: G0-R-local proof that those prerequisites still hold; no duplicate gate implementation

**Steps:**

- [ ] Run each exact `TestHermeticReleasePointer` ID from §9.2 and prove it asserts schema/version,
  source commit, exact source/runtime paths, byte parity, and real-HOME/XDG non-mutation.
- [ ] Assert `Makefile` invokes installer scripts through `bash` wherever the noexec controller may
  exercise them and that `verify` includes `verify-install`.
- [ ] Run `make verify-install` with throwaway HOME/XDG roots; inspect pointer/runtime before
  uninstall and verify teardown.
- [ ] Confirm the tests reject a wrong schema, source commit, source path, runtime path, or copied
  byte in controlled fixtures; a parse-only or existence-only test is insufficient.
- [ ] Confirm package version remains `0.1.0`; this task proves provenance, not release versioning.
- [ ] Do not modify `Makefile` or `install.sh`; any required change means G0-V is incomplete and is
  a stop condition, not scope to absorb into G0-R.

**Acceptance:**

```bash
python3 -m unittest \
  tests.test_authority_honesty.TestHermeticReleasePointer.test_schema_and_version_are_exact \
  tests.test_authority_honesty.TestHermeticReleasePointer.test_source_commit_matches_source_head \
  tests.test_authority_honesty.TestHermeticReleasePointer.test_source_and_runtime_are_exact_and_hermetic \
  tests.test_authority_honesty.TestHermeticReleasePointer.test_installed_package_contract_and_checker_bytes_match_source \
  tests.test_authority_honesty.TestHermeticReleasePointer.test_real_home_and_xdg_roots_are_untouched \
  tests.test_authority_honesty.TestHermeticReleasePointer.test_wrong_schema_commit_source_or_runtime_is_rejected \
  tests.test_authority_honesty.TestHermeticReleasePointer.test_mismatched_installed_bytes_are_rejected
make verify-install
make verify
```

**Rollback:** No independent T5 mutation. T3 owns any same-file documentation-test changes; G0-V's
owner and rollback rules govern canonical-gate defects.

**Dependencies:** T1–T4 and all exact G0-V receipts.

---

### Task G0-R-T6 — Deliver one router authority PR

**Files:**
- Every path in §10, exactly; no others

**Interfaces:**
- Consumes: accepted v3, accepted G0-R plan, exact precondition receipts, and T1–T5
- Produces: merged final G0-R router receipt for the separate composite-G0 acceptance gate

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
- [ ] Require both exact current contexts — `pr-automation / verify` and
  `pr-automation / job:repo.intent-router.m3-verify` — to succeed on the final G0-R head; this is
  the ordinary canary for the already-merged G0-V lock.
- [ ] Leave `G0` in progress. After the real G0-R merge exists, present its exact receipt with the
  already-recorded child receipts at the separate operator acceptance/ledger-closeout gate.

**Acceptance:** Exact merged final G0-R receipt exists; all local/remote checks are tied to the final
head; no `.github`, `Makefile`, `install.sh`, or external authority changed; composite G0 remains
open pending explicit acceptance.

**Rollback:** Before any downstream phase depends on reconciled IDs/declarations, revert G0-R through
one governed PR. After dependency, forward-fix. Never roll back G0-R0 freeze hardening as part of
this revert.

**Dependencies:** Accepted design v3; accepted G0-R v1; exact valid G0-R0, G0-V-R/H/P/L, and
G0-C-AWA receipts (plus G0-H only if required); T1–T5; explicit implementation authorization.

---

## 12. Prior G0-V verification-authority handoff

This plan neither authorizes nor mutates G0-V. Before G0-R implementation, a separately accepted
G0-V plan must have delivered and evidenced this acyclic sequence:

1. **G0-V-R — router prerequisite:** one ordinary router PR changes only the narrow canonical-gate
   surface required to make `make verify` compatible with `tmpfs,noexec`, include hermetic
   `verify-install`, and add the exact §9.2 provenance/byte/non-mutation tests.
2. **G0-V-H — host authority:** one `KleinPerkins/dev` PR updates both
   `M3_CUSTOM_COMMANDS["KleinPerkins/intent-router"]` and its qualification-ledger disposition to
   `["make", "verify"]`, with exact controller image/limits/source evidence and control-plane tests.
3. **G0-V-P — protected recipe:** after G0-V-H merges, one owner-gated protected recipe-only router
   PR generated by control-plane `sync`; no lock or ordinary product file shares the PR.
4. **G0-V-L — generated lock:** after G0-V-P merges, one lock-only router PR compiled from the
   merged default-branch recipe by the qualified compiler/release; no hand edit and no candidate
   recipe base.
5. Run controller doctor/remote parity before and after each serial phase. Keep the two required
   contexts unchanged. Record exact base/head/merge/check and digest/provenance receipts for each
   delivery.
6. Roll back in reverse authority order only while no dependent delivery exists; after dependency,
   forward-fix. Agents never self-approve, pre-arm, bypass a failing check, or use paid runners.

G0-V completion does not wait for G0-R. Exact-image qualification proves the command contract; the
final G0-R ordinary exact head is the target canary under the merged lock. If that canary fails,
G0-R stops and G0-V owners repair or roll back their own authority—G0-R does not edit protected or
host state.

---

## 13. Verification matrix

| Requirement | Evidence |
|---|---|
| Live base and receipt | fetched `origin/main`; PR #55 base/head/merge and exact-head check API |
| Design authority honest | accepted v3 path/digest match the immutable design authority; v2 remains byte-identical and superseded |
| Required child sequencing | exact G0-V-R/H/P/L and G0-C-AWA receipts exist before any G0-R edit; optional G0-H only if owner-proven |
| G0-R0 ledger honesty | focused listed tests + strict PR/commit ancestry |
| Revised phase completeness | independent `_ALL_PHASES` exact oracle; parser count derived from it; named `R2c` removal/assertion regression |
| No completed-history rewrite | base-vs-head field comparison for P0/R-core/A0/egress |
| No authoritative contract promotion | structured comparison of floors/options/enums/statuses |
| Pending declarations coherent | additive validator + freeze checker |
| Old split keys removed | `R2`, `R-resilience`, `R-surface` absent from both manifest phase containers; R2 catalog→R2c and proposal→R2a |
| Pending enum is writer-last and bidirectional | exact enum-extension record/map assertions for `{intent-feedback/v1, operator_choice, none}`; `none` absent actual/floor/writer |
| Proposal additive prose current | `intent-proposal.v1.json::additive_note` says A0/R2a; all other frozen meaning equal to base |
| Constitution meaning preserved | rule/invariant/status equality + phase-label tests |
| CLI taxonomy truthful | exact metadata map; inline C0 phrasebook-revisit marker; active handlers unchanged |
| CR1/CR2/KI unchanged | no-execution tests + no new consumer/runtime path |
| Proposal freeze truth | `tests.test_authority_honesty.TestProposalFreezeTruth.test_readme_and_architecture_name_proposal_frozen_not_provisional` and `.test_runtime_comments_do_not_call_proposal_provisional` |
| Runnerless documentation truth | `tests.test_authority_honesty.TestRunnerlessTruth.test_security_names_both_current_runnerless_check_contexts` and `.test_security_does_not_name_removed_actions_workflow` |
| Rollback not universally safe | `tests.test_authority_honesty.TestRollbackTruth.test_rollback_rejects_universal_safety_claim_and_names_dependency_boundary` |
| Built/pending/future states explicit | `tests.test_authority_honesty.TestBuiltStateTruth.test_active_docs_distinguish_implemented_pending_proof_and_future` |
| Hermetic pointer schema/version | `tests.test_authority_honesty.TestHermeticReleasePointer.test_schema_and_version_are_exact` |
| Hermetic source commit | `tests.test_authority_honesty.TestHermeticReleasePointer.test_source_commit_matches_source_head` |
| Hermetic source/runtime paths | `tests.test_authority_honesty.TestHermeticReleasePointer.test_source_and_runtime_are_exact_and_hermetic` |
| Installed byte integrity | `tests.test_authority_honesty.TestHermeticReleasePointer.test_installed_package_contract_and_checker_bytes_match_source` |
| Real HOME/XDG untouched | `tests.test_authority_honesty.TestHermeticReleasePointer.test_real_home_and_xdg_roots_are_untouched` |
| Pointer mismatch tests bite | `tests.test_authority_honesty.TestHermeticReleasePointer.test_wrong_schema_commit_source_or_runtime_is_rejected` |
| Installed-byte mismatch test bites | `tests.test_authority_honesty.TestHermeticReleasePointer.test_mismatched_installed_bytes_are_rejected` |
| Zero-link | `python3 -m unittest tests.test_zero_link` |
| Documentation governance | doc-warden `Overall: CONFORMANT` |
| Changed paths bounded | exact §10 local and GitHub compare lists; no G0-V-owned path |
| Final remote canary | both current required contexts `success` on exact final G0-R head under merged G0-V lock |
| Composite not overclaimed | G0 remains `in_progress`; RESUME directs separate acceptance/closeout |

---

## 14. Stop conditions and operator gates

Stop and return to the operator if:

- the accepted v3 path/digest or this accepted plan no longer matches the recorded immutable bytes,
  or explicit implementation authority is absent;
- any required G0-V-R/H/P/L or G0-C-AWA receipt is absent, stale, unverifiable, or no longer merged;
- host authority proves G0-H is required but its separate receipt is absent;
- any required change falls outside §10, including any attempted `Makefile`, `install.sh`, `.github`,
  host, or consumer mutation;
- a required correction changes a frozen required key, authoritative optional type, existing enum
  member, rule/invariant text, or machine-check status;
- any pending declaration cannot be represented by the G0-R0 checker without weakening it;
- an old reader must accept a newly emitted field/member in this delivery;
- exact completed-phase or child evidence would need rewriting rather than factual annotation;
- G0-R would need to mark itself or composite G0 done before a real merge and separate acceptance;
- a router commit would be used as evidence for an external consumer/host/protected-path commit;
- the canonical gate is not noexec-compatible or a hermetic pointer/source/runtime/byte test is
  parse-only, existence-only, or fails to bite on a controlled mismatch;
- canonical remote verification requires hand-editing a lock or combining serial recipe/lock phases;
- a protected-path merge would require the agent to self-approve, arm auto-merge, bypass a failing
  check, or use unauthorized admin merge;
- either current required check context is absent or non-success on the exact final G0-R head;
- doc-warden, zero-link, focused tests, `make verify`, `make status-verify`, or exact changed paths
  fail; or
- a far-reaching authority or compatibility decision not settled in accepted v3 appears.

Operator gates:

1. Ordered acceptance is complete: design v3 was accepted first, then this G0-R v1 plan. Neither
   acceptance authorizes implementation.
2. Separately plan, accept, authorize, and deliver G0-V and G0-C-AWA; G0-H only if owner-proven.
3. Explicitly authorize final G0-R implementation after every required receipt exists.
4. Use the ordinary reviewer-App-controlled merge path for G0-R; never pre-arm it.
5. After the real G0-R merge, separately accept/reject composite G0 and authorize its ledger
   closeout. No later phase starts before that gate.

---

## 15. Implementation-agent recommendation

Use the deep model tier with maximum reasoning for final G0-R. The work changes durable authority,
contract-roadmap provenance, ledger semantics, and rollback/security claims across many files even
though runtime behavior stays intentionally small. Do not parallelize writers in one worktree.

Expected cadence after all child-receipt preconditions and explicit implementation authorization:

1. Revalidate every G0-V/G0-C-AWA receipt and the G0-H not-required/required determination; stop on
   any gap before mutation.
2. Implement T1 and prove strict ledger honesty without closing G0.
3. Implement T2 and prove no authoritative contract promotion.
4. Implement T3 and run the exact stale-claim regressions.
5. Implement T4 and prove exact CLI metadata/no new handlers, including the C0 phrasebook marker.
6. Run T5's pre-existing G0-V hermetic/canonical-gate tests; do not absorb a G0-V defect.
7. Deliver T6 as one ordinary Draft PR, review to clean, and require both exact current checks.
8. Capture the G0-R merge receipt and stop for separate composite-G0 acceptance/closeout; do not
   begin any later phase.

---

## 16. Acceptance record

The operator accepted this plan on 2026-09-03 after accepting the exact v3 authority recorded above.
This acceptance approves:

- final-G0-R identity after completed G0-V/G0-C-AWA children;
- the exact router G0-R scope and changed-path set;
- the ledger/checkpoint and phase-ID model;
- pending-only contract declaration mapping;
- CLI taxonomy and the C0 phrasebook revisit marker;
- behavior-specific authority-honesty and inherited hermetic-provenance proof;
- delivery, rollback, and stop conditions; and
- the separate post-merge composite-G0 acceptance/ledger-closeout gate.

Acceptance still does not authorize implementation before exact child receipts and explicit
implementation authority. It never authorizes protected G0-V mutations, consumer changes,
composite-G0 closure, smart behavior, state persistence, fleet enrollment, release, or migration.

Recorded decision:

> **Accepted `g0-r-authority-honesty-v1.md` as the future executable basis for the final
> router-owned G0-R reconciliation after exact G0-V and G0-C-AWA receipts exist.**
