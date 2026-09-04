# G0-V-R local-gate prerequisite plan v1

**Status:** ACCEPTED — 2026-09-03  
**Plan-type:** agentic-execution  
**Purpose:** Define the one ordinary router PR that makes canonical `make verify`
noexec-compatible and adds hermetic release-pointer/source/runtime/byte-integrity proof before
host command qualification.
**Accepted design authority:** `docs/plans/roadmap-revision-step-3-design-v3.md`, SHA-256
`276693025446414411cf8cd016344b53d6179fd06bb791b9660f46f40fe3e184`.
**Execution-plan precedent:** `docs/plans/g0-r0-contract-freeze-hardening-v4.md` supplies the
agentic-execution shape only; accepted design v3 is the semantic authority for G0-V-R.

On 2026-09-03 the operator explicitly selected **"Accept the plan and deliver G0-V-R."** That
selection accepts these exact plan bytes and separately authorizes G0-V-R implementation/delivery
only after this accepted plan and its `docs/plans/README.md` index entry merge to live
`origin/main`. It does not authorize implementation from unmerged bytes or any host/protected-path
mutation.

---

## 1. Delivery identity, ownership, and order

G0-V-R is the first serial child of G0-V. It is owned wholly by
`KleinPerkins/intent-router` and lands as one ordinary router PR. It does not own the host command,
the protected recipe, the generated lock, or final G0-R reconciliation.

### Required order

1. **G0-R0 is done.** PR
   `https://github.com/KleinPerkins/intent-router/pull/55` merged as
   `e30644cfac2470143f45e89eff37b612dc9dbc28`; both required contexts succeeded on exact PR head
   `3da2b6ef01eaadc54ffadc749d2ffa0c4d4283bd`.
2. **G0-V-R lands first:** this plan's ordinary router prerequisite.
3. **G0-V-H follows:** the host verification authority changes and exact-image-qualifies the
   intent-router command as `["make", "verify"]`.
4. **G0-V-P follows:** the protected-path owner lands one generated recipe-only router PR from
   merged host authority.
5. **G0-V-L follows:** the protected-path owner lands one generated lock-only router PR compiled
   from the merged default-branch recipe.
6. **G0-C-AWA may proceed independently** of G0-V, under its own repository authority.
7. **Final G0-R waits** for merged G0-V-R/H/P/L and G0-C-AWA receipts, plus G0-H only if its owner
   proves that optional projection is required.

This order is acyclic. G0-V-R proves the local command before G0-V-H qualifies it; G0-V never
waits for G0-R; final G0-R consumes already-merged receipts without manufacturing them.

### In scope

- Interpreter-invoke every `install.sh` use in `Makefile`.
- Add the hermetic full install lifecycle to canonical `make verify`, after its existing test,
  freeze, strict-status, and static-install checks.
- Make the lifecycle clean up its throwaway roots on both success and failure.
- Strengthen the install doctor's existing release-pointer check from JSON-parse-only to exact
  identity and source/runtime byte-integrity validation.
- Add local, unprivileged execute-bit-independence and hermetic provenance/tamper regressions.
- Deliver one ordinary router PR and an exact G0-V-R receipt.

### Out of scope

- G0-V-H host command mapping or exact controller-image qualification.
- G0-V-P recipe generation or protected-path delivery.
- G0-V-L lock compilation or protected-path delivery.
- Final G0-R authority reconciliation, any ledger/resume update, or composite-G0 closeout.
- G0-C-AWA, G0-H, A0-P, F0, S0, R2a, provider, fleet, calibration, or surface work.
- Router proposal behavior, consumer execution/authorization, contracts, release publication,
  shelf/registry enrollment, synchronization, or host state.
- Making `bootstrap.sh` or `bin/intent` generally runnable from a noexec mount. Neither is reached
  by canonical `make verify`; widening to them would exceed the accepted G0-V-R purpose.
- Privileged mount creation or a local claim that the controller's exact image has qualified.

---

## 2. Verified current ground truth

Evidence is separated deliberately:

- **Source-confirmed local evidence:** read from the exact repository/base, Git history, or current
  protected configuration.
- **Local test evidence:** reproduced by the baseline/probes recorded below.
- **Standalone-review evidence:** the six named review findings drive plan corrections but do not
  count as implemented runtime proof.
- **Accepted-design evidence:** binding architecture/order from immutable design v3.
- **Later external evidence:** exact controller image/mount/limit qualification owned by G0-V-H;
  it is not claimed by this plan.

### 2.1 Repository and authority

- **Local source evidence:** canonical remote is
  `git@github.com:KleinPerkins/intent-router.git`.
- **Local source evidence:** branch is `docs/g0-v-r-local-gate-plan-v1`.
- **Local source evidence:** `HEAD`, fetched `origin/main`, and their merge base all equal
  `344ed6c65def54d6c0f13099145769466d75b9ae`.
- **Local source evidence:** the starting worktree was clean and had no staged files.
- **Local source evidence:** the accepted-design bytes hash to the exact authority digest recorded
  in this plan.
- **Live GitHub read evidence:** G0-R0 PR #55 is merged; base
  `040a746c119458136bafe493e73a46868356494c`, head
  `3da2b6ef01eaadc54ffadc749d2ffa0c4d4283bd`, merge
  `e30644cfac2470143f45e89eff37b612dc9dbc28`; both required checks reported `success` against that
  exact head.
- **Live GitHub read evidence:** current branch rules require both
  `pr-automation / verify` and
  `pr-automation / job:repo.intent-router.m3-verify`, each from verifier App integration
  `4274739`.

### 2.2 Baseline gates

**Local test evidence:** fresh baseline commands passed:

```text
make verify
  295 tests run; 4 deliberate future-phase skips; OK
  all five frozen-contract behavior floors PASS
  strict status verification PASS
  static install preflight PASS

make status-verify
  PASS — every done claim recomputed against disk/tests

make verify-install
  PASS — double install, doctor, uninstall in a throwaway HOME/XDG root

doc-warden check <absolute-worktree-root>
  Overall: CONFORMANT
```

The normal-mount lifecycle result does not prove noexec compatibility or tamper rejection.

### 2.3 Current `make verify` graph and execution form

`make -n verify` currently expands, in order, to:

```text
bash tests/run-tests.sh
bash checks/intent-contract-freeze.sh
PYTHONPATH=. python3 -m intent_router.status_verify --strict
./install.sh --check
echo "verify: OK"
```

The transitive source-script execution inventory is:

| Surface | Current invocation | Noexec relevance |
|---|---|---|
| unittest discovery | `bash tests/run-tests.sh` | Already interpreter-invoked |
| contract freeze | `bash checks/intent-contract-freeze.sh` | Already interpreter-invoked |
| strict ledger | `python3 -m intent_router.status_verify --strict` | Already interpreter-invoked |
| static install preflight | `./install.sh --check` | Direct pathname execution; fails when source execution is denied |
| `verify-install` install #1/#2 | `./install.sh` | Four lifecycle calls are direct pathname executions |
| `verify-install` doctor/uninstall | `./install.sh --doctor|--uninstall` | Same direct-execution defect |
| installer's freeze check | `bash "$RUNTIME/checks/intent-contract-freeze.sh"` | Already interpreter-invoked |
| freeze regression subprocess | `["bash", checker]` | Already interpreter-invoked |
| status-verifier tests/tools | `sys.executable`, `python3`, or image-provided `git`/`gh` | No repository script is directly executed |

`make verify` does **not** currently invoke `verify-install`. The standalone target cleans its
temporary directory only on its success path.

Other Make lifecycle targets (`install`, `repair`, `doctor`, `check`, `uninstall`) also directly
invoke `./install.sh`. G0-V-R changes those calls in the same Makefile edit so the invocation rule
cannot differ by target. `bootstrap.sh` contains direct `exec "$.../install.sh"` and `bin/intent`
is a shebang launcher; each would still depend on mount execution if used by pathname, but neither
participates in this gate and neither is allowlisted.

### 2.4 Reproduced local execution property

**Local test evidence:** an unprivileged focused probe copied `install.sh`, set mode `0644`, and
ran its help path:

```text
mode=644 direct_rc=126 interpreter_rc=0
```

The direct path was denied; `bash install.sh --help` succeeded. This proves the relevant local
property—explicit Bash invocation does not depend on the script's execute bit. It is not an exact
Linux `tmpfs,noexec` qualification.

### 2.5 Current release-pointer and lifecycle behavior

`install.sh` is the only release-pointer writer and validator. There is no separate pointer schema
or validator file.

The writer currently emits these exact fields:

| Field | Current hermetic value |
|---|---|
| `schema` | `intent-release-pointer/v1` |
| `version` | `intent_router.__version__`, currently `0.1.0` |
| `source` | exact source root |
| `commit` | `git -C "$SRC_ROOT" rev-parse HEAD`, or `unknown` when unavailable |
| `runtime` | exact `$XDG_DATA_HOME/intent-router/current` |
| `installed_at` | UTC second timestamp, preserved for an identical reinstall identity |

**Local test evidence:** a fresh throwaway install produced exact
schema/version/source/commit/runtime values and copied
representative package, contract, and checker bytes identically. The current doctor nevertheless:

- accepts any JSON object as a valid release pointer;
- does not validate pointer schema, version, source, commit, runtime, or timestamp;
- validates installed contract shape/freeze but not package/checker source-byte parity; and
- returned exit `0` after a controlled wrong pointer schema and after a controlled installed
  package-byte mutation.

Those two observed false accepts are the required red regressions. No real HOME/XDG path was
mutated by the probes.

### 2.6 Accepted-design evidence and external unknowns

- **Accepted-design evidence:** the host qualification workspace is specified as
  `tmpfs,noexec,nosuid,nodev`; G0-V-H owns exact-image/limit qualification of
  `["make", "verify"]`.
- **Local protected-config evidence:** the current recipe/lock still runs
  `["run-literal", "bash", "tests/run-tests.sh"]`, not canonical `make verify`.
- **External unknown:** this planning pass did not instantiate the controller image or its exact
  mounts. It therefore does not claim that `make verify` currently passes there.
- **External unknown:** the controller image's `/tmp` mount behavior and future G0-V-R exact-head
  check results remain unobserved.
- **Boundary:** G0-V-R proves source mechanics and hermetic behavior locally. G0-V-H must later
  reproduce the exact controller image/mount/limits and qualify the unchanged command. G0-V-P/L
  then deliver protected generated bytes.

---

## 3. Objective and non-goals

### Objective

After the G0-V-R implementation PR merges:

1. Canonical `make verify` preserves its existing ordered checks and then completes the full
   throwaway install/doctor/uninstall lifecycle.
2. Every repository shell script reached by that graph is opened through an explicit interpreter;
   source execute bits are not required.
3. A temporary source copy with repository scripts at mode `0644` passes `make verify-install`.
4. A throwaway pointer proves exact schema, package version, source HEAD, source root, runtime path,
   and a valid UTC install timestamp.
5. The installed Python package, all contract JSON bytes, and the shipped freeze checker match the
   source bytes before uninstall.
6. Doctor rejects controlled pointer-identity and installed-byte tampering.
7. The lifecycle touches only explicitly supplied throwaway HOME/XDG roots and removes its
   runtime/config/state/pointer plus outer/inner temp roots on success; ordinary failure preserves
   the original status and removes the same trapped tree.
8. Existing router, freeze, ledger, zero-link, no-execution, and install behavior remains green.
9. The merged receipt is sufficient for G0-V-H to qualify the exact merged source.

### Non-goals

- No exact controller qualification or protected automation change.
- No new contract/schema file and no modification to any frozen contract.
- No package version bump, release/tag, pin, shelf pointer, or enrollment.
- No installer redesign, backup model change, state-retention change, or general supply-chain
  attestation framework.
- No claim that pointer `commit` alone proves a clean source worktree. Local tests prove it equals
  source `HEAD`; exact committed bytes are bound later by the PR head/merge receipt and file
  digests.
- No arbitrary noexec sandboxing. The router remains a proposer, not a sandbox.

---

## 4. Exact meaning of noexec-compatible

For G0-V-R, **noexec-compatible** means all of the following:

1. The canonical command remains exactly `make verify`.
2. Every repository-owned shell file that command reaches is passed as data to an explicit
   `bash` process. No recipe relies on `execve("./script.sh", ...)`.
3. Python entry points are passed to `python3`/`sys.executable`; image-provided `make`, `bash`,
   `python3`, `git`, `grep`, `sed`, and similar tools remain external executable dependencies.
4. The source checkout's tracked execute bits may remain `100755`, but removing those bits in a
   temporary copy cannot break the tested lifecycle.
5. The ordered canonical gate is:
   `tests → contract freeze → strict status → static install check → hermetic install lifecycle`.
6. The lifecycle uses only throwaway HOME/XDG roots, invokes both source and installed copies
   through Bash, and cleans up through a trap.

### Local proof

Local unprivileged tests must combine:

- `make -n` graph inspection that rejects every direct Makefile `install.sh` execution and proves
  the ordered full gate;
- a temporary source copy with all repository shell/launcher execute bits cleared, an observed
  direct-execution denial, and a successful `make verify-install`; and
- real hermetic install, doctor, tamper-negative, byte-parity, and uninstall tests.

This simulates the property the source controls: scripts are read by interpreters and do not need
workspace execute permission.

### Later exact qualification

The local proof does **not** equate mode `0644` with every kernel/mount/image behavior. G0-V-H must
run `["make", "verify"]` in the exact controller image with its actual
`tmpfs,noexec,nosuid,nodev` workspace and limits. Any image-only failure belongs to G0-V-H
qualification and may require a new router forward-fix receipt; G0-V-R must not pre-claim it.

---

## 5. Exact implementation design

### 5.1 Makefile

The implementation must:

- replace every direct Makefile `./install.sh` command with explicit `bash ./install.sh`;
- preserve `bash tests/run-tests.sh`, `bash checks/intent-contract-freeze.sh`, and
  `python3 -m intent_router.status_verify --strict`;
- invoke `$(MAKE) --no-print-directory verify-install` after `bash ./install.sh --check` and before
  `verify: OK`;
- implement `verify-install` cleanup in POSIX `/bin/sh` syntax with one idempotent `cleanup`
  function, a `trap ... 0` exit handler, and separate HUP/INT/TERM handlers:
  - normal exit captures `$?`, disables all four traps, cleans, and exits with the captured status;
  - HUP/INT/TERM disable all four traps, clean, and exit with an explicit nonzero status;
  - a signal handler never returns to the recipe and can never print `verify-install: OK`;
- create one inner temp directory beneath the outer trapped lifecycle root and pass that exact path
  as `TMPDIR` to **every** install, doctor, and uninstall invocation, keeping `install.sh`'s own
  `mktemp` files inside the trapped tree;
- perform double install from the source via Bash;
- run doctor from the copied runtime via
  `bash "$XDG_DATA_HOME/intent-router/current/install.sh" --doctor`;
- run uninstall from the copied runtime via Bash, then positively assert runtime, pointer, config,
  and state paths are absent, explicitly call the idempotent cleanup, and only then report
  `verify-install: OK`; and
- keep target names and `.PHONY` membership unchanged.

Tests use an ordinary induced command failure to prove dynamic cleanup. HUP/INT/TERM behavior and
exit-status preservation are verified by static assertions over the Make recipe; tests do not send
real signals.

No tracked execute mode is removed. `tests/run-tests.sh`, `bootstrap.sh`, and `bin/intent` do not
change.

### 5.2 Release-integrity validator in `install.sh`

Add one read-only validator used by `do_doctor`; do not add a new mutating mode or pointer file.
The writer's six fields and `intent-release-pointer/v1` schema stay unchanged.

The validator must:

1. require the pointer and every monitored source/runtime file to be readable, regular, and
   non-symlink; do not impose a new exact permission mode;
2. parse the pointer as JSON and require string values for all six existing fields;
3. require `schema == "intent-release-pointer/v1"`;
4. require `version == intent_router.__version__` resolved from the pointer's source, currently
   `0.1.0`;
5. require canonical absolute `runtime` to equal the current XDG-derived `RUNTIME`;
6. allow the executing `install.sh` root to be only the exact pointer `source` or exact pointer
   `runtime`, preserving both source-invoked and installed-copy doctor use;
7. for both writer and validator Git children, construct the child environment by removing
   **every** inherited entry whose name starts with `GIT_`;
8. run canonical `git -C <source> rev-parse --show-toplevel`, require its resolved result to equal
   canonical `source`, then resolve `HEAD^{commit}` and require pointer `commit` to equal that exact
   commit object;
9. classify an exact source with its own `.git` directory/file, or a successful equal top-level
   result, as repository-backed; preserve `commit == "unknown"` only when Git is absent or
   canonical `source` is genuinely not a repository root, including a source directory nested
   beneath another repository whose reported top level differs; with Git present, any
   top-level/HEAD/commit failure for a repository-backed source is a fail-closed
   `source-identity` error rather than `unknown`;
10. parse `installed_at` as the exact UTC-second form `YYYY-MM-DDTHH:MM:SSZ`;
11. build deterministic relative-file sets for:
   - every regular, non-symlink `intent_router/**/*.py` file;
   - every regular, non-symlink `contracts/*.json` file; and
   - `checks/intent-contract-freeze.sh`;
12. exclude source `__pycache__`, `*.pyc`, and `*.pyo` from the installed runtime and reject any
    such installed artifact immediately after install and during doctor;
13. require nonempty source/runtime monitored sets to match exactly and compare every pair with
    SHA-256;
14. emit only path/category diagnostics, never source bytes, using stable categories
    `pointer-file-safety`, `pointer-identity`, `source-identity`, `runtime-file-safety`,
    `runtime-file-set`, `runtime-cache-exclusion`, and `runtime-byte-integrity`; and
15. return nonzero so `do_doctor` fails if any identity, required file, set, or byte comparison
    fails.

Resolve the package version without executing package code or writing `__pycache__` (parse the
single string assignment to `__version__` in `intent_router/__init__.py`). The broad `GIT_*`
filter—not a fixed variable list—is the implementation contract.

The doctor must accumulate the new integrity result without short-circuiting the existing
installed-contract JSON/freeze and CLI checks. This lets controlled semantic-neutral mutations
prove those older checks still pass while the new integrity category alone fails. No digest is
persisted in the pointer: byte proof is recomputed from source and runtime before uninstall.

### 5.3 Hermetic test harness

Create `tests/test_authority_honesty.py`; unittest discovery already includes it, so
`tests/run-tests.sh` does not change.

The helper must:

- use `TemporaryDirectory`/registered cleanup for every fixture;
- pass explicit throwaway `HOME`, `XDG_DATA_HOME`, `XDG_CONFIG_HOME`, and `XDG_STATE_HOME`;
- invoke shell files only as `["bash", path, ...]`;
- capture source `git rev-parse HEAD` and `intent_router.__version__` independently;
- take privacy-safe pre/post metadata snapshots of the real product roots without reading or
  logging router-state contents;
- always attempt hermetic uninstall in cleanup, even when an assertion fails; and
- never invoke `make verify` from a unittest (that would recurse through unittest discovery);
  graph checks use `make -n`, and dynamic checks invoke only `make verify-install`; and
- use no network, privileged mount, external repository, or persisted fixture.

Required exact test IDs:

```text
tests.test_authority_honesty.TestNoexecCompatibleGate.test_makefile_target_graph_is_interpreter_invoked_and_complete
tests.test_authority_honesty.TestNoexecCompatibleGate.test_verify_install_passes_with_nonexecutable_source_scripts
tests.test_authority_honesty.TestNoexecCompatibleGate.test_verify_install_cleans_throwaway_root_on_failure
tests.test_authority_honesty.TestHermeticReleasePointer.test_schema_and_version_are_exact
tests.test_authority_honesty.TestHermeticReleasePointer.test_source_commit_matches_source_head
tests.test_authority_honesty.TestHermeticReleasePointer.test_source_and_runtime_are_exact_and_hermetic
tests.test_authority_honesty.TestHermeticReleasePointer.test_installed_package_contract_and_checker_bytes_match_source
tests.test_authority_honesty.TestHermeticReleasePointer.test_real_home_and_xdg_roots_are_untouched
tests.test_authority_honesty.TestHermeticReleasePointer.test_wrong_schema_commit_source_or_runtime_is_rejected
tests.test_authority_honesty.TestHermeticReleasePointer.test_mismatched_installed_bytes_are_rejected
tests.test_authority_honesty.TestHermeticReleasePointer.test_git_source_identity_ignores_all_inherited_git_environment
tests.test_authority_honesty.TestHermeticReleasePointer.test_nested_nonrepository_source_does_not_inherit_parent_git_identity
tests.test_authority_honesty.TestHermeticReleasePointer.test_repository_backed_git_failure_is_rejected
```

The tests must make positive assertions over generated content and controlled negative assertions.
Existence-only or JSON-parse-only checks are insufficient.

Every tamper subtest follows this independent protocol:

1. clean install;
2. baseline doctor exit `0`;
3. exactly one controlled mutation;
4. prove pre-existing semantic checks still pass where applicable;
5. require doctor nonzero **and** the exact new integrity category expected for that mutation;
6. reinstall/reset; and
7. require baseline doctor exit `0` again.

The pointer-negative ID covers one-at-a-time mutations of `schema`, `version`, `source`, `commit`,
`runtime`, and `installed_at`; non-string values for every pointer field; and replacement of the
pointer with a symlink to otherwise valid bytes. It asserts `pointer-file-safety`,
`pointer-identity`, or `source-identity` as appropriate.

The byte-negative ID covers:

- comment-only installed Python mutation → `runtime-byte-integrity`;
- whitespace-only installed contract mutation while JSON and freeze checks still pass →
  `runtime-byte-integrity`;
- comment-only checker mutation while the installed freeze check still passes →
  `runtime-byte-integrity`;
- a monitored runtime file replaced by a symlink to byte-identical source →
  `runtime-file-safety`;
- one missing and one extra monitored runtime file, each in a fresh fixture →
  `runtime-file-set`; and
- an injected runtime `__pycache__`/`.pyc` artifact → `runtime-cache-exclusion`.

The positive installed-byte ID seeds source `__pycache__`, `.pyc`, and `.pyo` artifacts in a
temporary source copy, performs a clean install, and asserts those artifacts are absent from the
runtime immediately after install while all intended package/contract/checker bytes match.

The Git-environment ID injects hermetic values for `GIT_DIR`, `GIT_WORK_TREE`, `GIT_COMMON_DIR`,
`GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_CONFIG_GLOBAL`,
`GIT_CONFIG_SYSTEM`, `GIT_CONFIG_COUNT`, `GIT_TRACE`, and `GIT_TRACE_SETUP`; it requires exact
source/top-level/`HEAD^{commit}` identity through both install-time writer and doctor-time
validator calls, and proves no injected config/trace target was written.
The nested-nonrepository ID creates only a temporary parent Git repository and nested source copy,
requires `commit: unknown`, and proves the parent's HEAD is never attributed to the source. The
repository-backed-failure ID has two hermetic subtests: a temporary source with its own Git
metadata but no resolvable `HEAD^{commit}` must fail during pointer writing; then a clean committed
source is installed, its exact-source Git HEAD is made unresolvable with one controlled mutation,
doctor must emit `source-identity`, and restoration must return doctor to green. Neither path may
degrade to `unknown`.

---

## 6. Exact implementation changed-path allowlist

The future G0-V-R implementation PR's changed path set must equal exactly:

```text
Makefile
install.sh
tests/test_authority_honesty.py
```

All three paths are required. `tests/test_authority_honesty.py` is new; the other two exist.
File modes must remain unchanged.

Every other path is forbidden. Explicitly forbidden:

```text
.github/**
status.yml
RESUME.md
AGENTS.md
ARCHITECTURE.md
CONSTITUTION.md
README.md
ROLLBACK.md
SECURITY.md
contracts/**
checks/intent-contract-freeze.sh
tests/run-tests.sh
bootstrap.sh
bin/intent
intent_router/**
pyproject.toml
docs/plans/**
docs/adr/**
meta.yml
```

Also forbidden are host files, AWA files, release/shelf/registry/enrollment/synchronization files,
runtime state, generated recipes, and generated locks. A needed fourth path is a stop condition,
not implied scope.

---

## 7. Work items

### One-time full-green implementation entry

Run this entry gate once, immediately before T1 changes the tree:

- fetched live `origin/main` contains accepted design v3 at the exact recorded digest;
- G0-R0 merge `e30644c...` remains an ancestor of live `origin/main`;
- the G0-V-R plan status and its README index row both say `ACCEPTED` in live `origin/main`;
- the commits introducing that accepted plan and accepted index row are ancestors of live
  `origin/main`, and the plan SHA-256 is computed from
  `git show origin/main:docs/plans/g0-v-r-local-gate-prerequisite-v1.md`, not working-tree bytes;
- the implementation branch starts from that live accepted-plan main;
- exact G0-V-R plan acceptance plus separate implementation authority exist;
- the working path set is clean; and
- `python3 -m unittest` focused baselines, `make verify`, `make status-verify`,
  `make verify-install`, `git diff --check`, and the absolute-root doc-warden check all pass.

This is the sole pre-T1 full-green baseline. Record its source HEAD, test count/skips, command
results, accepted-plan commit/index commit, and accepted-plan tree digest.

### Controlled expected-red window

T1 intentionally adds tests before T2/T3 implement their behavior. During this bounded window:

- only the exact named expected-red IDs in T1 may fail, and each must fail for its recorded reason;
- every pre-existing test module from the implementation base must remain green, run from the
  immutable base module list obtained with
  `git ls-tree -r --name-only <base> -- 'tests/test_*.py'`;
- freeze, strict status, static install check, normal-mount `verify-install`, zero-link,
  no-execution, `git diff --check`, and doc-warden remain green;
- canonical `make verify` is expected to be red solely because unittest discovery includes the
  named new red tests; that expected result is recorded, not treated as a stop; and
- T2/T3 may proceed only while there is no additional red test or gate.

After T2, exactly the T3-owned IDs listed below may remain red. After T3, the expected-red window
closes: every focused test and the full canonical gate must be green. T4, pre-commit delivery, and
every post-commit head rerun are unconditionally full-green.

Tasks run in order **T1 → T2 → T3 → T4 → T5**. They land atomically in one ordinary PR.

### Task G0-V-R-T1 — Add biting regressions

**Files:**
- `tests/test_authority_honesty.py`

**Interfaces:**
- Consumes: current `Makefile`, `install.sh`, repository HEAD/version, and throwaway HOME/XDG roots
- Produces: the three noexec-source tests and ten exact hermetic pointer/integrity tests listed in
  §5.3; consumed by T2/T3 and later final G0-R

**Inspect:**

- [ ] Re-run `make -n verify` and `make -n verify-install`; record the direct calls and missing
  lifecycle edge.
- [ ] Re-run the 0644 direct-versus-Bash probe.
- [ ] Re-run one hermetic install and confirm the six pointer fields.
- [ ] Reconfirm that controlled schema and package-byte tampering currently leaves doctor at exit
  `0`.

**Act:**

- [ ] Add the exact §5.3 test classes/methods and hermetic helpers.
- [ ] For the nonexecutable-source test, copy the current source without `.git`, caches, or
  temporary artifacts; clear execute bits on all copied `*.sh`, `bootstrap.sh`, and `bin/intent`.
- [ ] Positively prove direct copied `install.sh` execution is denied before invoking
  `make verify-install` in that copy.
- [ ] For failure cleanup, point `TMPDIR` at a controlled empty directory, make only the temporary
  source copy's installer exit nonzero on the second source invocation after the first install has
  exercised installer `mktemp`, require `make verify-install` to fail, and assert the controlled
  directory contains no leaked outer, inner, or installer-created child.
- [ ] Independently inspect pointer values and hash every declared package/contract/checker source
  and runtime pair.
- [ ] Add broad `GIT_*` injection and nested-nonrepository source fixtures exactly as §5.3.
- [ ] Add fresh-fixture tamper helpers that enforce baseline-green → one mutation → expected
  category → reset → baseline-green, including semantic-neutral contract/checker mutations,
  pointer/file symlinks, non-string pointer values, missing/extra files, and cache artifacts.
- [ ] Add privacy-safe real-root before/after metadata snapshots and unconditional fixture cleanup.

**Observe:**

- [ ] These tests must be red before T2:
  - `TestNoexecCompatibleGate.test_makefile_target_graph_is_interpreter_invoked_and_complete`
    — direct installer recipes/full-lifecycle or POSIX cleanup contract is absent;
  - `TestNoexecCompatibleGate.test_verify_install_passes_with_nonexecutable_source_scripts`
    — a direct source-script execution is denied;
  - `TestNoexecCompatibleGate.test_verify_install_cleans_throwaway_root_on_failure`
    — the ordinary induced failure leaks the outer/inner temp tree.
- [ ] These tests must be red before T3 because the current installer/doctor/Git identity lacks
  the required behavior:
  - `TestHermeticReleasePointer.test_installed_package_contract_and_checker_bytes_match_source`
    — seeded source Python caches are copied into runtime;
  - `TestHermeticReleasePointer.test_wrong_schema_commit_source_or_runtime_is_rejected`
    — at least one controlled pointer invalidity is falsely accepted or miscategorized;
  - `TestHermeticReleasePointer.test_mismatched_installed_bytes_are_rejected`
    — at least one isolated byte/file-set/symlink/cache mutation is falsely accepted or
    miscategorized;
  - `TestHermeticReleasePointer.test_git_source_identity_ignores_all_inherited_git_environment`
    — injected `GIT_*` state reaches Git or changes/writes identity evidence;
  - `TestHermeticReleasePointer.test_nested_nonrepository_source_does_not_inherit_parent_git_identity`
    — the nested source incorrectly inherits its parent repository's HEAD.
  - `TestHermeticReleasePointer.test_repository_backed_git_failure_is_rejected`
    — a Git-present repository-backed source with unresolved `HEAD^{commit}` degrades to
    `unknown` instead of failing closed.
- [ ] The other four pointer tests pass against current untampered behavior.
- [ ] Every pre-existing base test module and non-unittest gate in the controlled expected-red
  protocol remains green. Any additional failure stops implementation.

**Verify:**

```bash
python3 -m unittest -v tests.test_authority_honesty
```

Expected at T1: exactly the nine named IDs above fail for their intended reasons. Run each ID
individually to bind its expected diagnostic, then run the immutable base test-module list and all
non-unittest gates from the controlled expected-red protocol. The aggregate module/full
`make verify` may be red only because those same nine IDs are discovered. No fixture or process
remains.

**Task-local acceptance:**

- Every required ID resolves.
- Each red test reports the intended direct-exec or false-accept defect.
- Positive tests assert values/bytes, not only presence.
- Test helpers mutate only temporary roots.
- No executor is required to make `make verify` green until T2/T3 close the explicitly bounded
  expected-red set.

**Rollback:** Remove the new test file before T2/T3 depend on it. Once T2/T3 land in the same PR,
revert tests and implementation together only before downstream G0-V dependencies exist.

**Dependencies:** The one-time full-green implementation entry.

---

### Task G0-V-R-T2 — Make the canonical gate interpreter-invoked

**Files:**
- `Makefile`

**Interfaces:**
- Consumes: T1 noexec regressions and existing `verify`, `verify-install`, and lifecycle targets
- Produces: interpreter-invoked target graph plus full canonical lifecycle; consumed by G0-V-H as
  exact command `["make", "verify"]`

**Inspect:**

- [ ] Confirm every current `./install.sh` recipe occurrence and the existing serial verify order.
- [ ] Confirm no other repository script is directly executed transitively by canonical verify.

**Act:**

- [ ] Apply §5.1 exactly.
- [ ] Preserve current target names and current test/freeze/status/static-check commands.
- [ ] Add `verify-install` after static check and before the success line.
- [ ] Implement the POSIX `/bin/sh` exit/signal/status-preserving, idempotent cleanup contract.
- [ ] Create the inner temp directory and pass it as `TMPDIR` to every lifecycle subprocess.
- [ ] Add installed-copy doctor/uninstall checks and positive post-uninstall absence assertions.
- [ ] Update only Makefile help text necessary to describe the strengthened gate.

**Observe:**

- [ ] `make -n verify` shows the exact §4 order.
- [ ] Every Makefile command containing `install.sh` also contains an explicit preceding `bash`.
- [ ] All three T1 `TestNoexecCompatibleGate` IDs turn green.
- [ ] Static assertions prove exit status preservation and non-returning HUP/INT/TERM handlers;
  no test sends a real signal.
- [ ] The six T3-owned IDs remain red for their exact expected reasons; do not weaken them.
- [ ] Every other new/base test and non-unittest gate remains green under the controlled
  expected-red protocol.

**Verify:**

```bash
python3 -m unittest -v \
  tests.test_authority_honesty.TestNoexecCompatibleGate
make verify-install
```

**Task-local acceptance:**

- Source scripts at mode 0644 pass the lifecycle while direct execution is demonstrably denied.
- `make verify-install` removes all throwaway paths on success.
- The dedicated induced-failure regression proves the cleanup trap empties its controlled
  `TMPDIR`.
- The target-graph regression proves the POSIX trap/status/signal contract statically.
- No tracked executable mode changes.

**Rollback:** Revert the Makefile as one body before G0-V-H consumes its receipt. After G0-V-H
qualification, forward-fix or reverse the dependent G0-V authorities in governed reverse order.

**Dependencies:** T1.

---

### Task G0-V-R-T3 — Enforce hermetic release integrity

**Files:**
- `install.sh`

**Interfaces:**
- Consumes: the existing six-field pointer writer, current source/runtime layout, and T1 tamper
  regressions
- Produces: read-only doctor validation of pointer identity and package/contract/checker byte
  parity; consumed by `make verify-install`, T4, G0-V-H, and later G0-R

**Inspect:**

- [ ] Confirm the pointer writer still derives version from `intent_router.__version__`, commit
  from source HEAD, and timestamp preservation from identical identity.
- [ ] Confirm current doctor is parse-only for the pointer and independently runs installed
  contract freeze.

**Act:**

- [ ] Add the exact §5.2 validator and call it from `do_doctor`.
- [ ] Make both writer and validator remove every inherited `GIT_*` child-environment entry,
  verify canonical source/top-level equality, and resolve `HEAD^{commit}`.
- [ ] Fail closed on Git-present failures after a source is proven repository-backed; retain
  `unknown` only for Git absent or an exact source that is not itself a repository root.
- [ ] Exclude `__pycache__`, `*.pyc`, and `*.pyo` during install and detect them during doctor.
- [ ] Emit the exact integrity categories from §5.2 while continuing older semantic doctor checks.
- [ ] Keep install, repair, check, and uninstall semantics unchanged.
- [ ] Keep the pointer's exact schema and six fields unchanged.
- [ ] Preserve source-invoked and installed-copy doctor support.
- [ ] Keep validation read-only and diagnostics content-free.

**Observe:**

- [ ] Untampered source-invoked and installed-copy doctor both pass.
- [ ] Every pointer-field tamper subtest now fails doctor.
- [ ] Every installed-byte tamper subtest now fails doctor.
- [ ] Every tamper subtest starts and ends baseline-green, performs exactly one mutation, and
  observes its exact integrity category.
- [ ] Semantic-neutral contract/checker mutations leave existing parse/freeze checks green.
- [ ] All injected `GIT_*` variables are inert; trace/config targets remain unwritten.
- [ ] A nested nonrepository source records `unknown`, never the parent repository's HEAD.
- [ ] A repository-backed source with unresolved `HEAD^{commit}` fails closed.
- [ ] Seeded source Python caches are absent immediately after install.
- [ ] Reinstalling identical source preserves `installed_at`.
- [ ] Static `--check` remains no-write.

**Verify:**

```bash
python3 -m unittest -v \
  tests.test_authority_honesty.TestHermeticReleasePointer
bash ./install.sh --check
make verify-install
```

**Task-local acceptance:**

- All ten exact `TestHermeticReleasePointer` IDs pass.
- Controlled negatives bite independently.
- All package Python, contract JSON, and checker bytes are compared.
- Package version remains `0.1.0`.
- No real HOME/XDG root changes.
- The controlled expected-red window is closed: `tests.test_authority_honesty`, every immutable
  base module, every focused gate, `make verify`, status, diff check, and doc-warden are all green.

**Rollback:** Revert installer and tests together before G0-V-H. After a downstream qualification
pins this behavior, forward-fix unless every dependent authority performs its own approved reverse
rollback.

**Dependencies:** T1–T2.

---

### Task G0-V-R-T4 — Run the complete local gate

**Files:**
- No new files; only the exact §6 set may remain changed

**Interfaces:**
- Consumes: T1–T3 implementation
- Produces: local exact-head-ready evidence and bounded diff for the ordinary PR

**Inspect:**

- [ ] Re-read the final Makefile graph and installer validator.
- [ ] Confirm no accepted design/plan, contract, runtime package, or protected path changed.
- [ ] Confirm no temp root, child process, or staged file remains.

**Act:**

- [ ] Run every focused and full command in §8 unconditionally green.
- [ ] Compare the changed path set to §6 by exact set equality.
- [ ] Re-run the accepted-design digest check.
- [ ] Prove no existing tracked path changes Git mode in the candidate base-to-working-tree diff.

**Observe:**

- [ ] All focused regressions pass.
- [ ] `make verify` now includes and passes `verify-install`.
- [ ] Strict status and zero-link remain green without ledger mutation.
- [ ] Documentation governance remains conformant.
- [ ] No expected-red exception remains.

**Verify:**

```bash
python3 -m unittest -v tests.test_authority_honesty
python3 -m unittest -v tests.test_zero_link tests.test_no_execution
make verify-install
make verify
make status-verify
git diff --check
/Users/laurence.duggan/dev/_ops/bin/doc-warden.sh check \
  "$(git rev-parse --show-toplevel)"
actual=$({ git diff --name-only; git diff --cached --name-only; \
  git ls-files --others --exclude-standard; } | sort -u)
expected=$(printf '%s\n' Makefile install.sh tests/test_authority_honesty.py)
test "$actual" = "$expected"
mode_changes=$(git diff --summary -- | awk '/^ mode change / {print}')
test -z "$mode_changes"
```

**Task-local acceptance:**

- Every command exits `0`.
- Changed paths equal all three and only the §6 paths.
- Full green evidence exists before commit.
- No generated/temp artifacts are tracked or left on disk.

**Rollback:** Before commit, restore only this task's allowlisted changes without destructive
history rewriting. After commit, use a normal corrective commit; never reset shared history.

**Dependencies:** T1–T3.

---

### Task G0-V-R-T5 — Deliver one ordinary router PR

**Files:**
- Exactly the three §6 paths

**Interfaces:**
- Consumes: accepted G0-V-R plan, explicit implementation authority, T1–T4 evidence, live
  `origin/main`, and current runnerless branch rules
- Produces: exact merged G0-V-R receipt for G0-V-H and final G0-R

**Inspect:**

- [ ] Fetch live `origin/main`; confirm no new conflicting gate change.
- [ ] Require the accepted plan file and its README `ACCEPTED` index entry to exist in
  `origin/main`; resolve each introducing commit and prove both commits are ancestors of live
  `origin/main`.
- [ ] Compute and record the accepted-plan digest from
  `git show origin/main:docs/plans/g0-v-r-local-gate-prerequisite-v1.md`; do not use working-tree
  bytes as delivery authority.
- [ ] Confirm the accepted-design digest from the same live main tree.
- [ ] Confirm `.github/**` remains unchanged and current required contexts still name verifier App
  integration `4274739`.
- [ ] Confirm current protected recipe still runs the old tests-only command; do not describe its
  success as full canonical-gate qualification.

**Act:**

- [ ] Commit with normal hooks; never use `--no-verify`.
- [ ] With the worktree clean at the new commit, rerun every T4 focused/full local command and
  record `local_evidence.head_sha = git rev-parse HEAD`.
- [ ] Require the hermetic pointer proof's `release_pointer.source_head` to equal that same HEAD.
- [ ] Push the implementation branch and open one ordinary **Draft** PR against `main`.
- [ ] Run the repository-required Bugbot review cadence until there are no actionable findings.
- [ ] Apply fixes as ordinary commits and invalidate/re-run prior exact-head evidence after every
  head change.
- [ ] After every head change, rerun the complete T4 evidence while clean and replace, never append
  to, the candidate `local_evidence` record.
- [ ] Keep the PR Draft until local proof, review, path equality, and exact-head checks are clean.
- [ ] Move through the ordinary ready path only after those conditions hold; reviewer App alone
  owns approval and native auto-merge arming.

**Observe:**

- [ ] PR base/head and GitHub compare path set are exact.
- [ ] `local_evidence.head_sha`, `release_pointer.source_head`, and final PR `headRefOid` are
  identical.
- [ ] Base/head raw mode comparison proves no existing tracked path changed mode; record
  `tracked_mode_changes: []`.
- [ ] Both required check contexts report `success` on the same final head SHA.
- [ ] The job context's current tests-only command is reported honestly; G0-V-H still owns exact
  `make verify` image qualification.
- [ ] After governed merge, the merge commit is an ancestor of fetched `origin/main`.

**Verify:**

```bash
git fetch --no-tags origin main
plan_commit=$(git log -1 --format=%H -S'**Status:** ACCEPTED' origin/main -- \
  docs/plans/g0-v-r-local-gate-prerequisite-v1.md)
index_commit=$(git log -1 --format=%H \
  -S'| [G0-V-R Local Gate Prerequisite v1](g0-v-r-local-gate-prerequisite-v1.md) | ACCEPTED |' \
  origin/main -- docs/plans/README.md)
test -n "$plan_commit"
test -n "$index_commit"
git merge-base --is-ancestor "$plan_commit" origin/main
git merge-base --is-ancestor "$index_commit" origin/main
git show origin/main:docs/plans/g0-v-r-local-gate-prerequisite-v1.md \
  | rg -F '**Status:** ACCEPTED'
git show origin/main:docs/plans/README.md \
  | rg -F '| [G0-V-R Local Gate Prerequisite v1](g0-v-r-local-gate-prerequisite-v1.md) | ACCEPTED |'
git show origin/main:docs/plans/g0-v-r-local-gate-prerequisite-v1.md | shasum -a 256
gh pr view <number> --repo KleinPerkins/intent-router \
  --json url,state,isDraft,baseRefName,baseRefOid,headRefOid,mergeCommit
gh api repos/KleinPerkins/intent-router/commits/<head>/check-runs
gh api repos/KleinPerkins/intent-router/compare/<base>...<head>
git diff --raw <base> <head> --
mode_changes=$(git diff --raw <base> <head> -- | \
  awk '$1 !~ /^:000000/ && substr($1,2) != $2 {print $NF}')
test -z "$mode_changes"
git merge-base --is-ancestor <merge> origin/main
```

**Task-local acceptance:**

- One merged ordinary PR receipt exists with all §9 fields.
- Accepted plan/index ancestry and the plan digest from live `origin/main` are recorded.
- Final local evidence and pointer source HEAD bind the exact PR head.
- Existing tracked path modes are unchanged.
- No protected path, host authority, or later G0-V delivery changed.
- No manual approval/arming, bypass, admin merge, force push, or paid runner was used.
- G0-V-H has a precise merged source input; it has not started implicitly.

**Rollback:** Apply §10. G0-V-R never rolls back another authority.

**Dependencies:** T1–T4; accepted plan; explicit implementation and governed-delivery authority.

---

## 8. Verification matrix

| Requirement | Local/focused evidence | Remote/later boundary |
|---|---|---|
| Existing test gate | `bash tests/run-tests.sh`; full unittest discovery | Current job context reruns this on exact PR head |
| Freeze/CR4 | `bash checks/intent-contract-freeze.sh`; `make verify` | No contract path changes |
| Strict ledger | `make status-verify`; also inside `make verify` | No `status.yml`/`RESUME.md` mutation |
| Noexec command form | Make dry-run test rejects direct repo-script execution | G0-V-H exact-image qualification remains required |
| Execute-bit independence | 0644 source-copy test: direct denied, `make verify-install` passes | Does not claim exact mount semantics |
| Cleanup on success/failure | Ordinary induced-failure temp-root test plus success assertions | No real-signal test |
| Exit/signal semantics | Static Make-recipe assertions: status-preserving trap 0; HUP/INT/TERM clean then exit nonzero | Exact image may exercise ordinary process termination later |
| Pointer schema/version | `...test_schema_and_version_are_exact` | Schema remains `intent-release-pointer/v1`; version `0.1.0` |
| Source commit | `...test_source_commit_matches_source_head` | Final PR head/merge and digests bind committed delivery |
| Git environment isolation | `...test_git_source_identity_ignores_all_inherited_git_environment` | Every inherited `GIT_*` removed; no injected trace/config writes |
| Exact repository root | `--show-toplevel` equals canonical source; `HEAD^{commit}` resolves; `...test_repository_backed_git_failure_is_rejected` | Repository-backed Git failures fail closed |
| Non-Git nested source | `...test_nested_nonrepository_source_does_not_inherit_parent_git_identity` | `unknown` is allowed only for genuine nonrepository source/Git absence |
| Source/runtime/hermetic paths | `...test_source_and_runtime_are_exact_and_hermetic` | G0-V-H consumes merged source, not a local temp path |
| Package/contract/checker bytes | `...test_installed_package_contract_and_checker_bytes_match_source` | Merge-tree file digests recorded |
| Python cache exclusion | Seeded source cache artifacts absent immediately after install and rejected in runtime | No broader artifact hashing |
| Pointer tamper negatives | Fresh baseline/one mutation/category/reset protocol in `...test_wrong_schema_commit_source_or_runtime_is_rejected` | Includes non-string fields and pointer symlink |
| Byte/file-set tamper negatives | Fresh baseline/one mutation/category/reset protocol in `...test_mismatched_installed_bytes_are_rejected` | Includes semantic-neutral bytes, file symlink, missing/extra/set mismatch |
| Independent bite | Existing contract/freeze semantic checks remain green where applicable; exact new category fails | Prevents unrelated-failure false greens |
| Real-root isolation | `...test_real_home_and_xdg_roots_are_untouched` | No installed operator runtime mutation |
| Install lifecycle | `make verify-install`, then canonical `make verify` | No release/install external mutation |
| Router execution boundary | `python3 -m unittest tests.test_no_execution` | CR1/CR2 unchanged |
| Zero-link | `python3 -m unittest tests.test_zero_link` | No downstream governed repository literal |
| Full canonical local gate | `make verify` | Current G0-V-R remote recipe is tests-only; G0-V-H qualifies full command |
| Diff hygiene | `git diff --check`; exact three-path set | GitHub compare returns same set |
| Tracked mode hygiene | Base/head raw-mode comparison; no existing path mode delta | Receipt records `tracked_mode_changes: []` |
| Documentation governance | absolute-root doc-warden check | No ADR required |
| Plan authority | Accepted plan and accepted index-entry commits are ancestors of live main; digest read from main tree | Unmerged plan bytes never authorize implementation |
| Ref-bound local evidence | Full local matrix rerun clean after every commit | Evidence HEAD and pointer source HEAD equal final PR head |
| Exact-head required contexts | Local names verified from live branch rules | Both contexts `success` on final head, integration `4274739` |

Remote success on the G0-V-R PR proves the current required contexts accepted that exact head. It
does not by itself prove the not-yet-delivered `make verify` recipe/lock; that claim is reserved for
G0-V-H/P/L and the later final-G0-R canary.

---

## 9. Exact merged G0-V-R receipt

Capture all fields below after governed merge. G0-V-H and final G0-R must reject an incomplete or
stale receipt.

```text
receipt_kind: G0-V-R
repository: KleinPerkins/intent-router
accepted_design_path
accepted_design_sha256
accepted_plan_path
accepted_plan_sha256_from_origin_main
accepted_plan_commit
accepted_index_commit
accepted_plan_and_index_are_ancestors_of_live_origin_main
pr_url
pr_number
base_branch: main
base_sha
head_sha
merge_sha
merged_at
merge_is_ancestor_of_live_origin_main
changed_paths
tracked_mode_changes: []
required_checks:
  - name
    integration_id
    head_sha
    conclusion
local_evidence:
  head_sha
  focused_test_ids
  make_verify_install
  make_verify
  make_status_verify
  zero_link
  no_execution
  git_diff_check
  doc_warden
noexec_local_proof:
  execute_bit_denial_observed
  interpreter_lifecycle_passed
  ordinary_failure_cleanup_passed
  posix_exit_status_contract_static_passed
  posix_signal_contract_static_passed
  exact_controller_image_qualified: false
release_pointer:
  schema: intent-release-pointer/v1
  package_version: 0.1.0
  source_head
  source_toplevel
  git_environment_injection_tests
  nested_nonrepository_test
  hermetic_identity_tests
  byte_integrity_tests
  tamper_negative_tests
  integrity_failure_categories
  python_cache_exclusion
merged_tree_sha256:
  Makefile
  install.sh
  tests/test_authority_honesty.py
protected_paths_changed: false
host_authority_changed: false
```

`changed_paths` must equal the exact §6 set. Each required check must name the final `head_sha` and
`conclusion: success`. `local_evidence.head_sha` and `release_pointer.source_head` must both equal
that same final `head_sha`; any later commit invalidates and replaces all local evidence.
`tracked_mode_changes` must be exactly `[]`. The local noexec receipt must explicitly remain
`exact_controller_image_qualified: false`; G0-V-H is the authority that later flips its own
qualification fact.

---

## 10. Rollback and forward-fix rules

### Before downstream G0-V dependency

- Before G0-V-H pins the merged G0-V-R receipt, a defect may be corrected by one governed
  router-owned revert PR.
- The revert makes G0-V incomplete again; the host command remains unchanged.
- Do not alter G0-R0 or any unrelated completed evidence.

### After G0-V-H, G0-V-P, or G0-V-L depends on G0-V-R

- Do not unilaterally revert G0-V-R. The dependent authority would retain a stale qualification,
  recipe, or lock.
- Preferred response: forward-fix in one new ordinary router PR, issue a replacement router
  receipt, then have G0-V-H requalify and G0-V-P/L regenerate through their owners as required.
- Any new router head invalidates the prior ref-bound local evidence and pointer source-HEAD claim;
  replacement evidence must be rerun clean on the replacement exact head before any dependent
  authority consumes it.
- A true rollback must proceed in reverse dependency order—G0-V-L, then G0-V-P, then G0-V-H, then
  G0-V-R—with each owner authorizing and recording its own rollback. This plan grants none of those
  later permissions.
- If final G0-R already records the receipt, that authority must be forward-fixed/reopened under its
  own plan; G0-V-R cannot rewrite its ledger.

No rollback uses force push, history rewriting, hand-edited generated bytes, or cross-authority
mutation.

---

## 11. PR and delivery cadence

1. Merge this exact accepted plan and its accepted README index entry to live main without
   modifying the frozen plan bytes.
2. Activate the operator's recorded G0-V-R implementation/delivery authority only after that
   merge.
3. Require the accepted plan and accepted README index entry to be merged ancestors of live main;
   record the accepted-plan digest from that tree.
4. Run the one-time full-green implementation entry.
5. Implement T1 and enter only the exact expected-red window.
6. Implement T2/T3 while all non-expected gates remain green; close the window full-green.
7. Complete T4 unconditionally green and commit with normal hooks.
8. Rerun every local proof clean on that exact commit; repeat after every head change.
9. Open one ordinary Draft implementation PR; no `.github` path.
10. Review to zero actionable findings.
11. Require local evidence, pointer source HEAD, both exact-head contexts, path equality, and empty
    tracked-mode delta on the final head.
12. Use only the reviewer-App-controlled ordinary merge path; never manually arm auto-merge.
13. Capture §9 after merge and stop.
14. Plan/accept/authorize G0-V-H separately. Do not begin G0-V-H, G0-V-P, G0-V-L, or final G0-R
    under this authority.

Permanent constraints: no paid runner, GitHub Actions runner, self-hosted runner, self-approval,
manual auto-merge arming, bypass, admin merge, direct main push, force push, hand-edited recipe, or
hand-edited lock.

---

## 12. Stop conditions and operator gates

### Binding repository/accepted-design stops

Stop if:

- accepted design v3 no longer hashes to the recorded digest;
- G0-R0 is no longer merged/valid;
- CR1/CR2, KI1–KI4, zero-link, or frozen/additive-within-v1 behavior would change;
- any frozen contract or constitutional meaning would change;
- any protected `.github` path, host/AWA authority, shelf/registry/synchronization authority, or
  final-G0-R-owned ledger/resume authority would be mutated from G0-V-R;
- final/pre-delivery canonical `make verify`, `make status-verify`, zero-link, no-execution, or
  doc-warden fails outside the explicitly bounded T1–T3 expected-red protocol;
- either required exact-head check is absent or non-success on the final PR head; or
- normal repository hooks/governed delivery cannot complete without bypass.

These derive from `AGENTS.md`, CR#/KI# authority, accepted design v3, and current runnerless
repository governance.

### Plan-specific stops

Stop and return to the operator if:

- implementation needs any path outside the exact three-path §6 allowlist, whether a fourth path
  or substitution/removal of one required path;
- the accepted plan or accepted README index entry is not an ancestor of live `origin/main`, or
  its tree digest/status cannot be proven;
- any T1/T2 expected-red ID fails for an unlisted reason, any additional test/gate turns red, or
  T3 does not close the window to unconditional full green;
- exact controller qualification appears necessary to make a local source-proof claim;
- the 0644 simulation fails for an image-independent reason not solved within the allowlist;
- cleanup cannot preserve ordinary failure status, keep inner `TMPDIR` artifacts trapped, or
  guarantee non-returning nonzero HUP/INT/TERM handlers without real-signal tests;
- strict doctor validation would break source-invoked or installed-copy doctor semantics;
- non-git `commit: unknown` compatibility cannot be retained without weakening repository-backed
  commit checks;
- any inherited `GIT_*` entry reaches a writer/validator Git child, canonical source/top-level
  equality cannot be proved, or a repository-backed HEAD failure would degrade to `unknown`;
- byte parity requires persisting new hashes, adding a contract, or broadening beyond the package,
  contracts, and freeze checker;
- a tamper test can pass without baseline doctor green, exactly one mutation, the expected
  integrity category, and post-reset baseline green;
- cache exclusion, symlink rejection, or monitored-set equality would require a new exact
  permission mode;
- real HOME/XDG isolation cannot be positively demonstrated without reading/logging private state;
- current protected config must change to make the ordinary G0-V-R PR pass;
- final `local_evidence.head_sha` or `release_pointer.source_head` differs from the final PR head,
  or any existing tracked path changes Git mode;
- a reviewer asks G0-V-R to absorb G0-V-H/P/L or final G0-R; or
- any far-reaching architecture/compatibility choice not settled by accepted design v3 appears.

These are conservative constraints of this execution plan, not new repository-wide policy.

### Operator gates

1. **Recorded acceptance gate:** on 2026-09-03 the operator selected
   **"Accept the plan and deliver G0-V-R,"** accepting these exact bytes and separately authorizing
   G0-V-R implementation/delivery.
2. **Publication gate:** that implementation/delivery authority is inactive until this exact
   accepted plan and its accepted README index entry are merged ancestors of live `origin/main`.
3. **Implementation gate:** once publication is proven, no second implementation-authorization
   prompt is required; every preflight, stop, scope, and receipt condition in this plan remains
   binding.
4. **Delivery gate:** implementation uses the ordinary reviewer-App-controlled PR path; no agent
   grants itself approval or merge authority.
5. **Handoff gate:** after the merged §9 receipt, stop. G0-V-H requires its own accepted plan and
   authority.

---

## 13. ADR determination

No ADR is required. Accepted design v3 already settles the binding noexec prerequisite,
verification-authority split, delivery order, and trust boundary. This accepted plan specifies the
execution mechanism inside that decision. Neither repository ADR conventions nor
`/Users/laurence.duggan/dev/_ops/doc-warden/POLICY.md` requires duplicating an already accepted
design decision as a new ADR.

If implementation uncovers a genuinely new durable architecture decision, stop rather than
smuggling it into this plan or creating an ADR without operator review.

---

## 14. Implementation-agent recommendation

Use the **deep** tier at **deep effort**, with concrete model `gpt-5.6-sol-max`, as one sole local
writer. Do not parallelize implementation writers in one worktree.

The changed code is small, but it alters the canonical shipping gate and provenance validator.
The implementation must preserve a precise local-versus-exact-image trust boundary, create
independently biting tamper tests, avoid recursive verification, keep hermetic roots private, and
produce a receipt consumed by three later authority-owned deliveries.

---

## 15. Recorded plan acceptance

The operator accepted this exact plan on 2026-09-03 and separately authorized G0-V-R
implementation/delivery after the publication gate in §12. Acceptance does not authorize
implementation from unmerged bytes, bypass any plan condition, or authorize G0-V-H/P/L, final
G0-R, host/protected-path work, or unrelated external mutation.

The accepted basis preserves:

- [x] the one-time full-green entry and bounded nine-ID → six-ID → zero-ID red/green sequence
  cannot deadlock T1–T3;
- [x] the POSIX cleanup contract preserves ordinary exit status, traps inner temp artifacts, and
  specifies non-returning nonzero HUP/INT/TERM behavior without real-signal tests;
- [x] writer and validator remove all inherited `GIT_*`, bind canonical top-level plus
  `HEAD^{commit}`, distinguish genuine nonrepository fallback, and fail closed for
  repository-backed Git failures;
- [x] every tamper bite uses clean baseline → one mutation → exact category → reset → clean
  baseline, including semantic-neutral bytes, non-string fields, symlinks, missing/extra set
  mismatch, and Python-cache exclusion;
- [x] accepted-plan/index ancestry and tree digest, final evidence/pointer/PR-head equality, and
  `tracked_mode_changes: []` are mandatory receipt evidence;
- [x] the implementation changed-path set remains exactly `Makefile`, `install.sh`, and
  `tests/test_authority_honesty.py`;
- [x] local 0644 execute-bit independence remains explicitly weaker than later G0-V-H exact
  `tmpfs,noexec,nosuid,nodev` controller qualification; and
- [x] all constitutional, protected-path, ownership, rollback, and handoff boundaries remain
  unchanged.
