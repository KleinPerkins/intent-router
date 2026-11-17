# Intent Router CI and delivery

This source prepares permanent standard hosted GitHub Actions for immutable
repository 1294651532, `KleinPerkins/intent-router`, default branch `main`.
The accepted amended G1 transition supersedes the old runnerless hosting restriction
for this target. Product phases, frozen contracts and held WIP remain separate.

The six nonempty shards in `.github/ci-contract.json` are closed and disjoint.
`contract` covers additive/frozen behavior, the constitution, executionless/zero-link
safety and the strict phase ledger. `routing` covers the deterministic floor and
golden set. `surfaces` covers CLI/MCP/doctor, synthetic state, egress, proposal
fixtures and a disposable HOME installation lifecycle. `ci-negative`, `local-review`
and `app-gate` execute the actual aggregate, account capture/PR creation and
trusted-main privileged App workflow/admission tests. The coverage test rejects
any missing, duplicate or newly unassigned `tests/test_*.py` module. Four existing
future-phase specification tests remain explicitly skipped; their phases are not
implemented by this CI change.

CI is unprivileged contents-read source on bounded `ubuntu-24.04` jobs with pinned
checkout, no stored checkout credentials and no secrets. Full source history is
needed by the existing strict ledger ancestry proof. Each job tests the exact
push revision or PR merge revision and verifies ordered base/head parents.
`ci-required` always runs and requires all six successful shard receipts bound to
the same repository, workflow, revision, run, attempt and PR tuple. Actions
producer 15368 supplies these checks. Local execution proves source behavior only.

The authoring agent automatically launches fresh independent originating-account
review before opening a ready PR and after any head, current base or trusted policy
change. Use the qualified same-account cloud route when available, otherwise the
qualified trusted local adapter. The operator does not initiate or perform technical
review. Capture the account around the trusted PR-creation operation, preserve its
separate origin record, and publish the actual unedited review receipt. Unknown
origin, unavailable matching runtime, incomplete/failed review and stale tuples
block delivery. See `local-review.md`, `pr-creation.md` and `github-delivery.md`.

Only Chaos Scheduler App4217367 may approve a head and request native squash
immediately for merge-ready PRs or native squash auto-merge for eligible blocked
PRs. Agents never merge or manipulate auto-merge. Trusted-main code validates fresh
review/origin evidence, complete exact CI, current merge parents, effective strict
checks/review/history/squash controls and installation identity before each write.

Initial publication remains gated by actual content/history/exposed-artifact
clearance. This initial source has policy disabled and no producers; repository
`REVIEWER_APP_ENABLED` stays OFF. Preserve current controls/preimages. Old
`.github/pr-*` files and required checks are historical bootstrap blockers only;
never restart or depend operationally on the retired controller. Exact owner/admin
initial PR-only admission is separate from automatic technical review. After it,
prove merged-main CI, independently admit qualified account enrollment, qualify
trusted-main App credentials and token cleanup with writes OFF, then complete the
root-owned successor-control cutover and actual App-only delivery proof. No local
success qualifies those platform gates. The source does not authorize visibility,
control, service, install, activation or held product changes.

Run `python3 -I -B scripts/verify.py local` for all six suites and repository gates.
`make verify` and `make status-verify` remain supported existing repository checks.
