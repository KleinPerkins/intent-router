# Intent-router roadmap revision — Step 3 design v1

**Status:** DRAFT — 2026-09-02  
**Plan-type:** standard  
**Purpose:** Reviewable revised architecture and roadmap design. This is not an ADR, authoritative
architecture, execution plan, or implementation authorization.

## PM overview

### What exists today

Intent-router already has a small, reliable safety floor:

- deterministic request normalization, catalog matching, verdicts, and proposals;
- frozen additive-within-v1 contracts;
- an executionless CLI and read-only MCP process surface;
- machine-local state-path guards and a Flavor-2 install lifecycle;
- AWA as the first implemented consumer, with its own kernel retaining consequence, confirmation,
  execution, outcome verification, and router-off behavior; and
- runnerless verification, contract freeze, status-ledger recomputation, zero-link, and operator
  egress checks.

P0, R-core, A0 implementation, and egress remain completed history. A0 has not yet earned its
separate human proof: the real-PM trial has not been recorded.

### Why revise the roadmap

The original roadmap jumps from one-consumer deterministic routing to a monolithic smart phase,
then calibration, resilience, and global surfaces. It does not yet define:

- how multiple consumers register without leaking host identities into this global capability;
- who owns each verb, kernel, catalog, and cross-repository prerequisite;
- how smart ranking learns without entering the safety or authorization path;
- how private raw history expires and derived evidence remains auditable;
- how quality is measured across a changing fleet without a global count hiding weak mappings; or
- how the second consumer completes source change, merge observation, sanctioned synchronization,
  and downstream convergence as one operator outcome.

### Operator value

The revised design lets an operator ask naturally for one atomic outcome and receive a trustworthy
proposal, while the responsible product still decides and executes. It creates a repeatable way to
add consumers, improves ambiguous-language matching, makes learning inspectable, and prevents new
or under-evidenced mappings from silently becoming automatic.

### What remains locked

- Router proposes only; it never executes or authorizes (CR1/CR2).
- Consumer kernels own real consequences, confirmation, allow/refuse, execution, and verification.
- Kernel safety holds with the router absent or off (KI1–KI4).
- Contracts remain additive within v1; no required key is removed, renamed, or retyped (CR4).
- Catalog, transcript, and repository content are data, never instructions (CR5).
- Degraded, drifted, or unresolved routing asks rather than guesses (CR6).
- Reviewable C0 precedes any C1 automation; destructive near-miss remains exactly zero (CR7).
- No learned or LLM component participates in safety classification, authorization, consequence,
  confirmation, or destructive-parameter authority (CR9).
- PM-facing output remains jargon-free and honestly qualified (CR10).
- State remains machine-local/private, no paid runners are introduced, and zero-link is preserved.

## Design status and evidence language

This document uses four labels:

- **Verified current:** observed on disk, in tests, or in the Step 1/Step 2 evidence.
- **Accepted design:** explicitly decided by the operator and binding on later design.
- **Proposed v1 addition:** field-level design for optional/additive implementation; not frozen or
  implemented by this document.
- **Future evidence gate:** a measured condition that must be met before activation or promotion.

Authoritative files remain unchanged until this draft is accepted. `ARCHITECTURE.md`,
`CONSTITUTION.md`, contracts, `status.yml`, `RESUME.md`, `SECURITY.md`, and `ROLLBACK.md` continue to
govern the current product.

## Accepted decisions

1. **Completion and proof are separate.** A phase may be implementation-complete while human or
   production proof remains pending. Proof is earned per phase, never as one product-wide badge.
2. **Controlled parallelism.** A0 implementation remains done. The A0 PM trial runs against a frozen
   A0 baseline while smart-layer work proceeds separately. A0 evidence proves only A0; every later
   phase has its own baseline, evidence, and operator gate.
3. **Bounded smart ranking.** The first smart layer reranks only deterministic non-zero candidates
   for ambiguous requests. It cannot add a candidate, change safety metadata, authorize, or execute.
   Invalid output, timeout, provider failure, or off mode returns to the deterministic result.
4. **Typed learning evidence.** Operator corrections and attributable system outcomes are stored
   separately and reviewably. Neither timelessly outranks the other. Unresolved or destructive
   disagreement asks; it never self-resolves through an opaque model.
5. **Mandatory bounded raw history.** Exact requests are retained machine-locally/private under CR3
   for a rolling 90 days. There is no opt-in/out mode and no indefinite retention. Deterministic
   expiry is mandatory. Derived/non-raw evidence may live longer under its own finite policy.
6. **Host-owned fleet authority.** This repository ships neutral schemas and validation. The host
   control plane owns repository identities, fleet membership, rollout state, and exact pins.
   Independent PR, documentation, and synchronization authorities remain separate.
7. **Narrow first automation.** C1 may affect only exact qualified read-only mappings. Writes and
   destructive actions remain review suggestions.
8. **Evidence horizon and early exit.** Initial C0 assessment runs through day 45, with cumulative
   checkpoints every fifth day. Objective sufficiency can trigger a formal assessment early; an
   agent recommends and the operator decides. If day 45 is insufficient, extension length comes
   from measured deficits and collection rates, rounded to an aligned fifth-day checkpoint.
9. **Quality target.** Approximately 300 independent strong proposals with zero false-strong
   observations is the proposed roughly 1% one-sided statistical risk target, not current
   performance. C0 establishes the review-burden limit. Destructive near-miss remains exactly zero.
10. **Learning continues.** Closing the initial window does not stop evidence collection,
    observation, resolver/model maintenance, drift checks, replay, or future recalibration.

## Lean end-state architecture

### Components and authority

| Component | Owns | Must not own |
|---|---|---|
| Neutral router SSP | Contract schemas, registration validation, deterministic candidate generation, optional bounded reranking, proposal serialization, private evidence processing, replay, snapshots, health | Host repository roster, consumer execution, authorization, consequences, confirmation |
| Consumer package | Atomic operation registry, kernel, catalog or catalog projection, parameters, live consequence, confirmation, execution, outcome verification, egress vocabulary, consumer proofs | Router ranking policy, another consumer's verbs, host fleet membership |
| Host fleet control plane | Stable repository identity, consumer enrollment, desired mode, approved digests, exact router release, prerequisite declarations, rollout cohort, cross-fleet report | Consumer execution semantics, router-private evidence, mutation of independent fleets |
| Router-private state | Raw request store, typed evidence log, derived intent map, replay labels, snapshots, receipts, metrics | Shared source control, remote raw storage, credentials, authorization decisions |
| Independent delivery authorities | PR verification/delivery, documentation governance, capability synchronization | Intent ranking, automatic intent enrollment, cross-authority mutation |
| Operator surfaces | Plain proposal/explanation/status, review suggestions, exact promotion/rollback decisions | Hidden execution or reusable approval |

The host control plane is outside this repository. This repository contains no host fleet roster or
downstream governed-repository identity. Neutral records use opaque IDs and bounded relative paths.

### Request path

1. Hear the operator's exact words.
2. Resolve the host-qualified consumer universe; if unavailable, use an explicitly supplied
   consumer catalog or degrade to ask.
3. Validate exact registration/catalog digests and effective mode.
4. Generate deterministic non-zero `(consumer, verb)` candidates from active and shadow consumers.
5. Apply deterministic verdict rules and collision checks.
6. For an ambiguous eligible set only, optionally rerank those same candidates.
7. Validate reranker output against the deterministic set and immutable safety metadata.
8. Return a proposal or ask. Shadow output is recorded but cannot affect the returned proposal.
9. The selected consumer adapter submits the operator's request to its own kernel.
10. The kernel independently computes consequence, confirmation, authorization, execution, and
    verified outcome.
11. Record operator and system evidence as separate typed observations.

## Proposed additive v1 records

These shapes are design inputs for later ADR/contract work. They do not modify frozen contracts.

### Router-owned neutral registration schema

Proposed schema: `intent-consumer-registration/v1`.

| Field | Type | Meaning |
|---|---|---|
| `schema` | constant string | `intent-consumer-registration/v1` |
| `version` | integer | Record version; starts at `1` |
| `consumer_id` | bounded string | Stable neutral consumer identifier |
| `repository_key` | UUID string | Opaque stable identity; no repository name |
| `registration_revision` | integer | Monotonic consumer-authored revision |
| `catalog.path` | relative path | Consumer-owned `intent-catalog/v1` |
| `catalog.digest` | SHA-256 string | Exact catalog bytes approved by consumer |
| `catalog.source` | enum | `authored` or `generated` |
| `operation_registry.path` | relative path | Consumer's semantic operation authority |
| `operation_registry.digest` | SHA-256 string | Exact operation registry bytes |
| `kernel_proofs.path` | relative path | Consumer-owned proof manifest |
| `kernel_proofs.digest` | SHA-256 string | Exact proof manifest |
| `egress.path` | relative path | Consumer egress terms/contract |
| `egress.digest` | SHA-256 string | Exact egress bytes |
| `contracts` | object | Compatible catalog/proposal/feedback schema strings |
| `selection.label` | bounded string | Plain consumer label for collisions/clarification |
| `selection.aliases` | bounded string array | Reviewed consumer-level aliases |
| `tests.router_off` | test-ID array | Consumer verification with router absent |
| `tests.kernel_contamination` | test-ID array | Kernel reads no router artifacts |
| `tests.catalog_parity` | test-ID array | Every routable verb maps to one kernel operation |
| `tests.outcome` | test-ID array | Real outcome verification |
| `deprecated` | boolean | Consumer is no longer eligible for new activation |
| `superseded_by` | string or null | Successor consumer registration |

Validation rejects absolute/escaping/symlinked paths, executable content, unknown contract major
versions, duplicate consumer IDs, unsafe catalog paths, missing proof classes, and digest mismatch.
It does not execute the named tests; runnerless consumer verification does.

### Consumer-owned records

The consumer repository owns:

- `.intent-router/consumer.json`, validating against the neutral registration schema;
- `intent-catalog/v1`, authored directly or generated deterministically from one operation registry;
- the operation registry and kernel implementation;
- a proof manifest containing exact test IDs and expected runnerless check names;
- golden cases and consumer egress terms; and
- deprecation/successor meaning.

If an operation registry already exists, the catalog is a deterministic projection. The repository
must not maintain two editable semantic authorities.

### Host-owned fleet record

Proposed host schema: `intent-fleet/v1`, owned and stored outside this repository.

| Field | Type | Meaning |
|---|---|---|
| `schema` | constant string | `intent-fleet/v1` |
| `repository_key` | UUID string | Stable host repository identity |
| `consumer_id` | string | Joins neutral registration |
| `registration_path` | relative path | Consumer record location |
| `registration_digest` | SHA-256 string | Approved exact registration |
| `catalog_digest` | SHA-256 string | Approved exact catalog |
| `operation_registry_digest` | SHA-256 string | Approved kernel operation authority |
| `proof_manifest_digest` | SHA-256 string | Approved proof set |
| `egress_digest` | SHA-256 string | Approved egress contract |
| `router_release` | immutable release ID | Exact router bytes used for qualification |
| `desired_mode` | enum | `off`, `shadow`, `active`, or `retired` |
| `cohort_id` | string or null | Rollout/evidence cohort |
| `prerequisites` | typed array | Independent authority and required state/check |
| `approved_at` | timestamp | Host approval time |
| `retired_at` | timestamp or null | Retirement time |
| `superseded_by` | string or null | Successor consumer ID |

No command, prompt, credential, raw request, or arbitrary executable value is allowed.

### Qualification and effective mode

Desired lifecycle mode and computed qualification are separate:

- `qualified`: all exact digests, release, proof receipts, and prerequisites match;
- `drifted`: previously qualified bytes or prerequisites changed;
- `unavailable`: registration or required authority cannot be read/verified;
- `under_evidenced`: structurally qualified mapping lacks its activation/promotion evidence.

Effective behavior is computed in this order:

1. `retired` is off and cannot be locally re-enabled.
2. A local exact `off` narrows any host mode.
3. `drifted` or `unavailable` degrades that consumer to ask.
4. `shadow` records proposals/evidence but cannot affect output.
5. `active + qualified` permits deterministic routing.
6. C1 automatic learning affects only exact `active + qualified + evidence-qualified` read-only
   mappings; `under_evidenced` mappings remain deterministic/shadow/ask.

There is no local `on` override that can defeat retirement, host off, failed prerequisites, or
qualification.

### Additive proposal metadata

The frozen eleven required `intent-proposal/v1` keys remain unchanged. Proposed optional additions:

| Field | Type | Purpose |
|---|---|---|
| `catalog_version` | string | Existing deferred addition; identifies consumer catalog revision |
| `registration_digest` | SHA-256 string | Binds the consumer registration |
| `catalog_digest` | SHA-256 string | Binds exact catalog bytes |
| `behavior_version` | string | Binds deterministic/rerank behavior |
| `candidate_set_digest` | SHA-256 string | Binds pre-rerank candidates |
| `rerank_source` | enum | Existing deferred addition: `deterministic` or `llm` |
| `rerank_revision` | string or null | Exact provider/model/config revision |
| `confidence_basis` | enum | `deterministic_match_strength`, `reranked_match_strength`, or `calibrated_probability` |
| `fallback_reason` | enum or null | `off`, `timeout`, `provider_error`, `invalid_output`, `drift`, or `none_eligible` |

The existing `confidence` number remains for v1 compatibility. Until calibration is proven,
operator surfaces label it **match strength**, never correctness probability. No consequence
descriptor enters the proposal.

### Typed evidence and correlation additions

The frozen required `intent-feedback/v1` floor remains unchanged. Proposed optional keys:

| Field | Type | Purpose |
|---|---|---|
| `event_id` | UUID string | Stable event identity |
| `raw_event_id` | UUID string | Reference to private raw record |
| `evidence_type` | enum | `operator_intent`, `operator_correction`, `factual_observation`, `system_outcome`, `hypothesis`, `preference` |
| `label_state` | enum | `accepted`, `corrected`, `rejected`, `clarified`, `aborted`, `abstained`, `unresolved` |
| `correlation_id` | UUID string | Joins proposal, kernel request, outcome, and review |
| `episode_id` | UUID string | Groups correlated retries/review events |
| `target_verb` | string or null | Corrected/confirmed verb |
| `registration_digest` | SHA-256 string | Exact registration |
| `catalog_digest` | SHA-256 string | Exact catalog |
| `policy_version` | string | Evidence/arbitration policy |
| `behavior_version` | string | Deterministic/rerank behavior |
| `model_revision` | string or null | Exact smart provider revision |
| `context_digest` | SHA-256 string | Bounded non-raw context identity |
| `independence_key` | SHA-256 string | Deduplicates correlated evidence |
| `supersedes_event_id` | UUID string or null | Explicit evidence correction/reversal |
| `attribution` | enum | `operator`, `consumer_kernel`, `system_observer`, or `agent_review` |

Add `abstain` only as an additive `operator_choice` enum extension if implementation requires it.
Do not repurpose an existing value. The frozen required `utterance` string carries a deterministic
non-raw normalized/redacted projection; exact wording lives only in the raw record referenced by
`raw_event_id`. The already-declared optional `consent_ref`, if retained, applies only to separately
governed historical import provenance and never gates live raw capture.

### Raw store and retention policy

Proposed private raw record:

| Field | Type | Purpose |
|---|---|---|
| `event_id` | UUID string | Joins typed evidence |
| `captured_at` | UTC timestamp | Retention start |
| `expires_at` | UTC timestamp | Exactly `captured_at + 90 days` |
| `consumer_id` | string | Scope |
| `utterance` | string | Exact raw request |
| `content_digest` | SHA-256 string | Integrity and receipt binding |

The store is a regular mode-0600 file beneath the guarded XDG state root; parent directories are
0700. Raw text never enters source control, host fleet records, dashboards, PRs, shared logs,
snapshots, remote services, or model-training exports.

Expiry runs:

- before/after append, at startup, and through a dedicated state-maintenance operation; `doctor`
  reports lifecycle state but does not mutate it;
- idempotently, deleting all records with `expires_at <= effective_now`;
- with aggregate receipt counts, oldest retained timestamp, expired backlog, and pre/post digest;
- under tests for exact boundary, restart, partial failure, clock regression, and interrupted write.

Normal scheduled expiry is lifecycle enforcement, not an operator-triggered destructive action. An
explicit purge before expiry is a separate kernel-owned destructive operation with exact scope,
literal confirmation, receipt, and irreversibility narration. Backups and snapshots may not extend
raw retention.

Derived evidence uses a separate finite policy proposed at 365 rolling days. This provides drift and
recalibration history without indefinite accumulation; Step 3 acceptance approves it as a design
default, while later evidence may justify a new forward-only policy. Expiry never rewrites frozen
historical receipts.

### Snapshots and receipts

Proposed snapshot manifest:

| Field | Type |
|---|---|
| `snapshot_id` | UUID string |
| `created_at`, `expires_at` | UTC timestamps |
| `consumer_id` or `fleet` | bounded scope |
| `through_event_id` | UUID string |
| `event_log_digest`, `map_digest` | SHA-256 strings |
| `behavior_version`, `policy_version` | strings |
| `registration_digests`, `catalog_digests` | sorted maps |
| `raw_included` | constant `false` |

Proposed private-state receipt:

| Field | Type |
|---|---|
| `operation_id` | UUID string |
| `action` | `append`, `expire`, `rebuild`, `snapshot`, `restore`, `promote`, `reverse`, or `purge` |
| `scope` | bounded consumer/cohort identifier |
| `requested_at`, `completed_at` | UTC timestamps |
| `pre_digest`, `post_digest` | SHA-256 strings or null |
| `affected_count` | integer |
| `status` | `applied`, `noop`, `refused`, or `failed` |
| `reason` | closed enum |
| `policy_version` | string |

Receipts contain no raw text. Retention receipts are routine lifecycle records; early-purge receipts
also bind the exact operator confirmation.

### CLI and MCP mutation taxonomy

Every router verb declares two independent properties:

- `executes_consumer=false` for every router command; and
- `mutates_router_state=true|false` according to its actual private-state behavior.

Mapping, explanation, catalog verification, and doctor are non-mutating. Append, expire/maintain,
snapshot, restore, rebuild, promote, reverse, and purge mutate router-private state. The read-only
MCP mirror exposes only non-mutating commands. This removes the current incorrect implication that
router-private writes would execute a consumer.

### Deprecation and retirement

- New registrations start `off`.
- Deprecation prevents new activation but keeps current exact mappings available until migration.
- Retirement sets host mode `retired`, disables routing, preserves a non-raw tombstone and receipts,
  and cannot be overridden locally.
- Frozen v1 catalog entries are marked with additive `deprecated:true` and optional
  `superseded_by`; they are not silently removed.
- A successor is separately registered, qualified, shadowed, and activated before the predecessor
  retires.

## Fleet behavior and lifecycle

### Fleet-wide selection

- Flatten exact active/shadow registrations into `(consumer, verb)` candidates.
- Run each catalog through the same deterministic normalization/scoring floor.
- A bounded reranker receives only non-zero deterministic candidates and inert request data.
- The reranker returns candidate IDs/scores only. Schema validation rejects added IDs, changed
  safety metadata, parameter invention, or instructions.
- A clear winner may be proposed; close cross-consumer or same-label collisions become weak and ask
  the operator to choose a plain consumer/outcome.
- No composite verb is invented. One request produces one proposed atomic consumer verb.
- Missing parameters remain missing; smart ranking does not fill destructive parameters.

### Router-off, failure, and drift

- Router absent/off: consumer degrades to ask and offers its plain explicit outcomes.
- Smart provider off/failing/late/invalid: return the deterministic proposal.
- Host roster unavailable: explicitly supplied consumer catalog may use the current single-consumer
  path; global routing asks.
- Registration/catalog/proof digest drift: only that consumer asks; other qualified consumers
  continue.
- Corrupt evidence/map: routing uses catalog-only deterministic behavior; automatic learning is off.
- Independent prerequisite failure: block only the dependent mapping and report which authority is
  missing; never repair another fleet automatically.

### Onboarding

1. Consumer implements one atomic kernel operation and router-absent behavior.
2. Consumer authors or generates catalog, registration, egress terms, goldens, and proof manifest.
3. Consumer verification proves paths, schema, catalog-to-operation parity, contamination, outcome,
   and egress.
4. Host adds exact registration/digests in `off`.
5. Independent prerequisite checks report without mutating their authorities.
6. Host moves exact qualified bytes to `shadow`.
7. Evidence and safety gates are reviewed.
8. Operator activates exact deterministic mapping/cohort.
9. C1 promotion, if ever eligible, is a separate exact read-only mapping decision.

### Updating a verb or consumer

- Kernel semantics land first or atomically with catalog/proof changes.
- Host digest mismatch immediately removes qualification.
- Updated bytes re-enter shadow; unaffected mappings remain active.
- Material catalog/policy/model/behavior change resets promotion evidence only for affected mappings.
- Prior evidence stays auditable under its exact versions.

### Cross-fleet conformance

A read-only host report joins by stable repository identity:

- intent registration, mode, qualification, and exact digests;
- required PR-delivery state;
- required documentation-governance state;
- required synchronization state;
- installed router release and router-off proof.

Each fleet remains independently authoritative. Missing conformance blocks the dependent intent
mapping only. The report never enrolls, repairs, or configures another fleet.

## Smart and evidence lifecycle

### Deterministic floor

The current L0–L2+L5 path remains valid by itself and is the fallback at every phase. Safety class,
tool path, confirmation requirement, and destructive parameters remain catalog/kernel/literal
derived. Deterministic goldens run with all smart components disabled.

### Shadow reranking

- Eligible only when deterministic candidates are non-zero and ambiguous.
- Receives bounded candidate labels/descriptions and inert request content.
- Cannot see credentials, raw history beyond the current request, kernel disposition, or
  authorization state.
- Runs with timeout, circuit breaker, schema validation, and exact provider/config revision.
- Shadow compares deterministic and reranked proposals but returns deterministic output.

### Selective activation

- Activate only after phase-specific shadow evidence and rollback proof.
- Start with exact qualified read-only mappings.
- Below evidence-backed confidence/selective-risk threshold, ask.
- Any safety metadata disagreement discards smart output.
- Last-good behavior/config remains atomically restorable.

### Typed arbitration

Evidence is partitioned by consumer, normalized intent, registration/catalog/policy/model/behavior
versions, context, and time. Operator correction and attributable system outcome remain separate:

- system success does not prove intent correctness;
- direct factual evidence may overturn a factual hypothesis but does not rewrite prior intent;
- correlated retries count once;
- unresolved/destructive disagreement asks;
- old evidence does not silently cross material version boundaries; and
- an expiring operator lock reopens review rather than flipping a mapping.

No automatic half-life is selected until each evidence stratum has sufficient reversals and
observation time. A future deterministic weight may use quality, independence, and a learned
per-stratum half-life; it is not an opaque adjudication model.

### Replay and frozen labels

- Freeze label revisions before evaluation.
- Group chronological splits by session and utterance family.
- Bind replay to exact registration, catalog, behavior, model, and policy revisions.
- Exclude unresolved labels from quality numerators while reporting their coverage.
- Rebuild derived maps deterministically from typed non-raw evidence.
- A golden regression, replay mismatch, or label-provenance gap aborts promotion.

### Forty-five-day sufficiency protocol

At days 5, 10, and every fifth day through 45, produce cumulative and latest-increment reports.
Time alone never proves sufficiency.

The formal exit gates are:

1. **Quality/safety:** at least 300 independent strong proposals and zero false-strong for the exact
   cohort; zero destructive near-miss across the registered universe.
2. **Mapping depth:** at least 30 independent strong proposals per promoted read-only
   `(consumer, verb, exact versions)` mapping.
3. **Family coverage:** every utterance family representing at least 5% of eligible traffic for a
   promoted mapping has at least 10 independent labeled proposals.
4. **Independence:** at most one countable strong proposal per three-hour episode for the same
   session, consumer, verb, target, and utterance family.
5. **Label quality:** every counted proposal has frozen disposition/provenance/versions; at least
   90% of all eligible cohort proposals have a usable final label.
6. **Representativeness:** use the complete eligible stream, list every registered consumer,
   mapping, family, risk class, abstention, exclusion, and unknown.
7. **Stability/burden:** current and prior fifth-day checkpoints have no new material
   under-covered mapping/family, false-strong, or destructive near-miss; review/clarification burden
   is no worse than the frozen deterministic baseline overall or per promoted mapping.

Every registered consumer appears in reporting. Promotion covers only the exact mappings that pass;
new, changed, and under-evidenced mappings remain shadow/ask and neither block nor silently join the
cohort.

When gates pass, the agent writes a formal assessment of depth, breadth, diversity,
representativeness, independence, label/outcome quality, safety, and review burden. The agent
recommends exit or continuation; the operator decides.

At day 45, calculate each countable deficit and divide by its independent-evidence rate over the
latest 15 days. Use the longest estimate, rounded up to the next fifth-day checkpoint with a
five-day minimum. A zero rate yields no invented date: narrow the proposed cohort or repair
collection. Safety, label, or representativeness failures require remediation and fresh affected
evidence, not waiting.

After exit, collection and fifth-day launch cadence may stop, but normal continuous evidence,
observation, maintenance, drift surveillance, replay, and scheduled recalibration continue.

### Promotion, reversal, and rollback

- Promotion is exact-cohort and operation-bound; no global C1 switch activates every mapping.
- Operator approval binds cohort/version digests and the formal assessment.
- Writes/destructive mappings remain review-only regardless of global evidence.
- Any false-strong, destructive near-miss, digest drift, label-integrity failure, or burden breach
  immediately returns affected mappings to shadow/ask.
- Reversal restores last-good behavior atomically and preserves evidence/receipts.
- Re-entry requires remediation plus fresh affected-mapping evidence; unaffected mappings continue.

## Worked second consumer: `refresh_model_tiers`

### Atomic proposal

- Consumer: subagent orchestration
- Verb: `refresh_model_tiers`
- Parameters inferred from wording: none
- Safety: write/shared consequence, determined live by the consumer kernel
- Router role: propose the verb only

### Trust and execution path

1. Router validates the exact Skills-side registration/catalog and proposes
   `refresh_model_tiers`.
2. Consumer adapter enters the Skills-owned kernel; the router cannot call source-control,
   verification, PR, or synchronization operations.
3. A Cursor-side observer captures the current subagent model enum, timestamp, Cursor version, and
   observation digest from the live tool schema. Ordinary CI cannot independently obtain this enum,
   so the observation is an explicit trust boundary, not presumed truth.
4. The kernel checks observation freshness and compares it with the source catalog, checker, and
   tests. No change returns `noop`.
5. A safe worktree updates exactly the model catalog, checker, and checker tests in lockstep.
6. Consumer verification checks enum membership, unavailable/superseded slugs, no inherited
   placeholder, tier completeness, cross-provider fallback, freshness, sibling-asset installation,
   and the full Skills gate.
7. The consumer delivers a governed PR through runnerless verification. It does not bypass checks,
   directly merge, or arm merge automation.
8. The kernel observes the exact source head merged to the live default branch.
9. It requests synchronization through the independent sanctioned authority; neither router nor
   consumer writes the downstream edge directly.
10. It verifies the downstream governed copy carries the expected source/catalog digest.
11. Only then does the operator outcome become `converged`.

### Idempotent staged receipts

One operation ID advances monotonically through:

`observed → source_ready → pr_open → merged → sync_requested → converged`

Each receipt binds observation digest, source pre/post digest, exact PR head, merged commit,
synchronization request ID, downstream digest, and timestamp. Retries resume the last verified
stage. Changed inputs refuse or create a new operation; duplicate PRs/sync requests are not opened.

The local daily freshness monitor remains an alarm/backstop. It does not own live enum observation,
source change, PR delivery, synchronization, or convergence.

## Verification, observability, and operations

### Runnerless verification ownership

| Owner | Required gate |
|---|---|
| Router repository | Canonical `make verify`, `make status-verify`, install verification, contract freeze, zero-link, no-execution, raw lifecycle, replay/fallback, and schema tests |
| Consumer repository | Full consumer verification with router absent plus exact-release seam, catalog/operation parity, consequences, outcome, and egress |
| Host control plane | Fleet schema/digest validation, prerequisite read-only conformance, rollout/qualification projection |
| Model-tier consumer | Live observation fixture validation plus complete Skills source/install checks |
| Independent synchronization authority | Source-to-downstream exact digest and convergence verification |

The verifier App owns the exact-head check. The reviewer App alone may arm native merge automation
under its policy. Agents do not bypass checks or pre-arm merge. No GitHub-hosted or self-hosted paid
runner is introduced.

### Operator observability

One plain dashboard/status projection shows:

- all registered consumers and exact lifecycle/qualification state;
- deterministic versus shadow/live rerank counts and fallback reasons;
- accepted/corrected/rejected/clarified/aborted/abstained outcomes;
- per-consumer/verb/family depth, label coverage, independence, and representation;
- false-strong, selective risk/coverage, review burden, conflicts/reversals, and outcome attribution;
- destructive near-miss as an absolute count;
- raw oldest/next-expiry/expired-backlog counts without raw content;
- drift, provider health, replay, snapshot, rollback, and prerequisite state; and
- checkpoint gate status, deficits, collection rates, extension estimate, and exact promotable
  cohort.

No bare green status is enough. Output states what was checked, what is unknown, and whether a
mapping is deterministic, shadow, active, under-evidenced, or degraded.

### Privacy and security

- Private state paths are XDG-rooted, regular, owned by the user, 0700 directories/0600 files, with
  no symlink or special-file writable component.
- Raw requests expire at 90 days even if replay, snapshot, uninstall, restore, or provider features
  fail. Privacy lifecycle is not disabled by feature rollback.
- Derived evidence has its own finite policy and no raw text.
- Model input is bounded to the current request and deterministic candidates; historic raw records
  are not silently sent to a provider. Raw retention never implies permission for provider egress;
  any provider deployment must have its own reviewed data-handling policy.
- Secrets/credentials are never fleet fields, proposal metadata, receipts, metrics, or dashboard
  output.
- Content is data; injection text cannot change candidate identity, safety class, confirmation, or
  kernel behavior.
- The router is a proposer, not a sandbox. Consumer/kernel residual risk remains independently
  governed.

## Complete revised phase ladder

Every implementation phase lands independently and records its own proof. “Rollback” below means a
governed revert/disable to the last-good phase plus honest ledger/resume regeneration; frozen v1
required floors are never removed.

### Preserved completed history

| Phase | Goal and delivered production step | Acceptance/proof | Dependencies, rollback, operator gate |
|---|---|---|---|
| P0 — durable floor | Frozen contracts, constitution, zero-link, status ledger, declared lifecycle | Existing recomputable tests and merged evidence remain | Genesis dependency; revert only through governed PR; no new gate |
| R-core — deterministic router | L0–L2+L5 engine, functional proposal/explain/verify/doctor and read-only MCP process | Existing goldens, contract, no-execution, state, CLI/MCP checks | P0; revert R-core PR; deterministic floor remains historical boundary |
| A0 — first-consumer implementation | Frozen proposal envelope, AWA catalog/loop/seam/kernel-first reference proof | Existing router and consumer implementation tests; implementation `done` | R-core; revert paired changes independently; human proof remains A0-P |
| egress — operator output contract | Shared/consumer egress checks and plain honest output | Existing active CR10 reference tests | A0; revert presentation enforcement without changing kernel outcome |

### Near term

| Phase | Goal and concrete deliverables | Acceptance/proof | Dependencies, rollback, operator gate |
|---|---|---|---|
| G0 — authority honesty | Reconcile authoritative docs/ledger, exact merged egress state, canonical runnerless recipes/seams, release provenance, freeze-check completeness, CLI state-mutation taxonomy | All claims recompute; canonical router/consumer gates exact; no history rewritten | Current completed floor; revert G0 PR; operator accepts reconciled authorities |
| A0-P — frozen human proof | Freeze A0 release/catalog/behavior and record sanitized real-PM trial evidence | PM completes trial; evidence names exact baseline and only A0 claims | G0 baseline; runs in controlled parallel; no code rollback, proof remains pending until passed; operator signs A0 proof |
| F0 — neutral fleet substrate | Neutral registration schema/validator, host-record interface, qualification/effective-mode rules, fleet-wide deterministic candidate projection | Schema bite tests, zero-link, collision/ask, local narrowing, drift isolation, router-off | G0; parallel wave; disable global selection to current single-consumer path; operator accepts host interface |
| S0 — evidence/privacy foundation | Typed evidence/correlation, mandatory 90-day raw store/expiry, finite derived policy, receipts, replay labels, snapshots excluding raw, universe reporting | Boundary/restart/clock/privacy tests, deterministic rebuild, raw expiry cannot be bypassed | G0; parallel wave; disable evidence learning while keeping active expiry; operator accepts privacy proof |
| R2a — bounded semantic shadow | Candidate-only reranker, timeout/circuit breaker, schema validation, injection isolation, deterministic fallback, match-strength egress | Shadow cannot affect product; smart off/failure exact deterministic replay; zero safety metadata change | G0 + deterministic candidates; parallel wave; switch provider off; no activation gate yet |
| C0 — reviewable evidence | Manual phrasebook/review suggestions, fifth-day reports, objective gates, deficit extension, complete-universe coverage | Checkpoint protocol reproducible; labels frozen; no automatic mapping change | F0 + S0; R2a may remain shadow; operator decides any early window exit |
| A1 — AWA maturation | Exact router release pin, persistent typed feedback, production-surface truth, exact runnerless seam | Router-present and router-absent full gates, PM proof attribution, no stale mutable pin | A0-P + F0/S0; return AWA mapping to deterministic/ask; operator accepts AWA qualification |
| R-resilience-a — smart safety | Timeout/circuit breaker, last-good behavior, corruption fallback, provider and state health | Fault injection proves deterministic/ask fallback and atomic rollback | R2a + S0; provider off/last-good restore; no live gate |
| R2b — selective live reranking | Exact read-only cohort activation using selective prediction | Its own shadow evidence, golden/replay parity, checkpoint quality/safety/burden gates | C0 + resilience-a; affected cohort back to shadow; operator binds exact cohort activation |
| R2c — typed parameters | Deterministic low-risk resolvers; learned extraction only where later justified; destructive values literal/confirmed | Per-field fixtures, missing-param honesty, CR9 proofs, smart-off equivalence | R2b; disable resolver and return missing params; operator gate for any learned field class |

### Medium term

| Phase | Goal and concrete deliverables | Acceptance/proof | Dependencies, rollback, operator gate |
|---|---|---|---|
| R-resilience-b — recovery | Behavior hashes, event rebuild, snapshots/restores, drift/re-heal, richer doctor | Corruption/rebuild/restore tests; raw never enters snapshot; expiry survives restore | S0 + resilience-a; restore last-good non-raw snapshot or catalog-only mode |
| R-surface-a — production surfaces | Complete CLI, read-only MCP, thin rule/skill, honest production wiring classification | Surface tests distinguish declared, compatible, and live; CLI metadata separates consumer execution from router-state mutation | Resilience-b; remove optional surfaces without changing library/kernel safety |
| R-surface-complete — release | Immutable release, global binding, lifecycle enrollment, host overlay handoff | Install/check/repair/uninstall, zero-link parity, exact provenance | Surface-a; revert binding/enrollment, preserve state/expiry; operator release gate |
| F1 — host fleet activation | Activate host control plane and manage AWA through exact registration/digests | Host projection, prerequisite report, drift/local-off/retire tests | Surface-complete + A1; host mode off and single-consumer fallback; operator enrolls AWA |
| B0 — second consumer | Deliver `refresh_model_tiers` from proposal through converged downstream state | Live enum trust receipt, full source gate, exact merge, idempotent sync, downstream digest | F1 + independent delivery/sync; retire mapping/cancel before shared mutation; operator approves consequential stages |
| O0 — fleet observability | Plain dashboard/status, checkpoint deficits, privacy/drift/provider/rollback state | No raw leakage; all registered consumers visible; unknowns explicit | F1 + S0/C0; projection can be rebuilt/disabled |
| C1 — automatic calibration | Activate exact evidence-qualified read-only mappings only | Accepted ~300/zero target plus per-mapping/family/label/stability/burden gates; zero destructive near-miss | C0 + O0 + R2b; exact cohort back to shadow and last-good map; operator promotion gate |
| M0 — migration design/dry run | Adapters, deprecation, retirement, tombstones, rollback inventory; no automatic migration | Dry-run receipts, no authority duplication, every source/target/rollback named | F1/B0/C1; discard dry-run projections; operator approves any later migration |
| W1 — STRONG rollout | Onboard qualified local-job repair and low-risk PR operation one atomic verb at a time | Each kernel-first, router-off, exact evidence, prerequisite, and egress gate | F1/O0; per-mapping off/retire; operator enrollment and activation |

### Long term

| Phase | Goal and concrete deliverables | Acceptance/proof | Dependencies, rollback, operator gate |
|---|---|---|---|
| S2 — discovery intelligence | Local clustering of none/clarify/correction cases into review suggestions | No automatic catalog mutation, privacy bounded, suggestion precision reported | C1 + sufficient evidence; disable clustering and retain deterministic routing |
| W2 — SOLID rollout | Add qualified documentation, capability, synchronization, and private-context verbs | Per-consumer kernel and exact cohort evidence; consequential actions remain kernel-gated | W1 + independent authorities; per-mapping retire; operator gates each enrollment |
| S3 — supervised routing, conditional | Replace/augment reranking only if direct labels and learning curves prove durable value | Chronological holdout beats simpler baseline by accepted margin without safety/burden regression | S2 + adequate labels; revert to bounded reranker; operator model-promotion gate |

## G0 source-of-truth reconciliation matrix

This draft does not edit these authorities. After acceptance, G0 makes one reviewed honesty change
set with the following intended corrections.

| Authority | Current contradiction/staleness | Exact intended correction |
|---|---|---|
| `README.md` | Presents P0 and all commands as stubs; proposal as provisional | State verified completed floor and functional commands; proposal frozen in A0; point current work to G0/controlled parallel roadmap |
| `RESUME.md` | Says egress router PR is open; gives monolithic L3+L4 R2 as exact next action; uses product-wide “proven” language | Record egress merged; separate A0 implementation from A0-P proof; identify G0 then A0-P/F0/S0/R2a controlled parallel work; remove automatic L4 scope |
| `status.yml` | A0 title includes trial while `done`; R2 entry says A0 proven; K lanes stale; monolithic pending phases | Preserve completed IDs/commits; add phase-specific proof state/A0-P; split pending phases; make first pending router phase G0; reconcile K rows only to exact consumer evidence |
| `ARCHITECTURE.md` | Treats broad L3/L4 as one R2 build; lacks fleet authority, mandatory retention, typed evidence, moving-universe and checkpoint design; `confidence` reads as confidence | Adopt bounded candidate-only reranking, deterministic-first parameters, host/consumer/router boundaries, 90-day raw lifecycle, typed stores, match-strength semantics, and exact promotion cohorts |
| `CONSTITUTION.md` and constitution contract | Locked rules are sound; phase annotations/activation plan reflect old monolith | Preserve rule meaning and frozen required floor; update only phase references/machine-check status through additive reviewed changes |
| Contract JSON and additive manifest | Frozen floors omit new optional metadata; deferred additions reflect old R2/C1 grouping | Add only accepted optional keys/enum extensions after schema review; strengthen freeze tests for optional frozen fields; never remove/retype |
| `SECURITY.md` | P0/no-runtime framing and several Spec rows are stale; cites a native workflow despite runnerless policy; lacks raw expiry/provider/evidence threats | Recompute each row against current tests; document runnerless checks, provider isolation, raw 90-day lifecycle, snapshot exclusion, typed evidence and residuals |
| `ROLLBACK.md` | Calls phase revert “always safe”; egress text assumes open PR; event log described as full truth without raw-expiry split | Record merged egress commit, external-consumer-aware rollback, exact cohort shadow reversal, non-raw event truth plus expiring raw sidecar, and privacy lifecycle surviving rollback |
| `.github/pr-automation.json` and lock | Router job does not run complete canonical verification | Make runnerless recipe execute canonical router/status/install gates; regenerate lock under its authority |
| Consumer runnerless recipe/seam | Does not run the full canonical consumer plus exact co-installed router seam | Consumer-owned change runs router-absent full verify and exact-release present seam; no mutable branch proof |
| Release pointer/install evidence | Pointer provenance lags matching installed bytes | Reissue/reinstall exact immutable release and verify source/contracts/package digests |
| AWA trial/egress/pin prose | Stale action counts, open/spec/native-job claims, mutable pin language | Correct to live catalog/surface counts, merged state, runnerless seam, frozen A0 baseline, and exact release pin |
| Host control-plane records | No intent fleet authority exists | Add host-owned roster/schema instance only after neutral interface acceptance; keep identities outside this repository |

G0 does not retroactively rename completed phases or fabricate proof. It records observed history,
adds future phase records, and separates implementation status from phase-specific evidence.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Smart output appears authoritative | Candidate-only schema, deterministic fallback, match-strength copy, consumer kernel independence |
| Global count hides weak mappings | Exact cohort plus per-mapping, material-family, label, independence, representation, and stability gates |
| Fleet growth continually resets promotion | Report all consumers; new/changed mappings remain shadow/ask and do not block qualified cohorts |
| Raw history accumulates or leaks | Mandatory 90-day deterministic expiry, private path, no raw snapshots/dashboard/remote storage, receipts |
| Derived evidence becomes indefinite | Separate finite policy, expiry receipts, forward-only policy changes |
| Correlated retries inflate evidence | Three-hour episode independence key and complete-stream reporting |
| Operator/system conflict flips intent | Typed evidence, version/context partitions, review suggestions, ask on unresolved/destructive cases |
| Host authority collapses into router | Neutral registration here; roster and identities in host control plane |
| Independent fleet is silently mutated | Read-only conformance; missing prerequisite blocks only dependent mapping |
| Live model enum is treated as ordinary CI truth | Explicit Cursor observation receipt, freshness/version digest, kernel validation |
| Source merge is mistaken for end-to-end success | Staged receipts and downstream convergence proof |
| Rollback disables privacy enforcement | Raw expiry remains active whenever retained records exist |
| Review burden overwhelms operator | C0 measures baseline; C1 cannot worsen it per mapping or overall |

## Non-goals

- No execution or authorization in the router.
- No model in safety, consequence, confirmation, or destructive-parameter authority.
- No online learning, reinforcement learning, autonomous weight update before C1, or opaque
  adjudication model.
- No vector database until a demonstrated scale/quality need; none exists now.
- No remote raw-request store or automatic historical export.
- No autonomous catalog, consumer, host fleet, PR, documentation, or synchronization mutation.
- No composite verbs or generic arbitrary-command routing.
- No paid Actions runners or bypass of runnerless verifier/reviewer ownership.
- No v2 contract by default and no removal/rename/retype inside v1.
- No global “proven” state and no time-only evidence sufficiency.

## Migration and deprecation strategy

M0 remains design/dry-run only:

1. inventory existing operation registries/catalog-like surfaces;
2. identify one semantic authority per consumer;
3. generate adapters/projections without changing current behavior;
4. validate exact digests and router-off behavior;
5. shadow successor registrations;
6. migrate one exact mapping only after operator approval;
7. retain non-raw tombstones/receipts and rollback path;
8. mark predecessor deprecated, then retired; and
9. remove adapters only after no active host reference remains.

No bulk migration, silent enrollment, or automatic retirement occurs.

## Smallest future implementation-plan bodies

Create these detailed plans only after this design is accepted:

1. **G0 authority honesty and verification hardening** — reconcile the matrix, canonical runnerless
   gates/seams, provenance, freeze coverage, and CLI taxonomy.
2. **A0-P real-PM proof** — freeze baseline, run trial, retain sanitized phase-specific evidence.
3. **F0 neutral fleet substrate** — registration validator, host interface, qualification,
   deterministic fleet selection, collision/drift/off behavior.
4. **S0 evidence/privacy foundation** — typed log/correlation, 90-day raw expiry, finite derived
   policy, receipts, replay, snapshots, and all-universe reporting.
5. **R2a bounded semantic shadow** — candidate-only provider boundary, injection isolation,
   deterministic fallback, and shadow evaluation.
6. **C0 checkpoint and reviewable calibration** — phrasebook review, frozen labels, fifth-day
   reports, exit/extension assessment.
7. **A1 AWA maturation** — exact pin, persistent evidence, truthful production surfaces and
   runnerless seam.
8. **R-resilience-a smart safety** — timeout/circuit breaker, corruption fallback, provider health,
   and last-good rollback.
9. **R2b selective live reranking** — one exact read-only cohort and its activation/rollback gate.
10. **R2c typed parameters** — deterministic resolvers first; any learned low-risk field separately
    justified.
11. **R-resilience-b recovery** — event rebuild, snapshots/restore, behavior hashes, drift/re-heal.
12. **R-surface-a production surfaces** — complete CLI/MCP/rule/skill and truthful wiring states.
13. **R-surface-complete release** — immutable release, global binding, enrollment, host handoff.
14. **F1 host fleet activation** — host roster/projection and AWA managed enrollment.
15. **B0 model-tier consumer** — live observation through exact downstream convergence.
16. **O0 fleet observability** — private-safe dashboard, deficits, drift, and qualification.
17. **C1 exact read-only cohort promotion** — created only when formal evidence exists.
18. **M0 migration dry run** — adapters, deprecation, retirement, receipts, and rollback inventory.
19. **W1 first qualified candidate wave** — one atomic consumer verb at a time after fleet proof.
20. **S2/W2/S3 conditional long-term plans** — created separately only when each entry gate has real
    evidence; no speculative implementation plan now.

Each implementation body remains one discrete production step and one governed PR unless its owning
authority requires a separate repository PR. Cross-repository outcomes use linked exact receipts,
not one mixed commit.

## Acceptance checkpoint

Accepting this draft means:

- its accepted decisions and architecture become the basis for authoritative reconciliation;
- G0 may create the first detailed execution plan and reviewed authority changes;
- completed history remains unchanged;
- no smart activation, fleet enrollment, release, migration, C1 promotion, or external mutation is
  authorized by acceptance alone; and
- each later operator gate remains required.

No genuinely far-reaching unresolved design choice was found. The next decision is:

> **Accept, revise, or reject this Step 3 design draft as the basis for G0 planning and authoritative
> reconciliation.**

