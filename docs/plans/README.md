# Plans

This directory contains multi-session plans for `intent-router`.

**Governance:** `~/dev/_ops/doc-warden/POLICY.md` — see **Canonical records**,
**Lifecycle and prerequisites**, and **Reconciliation and egress**.
Plans are **byte-identical-forever** once their Status line reads `ACCEPTED` — no in-place edits
after approval. A revision is a new `{{slug}}-v2.md` with a `Supersedes:` pointer; the prior
version is never modified.

## Index

| Plan | Status | Date | Notes |
|---|---|---|---|
| [Roadmap Revision Step 1 Ground Truth v1](roadmap-revision-step-1-ground-truth-v1.md) | DRAFT | 2026-09-01 | Evidence journal; not an execution plan |
| [Roadmap Revision Step 2 Ecosystem and Learning v1](roadmap-revision-step-2-ecosystem-and-learning-v1.md) | DRAFT | 2026-09-02 | Ecosystem, fleet, learning, privacy, measurement, and roadmap-revision evidence; not an execution plan |
| [Roadmap Revision Step 3 Design v1](roadmap-revision-step-3-design-v1.md) | DRAFT | 2026-09-02 | Reviewed prior version replaced by v2 review candidate; retained byte-for-byte |
| [Roadmap Revision Step 3 Design v2](roadmap-revision-step-3-design-v2.md) | ACCEPTED | 2026-09-02 | Active design basis; hardened contract, privacy, dependency, and governance architecture |
| [G0-R0 Contract Freeze Hardening v1](g0-r0-contract-freeze-hardening-v1.md) | SUPERSEDED | 2026-09-02 | Superseded by v2; preserved byte-for-byte as historical input (SHA-256: `908f8915bf70c138df168a2ee0e46a1cabf4943f6baa31c970e62895aaaa2c97`) |
| [G0-R0 Contract Freeze Hardening v2](g0-r0-contract-freeze-hardening-v2.md) | ACCEPTED | 2026-09-02 | Accepted G0-R0 implementation basis; hardened successor incorporating 12 swarm review findings; implementation not yet authorized |

## Conventions

- Filename: `<slug>-vN.md` where `N` starts at `1`
- Status values: `DRAFT` → `ACCEPTED` → `SUPERSEDED` (tracked in the index row, NOT in the plan file itself after acceptance)
- A new version (`-v2`, `-v3`, …) is created when a material revision is needed post-acceptance; the prior version is immutable
- Draft plans may be edited in place before acceptance; accepted plans may not

## Archive

Superseded and retired plans that are no longer active but preserved for history live in
`docs/archive/plans/` (moved via `git mv`, not deleted).
