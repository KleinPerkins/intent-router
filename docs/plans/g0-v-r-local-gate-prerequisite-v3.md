# G0-V-R local-gate prerequisite continuation plan v3

**Status:** ACCEPTED — 2026-09-04
**Plan-type:** agentic-execution
**Supersedes:** `docs/plans/g0-v-r-local-gate-prerequisite-v2.md` only upon acceptance and merge
**Predecessor SHA-256:** `a80085e1f69f45b7fc617bd6e06000b010106f9ba34d0ec0af8d0a3562b529d2`
**Governing design:** `docs/plans/roadmap-revision-step-3-design-v5.md` only if v5 is accepted and
merged in the same corrective delivery
**Purpose:** Correct v2's lifecycle assertions and acceptance task without changing its G0-V-R
route logic or operational design.

## 1. Root cause, freeze, and state

Bugbot correctly found that operator-accepted v2 says it is Draft, calls v4 a candidate awaiting
joint acceptance, says v1 remains active, and defines a T0 procedure for an acceptance event that
the PR branch records as complete. Those statements conflict with v2's branch Status and index.
V2 has not merged to default, so v1 remains the live plan despite that branch-only index transition.

Binding repository and doc-warden policy freezes accepted semantic versions byte-for-byte.
Therefore v2 is preserved at SHA-256
`a80085e1f69f45b7fc617bd6e06000b010106f9ba34d0ec0af8d0a3562b529d2`; this correction uses v3
rather than editing, amending, or reverting v2. V4 is likewise preserved at SHA-256
`ddcb06643995c8d794b9a48c530dd7bc2ad7666d8210cddec6dc5f4a25bf25ed`.

While v3/v5 Status is `DRAFT` and PR #59 is unmerged, live `origin/main` remains governed by plan
v1 and design v3. V2/v4 are operator-accepted, frozen intermediate PR-branch records; neither has
ever been active on live default. A valid v5/v3 acceptance and governed PR #59 merge introduce and
supersede v2/v4 in the same merge and establish v3/v5 as the active live authorities.

## 2. Exact incorporation and amendment

V3 incorporates the following operational content without semantic change:

- accepted plan v1 §§3–6 for the objective, noexec meaning, exact three-file implementation
  design, and implementation allowlist;
- v2 §2 and §3;
- v2 §4 items 4–11;
- v2 Work items T1 through T6 inclusive, beginning at
  `### Task G0-V-R-v2-T1 — Diagnose the exact sandbox` and ending with T6's
  `**Dependencies:** T5 and explicit exact-head Ready authorization.`;
- v2 §5 acceptance rows A2–A12;
- v2 §6;
- v2 §7 except the historical `Joint successor acceptance` row;
- v2 §8 except its first two plan-specific bullets about accepting/staging v4/v2; and
- v2 §9 gates 2–7 plus §10's ADR determination.

Those incorporated ranges continue Route A/Route B, exact PR #58 scope, evidence, stops,
conditional rollback attribution, Draft/Ready sequencing, reviewer-App ownership, and
operation-specific gates without operational change. Numbered v2 task labels and source text
remain historical identifiers.

Authority references are closed and rebind only after the corrective merge:

- every incorporated governing-design reference resolves to accepted v5 on live default;
- every incorporated accepted-plan reference for this continuation resolves to accepted v3 on
  live default;
- every incorporated T0 dependency resolves to completed T0-C below, including the governed PR #59
  merge; and
- specifically, incorporated v2 T1 cannot consume branch-only v4/v2 acceptance and is ineligible
  until live `origin/main` contains the PR #59 merge with v5/v3 as the active indexed authorities.

V3 supersedes only:

1. every v2 statement whose truth depends on v2 being Draft, a candidate, unaccepted, not yet
   superseding v1, or awaiting future joint acceptance with v4;
2. v2's `Governing design candidate` metadata and conditional future-delivery wording;
3. v2 T0 in full, v2 §5 row A1, v2 §7's historical joint-acceptance row, v2 §8's two
   acceptance-specific stop bullets, v2 §9 gate 1, and v2's closing Draft/non-supersession
   paragraph; and
4. any carried reference that would otherwise imply the prior v4/v2 acceptance authorizes v5/v3.

The replacement lifecycle and acceptance procedure are in §1 and T0-C below. No product, contract,
controller, Dev, host, receipt, privacy, provider, or capacity design changes. PR #58 remains
Draft and untouched.

## Work items

### Task G0-V-R-v3-T0-C — Accept the corrective successors atomically

**Files:**
- `docs/plans/roadmap-revision-step-3-design-v5.md`
- `docs/plans/g0-v-r-local-gate-prerequisite-v3.md`
- `docs/plans/README.md`

**Interfaces:**
- Consumes: immutable operator-accepted v4/v2 branch bytes and digests, independently reviewed
  Draft v5/v3 bytes,
  deterministic prospective accepted v5/v3 bytes, and one explicit operator acceptance decision
  naming both prospective accepted digests
- Produces: an exact corrective status/index commit on Draft PR #59 and its eventual governed merge
  to live default; only that completed merge leaves v5/v3 active and satisfies T0-C
- Must not mutate: v4/v2 or any other accepted plan bytes, PR #58, product/contracts,
  `.github/**`, external repositories, protected-host state, or GitHub Ready/approval/merge state

- [ ] Require v4 SHA-256
  `ddcb06643995c8d794b9a48c530dd7bc2ad7666d8210cddec6dc5f4a25bf25ed` and v2 SHA-256
  `a80085e1f69f45b7fc617bd6e06000b010106f9ba34d0ec0af8d0a3562b529d2`.
- [ ] Before the v5/v3 status transition, stage exactly the three files above. Require the current cached
  paths to be exactly README/v5/v3 and the cumulative `origin/main...HEAD` plus cache compare to
  be exactly:

  ```text
  docs/plans/README.md
  docs/plans/g0-v-r-local-gate-prerequisite-v2.md
  docs/plans/g0-v-r-local-gate-prerequisite-v3.md
  docs/plans/roadmap-revision-step-3-design-v4.md
  docs/plans/roadmap-revision-step-3-design-v5.md
  ```

- [ ] Run `git diff --cached --check`, `git diff --check`, and doc-warden before acceptance.
  Require doc-warden to name v3, v5, v2, and v4 as `CONFORMANT`.
- [ ] Before the status transition, construct the prospective accepted bytes deterministically in
  memory or another non-repository review surface. The transformation is closed to:
  - v5 and v3 Status tokens: `DRAFT` → `ACCEPTED`;
  - v4 index row: status `SUPERSEDED`, note
    `Immutable branch design record; introduced and superseded in corrective PR #59 merge`;
  - v5 index row: status `ACCEPTED`, note
    `Active design basis; lifecycle-corrected v4 architecture and G0-V-Q sequencing`;
  - v2 index row: status `SUPERSEDED`, note
    `Immutable branch plan record; introduced and superseded in corrective PR #59 merge`; and
  - v3 index row: status `ACCEPTED`, note
    `Active G0-V-R continuation basis; lifecycle-corrected v2 operations`.
- [ ] Review the exact prospective three-file diff and compute both prospective accepted successor
  SHA-256 digests. The prior v4/v2 acceptance is not authority for these bytes.
- [ ] Obtain a new explicit operator decision naming both prospective accepted v5/v3 digests.
- [ ] Acceptance is valid only when the record contains that explicit decision, the exact closed
  transformation, matching post-transformation hashes, the exact three current-commit paths and
  five cumulative PR paths, and the eventual governed PR #59 merge.
- [ ] After the explicit decision, apply exactly the reviewed transformation, stage exactly
  README/v5/v3, recompute both digests, and require exact matches before commit.
- [ ] Reprove immutable v4/v2 digests, the three cached paths, the five cumulative PR paths, and
  exact README transitions. Require design v3 and plan v1 to remain `SUPERSEDED` in the final
  branch index.
- [ ] Run `git diff --cached --check`, `git diff --check`, doc-warden, `make verify`, and
  `make status-verify`; require all four plan versions to be named `CONFORMANT`.
- [ ] Commit and push normally to the existing branch and update Draft PR #59. Keep it Draft and
  unarmed. Do not touch PR #58, mark Ready, approve, arm auto-merge, or merge.
- [ ] After the reviewer-App-governed PR #59 merge, fetch live `origin/main` and prove the merge,
  exact five-path compare, v4/v2 immutable digests, v5/v3 accepted digests, and active v5/v3 index
  rows. Only then mark T0-C complete or allow incorporated T1 to begin.

**Task-local acceptance:** T0-C is complete only after the operator names and accepts exact
prospective v5/v3 digests, the committed bytes match, v4/v2 remain immutable, the PR compare is
exactly five paths, and the governed PR #59 merge is verified on live `origin/main`. That merge
introduces and supersedes v4/v2 atomically, so their contradictory lifecycle assertions never
become live active authority; v5/v3 are the active final authority.

**Rollback:** Before v5/v3 acceptance, revise only their Draft bytes and Draft index rows. After
acceptance, freeze v5/v3 and use new successors for any correction. Before PR merge, the branch may
be closed through the ordinary governed path; never rewrite or mutate v4/v2.

**Dependencies:** Immutable v4/v2 branch commit
`e40436c6ab97dd56fc7f5f2d049e831bd92569db`, independently reviewed v5/v3 Drafts, a new explicit
prospective-digest acceptance decision, and the ordinary reviewer-App-governed delivery path.
Incorporated T1 has a hard completion dependency on the eventual PR #59 merge being verified on
live default with v5/v3 as active indexed authorities.

## 3. Corrective delivery and authority boundary

The corrective chain's final PR compare is exactly README, v2, v3, v4, and v5. Before its merge,
live `origin/main` remains governed by design v3 and plan v1; frozen v4/v2 exist only on the branch.
The valid merge introduces and supersedes v4/v2 atomically and leaves v5/v3 active. This is a
plan-specific corrective delivery; the binding repository rule is only that accepted semantic
versions freeze and corrections use successors.

Before the status transition and governed PR #59 merge, this file changes no live authority.
Acceptance is valid only under T0-C and becomes live authority only when that merge is verified on
`origin/main`. In every state, v3 grants no controller/Dev/protected-path/protected-host mutation
without separately accepted owner plans and operation-bound gates. It does not change or authorize
PR #58, Ready, approval, auto-merge, merge, or later G0-V work.
