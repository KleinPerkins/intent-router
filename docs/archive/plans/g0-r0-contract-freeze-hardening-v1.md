# G0-R0 contract-freeze hardening plan v1

**Status:** DRAFT — 2026-09-02  
**Plan-type:** agentic-execution  
**Purpose:** Implementer-grade plan for the router-owned G0-R0 phase. This plan is not accepted and
authorizes no implementation.

## 1. Phase boundary

G0-R0 closes one verified guard gap before any new authoritative v1 optional field or enum member
lands. It changes contract-freeze metadata, checker logic, and adversarial tests only. It does not
add product contract fields, implement later phases, or reconcile the broader roadmap authorities.

Accepted design authority:
`docs/plans/roadmap-revision-step-3-design-v2.md`, accepted digest
`9f1098920e531818d1e845f7f11ed3480a7d86ffb738326c98f819835fc8afb1`.

## 2. Confirmed current ground truth

### 2.1 Reproduced defect

The shipped checker currently freezes:

- expected files/status in `checks/intent-contract-freeze.sh::EXPECTED` (around lines 48–54);
- exact top-level required maps in `FLOOR` (around lines 62–83);
- one nested required map in `NESTED_FLOOR` (around lines 87–89); and
- selected enum subsets in `ENUM_FLOOR` (around lines 92–102).

It does not compare top-level `optional_keys`, nested `optional_keys`, or every declared enum.

The defect was reproduced on 2026-09-02 through the existing
`tests.test_contract_freeze._run_checker_against` temporary-copy harness:

1. copy the real contracts into a temporary `INTENT_HOME`;
2. remove `intent-feedback/v1.optional_keys.correction`; and
3. run the shipped `checks/intent-contract-freeze.sh`.

Observed result: exit code `0`, all five contracts reported `PASS`, and
`intent-contract-freeze: OK`.

This confirms current behavior. The intended post-phase behavior is exit non-zero with a diagnostic
naming the removed frozen optional key.

### 2.2 Existing protections

- Required-key set equality and required type equality already bite.
- `intent-catalog/v1` nested `param` required keys already bite.
- Selected enum-member removal already bites.
- Freeze status/date/exemption and schema/version/freeze strings already bite.
- `tests/test_additive_compat.py` checks deferred-addition/manifest agreement and prevents some
  key collisions/removals, but it does not freeze all currently accepted optional names/types.
- `make verify` runs `tests/run-tests.sh`, the shell checker, strict status verification, and install
  static preflight.
- `tests/run-tests.sh` discovers every `tests/test_*.py`.
- The current runnerless protected job `repo.intent-router.m3-verify` runs
  `bash tests/run-tests.sh`; therefore new unittest regressions in `tests/test_contract_freeze.py`
  run remotely. It does not run the full canonical `make verify`.
- No staged/unstaged runner-configuration change exists at planning time.

### 2.3 Current five-contract frozen inventory

The implementation copies this exact accepted behavior into one declarative manifest floor. It does
not infer a floor dynamically from the contract being checked.

| Contract | Required top-level floor | Frozen optional floor | Nested floor | Enum-member floor |
|---|---|---|---|---|
| `intent-catalog/v1` | `verb:string`; `aliases:array`; `examples:array`; `param_schema:array<param>`; `preconditions:array`; `safety_class:enum`; `tool_path:enum`; `start_point_rules:object`; `plain_label:string`; `consequence_copy:string` | none | `param.required={name:string,type:enum,required:bool}`; `param.optional={enum:array,source:enum}` | `safety_class={read,write,destructive}`; `tool_path={cli,mcp,hook}`; `param.type={string,int,number,bool,enum,path,ref}`; `param.source={literal,regex,enum,repo-resolver,llm}` |
| `intent-map/v1` | `intent_key:string`; `utterance_examples:array`; `target_verb:string`; `param_bindings:object`; `weight:number`; `confidence:number`; `hit_count:int`; `last_used:string|null`; `outcome_stats:object`; `source:enum`; `version:int` | none | none | `source={seed,manual,feedback}` |
| `intent-feedback/v1` | `ts:string`; `consumer:string`; `catalog_version:string`; `utterance:string`; `proposal:object`; `operator_choice:enum`; `verdict:enum`; `confidence:number`; `outcome:enum`; `session_id:string` | `correction:object|null` | none | `operator_choice={accept,correct,reject,clarify,abort}`; `outcome={success,refused,failed,noop,unknown}`; `verdict={strong,weak,none}` |
| `intent-constitution/v1` | `rules:array<rule>`; `kernel_invariants:array<invariant>`; `machine_checks:object`; `banned_terms:object`; `operator_outcomes:array` | none | none | `machine_check.status={active,spec}` |
| `intent-proposal/v1` | `consumer:string`; `verb:string`; `params:object`; `start_point:string`; `safety_class:enum`; `tool_path:enum`; `confidence:number`; `verdict:enum`; `why:array`; `missing_params:array`; `requires_confirmation:bool` | none | none | `verdict={strong,weak,none}`; `safety_class={read,write,destructive}`; `tool_path={cli,mcp,hook}` |

The current checker omits the frozen `correction` optional; both nested catalog optionals;
catalog `param.type`/`param.source`; feedback `verdict`; and constitution
`machine_check.status`.

## 3. Objective

After G0-R0:

1. one existing declarative artifact contains the complete expected frozen behavior for all five
   v1 contracts;
2. the shell checker compares actual contracts to that floor;
3. removal/rename/retype/type-union narrowing of required, optional, and nested fields fails;
4. removal of any accepted enum member fails;
5. unrecorded optional/enum additions fail;
6. sanctioned additive optional/enum expansion succeeds only when contract, deferred addition, and
   manifest freeze metadata move together;
7. all old fixtures/readers and completed-phase tests still pass; and
8. the exact required runnerless check proves the same regressions remotely.

## 4. Locked invariants and non-goals

### Locked

- CR1/CR2: router still proposes only and never authorizes.
- CR4: additive within v1; no required removal/rename/retype/addition.
- CR5: contract/catalog content remains data.
- KI1: consumer remains safe with router absent.
- Zero-link remains green.
- All five v1 contracts remain frozen.
- One phase, one router PR.
- No paid or Actions runner.

### Non-goals

- No new optional field or enum member in any product contract.
- No F0 registration/fleet schema.
- No proposal/feedback typed-event additions.
- No State Controller, raw store, provider, smart ranking, AWA, host, or synchronization change.
- No authoritative architecture/security/rollback reconciliation; that belongs to G0-R.
- No runner recipe/lock change unless the current remote job fails to execute the new tests. Current
  inspection says it already executes them, so none is planned.
- No broad ledger/RESUME rewrite.

## 5. Simplest durable freeze model

### 5.1 Single declarative expected floor

Extend the existing `contracts/additive-manifest.json` with a top-level
`frozen_behavior` object keyed by the five schema strings.

For each schema, record:

- file name;
- expected frozen status;
- exact top-level `required_keys` name→type map;
- exact currently accepted top-level `optional_keys` name→type map;
- exact nested required/optional name→type maps that the current contract format expresses; and
- exact currently accepted enum-member sets.

This is not a new registry. The additive manifest already owns the cross-contract additive roadmap.
It becomes the one declarative **expected** frozen baseline. Contract JSON remains the actual
declared shape; checker Python compares actual to expected. The checker no longer owns duplicate
`FLOOR`, `NESTED_FLOOR`, or `ENUM_FLOOR` constants.

### 5.2 Exact comparison rules

- Required map: exact key set and exact type strings.
- Optional map: exact key set and exact type strings.
- Nested required/optional maps: exact container set, exact key set, exact type strings.
- Enums: exact unique member set against the accepted floor.
- Type strings are semantic atoms in the existing format. Exact equality catches union narrowing,
  e.g. `object|null → object` or `string|null → string`.
- Contract schema/version/status/freeze metadata remains checked.
- Extra/missing contract file remains checked.
- `deferred_additions` remains required and is still cross-checked by additive compatibility tests.

Exact optional/enum equality intentionally means that even an additive field/member cannot become
authoritative accidentally. A sanctioned addition updates, in one PR:

1. the contract's actual `optional_keys` or `enums`;
2. that contract's `deferred_additions`;
3. `additive-manifest.deferred_phases`; and
4. `additive-manifest.frozen_behavior`.

The updated checker and generated tests must pass before a writer uses the addition. Future
additions remain additive; the process freezes the expanded floor rather than forbidding expansion.

## 6. Planned file/symbol changes

| File | Current symbol/area | Planned change |
|---|---|---|
| `contracts/additive-manifest.json` | top-level metadata, `required_additive_phases`, `deferred_phases` | Add complete `frozen_behavior` for all five contracts; do not add product fields or change deferred phase meaning |
| `checks/intent-contract-freeze.sh` | embedded Python `EXPECTED`, `FLOOR`, `NESTED_FLOOR`, `ENUM_FLOOR`, contract loop | Load/validate manifest floor; remove duplicated floor constants; compare exact required/optional/nested/enum shapes with clear diagnostics |
| `tests/test_contract_freeze.py` | `_run_checker_against`, `_edit_json`, `_FROZEN`, `TestContractFreezeRegression` | Add manifest-aware temporary mutation helpers and table-driven adversarial matrix |
| `tests/test_additive_compat.py` | `_load_manifest`, `TestAdditiveCompat` | Validate manifest floor covers exactly five contracts and sanctioned additions update actual/deferred/frozen metadata coherently |
| `status.yml` | phase list/current phase | No R0 implementation-PR edit; G0-R later records the merged G0-R0 receipt as its own completed ledger entry |
| `RESUME.md` | exact next action | No R0 implementation-PR edit; broader G0-R reconciliation changes the pointer after exact G0-R0 merge evidence exists |
| `Makefile`, `tests/run-tests.sh` | `verify`, unittest discovery | No planned change; existing paths execute new checks |
| `.github/pr-automation.json`, lock | required check and protected recipe | No planned change; existing protected recipe runs all unittests |

## 7. Systematic adversarial matrix

Tests derive cases from `frozen_behavior` rather than one test per field.

| Mutation family | Generated scope | Expected result |
|---|---|---|
| Remove required field | Every top-level and nested required entry across five contracts | Shell checker non-zero; diagnostic names schema/path and `DROPPED` |
| Retype required field | Every required entry using a deterministic unequal sentinel type | Non-zero; `RETYPED` |
| Add required field | At least one top-level and one nested representative | Non-zero; required addition needs v2 |
| Remove optional field | Every top-level/nested frozen optional; begins with `intent-feedback.correction` | Non-zero; `DROPPED frozen optional` |
| Retype optional field | Every frozen optional | Non-zero; `RETYPED frozen optional` |
| Narrow union | Every required/optional type string containing `|` | Non-zero; names original and narrowed type |
| Remove enum member | Every member of every enum floor across all five contracts | Non-zero; names enum/member |
| Add unrecorded optional | Representative top-level and nested additions without manifest floor update | Non-zero; unexpected optional |
| Add unrecorded enum member | Representative enum addition without manifest floor update | Non-zero; unexpected enum member |
| Sanctioned optional addition | Temporary contract + deferred addition + deferred-phase manifest + frozen floor update | Checker passes and additive validator accepts |
| Sanctioned enum extension | Temporary enum + deferred enum addition + manifest records | Checker passes and additive validator accepts |
| Old fixtures/readers | Unmodified repository full suite | Existing fixtures/readers still pass |

Generated cases must preserve deterministic names/subtests so a failing field is obvious. A failure
message must include contract schema plus dotted path, e.g.
`intent-feedback/v1 optional_keys.correction RETYPED`.

## 8. Execution task blocks

### Task G0-R0-T1 — Declare complete frozen behavior

**Purpose:** Make the existing additive manifest the sole declarative expected floor.

**Files:**

- `contracts/additive-manifest.json`
- `tests/test_additive_compat.py`

**Interfaces:**

- Input: current five contract JSON files.
- Output: `frozen_behavior` matching the inventory in §2.3.
- No product contract shape change.

**Steps:**

- [ ] Add `frozen_behavior` with exactly five schema keys, file/status, exact top required/optional,
  nested required/optional, and enum floors.
- [ ] Preserve all existing `required_additive_phases` and `deferred_phases` meaning byte-for-byte
  except formatting required by the JSON edit.
- [ ] Add additive-compat assertions that manifest coverage is exactly the five contract schemas,
  each file/schema resolves, maps are objects, enum floors are unique arrays, and actual baseline
  equals the declared floor before mutations.
- [ ] Assert `correction:object|null`, catalog nested optionals, all four catalog enum sets,
  feedback `verdict`, and constitution `machine_check.status` are present.

**Tests:**

- `python3 -m unittest tests.test_additive_compat`
- `bash checks/intent-contract-freeze.sh` (expected to stay green before T2 rewires it only if T1 is
  staged with a backward-compatible manifest addition)

**Acceptance:**

- Manifest parses and covers all inventory rows.
- Existing deferred-addition tests retain their meaning.
- No five-contract content changes.

**Rollback:** Revert T1 while no checker depends on `frozen_behavior`. Once T2 lands atomically in
the same PR, roll back T1+T2 together only before dependent authoritative additions.

**Dependencies:** Accepted Step 3 v2; no code dependency.

**Expected evidence:** focused unittest output and manifest diff showing only freeze metadata.

### Task G0-R0-T2 — Rewire the shipped checker

**Purpose:** Make the production freeze gate enforce the declarative floor.

**Files:**

- `checks/intent-contract-freeze.sh`
- `contracts/additive-manifest.json`

**Interfaces:**

- `INTENT_HOME` remains the role-resolved test/install root.
- Exit `0` only when every frozen behavior comparison passes.
- PASS/FAIL text remains shell-readable and names exact drift.

**Steps:**

- [ ] Load and validate `contracts/additive-manifest.json`.
- [ ] Replace embedded `FLOOR`, `NESTED_FLOOR`, and `ENUM_FLOOR` with
  `frozen_behavior`; keep only the finite expected five schema/file set or derive it from the
  validated manifest.
- [ ] Compare required and optional maps exactly at top/nested paths.
- [ ] Compare enum member sets exactly; reject duplicates/non-strings.
- [ ] Keep schema/version/status/freeze strings/date/exemption, file presence, and unexpected v1
  contract checks.
- [ ] Retain `deferred_additions` object validation.
- [ ] Emit path-specific `DROPPED`, `ADD`, `RETYPED`, and enum diagnostics.
- [ ] Update checker comments to state the manifest is expected authority and contracts are actual
  declarations.

**Tests:**

- `bash checks/intent-contract-freeze.sh`
- `python3 -m unittest tests.test_contract_freeze.TestContractFreeze`

**Acceptance:**

- Current repository passes.
- Removing `correction` now fails.
- No duplicate expected floor remains in checker code.

**Rollback:** T1+T2 governed revert is allowed only before any later optional/enum authority depends
on this floor. After dependency, weakening/removal is forbidden; forward-fix only.

**Dependencies:** T1 must land before or atomically.

**Expected evidence:** checker PASS on real tree and reproduced defect FAIL output.

### Task G0-R0-T3 — Generate the adversarial freeze matrix

**Purpose:** Prove every accepted field/member bites through the shipped checker.

**Files:**

- `tests/test_contract_freeze.py`

**Interfaces:**

- Reuse `_run_checker_against(mutate)`.
- Add helpers that load/mutate the temporary additive manifest and enumerate its frozen floor.

**Steps:**

- [ ] Convert representative required/enum regressions into table-driven subtests where practical,
  retaining explicit proposal unfreeze coverage.
- [ ] Generate remove/retype cases for every top/nested required and optional entry.
- [ ] Generate enum-member removal for every declared floor.
- [ ] Generate union-narrowing cases for every `|` type.
- [ ] Add explicit first regression for missing `intent-feedback.optional_keys.correction`.
- [ ] Add unrecorded optional/enum-addition failures.
- [ ] Add sanctioned optional/enum-addition passing fixtures that update actual, deferred, and
  manifest freeze metadata together.
- [ ] Ensure each failure checks non-zero plus schema/dotted-path diagnostic.

**Tests:**

- `python3 -m unittest tests.test_contract_freeze`
- Temporarily break one generated case locally to prove the matrix itself bites, then restore before
  commit.

**Acceptance:**

- All inventory entries are enumerated with no hand-maintained duplicate field list in the test.
- The exact reproduced `correction` defect is closed.
- Legitimate sanctioned additive growth remains possible.

**Rollback:** Same dependency rule as T2. Test-only corrections may forward-fix; never delete guard
coverage after downstream dependency.

**Dependencies:** T1/T2.

**Expected evidence:** unittest subtest count/field paths and passing real-tree gate.

### Task G0-R0-T4 — Prove additive and legacy compatibility

**Purpose:** Ensure stronger freezing does not convert additive v1 into a closed/no-growth schema.

**Files:**

- `tests/test_additive_compat.py`
- `tests/test_contract_freeze.py`
- existing fixtures/readers (verification only; edit only if a test reveals a genuine bug, then
  stop because that exceeds this plan)

**Interfaces:**

- Contract `deferred_additions` ↔ manifest `deferred_phases` remains bidirectional.
- Manifest frozen floor ↔ actual accepted shape becomes exact.

**Steps:**

- [ ] Assert every authoritative optional/enum addition updates all required metadata in one
  temporary fixture.
- [ ] Assert deferred-but-not-yet-authoritative keys do not enter the frozen actual optional floor.
- [ ] Assert existing required-floor tests remain intact.
- [ ] Run full suite to prove old proposal/catalog/feedback fixtures and readers still parse.
- [ ] If compatibility requires runtime/product changes, stop; do not broaden G0-R0.

**Tests:**

- `python3 -m unittest tests.test_additive_compat tests.test_contract_freeze`
- `make verify`
- `make status-verify`

**Acceptance:**

- Sanctioned additive fixture passes.
- Unsanctioned additions and all narrowing/removal/retypes fail.
- Full existing suite is unchanged-green.

**Rollback:** Governed revert before dependencies; forward-fix after.

**Dependencies:** T1–T3.

**Expected evidence:** focused tests plus canonical local gates.

### Task G0-R0-T5 — Deliver one router PR and capture proof

**Purpose:** Establish the first composite-G0 child receipt without claiming broader G0 completion.

**Files:**

- G0-R0 implementation files from T1–T4
- no `.github/*`, `status.yml`, or `RESUME.md` changes

**Interfaces:**

- Required remote check: `pr-automation / verify`.
- Protected recipe job: `repo.intent-router.m3-verify` → `bash tests/run-tests.sh`.

**Steps:**

- [ ] Run focused tests, `make verify`, `make status-verify`, and `git diff --check`.
- [ ] Confirm zero-link and that no product contract content changed.
- [ ] Open one Draft router PR for G0-R0; do not pre-arm or bypass automation.
- [ ] Confirm the existing required remote check runs the new unittest matrix and passes on the
  exact PR head.
- [ ] Run the governed review cadence below until clean.
- [ ] After the governed merge, capture PR URL, exact live-default merge commit, check identity/head,
  manifest digest, checker digest, and test evidence as the G0-R0 child receipt.
- [ ] Hand that receipt to G0-R; do not claim composite G0 closed.

**Tests:**

- Local gates above.
- Remote `pr-automation / verify` on exact PR head.

**Acceptance:**

- Exact merged receipt exists.
- No later additive authority has landed ahead of G0-R0.
- No runner configuration changed.

**Rollback:** Before dependent additions, governed revert of the G0-R0 PR is allowed. Once later
v1 optional/enum authority relies on the guard, weakening/revert is forbidden; forward-fix in a new
PR is the only safe response.

**Dependencies:** T1–T4 and operator approval to implement/merge; this DRAFT plan grants neither.

**Expected evidence:** local logs, remote exact-head check, merged commit/PR, child receipt.

## 9. Ledger and resume handling

G0-R0 should become its own phase/checkpoint entry, but not inside the G0-R0 implementation PR.

Reason:

- current `status.yml`/`tests.test_status_verify._ALL_PHASES` encode the old monolithic ladder;
- `current_phase` must equal the first non-done router phase;
- a `done` row requires a real PR, exact resolvable/ancestor commit, and passing test IDs; and
- the governed merge commit does not exist until after the implementation PR merges.

Therefore:

1. G0-R0 PR changes only freeze metadata/checker/tests.
2. Its merge/check receipt proves the child delivery.
3. The immediately following G0-R authority-honesty PR adds the `G0-R0` done row, updates status
   parser/test expected phase IDs, introduces the composite G0 checkpoint/future split, and
   regenerates `RESUME.md`.
4. The row may be `done` only when it pins the real merged G0-R0 commit, PR, files, and passing test
   IDs.
5. Completed P0/R-core/A0/egress evidence is preserved exactly; no historical test meaning changes.

This narrowly defers broader ledger reconciliation to its accepted owner while giving G0-R0 an
honest exact receipt.

## 10. Runnerless remote proof

Current sanctioned path:

- check name: `pr-automation / verify`;
- required protected job: `repo.intent-router.m3-verify`;
- command: `bash tests/run-tests.sh`;
- unittest discovery: every `tests/test_*.py`.

Thus the current recipe already runs the new generated contract-freeze tests. G0-R0 does not edit
runner files. Local `make verify` remains mandatory because it separately executes the shell freeze,
strict status verification, and install static check. Local `make status-verify` is rerun explicitly
for the requested evidence.

Canonical remote recipe hardening to `make verify` belongs to G0-R, not this isolated phase. If the
remote job fails to discover the new tests in practice, stop and re-scope with the operator; do not
silently edit protected runner configuration.

## 11. Acceptance ledger and traceability

| Requirement | Deterministic test/evidence |
|---|---|
| Reproduced defect closed | Generated optional-removal case for `intent-feedback/v1.optional_keys.correction` returns non-zero |
| All five contracts covered | Manifest coverage test: exact five schema/file keys |
| Required floors preserved | Generated every required remove/retype; representative added-required |
| Top optional floors frozen | Generated every top optional remove/retype |
| Nested semantics frozen | Generated catalog `param` required/optional remove/retype |
| All enum floors frozen | Generated every enum-member removal, including currently omitted enum sets |
| Union narrowing fails | Generated every `|` type narrowing |
| Unrecorded additions fail | Optional/enum addition without manifest floor update |
| Sanctioned additions work | Temporary atomic contract/deferred/manifest/floor optional and enum fixtures pass |
| One expected authority | Checker contains no `FLOOR`/`NESTED_FLOOR`/`ENUM_FLOOR`; manifest owns expected maps |
| Legacy compatibility | Existing full test suite/fixtures pass unchanged |
| CR1/CR2/CR5/KI1 unchanged | `make verify`; no runtime/consumer files changed |
| CR4/zero-link | Freeze/additive/zero-link tests pass |
| Honest phase evidence | G0-R0 child receipt; later G0-R ledger row only after real merge |
| Local proof | Focused tests, `make verify`, `make status-verify`, `git diff --check` |
| Remote proof | Exact-head `pr-automation / verify` includes generated unittest matrix |
| One phase/one PR | One G0-R0 router PR; no mixed G0-R changes |

## 12. Stop conditions and operator gates

Stop implementation and return to the operator if:

- any fix requires changing a five-contract product field/member;
- checker hardening would reject current valid fixtures/readers without a metadata error;
- one declarative manifest cannot represent an existing contract's actual type semantics;
- a required test needs runtime, AWA, host, provider, State Controller, or registry work;
- remote proof does not execute the new tests and would require protected runner changes;
- zero-link fails;
- completed phase evidence would need rewriting;
- an authoritative optional/enum addition has landed before the guard; or
- a far-reaching compatibility decision appears.

Operator gates:

1. Accept/revise this plan before implementation.
2. Explicitly authorize the G0-R0 implementation PR.
3. Follow the repository's governed review/merge gate.
4. Accept the merged G0-R0 child receipt into composite G0/G0-R reconciliation.

## 13. Implementation-agent recommendation and cadence

Use the **deep** model tier with maximum available reasoning. Recommended concrete model:
`claude-opus-4-8-thinking-max`.

Why: the code change is small, but it mutates a frozen compatibility guard whose failure can bless
future breaking v1 changes. The agent must reason across shell-embedded Python, five declarative
contract shapes, generated adversarial testing, additive compatibility, rollback, and status-proof
semantics. Economy/standard execution is not proportionate to that irreversibility risk.

Expected cadence after plan acceptance:

1. implement T1–T4 in one isolated worktree;
2. run focused and canonical local gates;
3. open one **Draft** G0-R0 PR, leaving merge automation unarmed;
4. run `/loop /review-bugbot` until no actionable findings remain;
5. confirm exact-head runnerless verification;
6. merge only through the governed operator/reviewer gate;
7. capture the exact G0-R0 receipt; and
8. stop before G0-R planning/reconciliation.

No implementation agent is launched by this plan.

## 14. Plan acceptance checkpoint

Accepting this plan authorizes neither code changes nor delivery. It only approves G0-R0's exact
implementation scope and evidence model.

Decision:

> **Accept, revise, or reject `g0-r0-contract-freeze-hardening-v1.md` for a later explicitly
> authorized one-PR implementation.**

