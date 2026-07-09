# ROLLBACK — per-phase and state rollback

> How to undo any phase and how to recover router state. The router is **zero-link + additive**, so
> a phase revert is always safe: nothing else in the tree links to it, and no contract field is ever
> removed (only added), so reverting a phase's PR cannot orphan a consumer.

## Per-phase rollback (code)

Each phase lands as **its own PR**. To roll a phase back:

1. Identify the phase's merge commit / PR from `status.yml` (`pr` + `commit` fields).
2. Revert that PR (`git revert -m 1 <merge-commit>`), open the revert as its own PR, and let CI
   (`make verify`) confirm green — the repo returns to the prior phase's frozen state.
3. Flip the phase's `status.yml` entry back to `pending`, remove its `passed_test_ids`, and
   regenerate `RESUME.md` to point at it again. `make status-verify` then recomputes the ledger to
   match disk.

Why this is always safe:

- **Zero-link:** a router phase references no downstream governed repo, so reverting it cannot break
  an external consumer's build (the consumer's kernel holds router-off — KI1).
- **Additive-within-v1 (CR4):** a phase only ADDS contract fields. Reverting removes fields the
  prior phase never used, so older data/proposals stay valid against the still-frozen v1 floor.
- **Proposal freeze (A0):** A0 froze `intent-proposal/v1` (`provisional → frozen`). Reverting the A0
  PR cleanly reverts the envelope freeze (status → `provisional`, `freeze_exempt: true`, `frozen:
  null`) and the four A0 machine-checks (`active → spec`). This is safe because the freeze only
  LOCKED the existing 11-key floor + recorded an additive OPTIONAL field (`catalog_version`) — it
  removed nothing, so a revert drops only the lock, never a required key.

## egress rollback (spans two repos)

egress is one deliverable across two PRs: the router side (this repo's `egress` branch PR — the PR
URL + pinned commit are in `status.yml`) and the AWA side (**[#26](https://github.com/KleinPerkins/awa/pull/26)**,
already merged to `KleinPerkins/awa` main). To roll egress back:

1. Revert the router egress PR: this flips the CR10 machine-check `egress_zero_banned_terms`
   `active → spec` and restores the `tests/test_deferred_spec.py::test_spec_egress_zero_banned_terms`
   placeholder to a skipped SPEC stub (plus the `CONSTITUTION.md` CR10 annotation back to `spec → egress`).
   Safe by construction: the flip added no contract field (`banned_terms`/tiers are unchanged — the
   `deferred_additions.egress` additive roadmap entry is untouched), so a revert removes only the
   status flip + the reference-test body, never a frozen key.
2. Optionally revert the AWA sibling PR #26 (removes the seven-surface egress test + `plain_*`
   renderers — all ADDITIVE to the AWA tree, so the kernel safety guarantee is unaffected: it holds
   router-off either way, KI1).
3. Flip `status.yml` `egress → pending`, clear its `passed_test_ids`/`pr`/`commit`, set
   `current_phase: egress`, and regenerate `RESUME.md`. `make status-verify` then recomputes to match disk.

Either revert alone leaves a coherent tree (the router revert is independently safe because nothing in
this repo links to the consumer). The egress flip is presentation/enforcement only — it changed no
routing, proposal, or kernel decision — so reverting it cannot alter any allow/refuse outcome.

## A0 rollback (spans two repos)

A0 is one deliverable across two PRs: the router side
(**[#4](https://github.com/KleinPerkins/intent-router/pull/4)**, `a0/proposal-freeze`, commit
`558500f`) and the AWA side (sibling PR in `KleinPerkins/awa`). To roll A0 back:

1. Revert the AWA sibling PR (removes the consumer catalog/loop/translators/consequence/golden/seam/
   contamination/off-switch surfaces — all additive to the AWA tree, so the kernel safety guarantee is
   unaffected: it holds router-off either way, KI1).
2. Revert the router PR #4 (flips `intent-proposal/v1` frozen → provisional and the four A0
   machine-checks active → spec, per the freeze bullet above).
3. Flip `status.yml` A0 → `pending`, clear its `passed_test_ids`/`pr`/`commit`, set
   `current_phase: A0`, and regenerate `RESUME.md`. `make status-verify` then recomputes to match disk.

Order matters only if you want each intermediate state green; either revert alone leaves a coherent
tree (the router revert is independently safe because nothing in this repo links to the consumer).

**Special case — a frozen contract.** `intent-catalog/v1`, `intent-map/v1`, `intent-feedback/v1`,
and the constitution contract are frozen in P0. Rolling back a LATER phase must never remove a v1
required key (that would be a breaking change, not a revert). A later phase only ever ADDED optional
keys / enum values; reverting drops exactly those additions, leaving the v1 floor intact. If a
revert would touch a v1 required key, STOP — that indicates the later phase illegally mutated the
floor and the fix is forward (a corrective PR), not a floor-breaking revert.

## State rollback (runtime data)

Router state is event-sourced under `${XDG_STATE_HOME:-~/.local/state}/intent-router/`:

- **Versioned snapshots:** `<consumer>/map.snapshots/<ts>.json`. Restore with `intent restore
  <snapshot>` (verb activates in R-resilience) — atomically replaces `map.json`.
- **Event-sourced rebuild:** `events.jsonl` is the truth. `intent rebuild` (R-resilience)
  deterministically reconstructs `map.json` from the full event log, so a corrupt/lost projection is
  always recoverable without data loss.
- **Corrupt store fallback:** if both the projection and snapshots are unusable, the router runs
  L0–L2 on the catalog alone → conservative proposals, and degrades to ask (CR6) — it never guesses a
  destructive action while degraded.
- **Uninstall preserves state by default option:** `./install.sh --uninstall --keep-state` retains
  the event log + snapshots for a later reinstall/rebuild.

## Genesis rollback

P0 landed as the `p0-durable-artifacts` PR on top of the genesis `main`. Reverting the P0 PR returns
the repo to the genesis skeleton (README/LICENSE/.gitignore/Makefile/pyproject/meta.yml) with no
durable artifacts — a clean, empty-of-design state.
