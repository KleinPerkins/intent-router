# G0-V-R local-gate prerequisite continuation plan v3

**Status:** DRAFT — 2026-09-04
**Plan-type:** agentic-execution
**Supersedes:** `docs/plans/g0-v-r-local-gate-prerequisite-v2.md` only upon acceptance and merge
**Predecessor SHA-256:** `a80085e1f69f45b7fc617bd6e06000b010106f9ba34d0ec0af8d0a3562b529d2`
**Governing design:** `docs/plans/roadmap-revision-step-3-design-v5.md` only if v5 is accepted and
merged in the same corrective delivery
**Purpose:** Correct v2's lifecycle assertions and acceptance task without changing its G0-V-R
route logic or operational design.

## 1. Root cause, freeze, and state

Bugbot correctly found that accepted v2 still says it is Draft, calls v4 a candidate awaiting
future joint acceptance, says v1 remains active, and defines a T0 procedure for an acceptance event
that already occurred. Those statements conflict with v2's accepted Status and index transition.

Binding repository and doc-warden policy freezes accepted semantic versions byte-for-byte.
Therefore v2 is preserved at SHA-256
`a80085e1f69f45b7fc617bd6e06000b010106f9ba34d0ec0af8d0a3562b529d2`; this correction uses v3
rather than editing, amending, or reverting v2. V4 is likewise preserved at SHA-256
`ddcb06643995c8d794b9a48c530dd7bc2ad7666d8210cddec6dc5f4a25bf25ed`.

While Status is `DRAFT`, v2 remains the active G0-V-R continuation plan and v4 remains the active
design. Upon joint v5/v3 acceptance and merge, v3 governs G0-V-R continuation under v5.

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

Those incorporated ranges continue to govern Route A/Route B, exact PR #58 scope, evidence, stops,
conditional rollback attribution, Draft/Ready sequencing, reviewer-App ownership, and
operation-specific gates. References within them to T0 mean the corrective task below. Numbered
task labels remain historical identifiers; no task is replayed merely because this successor
exists.

V3 supersedes only:

1. every v2 statement whose truth depends on v2 being Draft, a candidate, unaccepted, not yet
   superseding v1, or awaiting future joint acceptance with v4;
2. v2's `Governing design candidate` metadata and conditional future-delivery wording;
3. v2 T0 in full, v2 §5 row A1, v2 §7's historical joint-acceptance row, v2 §8's two
   acceptance-specific stop bullets, v2 §9 gate 1, and v2's closing Draft/non-supersession
   paragraph; and
4. any carried reference that would otherwise imply the prior v4/v2 acceptance authorizes v5/v3.

The replacement lifecycle and acceptance procedure are in §§1 and 3. No product, contract,
controller, Dev, host, receipt, privacy, provider, or capacity design changes. PR #58 remains
Draft and untouched.

## Work items

### Task G0-V-R-v3-T0-C — Accept the corrective successors atomically

**Files:**
- `docs/plans/roadmap-revision-step-3-design-v5.md`
- `docs/plans/g0-v-r-local-gate-prerequisite-v3.md`
- `docs/plans/README.md`

**Interfaces:**
- Consumes: immutable accepted v4/v2 bytes and digests, independently reviewed Draft v5/v3 bytes,
  deterministic prospective accepted v5/v3 bytes, and one explicit operator acceptance decision
  naming both prospective accepted digests
- Produces: one corrective commit on Draft PR #59 whose cumulative compare is exactly five
  documentation paths and whose eventual merge atomically leaves v5/v3 active
- Must not mutate: v4/v2 or any other accepted plan bytes, PR #58, product/contracts,
  `.github/**`, external repositories, protected-host state, or GitHub Ready/approval/merge state

- [ ] Require v4 SHA-256
  `ddcb06643995c8d794b9a48c530dd7bc2ad7666d8210cddec6dc5f4a25bf25ed` and v2 SHA-256
  `a80085e1f69f45b7fc617bd6e06000b010106f9ba34d0ec0af8d0a3562b529d2`.
- [ ] While v5/v3 still say Draft, stage exactly the three files above. Require the current cached
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
- [ ] Construct the prospective accepted bytes deterministically in memory or another
  non-repository review surface. Change only:
  - v5 and v3 Status tokens: `DRAFT` → `ACCEPTED`;
  - v4 index row: status `SUPERSEDED`, note
    `Immutable prior design; superseded by accepted v5`;
  - v5 index row: status `ACCEPTED`, note
    `Active design basis; lifecycle-corrected v4 architecture and G0-V-Q sequencing`;
  - v2 index row: status `SUPERSEDED`, note
    `Immutable prior plan; superseded by accepted v3`; and
  - v3 index row: status `ACCEPTED`, note
    `Active G0-V-R continuation basis; lifecycle-corrected v2 operations`.
- [ ] Review the exact prospective three-file diff and compute both prospective accepted successor
  SHA-256 digests. The prior v4/v2 acceptance is not authority for these bytes.
- [ ] Obtain a new explicit operator decision naming both prospective accepted v5/v3 digests.
- [ ] Only after that decision, apply exactly the reviewed transformation, stage exactly
  README/v5/v3, recompute both digests, and require exact matches before commit.
- [ ] Reprove immutable v4/v2 digests, the three cached paths, the five cumulative PR paths, and
  exact README transitions.
- [ ] Run `git diff --cached --check`, `git diff --check`, doc-warden, `make verify`, and
  `make status-verify`; require all four plan versions to be named `CONFORMANT`.
- [ ] Commit and push normally to the existing branch and update Draft PR #59. Keep it Draft and
  unarmed. Do not touch PR #58, mark Ready, approve, arm auto-merge, or merge.

**Task-local acceptance:** The operator names and accepts exact prospective v5/v3 digests; the
committed bytes match; v4/v2 remain immutable; and the Draft PR has exactly the five-path
corrective chain. Upon eventual governed merge, v4/v2 are introduced and superseded in that same
merge, so their contradictory lifecycle assertions never become live active authority on default;
v5/v3 are the active final authority.

**Rollback:** Before v5/v3 acceptance, revise only their Draft bytes and Draft index rows. After
acceptance, freeze v5/v3 and use new successors for any correction. Before PR merge, the branch may
be closed through the ordinary governed path; never rewrite or mutate v4/v2.

**Dependencies:** Immutable v4/v2 commit
`e40436c6ab97dd56fc7f5f2d049e831bd92569db`, independently reviewed v5/v3 Drafts, and a new
explicit prospective-digest acceptance decision.

## 3. Corrective delivery and authority boundary

The corrective chain's final PR compare is exactly README, v2, v3, v4, and v5. V4/v2 remain
immutable accepted historical versions in Git and are superseded only by the later v5/v3
acceptance-and-merge transition. This is a plan-specific corrective delivery; the binding
repository rule is only that accepted semantic versions freeze and corrections use successors.

While Status is `DRAFT`, this file authorizes no acceptance transformation and v2 remains active.
Upon explicit prospective-digest acceptance and merge, v3 supersedes v2 and governs G0-V-R
continuation. In either state, v3 grants no controller/Dev/protected-path/protected-host mutation
without the separately accepted owner plans and operation-bound gates incorporated from v2. It
does not change or authorize PR #58, Ready, approval, auto-merge, merge, or later G0-V work.
