# intent-router

**intent-router turns a plain-language operator request into a _proposed_ action for a consumer
tool to run — it never runs anything itself.** A consumer (AWA is the first) hands the router an
utterance ("is everything okay?", "put this work somewhere safe"), the router matches it against
that consumer's own catalog of verbs, and returns a structured **proposal**: which verb, which
parameters, how confident, and whether the operator must confirm. The consumer's own kernel then
makes the real decision. **The router proposes; the kernel decides.**

> **Kernel-first (constitutional):** the consumer's safety guarantee holds with the router
> **OFF**. Uninstall intent-router and the consumer degrades to asking the operator + its own
> explicit path; the kernel still refuses, denies, and audits exactly as before. The router is
> never in the authorization chain and the kernel never reads a router artifact. See
> [`CONSTITUTION.md`](CONSTITUTION.md) and [`ARCHITECTURE.md`](ARCHITECTURE.md).

## Status — P0 (Architecture & Contracts Freeze)

This repository is at **phase P0**. What exists today is the **durable architecture**, not a
runtime:

- Full-system design of record — [`ARCHITECTURE.md`](ARCHITECTURE.md).
- Five versioned contracts under [`contracts/`](contracts/) with a behavior-only freeze checker.
- The [`CONSTITUTION.md`](CONSTITUTION.md) (numbered router rules + kernel invariants) and its
  machine-checkable contract.
- A machine-verified phase ledger — [`status.yml`](status.yml) + `make status-verify`.
- A single always-current resume pointer — [`RESUME.md`](RESUME.md) — and
  [`ROLLBACK.md`](ROLLBACK.md).
- Golden-set/test scaffolding (`tests/`), including an **additive-compatibility proof** that every
  deferred phase only ADDS to the v1 contracts.

**There is NO L0–L5 routing logic yet.** Every CLI/MCP verb is a thin *"not yet"* stub. The next
phase (`R-core`) builds the deterministic, executionless pipeline. Read [`RESUME.md`](RESUME.md)
for the exact next action.

## Requirements

- Python **3.9+** (standard library only — no third-party dependencies).

## Clone and install

```bash
git clone git@github.com:KleinPerkins/intent-router.git
cd intent-router
./install.sh            # idempotent, backup-before-write; installs into your XDG dirs
./install.sh --doctor   # read-only health check of the install
make verify             # test + contract freeze + status-verify + install --check
```

`install.sh` copies a self-contained runtime into `$XDG_DATA_HOME/intent-router/current`, writes a
config env (`$XDG_CONFIG_HOME/intent-router/env`), ensures the local-disk state dir
(`$XDG_STATE_HOME/intent-router`), and writes a self-describing release pointer. There is **no**
sibling-repo dependency — a fresh clone installs on its own. It wires **no** Cursor hooks and **no**
MCP server in P0 (hooks stay OFF until phase C1; the read-only MCP mirror lands with the runtime).

## Command surface (declared in P0; all verbs stub to "not yet")

The `intent` CLI surface is **declared** now so it is stable across the multi-session build, but no
verb does routing work in P0:

- **read-only (activated in `R-core`):** `map`, `explain`, `catalog-verify`, `doctor`
- **later phases:** `feedback`, `phrasebook {diff,review,apply}`, `calibrate`, `seed`, `snapshot`,
  `restore`, `rebuild`, `status`

There is **no mutating tool path by construction** — the router serializes proposals and never
executes a consumer verb.

## Layout

```
contracts/    the five FROZEN/PROVISIONAL versioned contracts (catalog, map, proposal, feedback, constitution)
checks/       the behavior-only contract-freeze checker (mirror of AWA's freeze pattern)
intent_router/  Python package (stdlib only): version, CLI "not-yet" stub, status-verify ledger gate
tests/        the executable architecture: contract-freeze, additive-proof, zero-link, status-verify, golden sets
bin/          the `intent` launcher shim
install.sh    Standalone System Package installer; bootstrap.sh = clone + install
ARCHITECTURE.md / CONSTITUTION.md / RESUME.md / ROLLBACK.md / status.yml   the durable artifacts
```

## Versioning & the frozen contracts

`intent_router/__init__.py:__version__` is the package version. The contracts in `contracts/`
freeze **behavior** (schema strings + required-key floors) and are **additive-within-v1**: a new
field is allowed, a removal/rename/retype is a breaking change. `intent-catalog/v1`,
`intent-map/v1`, `intent-feedback/v1`, and the constitution contract are **frozen** in P0;
`intent-proposal/v1` is **PROVISIONAL** (its envelope freeze is deferred to phase A0, which
exercises it against a real fixture — highest re-architecture risk).

## License

Proprietary — © KleinPerkins. All rights reserved. See [`LICENSE`](LICENSE).

## Continuous integration and governed delivery

Source CI defines six hosted Actions shards and the `ci-required` aggregate.
Run `python3 -I -B scripts/verify.py local` for source verification.

[The initial source admission](https://github.com/KleinPerkins/intent-router/pull/61)
contains the account-bound review and App delivery adapters. Ready PRs require
fresh independent review from their originating Codex account. The qualified
Chaos Scheduler App owns approval and native squash through the
[documented delivery process](docs/ci-delivery.md). Local verification does not
establish hosted CI, App activation, installation or product-release completion.
The retired PR controller is deprecated and must not resume. Product WIP stays held.
