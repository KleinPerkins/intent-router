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
- **Provisional proposal:** until A0 freezes `intent-proposal/v1`, reverting A0 also reverts the
  envelope freeze cleanly (status → provisional).

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
