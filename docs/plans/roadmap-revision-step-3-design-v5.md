# Intent-router roadmap revision — Step 3 design v5

**Status:** DRAFT — 2026-09-04
**Plan-type:** standard
**Supersedes:** `docs/plans/roadmap-revision-step-3-design-v4.md` only upon acceptance and merge
**Predecessor SHA-256:** `ddcb06643995c8d794b9a48c530dd7bc2ad7666d8210cddec6dc5f4a25bf25ed`
**Purpose:** Correct v4's lifecycle assertions without changing its architecture, sequencing,
scope, evidence, rollback, or authority boundaries.

## 1. Root cause and binding correction rule

Bugbot correctly found that operator-accepted v4 contains body text written for a Draft state while
its PR-branch Status and index row say `ACCEPTED`. The branch record therefore contradicts itself.
V4 has not merged to default, so its statement that v3 remains live was operationally accurate even
though it conflicted with the branch index.

Binding repository and doc-warden policy freezes an accepted semantic version byte-for-byte.
Therefore v4 is preserved at SHA-256
`ddcb06643995c8d794b9a48c530dd7bc2ad7666d8210cddec6dc5f4a25bf25ed`; this correction is a new
successor rather than an in-place edit, amend, or revert.

While v5 Status is `DRAFT` and PR #59 is unmerged, live `origin/main` remains governed by design
v3. V4 is an operator-accepted, frozen intermediate record on the PR branch; it has never been
active on live default. A valid v5 acceptance and governed PR #59 merge introduce and supersede v4
in the same merge and establish v5 as the active live design.

## 2. Normative amendment

V5 carries every v4 architecture decision, operational sequence, invariant, non-goal, route,
evidence requirement, stop, rollback rule, and authority boundary forward by reference without
semantic change.

The only amendment is lifecycle truth:

1. Every v4 statement whose truth depends on v4 being Draft, a candidate, unaccepted, not yet
   superseding v3, or awaiting a future acceptance delivery is superseded.
2. This includes v4's Draft-specific Purpose sentence; §1's active-predecessor/conditional-successor
   wording; §4's future joint-acceptance procedure and Draft-state assertions; §7's statement about
   what “these Draft bytes” authorize; and §11's closing Draft/non-supersession statement.
3. V4 was operator-accepted and frozen on the PR branch in commit
   `e40436c6ab97dd56fc7f5f2d049e831bd92569db`; it never became live-default authority. The
   corrective delivery preserves that commit and v4's bytes as history.
4. References in carried-forward v4 operational text to the governing design mean v5 after v5 is
   accepted and PR #59 is merged to live default.

No product, contract, controller, Dev, host, receipt, privacy, provider, or capacity design is
added or changed.

## 3. Authority remains bounded

A valid accepted-and-merged v5 establishes intent-router design and sequencing authority only. It
does not by itself authorize:

- controller or Dev repository mutation;
- `.github/**` or other protected-path mutation;
- protected-host staging, activation, recovery, or rollback;
- changing PR #58, marking it Ready, or merging it; or
- beginning any later G0-V child.

All separately accepted owner plans, exact-head decisions, operation IDs/owner GOs, recovery
identity, Draft/Ready sequencing, reviewer-App ownership, and other operation-specific gates
carried from v4 remain mandatory.

CR1/CR2, CR4, CR5, KI1, router-off safety, zero-link, frozen contracts, and the no-paid-runner
boundary remain unchanged.

## 4. Corrective joint delivery

G0-V-R v3 defines the one corrective acceptance task. The branch contains frozen v4/v2 records in
commit `e40436c6ab97dd56fc7f5f2d049e831bd92569db`; neither has been live-default authority.

Before the v5/v3 status transition, the exact prospective bytes and index transformation must be
constructed and reviewed. The acceptance/delivery record is valid only when it contains:

1. a new explicit operator decision naming both prospective accepted v5/v3 digests;
2. only the two status-token changes and four index transitions specified by v3;
3. matching post-transformation v5/v3 hashes;
4. exactly the allowed current-commit and cumulative PR paths; and
5. the eventual governed PR #59 merge to live default.

The resulting PR compare is exactly five documentation paths:

```text
docs/plans/README.md
docs/plans/g0-v-r-local-gate-prerequisite-v2.md
docs/plans/g0-v-r-local-gate-prerequisite-v3.md
docs/plans/roadmap-revision-step-3-design-v4.md
docs/plans/roadmap-revision-step-3-design-v5.md
```

The valid merge introduces and supersedes v4/v2 atomically, so their contradictory lifecycle
assertions never become live active authority. That merge leaves v5/v3 as the active authorities
and leaves v4/v2 bytes and digests unchanged.

## 5. State-safe acceptance boundary

Before the status transition and governed PR #59 merge, this file changes no live authority;
design v3 on `origin/main` remains governing. Acceptance is valid only under §4 and becomes live
authority only when the governed merge lands. In every state, this document grants no
external-owner, protected-path, protected-host, PR #58 Ready, approval, auto-merge, or merge
authority by itself.
