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
| [G0-R0 Contract Freeze Hardening v1](../archive/plans/g0-r0-contract-freeze-hardening-v1.md) | SUPERSEDED | 2026-09-02 | Archived; superseded by v2 (SHA-256: `908f8915bf70c138df168a2ee0e46a1cabf4943f6baa31c970e62895aaaa2c97`) |
| [G0-R0 Contract Freeze Hardening v2](../archive/plans/g0-r0-contract-freeze-hardening-v2.md) | SUPERSEDED | 2026-09-02 | Archived; superseded by v3 (SHA-256: `d417c5b26742816be4349a8b8a31331c67bfbab0517f232ef2a7846950b0c76b`) |
| [G0-R0 Contract Freeze Hardening v3](../archive/plans/g0-r0-contract-freeze-hardening-v3.md) | SUPERSEDED | 2026-09-02 | Archived; superseded by v4; doc-warden structural fix (SHA-256: `1fb88205edf418b404614790a48c820202f1191025379a3cad3589b62a7732ac`) |
| [G0-R0 Contract Freeze Hardening v4](g0-r0-contract-freeze-hardening-v4.md) | ACCEPTED | 2026-09-02 | Active G0-R0 implementation basis; doc-warden compliant successor to v3 (renamed §8 to `## Work items`, added `**Interfaces:**` blocks) |

## Conventions

- Filename: `<slug>-vN.md` where `N` starts at `1`
- Status values: `DRAFT` → `ACCEPTED` → `SUPERSEDED` (tracked in the index row, NOT in the plan file itself after acceptance)
- A new version (`-v2`, `-v3`, …) is created when a material revision is needed post-acceptance; the prior version is immutable
- Draft plans may be edited in place before acceptance; accepted plans may not

## Archive

Superseded and retired plans that are no longer active but preserved for history live in
`docs/archive/plans/` (moved via `git mv`, not deleted).
