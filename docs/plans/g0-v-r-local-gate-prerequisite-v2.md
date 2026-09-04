# G0-V-R local-gate prerequisite continuation plan v2

**Status:** ACCEPTED — 2026-09-04
**Plan-type:** agentic-execution
**Supersedes:** `docs/plans/g0-v-r-local-gate-prerequisite-v1.md` only upon acceptance
**Predecessor SHA-256:** `feb9b03380e4f40f44aeff8f53a02eb5054f59d6d578eb9866a5812689aecf8f`
**Governing design candidate:** `docs/plans/roadmap-revision-step-3-design-v4.md`, accepted only
in the same future docs-only delivery as this plan
**Purpose:** Continue the already-built G0-V-R implementation on existing Draft PR #58 after a
diagnostic-first, owner-serialized sandbox qualification. Preserve v1's exact implementation
contract; do not replay its historical red/green build.

## 1. Authority and incorporation

Accepted v1 remains active and byte-identical while this file is Draft. If v2 is accepted, it
replaces v1's continuation/delivery authority but incorporates these accepted v1 sections without
change:

- §3 objective and non-goals;
- §4 exact meaning of noexec-compatible;
- §5 exact `Makefile`, `install.sh`, and hermetic-test implementation design; and
- §6 exact three-path implementation allowlist.

If the plans appear to conflict, v1 controls those implementation semantics and v2 controls only
the post-build qualification, continuation, evidence, and delivery sequence. V1's completed
expected-red tasks are history, not work to repeat. Its custom receipt template and old delivery
sequence do not carry forward.

This plan remains subject to CR1/CR2 (router proposes, never executes or authorizes), CR4
(additive-within-v1), CR5 (untrusted content is data), KI1 (consumer safety remains router-off), and
zero-link. It changes no router contract, additive manifest, proposal behavior, consumer kernel,
required Check, rule, recipe, or product phase.

## 2. Current observation

The following facts were observed on 2026-09-04 and must be refreshed before use:

- [PR #58](https://github.com/KleinPerkins/intent-router/pull/58) is open, Draft, unarmed, and
  mergeable on branch `feat/g0-v-r-local-gate-prerequisite`.
- Its observed base is
  `3c4d231d1e942b1ed1b13bfb69f6c61e7ac2dc3b`; that base is historical provenance, not a pin.
- Its observed head is `aa0cc15c4d4b9b73288cd7c6a9af73dcb816f8b1`.
- Its compare changes exactly:

  ```text
  Makefile
  install.sh
  tests/test_authority_honesty.py
  ```

- The PR records local green in roughly 151 seconds, including v1's full local gate and the three
  Bugbot-driven regression fixes already present on that head:
  `test_runtime_reinstall_preserves_validated_source_provenance`,
  `test_release_pointer_helper_respects_python_39_floor`, and
  `test_normal_installed_cli_does_not_create_runtime_bytecode`.
- Required CheckRun `100931502200`,
  `pr-automation / job:repo.intent-router.m3-verify`, belongs to verifier App `4274739`, binds the
  observed head, and concluded `action_required`.
- Controller history records two attempts that each reached the selected 300-second sandbox
  ceiling without a normal exit or captured streams.
- The exact command remains `["run-literal", "bash", "tests/run-tests.sh"]`.
- Current assignment/lock authority selects `stdlib-shell.v1`; the generated lock materializes
  300 seconds and changes no recipe meaning.

These are observations, not merged evidence. They prove a remote blocker but not that timeout is
its root cause. Current controller policy rejects/skips Draft PRs during discovery and dispatch,
so the historical CheckRun does not make future pre-Ready Check evidence possible.

## 3. Objective and non-goals

### Objective

1. Diagnose the unchanged command on an exact PR #58 head in the exact controller sandbox.
2. Select one explicit route:
   - **Route A — no capacity:** repeatable healthy completion within `stdlib-shell.v1`; skip every
     Dev assignment, lock, activation, and capacity task.
   - **Route B — capacity:** repeatable normal completion beyond 300 seconds; explicitly accept
     and qualify only the existing cataloged `awa-authoritative-verify.v1`.
3. On Route B only, change intent-router's profile reference through a separately proven Dev
   reprofile path, generate one lock-only target change, activate it through the requiredness
   lifecycle, and prove forward qualification or exact rollback.
4. Continue the existing PR #58 without rewriting history or rebuilding the implementation.
5. While it remains Draft, re-prove its exact compare, local gates, and Bugbot result.
6. After explicit Ready authorization, treat both required exact-head Checks as the production
   canary and merge gate.
7. Record completion using ordinary Git, PR, CheckRun, and existing operation evidence.

### Non-goals

- No new product phase, router contract, receipt schema, canonical-JSON profile, event journal,
  evidence store, lease, distributed CAS, dependency manifest, or fleet transaction system.
- No post-merge Dev receipt-only PR and no `g0-v-r-receipt/v2` namespace.
- No separate target-lock plan unless future binding target policy newly requires one. Current
  policy marks `.github` protected and requires owner handling; it does not require another plan.
- No proposal discriminator, typed-feedback envelope, raw-event rule, sort key, stream union,
  provider/privacy lifecycle, calibration, legacy migration, or other S0/R2/future-roadmap work.
- No PR #58 command, recipe, dependency, required-Check, ruleset, coverage-mode, router
  package-version/release, shelf, registry, enrollment, or synchronization change.
- No execution-catalog, profile, or resource mutation. Any new profile would change the semantic
  catalog digest and require separate controller architecture, fleet-wide relock planning, and
  successor authority.
- No paid, GitHub-hosted, or self-hosted Actions runner.
- No mutation of another repository or the protected host under this plan's authority.

## 4. Required authority sequence

1. Review v4 and v2 together.
2. On explicit acceptance, deliver both plus the index in one docs-only PR. That same merge marks
   v3/v1 `SUPERSEDED` and v4/v2 `ACCEPTED`; it changes no accepted predecessor bytes.
3. Keep PR #58 Draft/unarmed and untouched through that acceptance delivery.
4. After acceptance, separately author, review, accept, and merge a controller-owner plan for
   exact-sandbox diagnosis and any conditional controller-owned defect or instrumentation work.
5. Diagnose first:
   - Route A proceeds directly to explicit PR #58 Resume, Draft audit, and pre-Ready proof.
   - Route B requires explicit acceptance of the complete existing broad-profile delta, then a
     separately accepted Dev-owner plan for the reprofile path, generated-lock publication,
     requiredness activation, exact-sandbox qualification, and rollback.
6. On Route B, use distinct fresh operation IDs/owner GOs for every mutation and a distinct
   recovery operation ID; never share one operation ID across the flow.
7. If Route B qualification fails, restore and prove the complete prior preimage before stopping.
8. On either successful route, obtain explicit Resume authority, then audit/refresh and locally
   re-prove PR #58 while it remains Draft.
9. Present the exact route/head/base/compare evidence and obtain a separate explicit Ready
   decision.
10. After Ready, require both exact-head production Checks. Let the reviewer App own approval and
    auto-merge; if either Check is absent, stale, wrong-App, non-success, or diverges from route
    evidence, return to Draft before remediation/retry.
11. Stop after merge evidence is recorded. G0-V-H remains separately planned and unauthorized.

This sequence is plan-specific. Binding authority remains in this repository's accepted
design/rules and each external owner's accepted policy and plan.

## Work items

### Task G0-V-R-v2-T0 — Accept the successors atomically

**Files:**
- `docs/plans/roadmap-revision-step-3-design-v4.md`
- `docs/plans/g0-v-r-local-gate-prerequisite-v2.md`
- `docs/plans/README.md`

**Interfaces:**
- Consumes: independently reviewed Draft bytes, deterministic prospective accepted bytes, and one
  explicit operator acceptance decision naming both prospective accepted successor digests
- Produces: one docs-only acceptance commit with atomic v3/v1 → v4/v2 index transitions
- Must not mutate: accepted v3/v1 bytes, PR #58, product files, `.github/**`, external
  repositories, GitHub operational state, or the host

- [ ] Keep v3/v1 rows `ACCEPTED` and v4/v2 rows `DRAFT` until the acceptance decision.
- [ ] Stage exactly the three files above so `git ls-files` includes both successors. Assert the
  cached changed-path allowlist, run `git diff --cached --check`, and run doc-warden. Require its
  output to name and classify both successor files; an untracked-only green run is insufficient.
- [ ] While the files still say Draft, deterministically construct the prospective accepted bytes
  in memory or another non-repository review surface. The only transformations are:
  - both successor Status lines: replace only `DRAFT` with `ACCEPTED`;
  - v3 index: status `SUPERSEDED`, note
    `Immutable prior design; superseded by accepted v4`;
  - v4 index: status `ACCEPTED`, note
    `Active design basis; diagnostic-first G0-V-Q with Route A or catalog-stable Route B`;
  - v1 index: status `SUPERSEDED`, note
    `Immutable prior plan; superseded by accepted v2`; and
  - v2 index: status `ACCEPTED`, note
    `Active G0-V-R continuation basis; route-aware sandbox qualification and Ready-triggered production Checks`.
- [ ] Review the exact prospective three-file diff and compute both prospective accepted successor
  SHA-256 digests. Obtain one explicit operator decision naming those two digests.
- [ ] After authorization, apply exactly the reviewed transformation, stage exactly the three
  paths, recompute both successor digests, and require exact matches before commit.
- [ ] Reassert the cached changed-path allowlist; run `git diff --cached --check`,
  `git diff --check`, doc-warden, `make verify`, and `make status-verify`. Require doc-warden to
  name/check both accepted successors.
- [ ] Merge through the ordinary governed docs path without touching PR #58.

**Task-local acceptance:** Both successors become active in the same merge; both predecessors
remain byte-identical; no interval exists with accepted v2 and active v1.

**Rollback:** Before acceptance, edit or remove only Draft bytes/rows. After acceptance, freeze the
successors and use a new version for correction.

**Dependencies:** Independent review and explicit joint documentation acceptance.

### Task G0-V-R-v2-T1 — Diagnose the exact sandbox

**Files:**
- None in intent-router
- External owner plans define their own exact changed-path allowlists

**Interfaces:**
- Consumes: accepted v4/v2, accepted controller-owner diagnostic plan, unchanged PR #58 command, exact selected
  PR head, current sandbox/profile/config/assignment/lock identities
- Produces: ordinary bounded diagnostic evidence and one decision: Route A, Route B, defect, or
  unresolved
- Must not mutate: production assignment/lock/config, PR #58 bytes/body/state, recipe, Checks,
  rulesets, or any repository without its own accepted owner plan

- [ ] Record the selected PR head/tree and prove the command closure still resolves to
  `["run-literal", "bash", "tests/run-tests.sh"]`.
- [ ] Use the controller's real execution path with the exact image, tool inventory, network,
  non-root/read-only-root settings, `tmpfs,noexec,nosuid,nodev` mount, CPU, memory, pids, disk,
  inodes, output bound, controller release, live config generation, assignment, profile, recipe,
  and lock.
- [ ] Under the controller owner's diagnostic authority, observe long enough outside live PR
  admission to distinguish normal completion from stall. Do not change the production assignment.
- [ ] For each run record start/end/elapsed, last completed stage/test when available, exit or
  precise failure disposition, bounded stdout/stderr counts/truncation/digests, limit violations,
  cleanup/residue, and every identity above.
- [ ] Require two unchanged runs before concluding that more time is needed. If the first run
  proves a deterministic defect, stop and fix it instead.
- [ ] Classify:
  - **Route A:** after any separately governed defect fix, repeatedly completes healthily within
    300 seconds; keep `stdlib-shell.v1`, skip T2/T3, and proceed to T4 after Resume authorization;
  - hangs/pathologically stalls/leaks/fails cleanup: fix the defect in its owning repository;
  - **Route B:** repeatedly exits normally after 300 seconds with no other limit or pathological
    stall; proceed to T2;
  - contradictory/insufficient evidence or another resource cause: stop for a successor decision.
- [ ] After any owner-repository fix, rerun this task from a clean exact head. A router fix must
  remain within PR #58's exact three paths; otherwise stop.

**Task-local acceptance:** Evidence establishes Route A or Route B, or identifies a specific defect
that must be fixed before diagnosis repeats. A pair of bare timeouts is not accepted as proof that
timeout is causal.

**Rollback:** None for read-only diagnosis. Any diagnostic instrumentation or defect fix uses that
owner's ordinary rollback path.

**Dependencies:** T0 and a separately accepted controller-owner plan.

### Task G0-V-R-v2-T2 — Prepare the catalog-stable Route B assignment

**Files:**
- In intent-router: `.github/pr-automation.lock.json` only, in a separate protected-path PR
- In Dev: only paths accepted by its owner plan
- No PR #58 path

**Interfaces:**
- Consumes: T1 Route B evidence, existing cataloged `stdlib-shell.v1` and
  `awa-authoritative-verify.v1`, merged unchanged recipe, qualified compiler/release, and a
  separately accepted Dev-owner plan
- Produces: one semantic intent-router profile-reference change and one compiler-generated lock
  candidate
- Must not change: execution-catalog/profile/resource bytes or digest, another assignment, any
  non-profile intent-router field, recipe, command, dependency graph, required Checks, `local`
  coverage, ruleset, or PR #58

- [ ] Record that 7,200 seconds is the existing broad profile's ceiling, not measured need.
- [ ] Present and obtain explicit operator acceptance of the full
  `awa-authoritative-verify.v1` delta: exact catalog image digests and both tool inventories, plus
  7,200 seconds, 2 CPUs, 2,048 MiB memory, 512 pids, 8,192 MiB disk, 65,536 inodes, and
  16,777,216 output bytes.
- [ ] If that profile is rejected or exact-sandbox evidence shows it unsuitable, stop. A new
  profile requires separate controller architecture, fleet-wide relock design, and successor
  authority.
- [ ] Require the accepted Dev plan to identify—or add and test—a narrow existing-assignment
  reprofile path. It must preserve `local`, both required Checks, coverage mode, and every
  non-profile field while changing only intent-router's profile reference.
- [ ] Record that generic assignment `sync` is unsuitable because it stages new assignments as
  `manual_only`, and generic transcription is unsuitable for an existing required-check
  assignment.
- [ ] Require that Dev plan to define exact changed-path allowlists and the exact serial
  publication, `stage-requiredness`/`finalize-requiredness`, recovery, and rollback order. Any
  tooling addition belongs to Dev and must be tested there before use.
- [ ] Prove the checked-in execution catalog and its semantic digest remain unchanged. Because no
  digest-covered catalog value changes, this route does not trigger fleet-wide relock.
- [ ] In the Dev authority, make one semantic change only: intent-router's profile assignment.
- [ ] Generate, do not edit, `.github/pr-automation.lock.json` from the merged assignment and merged
  unchanged recipe with the qualified compiler.
- [ ] Prove the target PR compare is exactly the one lock path and the compiler reproduces its bytes.
- [ ] Follow the protected-path checks and obtain the target owner's exact-head merge decision. Do
  not infer target authorization from Dev-plan acceptance.

**Task-local acceptance:** The existing broad profile's complete delta is explicitly accepted;
the Dev reprofile path is proven; only intent-router's profile reference changes semantically; the
catalog digest is unchanged; and one generated lock-only head is reproducible and merged through
the protected path.

**Rollback:** Before live activation, close/revert the candidate through ordinary owner paths.
Nothing has been transcribed to the host.

**Dependencies:** T1 Route B and exact Dev/target owner authority. Route A skips T2.

### Task G0-V-R-v2-T3 — Activate and qualify Route B

**Files:**
- No new PR #58 file
- The only target source change is the T2 generated lock
- Live state is limited to intent-router's assignment projection under the Dev owner's plan

**Interfaces:**
- Consumes: T2 merged owner assignment and lock, proven Dev reprofile path and exact serial order,
  distinct fresh forward/recovery operation identities and owner GOs, current live preimage
- Produces: healthy live profile/lock parity plus exact-sandbox broad-profile qualification, or a
  fully proven restoration of the prior preimage
- Must not change: another assignment, recipe, command, required Check, coverage mode, ruleset,
  outer service configuration, PR #58 head/body/Draft posture, or controller semantics

- [ ] Retain the exact prior `stdlib-shell.v1` assignment, generated lock, live config, and
  controller/compiler release identities before mutation.
- [ ] Enter one serialized maintenance window using the documented pause/drain and status controls.
  Require no active, owed, or recovery work before cutover.
- [ ] For every forward mutation, use a distinct fresh, non-replayable operation ID and matching
  owner GO. Allocate the separately required recovery operation ID; never share one ID across
  mutations.
- [ ] Follow the accepted Dev plan's exact serial order, including documented
  `stage-requiredness` and then `finalize-requiredness`; do not use generic assignment `sync` or
  generic transcription as a substitute.
- [ ] Run control-plane/fleet parity and live doctor while paused; prove merged
  assignment/generated-lock/live-config parity and no residue before owner-directed resume.
- [ ] Keep PR #58 Draft. Its required Checks cannot be the qualification because controller policy
  skips Draft PRs.
- [ ] Through the separately governed exact-sandbox diagnostic path, run the unchanged command on
  the selected exact PR #58 head under active `awa-authoritative-verify.v1`. Prove repeatable
  healthy completion and record elapsed/progress/exit/bounded streams/limits/residue and every
  profile/config/assignment/lock identity.
- [ ] Prove every non-target assignment and every forbidden authority stayed unchanged.

If activation, live parity, or exact-sandbox qualification fails, keep PR #58 Draft and attribute
the failure before external mutation. Invoke rollback only when evidence implicates the broad
profile, assignment, generated lock, activation, capacity behavior, or live parity; live
safety/parity is unhealthy; or binding owner policy requires it. An unhealthy live safety/parity
state follows owner rollback immediately.

If qualification instead exposes a source/test failure clearly confined to PR #58 and unrelated to
capacity, keep the qualified healthy Route B assignment active. Under explicit Resume authority,
fix forward within the exact three-file contract, rerun local/Bugbot evidence, and repeat
qualification before Ready; a required fourth path is a stop. If attribution is ambiguous, stop
for owner diagnosis without arbitrary external mutation.

When rollback is triggered:

- [ ] Keep or return the controller to paused/drained state.
- [ ] Use distinct fresh, non-replayable operation IDs and matching owner GOs for every rollback
  mutation plus a distinct recovery operation ID.
- [ ] Restore the exact prior assignment/profile/live-config preimage through the Dev plan's
  reverse requiredness/publication order.
- [ ] Generate the prior lock through the same compiler/lifecycle; never hand-edit it.
- [ ] Obtain the target owner's exact-head rollback decision and merge only that generated lock.
- [ ] Prove generated-lock, assignment/profile, and live-config parity; run control-plane/fleet
  verification and live doctor; prove no residue and no active/owed/recovery work.
- [ ] Optionally run a known-good workload that completes within 300 seconds as a controller smoke.
  Do not require PR #58 to pass under restored `stdlib-shell.v1`.
- [ ] Preserve the failed forward and successful reversal in ordinary operation/Git/PR/Check
  history. Keep or return PR #58 Draft and blocked, then stop.

**Task-local acceptance:** Exact-sandbox qualification succeeds under the active broad profile with
healthy authority parity, or the complete prior preimage is restored and proven when rollback is
triggered. A failed or ambiguous qualification never leads to PR #58 continuation.

**Rollback:** The failure branch above is mandatory. No custom dependency manifest is needed
because PR #58 and later G0-V children are still blocked.

**Dependencies:** T2 and all exact Dev operation/recovery gates. Route A skips T3.

### Task G0-V-R-v2-T4 — Audit and refresh existing PR #58

**Files:**
- `Makefile`
- `install.sh`
- `tests/test_authority_honesty.py`

**Interfaces:**
- Consumes: T1 Route A evidence or successful T3 Route B qualification, explicit Resume
  authorization, existing PR #58 branch/head, live `main`, v1 §§3–6 implementation contract
- Produces: one descendant exact head on the same branch/PR with current-main ancestry and the same
  three-path compare
- Must not change: implementation scope, protected paths, file modes, PR Draft posture, external
  authority, or history

- [ ] Fetch the then-live PR base/head and GitHub comparison. Confirm pre-refresh head
  `aa0cc15c4d4b9b73288cd7c6a9af73dcb816f8b1` remains an ancestor unless an earlier authorized
  within-scope fix was recorded.
- [ ] Audit existing bytes against every incorporated v1 §3–§6 requirement and retain all current
  Bugbot regressions. Do not reconstruct the historical red window or open a replacement PR.
- [ ] Merge then-live `main` into the existing feature branch with an ordinary merge commit.
  Do not rebase, force push, hard reset, or cherry-pick a reconstructed branch.
- [ ] Stop on conflict rather than choosing semantic bytes without review.
- [ ] Re-fetch the live base immediately before push; if it advanced, repeat the ordinary merge.
- [ ] Prove old head ancestry, current-base ancestry, exact three-path compare, and no tracked mode
  change.
- [ ] Push normally with hooks while keeping PR #58 Draft/unarmed.

**Task-local acceptance:** Same PR and branch, descendant history, current-main ancestry, exact
three-file compare, no mode delta, no history rewrite.

**Rollback:** Do not push a conflicted or unreviewed merge. Once a merge commit exists, preserve
history and use ordinary corrective commits; do not reset, discard, or rewrite it.

**Dependencies:** T1 Route A or successful T3 Route B, plus explicit Resume authorization.

### Task G0-V-R-v2-T5 — Build the pre-Ready proof

**Files:**
- Exactly the T4 three-file PR compare

**Interfaces:**
- Consumes: T4 exact head and stable live base
- Produces: exact-head local verification, clean Bugbot review, base/head/compare record, and the
  applicable route evidence for a Ready decision
- Must not reuse: local results or Bugbot output from any prior head

- [ ] From a clean exact head run:

  ```sh
  python3 -m unittest -v tests.test_authority_honesty
  python3 -m unittest -v tests.test_zero_link tests.test_no_execution
  make verify-install
  make verify
  make status-verify
  git diff --check origin/main...HEAD
  /Users/laurence.duggan/dev/_ops/bin/doc-warden.sh check \
    "$(git rev-parse --show-toplevel)"
  ```

- [ ] Record actual counts/skips/durations and require
  `local_evidence.head_sha == release_pointer.source_head == current PR head`.
- [ ] Run a fresh full-branch Bugbot review on that exact head.
- [ ] If a valid fix changes the head, restart this entire task, including Bugbot.
- [ ] Record live `baseRefName`, `baseRefOid`, `headRefOid`, merge base, ordered changed paths, and
  tracked mode delta.
- [ ] Keep the PR Draft. Do not request or claim controller CheckRuns: policy skips Draft PRs.
- [ ] Assemble the Ready packet:
  - exact PR head/base/merge-base/ordered compare/modes;
  - exact-head local results and fresh Bugbot result; and
  - Route A diagnostic evidence, or Route B assignment/lock/activation/exact-sandbox qualification
    evidence and active profile/lock identity.
- [ ] Re-fetch base/head/comparison immediately before presenting the packet. Any change invalidates
  the local/review/compare packet and returns to T4/T5.
- [ ] Present that packet and request explicit Ready authorization for the exact route/head/base.

**Task-local acceptance:** One stable base/head/compare has exact three-file scope, clean local
proof, zero actionable Bugbot findings, complete route evidence, and remains Draft pending an
explicit Ready decision.

**Rollback:** Keep Draft and fix forward. A renewed sandbox capacity failure returns to the owning
G0-V-Q plan; do not increase capacity here.

**Dependencies:** T4.

### Task G0-V-R-v2-T6 — Ready, merge, and record ordinary evidence

**Files:**
- No additional PR #58 path

**Interfaces:**
- Consumes: T5 report and explicit Ready authorization naming its exact base/head
- Produces: both required exact-head production Checks and native governed squash merge, or Draft
  posture plus failure attribution, owner remediation, and conditional Route B rollback
- Must not use: admin merge, manual auto-merge arming, direct main push, force, or a receipt-only
  follow-up PR

- [ ] Revalidate head, base, compare, local evidence, Bugbot result, route evidence, and active
  profile/lock immediately before Ready.
- [ ] Mark only that exact head Ready after the operator's explicit decision.
- [ ] After Ready, obtain both exact-head Checks from verifier App `4274739`:
  `pr-automation / verify` and
  `pr-automation / job:repo.intent-router.m3-verify`. These are the production canary and merge
  gate.
- [ ] Reviewer App exclusively owns approval and native auto-merge arming; GitHub native squash
  merge is the merge path. Do not call `gh pr merge --auto`.
- [ ] If either Check is absent, stale, wrong-App, non-success, or inconsistent with the route
  evidence, return PR #58 to Draft before any retry. Remediate through the correct owner, refresh
  T4/T5 evidence, and require a new explicit Ready decision even if the head SHA is unchanged.
- [ ] On Route B, invoke T3's exact-preimage rollback only when evidence implicates the broad
  profile, profile assignment, generated lock, activation, capacity behavior, or live parity; live
  safety/parity is unhealthy; or binding Dev/controller policy requires rollback.
- [ ] For a source/test failure clearly confined to PR #58 and unrelated to capacity, keep the
  successfully qualified healthy Route B assignment active, fix forward within the exact
  three-file contract, rerun T4/T5 local and Bugbot evidence, and obtain a new Ready decision. A
  required fourth path is a stop.
- [ ] If attribution is ambiguous, keep PR #58 Draft and stop for owner diagnosis without
  arbitrary external mutation. If live safety/parity is unhealthy, follow owner rollback policy
  immediately.
- [ ] If base/head/evidence changes before merge, return to Draft, then T4/T5, and obtain a new
  Ready decision.
- [ ] Do not require a manual pause after green Checks. The reviewer App may approve, arm, and
  complete native merge before a separate observation step.
- [ ] After merge, fetch live `main`; record PR URL/number, final base/head, exact compare, both
  exact-head CheckRuns, merge SHA, and changed paths. If merge already occurred, validate this
  evidence retrospectively against the final head.
- [ ] Independently require `git rev-parse <merge-sha>^1` to equal the base SHA recorded immediately
  before merge.
- [ ] Require live default to contain the reviewed three implementation paths from the exact head
  and the merge commit to be an ancestor.
- [ ] Stop. Do not create a Dev receipt PR or begin G0-V-H.

**Task-local acceptance:** Both required Checks succeed from verifier App `4274739` on the exact
reviewed head; that head merges through the reviewer-App/native path; ordinary Git/PR/Check evidence
is complete; first parent equals recorded base.

**Rollback:** Before later G0-V work depends on the merge, an ordinary router revert may restore
the three implementation paths under fresh authority and full proof. Route B profile restoration
is a separate Dev operation using T3's retained preimage and existing lifecycle. Once a later
child depends on either change, use v3's owner-by-owner reverse order or forward-fix.

**Dependencies:** T5 and explicit exact-head Ready authorization.

## 5. Acceptance tests

The plan is complete only when all applicable rows are proven:

| ID | Requirement |
|---|---|
| A1 | Prospective accepted v4/v2 digests are reviewed and explicitly accepted before the exact staged transformation; v3/v1 bytes remain unchanged and rows transition atomically. |
| A2 | Exact-sandbox diagnosis records elapsed, progress when available, disposition, bounded streams, profile/config identity, residue, and repeatability and selects Route A or Route B. |
| A3 | A stall/defect is fixed through its owner; timeout is not raised to conceal it. |
| A4 | Route A keeps `stdlib-shell.v1` and skips all Dev assignment, lock, activation, and capacity tasks. |
| A5 | Route B reuses only existing `awa-authoritative-verify.v1` after full-delta acceptance and qualification; the execution catalog/digest remain unchanged. |
| A6 | Route B uses a Dev-owned, tested existing-assignment reprofile path; one semantic profile reference and one generated lock path change while `local`, required Checks, coverage, recipe, command, ruleset, and all other assignments remain unchanged. |
| A7 | Route B uses fresh per-mutation operation IDs/owner GOs, a distinct recovery ID, retained preimage, requiredness stage/finalize, pause/drain, parity, doctor, no-residue/no-work proof, and exact-sandbox qualification or exact rollback. |
| A8 | PR #58 remains Draft through descendant-only refresh, exact three-path comparison, fresh local verification, and fresh Bugbot review. |
| A9 | Ready explicitly names the exact route/head/base/compare packet; only then do both verifier-App Checks run as the production canary and merge gate. |
| A10 | Any absent, stale, wrong-App, non-success, or route-divergent Check returns PR #58 to Draft and requires refreshed evidence plus a new Ready decision; Route B rollback occurs only for capacity/profile/assignment/lock/activation/parity evidence or binding owner policy, while a clear three-file router failure fixes forward and ambiguous attribution stops for diagnosis. |
| A11 | Merge SHA is on live default and its first parent independently equals the recorded pre-merge base. |
| A12 | No custom receipt namespace/store/journal/dependency machinery or post-merge Dev evidence PR exists. |

## 6. Evidence record

Use links, IDs, SHAs, digests, and existing operation receipts—not a new schema:

- prospective and post-transformation accepted v4/v2 SHA-256 digests, exact three-path staged diff,
  doc-warden successor results, and joint acceptance merge;
- controller accepted-plan path/digest/merge, plus the Dev accepted-plan path/digest/merge on
  Route B only;
- Route A or Route B diagnostic run IDs, head/tree,
  elapsed/progress/disposition/streams/residue, and exact sandbox identity;
- external implementation PR/head/merge/release IDs when a controller defect fix is needed;
- on Route B, selected existing profile ID/digest, complete field comparison, and unchanged
  execution-catalog digest;
- on Route B, Dev assignment PR/head/merge and before/after assignment digests;
- on Route B, every distinct forward/recovery/rollback operation ID and owner GO, existing
  lifecycle evidence, and retained preimage digest/location;
- on Route B, generated-lock PR base/head/compare/checks/merge and
  compiler/recipe/assignment/lock/live-config digests;
- on Route B, exact-sandbox qualification, and rollback assignment/lock PRs, parity, doctor,
  residue/work-state proof when used;
- PR #58 final base/head/merge-base/paths/modes;
- exact-head local commands/results/durations and Bugbot result;
- both required final CheckRun IDs, verifier App ID, head SHAs, and conclusions;
- PR #58 merge SHA, live-default ancestry, and `merge^1 == recorded base`.

Git history makes the merged implementation durable; existing lifecycle receipts make the
assignment operation auditable. There is no interval waiting for a separately published G0-V-R
receipt and therefore no receipt-reversal or Dev-address contract to solve.

## 7. Changed-path boundaries

| Delivery | Exact intent-router changed paths |
|---|---|
| Joint successor acceptance | `docs/plans/roadmap-revision-step-3-design-v4.md`, `docs/plans/g0-v-r-local-gate-prerequisite-v2.md`, `docs/plans/README.md` |
| Route B capacity lock only | `.github/pr-automation.lock.json` only |
| Existing G0-V-R PR #58 | `Makefile`, `install.sh`, `tests/test_authority_honesty.py` |

External controller/Dev plans must declare and enforce their own exact allowlists. This plan grants
no external path. Any fourth PR #58 path, any second capacity-lock path, or any edit to accepted
v3/v1 is a stop.

## 8. Stop conditions

### Binding repository/design stops

Stop if CR1/CR2/CR4/CR5, KI1, zero-link, frozen contracts, or router-off safety would change; a
paid runner or GitHub Actions workflow is proposed; required verifier-App identity/check names or
rulesets change; accepted predecessor bytes change; or normal repository hooks/governed delivery
would require bypass.

### External owner-policy stops

Stop if the controller diagnostic plan is absent/unaccepted; on Route B, stop if the Dev plan or
its tested existing-assignment reprofile path is absent/unaccepted. Also stop if released profile
immutability is violated; diagnostic or mutation uses an unqualified controller/compiler; a fresh
per-mutation operation ID/owner GO, distinct recovery ID, overlap guard, retained preimage,
pause/drain, requiredness stage/finalize, doctor, rollback, ordinary evidence, or no-work/no-residue
proof is missing; the live profile/lock differs from merged source authority; or an external
change exceeds its owner's accepted allowlist. Report to that owner; do not repair it under router
authority.

### Plan-specific stops

Stop if:

- v4/v2 cannot be accepted together in one docs-only transition;
- the successors are not staged before doc-warden, cached paths exceed the exact three docs, or
  prospective/post-transformation accepted digests differ;
- PR #58 is mutated before Route A or Route B is proven and Resume is explicit;
- diagnosis uses a different command, head, image, mount, or resource envelope;
- diagnosis stalls/pathologically hangs or does not establish repeatability;
- Route B proposes a new profile/catalog mutation, treats 7,200 seconds as measured need, or lacks
  explicit full-delta acceptance and exact-sandbox qualification;
- generic assignment `sync`/transcription is used instead of a proven existing-assignment
  reprofile and requiredness path;
- an operation ID/owner GO is replayed or shared, or the recovery operation ID is missing;
- another assignment, the recipe, command, dependency, required Check, coverage mode, ruleset, or
  outer controller deadline changes;
- the lock is hand-edited or not reproducible;
- target-owner exact-head authorization is absent;
- a Route B capacity/profile/assignment/lock/activation/parity failure triggers rollback but does
  not restore and prove the exact prior preimage;
- a clear PR #58 source/test failure causes external rollback, exceeds the three-file contract, or
  skips renewed local/Bugbot/Ready proof;
- ambiguous attribution causes arbitrary external mutation instead of Draft posture and owner
  diagnosis, or unhealthy live safety/parity does not follow owner rollback policy immediately;
- branch refresh conflicts, rewrites history, loses old-head ancestry, adds a path, or changes a
  tracked mode;
- a controller Check is required or claimed while PR #58 remains Draft;
- any exact head lacks full local/Bugbot replacement evidence before Ready;
- base/head/compare moves without returning to T4/T5;
- Ready is inferred, stale, reused, or not renewed after a failed/divergent Check even on the same
  head;
- PR #58 would require admin merge or manual auto-merge arming; or
- merge first-parent validation fails.

These are conservative safeguards for this plan, not new repository-wide policy.

## 9. Exact operator gates

1. **Joint documentation acceptance:** one explicit decision names both prospective accepted
   successor digests and accepts their exact transformation plus the atomic index transition.
   Until then both files remain Draft.
2. **Controller plan acceptance:** the controller owner accepts exact-sandbox diagnosis and any
   defect/instrumentation work. Router acceptance confers no controller authority.
3. **Route B profile/Dev plan acceptance:** only on Route B, the operator accepts every
   `awa-authoritative-verify.v1` delta and the Dev owner accepts a plan that owns and proves the
   reprofile/publication/requiredness/rollback path.
4. **Route B mutation gates:** every forward or rollback mutation gets a fresh operation ID and
   matching owner GO; recovery uses its own ID. The target owner separately authorizes each exact
   generated protected-path head.
5. **PR #58 Resume:** after T1 Route A or successful T3 Route B, the operator explicitly authorizes
   Draft branch refresh and pre-Ready evidence replacement.
6. **PR #58 Ready:** after T5, the operator explicitly authorizes Ready for the reported exact
   route/base/head/compare/evidence. Ready may trigger controller Checks and reviewer-App
   auto-merge. Any absent, stale, wrong-App, non-success, or route-divergent Check requires Draft
   posture, failure attribution, refreshed evidence, and a new decision before retry. Route B
   rollback additionally requires the narrow trigger in T3/T6 or binding owner policy.
7. **Handoff:** after T6 evidence, stop. G0-V-H needs separate accepted authority.

## 10. ADR and acceptance boundary

No intent-router ADR is required. Accepted v3 already owns the runnerless authority split and
generated-lock boundary; v4/v2 narrowly repair sequencing after an observed operational failure.
The controller and Dev plans make their own ADR determinations. A reusable capacity platform,
new evidence protocol, or changed execution semantics would require owner-specific architecture
review and is outside this plan.

This file remains Draft. It does not accept or supersede any plan, resume or change PR #58, create
an external plan, change a profile/assignment/lock, operate the host, or authorize implementation.
