# AGENTS.md — intent-router

Agent entrypoint for `KleinPerkins/intent-router`. Read this, then `RESUME.md` (exact next action),
then `ARCHITECTURE.md` + `contracts/` + `CONSTITUTION.md` (locked design). Run `make verify` +
`make status-verify` before trusting any claim about what is built.

## What this repo is

A shared, global capability (`kind: tool`, Flavor-2 standalone-release) that turns an operator
utterance into a **proposed** consumer verb. **The router proposes; the consumer's kernel decides.**
AWA is the first consumer. Kernel-first: the consumer's safety holds with the router uninstalled.

## Hard invariants (do not violate)

- **Router proposes, never executes, never authorizes** (CR1/CR2). No execution path in the surface.
- **Kernel-first** (KI1): a consumer's `verify` must pass with the router uninstalled.
- **Zero-link:** name no downstream governed repo anywhere in the tree (`tests/test_zero_link.py`).
  Referencing the first consumer (AWA) is fine — AWA is a sibling capability, not a forbidden token.
- **Contracts additive-within-v1** (CR4): add fields, never remove/rename/retype. No v2 for this work.
- **Freeze timing:** `intent-catalog/v1`, `intent-map/v1`, `intent-feedback/v1`, and the constitution
  contract are FROZEN. `intent-proposal/v1` is PROVISIONAL — do NOT freeze it until A0 exercises it
  against a real fixture.
- **Ledger cannot lie:** `status.yml` is gated by `make status-verify`, which recomputes every `done`
  claim against disk + tests. Update the ledger honestly; deferred behavioral tests sit skipped with
  a "SPEC: future session <phase>" reason, never silently passing.

## Working here

- Do the design in `ARCHITECTURE.md`; do the numbered rules in `CONSTITUTION.md`
  (+ `contracts/intent-constitution.v1.json`). Reference rules by number (CR#, KI#).
- Each phase lands as its own PR; flip its `status.yml` entry to `done` with real `passed_test_ids`,
  regenerate `RESUME.md`, and record the rollback path. `make verify` is the repo gate.
- Do NOT create the `capabilities/skills/global/tools/intent-router` shelf pointer or WF1 enrollment
  until R-surface-complete (keeps P0 zero-link trivially clean).
- Repo mutations: this repo is not under `~/dev`, so the ~/dev worktree guard does not apply; still
  use branch + PR, never push to `main` directly.

## Phase ladder (see status.yml for live state)

P0 (done) → R-core → A0, with the consumer kernel-safety lanes (K0/K1/K2) in parallel; egress + R2
after A0; C0 → C1 (promotion gate); R-resilience; R-surface-complete; M0 (migration design-only).


<!-- doc-warden:begin -->
## Documentation governance

This repo's documentation structure is governed by `doc-warden`.

| Artifact type | Location |
|---|---|
| Plans | `docs/plans/` — index at `docs/plans/README.md` |
| ADRs | `docs/adr/` — index at `docs/adr/README.md` |
| Runbooks | `docs/runbooks/` |
| Glossary | `docs/GLOSSARY.md` (created when genuine terminology ambiguity arises) |

**Policy:** `~/dev/_ops/doc-warden/POLICY.md`
**Engine:** `~/dev/_ops/bin/doc-warden.sh check intent-router` (read-only health check)
<!-- doc-warden:end -->
