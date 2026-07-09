# intent-router — security model + verification ledger

> Authoritative security doc for intent-router. It records individually verifiable rows rather than a
> self-referential "posture verified sound" bless. Status legend: **Verified** (closed with a green
> test now) / **Spec** (the enforcing test is deferred to a named phase — honestly not yet closed).
>
> **P0 reality:** there is NO routing runtime yet. The dominant P0 security property is *structural*:
> the router surface is executionless and the whole capability is zero-link. Runtime rows (redaction,
> injection resistance, contamination) are specified with their enforcing test deferred to the phase
> that builds the behavior — never marked closed before then.

## Threat model

- **Assets.** The operator's machine + credentials; the consumer's repos; the integrity of the
  consumer's kernel decision (allow/refuse).
- **Adversaries.** (a) A poisoned data source — a repo/transcript/catalog example crafted to steer a
  proposal ("prompt injection"); (b) a corrupted or tampered router store; (c) anyone hoping the
  router can be coerced into executing or authorizing an action.
- **Core defense (kernel-first, KI1).** The router is NEVER in the authorization chain and never
  executes. The consumer's kernel makes the real decision and never reads a router artifact (KI2).
  Uninstalling the router degrades safely to ask (CR6). So the worst a compromised/poisoned router
  can do is propose a *wrong* action that the operator/kernel still gates — it cannot flip a refuse
  into an allow (KI3).

## Ledger

| ID | Assertion | Status | Evidence / close method |
|---|---|---|---|
| R1 | The router surface is **executionless** — no code path runs a consumer verb (CR1). | **Verified (P0)** | `tests/test_cli_stub.py::test_no_execution_path` greps the CLI surface for exec primitives (subprocess/os.system/exec/eval/popen) = 0; every declared verb returns the not-yet signal with no side effect. |
| R2 | The capability is **zero-link** — it names no downstream governed repo. | **Verified (P0)** | `tests/test_zero_link.py` scans the git surface that is/would be committed (`git ls-files --cached --others --exclude-standard`) against the forbidden-token list (mirrors the orchestrator's `zero-link --mode global`). |
| R3 | Contracts are **additive-within-v1**; accumulated learning stays replayable (feedback frozen before first write). | **Verified (P0)** | `checks/intent-contract-freeze.sh` + `tests/test_additive_compat.py`; `intent-feedback/v1` frozen in P0 (before any C0 event). |
| R4 | The status ledger **cannot lie** about what is built. | **Verified (P0)** | `intent_router/status_verify.py` recomputes every `done` claim against disk + by running the referenced tests; `tests/test_status_verify.py` proves a lying ledger fails. |
| R5 | Router **state is private + local-disk** (600 files / 700 dirs), never a shared repo or synced path (CR3). | **Spec → R-core** | `.gitignore` already blocks `.intent-router/`; the runtime path policy + the `state_is_private` test land with the store in R-core. |
| R6 | **Prompt-injection resistance:** repo/transcript/catalog content is DATA; it can never change a proposal's `safety_class` (CR5). | **Spec → R2** | `prompt_injection_data_not_instruction` machine-check; test lands with L3/L4. |
| R7 | **Destructive params confirm literally:** an LLM-inferred destructive param requires literal-value confirmation; deterministic extraction for destructive slots (CR9). | **Spec → R2** | catalog per-param `extractor`/`confirm_literal` (additive in R2) + `destructive_param_literal_confirm` test. |
| R8 | **Feedback log redaction:** no secret/PII persisted into the event log; consented/redacted seeding only. | **Spec → C1** | `redacted`/`consent_ref` fields (additive in C1) + a redaction pass at write time. |
| R9 | **Structural non-contamination:** the consumer kernel reads ZERO router artifacts (KI2); a confidence-1.0 proposal yields the identical kernel decision as the hand-typed equivalent (KI3). | **Spec → A0** | greppable kernel-read audit + the behavioral contamination test, in the consumer repo, pinning the router contract version. |
| R10 | Commit-time secret/identity safety is **reproducible for every clone**. | **Verified (P0)** | CI `.github/workflows/baseline.yml` runs `baseline-verify.sh` (committed-credential scan + minimal workflow permissions) on every push/PR; `make fix-hooks` installs the KleinPerkins local commit guards where the host overlay is present (see below). |

## Commit-time guards (intentional exception, documented)

The KleinPerkins standard local commit guards (identity-guard / data-guard / session-lock) are a
**machine-local developer aid** owned by the `KleinPerkins/dev` host overlay
(`~/dev/_ops/bin/install-identity-guard.sh`). They are **not vendored** into this standalone
capability on purpose:

- `.git/hooks` are per-clone and do **not** travel with the repo, so installing them into one clone
  is not a reproducible, portable guarantee for other contributors.
- Vendoring copies of the overlay's guard scripts would couple this generic, zero-link capability to
  one machine's layout and drift from the upstream source of truth.

Instead, the **durable, reproducible** commit safety for *every* clone and CI run is the committed
CI baseline (`.github/workflows/baseline.yml` → `baseline-verify.sh`: committed-credential-file scan
+ minimal workflow permissions) plus branch protection — which run regardless of any local setup.
For local defense-in-depth on a KleinPerkins/dev machine, run **`make fix-hooks`**; it installs the
overlay guards when present and otherwise prints a clear note and no-ops (never fails a fresh clone).

## Honest residuals (documented, not hidden)

- **The router is a proposer, not a sandbox.** Its safety value is that it CANNOT execute or
  authorize; correctness of a *proposal* is gated by the kernel + operator confirmation, not by the
  router being infallible.
- **Same-user data safety is detect-only downstream.** Anything the router proposes still runs
  through the consumer's kernel, whose own residuals apply (see the consumer's SECURITY.md). The
  router adds a fail-to-ask surface, not a new deletion-prevention guarantee.
- **P0 verifies structure, not runtime.** Rows R5–R9 are Spec: their enforcing tests are written by
  the phase that builds the behavior. They are intentionally NOT marked closed here.
