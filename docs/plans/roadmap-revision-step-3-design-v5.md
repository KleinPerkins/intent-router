# Intent-router roadmap revision — Step 3 design v5

**Status:** DRAFT — 2026-09-04
**Plan-type:** standard
**Supersedes:** `docs/plans/roadmap-revision-step-3-design-v4.md` only upon acceptance and merge
**Predecessor SHA-256:** `ddcb06643995c8d794b9a48c530dd7bc2ad7666d8210cddec6dc5f4a25bf25ed`
**Purpose:** Correct v4's lifecycle assertions without changing its architecture, sequencing,
scope, evidence, rollback, or authority boundaries.

## 1. Root cause and binding correction rule

Bugbot correctly found that accepted v4 still contains body text written for its former Draft
state: it says v3 remains active, describes v4 acceptance as future, and closes by saying v4
remains Draft and does not supersede anything. Those statements conflict with v4's accepted Status
and index transition.

Binding repository and doc-warden policy freezes an accepted semantic version byte-for-byte.
Therefore v4 is preserved at SHA-256
`ddcb06643995c8d794b9a48c530dd7bc2ad7666d8210cddec6dc5f4a25bf25ed`; this correction is a new
successor rather than an in-place edit, amend, or revert.

While Status is `DRAFT`, v4 remains the active design. Upon v5 acceptance and merge, v5 becomes the
active design and v4 becomes an immutable superseded historical version.

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
3. V4 was accepted in commit `e40436c6ab97dd56fc7f5f2d049e831bd92569db`. The corrective
   delivery defined by G0-V-R v3 preserves that commit and v4's bytes as history, then establishes
   v5 as the active design.
4. References in carried-forward v4 operational text to the governing design mean v5 after v5 is
   accepted and merged.

No product, contract, controller, Dev, host, receipt, privacy, provider, or capacity design is
added or changed.

## 3. Authority remains bounded

Acceptance of v5 establishes intent-router design and sequencing authority only. It does not by
itself authorize:

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

G0-V-R v3 defines the one corrective acceptance task. The branch already contains immutable
accepted v4/v2 in commit `e40436c6ab97dd56fc7f5f2d049e831bd92569db`. Upon explicit acceptance
of prospective v5/v3 bytes, the same Draft PR may add v5/v3 and atomically transition the index:
v4/v2 become `SUPERSEDED`; v5/v3 become `ACCEPTED`.

The resulting PR compare is exactly five documentation paths:

```text
docs/plans/README.md
docs/plans/g0-v-r-local-gate-prerequisite-v2.md
docs/plans/g0-v-r-local-gate-prerequisite-v3.md
docs/plans/roadmap-revision-step-3-design-v4.md
docs/plans/roadmap-revision-step-3-design-v5.md
```

V4/v2 are introduced and superseded in the same eventual merge to default, so their contradictory
lifecycle assertions never become live active authority there. V5/v3 are the final active
authorities after that merge. V4/v2 bytes and digests remain unchanged.

## 5. State-safe acceptance boundary

While Status is `DRAFT`, this file changes no authority and v4 remains active. Upon acceptance and
merge under G0-V-R v3's prospective-digest gate, v5 supersedes v4 and becomes the active design.
In either state, this document grants no external-owner, protected-path, protected-host, PR #58
Ready, approval, auto-merge, or merge authority by itself.
