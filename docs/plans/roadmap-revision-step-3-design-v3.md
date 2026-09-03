# Intent-router roadmap revision — Step 3 design v3

**Status:** ACCEPTED — 2026-09-03  
**Plan-type:** standard  
**Supersedes:** `docs/plans/roadmap-revision-step-3-design-v2.md`  
**Purpose:** Record the accepted hardened architecture and roadmap design that governs later
authority-owned reconciliation and implementation planning. This is not an ADR, execution plan, or
implementation authorization.

## PM overview

### Current built floor

Intent-router already has a reliable deterministic base:

- request normalization, catalog matching, verdicts, and schema-shaped proposals;
- frozen additive-within-v1 contracts;
- executionless CLI and read-only MCP process surfaces;
- machine-local path guards and a Flavor-2 install lifecycle;
- AWA as the first implemented consumer, whose kernel still owns consequence, confirmation,
  allow/refuse, execution, outcome verification, and router-off behavior; and
- runnerless verification, contract freeze, zero-link, ledger recomputation, and egress checks.

P0, R-core, A0 implementation, and egress remain completed history. A0 human proof remains
separate: its real-PM trial has not yet been recorded.

### Why the roadmap changes

The old roadmap moves too quickly from one-consumer deterministic routing into a combined smart
phase. It does not yet provide a safe, repeatable answer for:

- registering multiple consumers without putting host identities in this global capability;
- proving exact catalog/kernel/runnerless compatibility across versions;
- letting semantic ranking improve ambiguous requests without entering safety or authorization;
- retaining mandatory private raw history while reliably deleting it after 90 days;
- collecting typed, non-reconstructable longer-lived evidence;
- measuring a moving fleet without allowing one global count to hide weak mappings; or
- completing the second consumer's source PR, exact merge, sanctioned synchronization, and
  downstream convergence as one operator outcome.

### Operator value

The operator can ask naturally for one atomic outcome. The router proposes the best reviewed
consumer verb; that consumer still decides and executes. New consumers enter through one governed
registration lifecycle, ambiguous requests improve behind deterministic fallback, private evidence
remains inspectable, and no under-evidenced mapping silently becomes automatic.

### Locked boundaries

- Router proposes only; it never executes or authorizes (CR1/CR2).
- Consumer kernels remain independent and safe with the router absent/off (KI1–KI4).
- V1 evolves additively: no required removal, rename, or retype (CR4).
- Catalog, request, transcript, and repository content are data, never instructions (CR5).
- Drift, ambiguity, or failure degrades to deterministic behavior or ask (CR6).
- C0 remains reviewable before C1; destructive near-miss is always zero (CR7).
- No model participates in safety class, consequence, confirmation, authorization, or destructive
  parameter authority (CR9).
- PM egress remains plain and honestly qualified (CR10).
- State stays machine-local/private. No paid runners, remote raw storage, autonomous
  cross-authority mutation, or global shelf/enrollment before surface completion.

## Status language

- **Verified current:** observed on disk/tests or recorded in the Step 1/Step 2 evidence journals.
- **Accepted design:** operator-decided and binding on later authoritative reconciliation.
- **Accepted v3 correction:** new v3 meaning accepted with this document.
- **Proposed v1 addition:** field-level additive design; not implemented or frozen here.
- **Future gate:** evidence or delivery required before activation/promotion.

This accepted v3 supersedes `docs/plans/roadmap-revision-step-3-design-v2.md` as the active design
basis. V2 remains byte-identical history. The current built-state authorities remain
`ARCHITECTURE.md`, `CONSTITUTION.md`, contracts, `status.yml`, `RESUME.md`, `SECURITY.md`, and
`ROLLBACK.md` until later authority-owned reconciliation lands.

## Accepted v2 decisions carried into v3

1. A phase can be implementation-complete while its proof remains pending. Proof is phase-specific,
   never one product-wide badge.
2. A0's PM trial runs against a frozen A0 baseline while A0-P, F0, S0, and R2a engineering/shadow
   work proceeds in controlled parallel. Evidence never crosses phase boundaries silently.
3. The first smart layer reranks only deterministic non-zero candidates for ambiguous requests.
   It cannot add candidates, alter safety metadata, authorize, or execute; every failure returns to
   deterministic behavior.
4. Operator corrections and attributable system outcomes are separate, typed, reviewable evidence.
   Neither timelessly outranks the other.
5. Exact raw requests are mandatory machine-local/private history for a rolling 90 days. There is
   no opt-in/out or indefinite retention. Derived evidence begins with the same 90-day finite
   baseline and may be extended only forward, by class, after measured need and explicit operator
   approval.
6. Fleet authority is host-owned. This repository ships neutral schemas/validation only.
   Independent PR, documentation, synchronization, and consumer authorities remain separate.
7. Initial C1 can affect exact qualified read-only mappings only. Writes and destructive actions
   remain review suggestions.
8. C0 starts with a 45-day horizon and fifth-day checkpoints. Objective sufficiency can trigger a
   formal assessment early; the agent recommends and the operator decides. Day-45 extension is
   calculated from measured deficits/rates, never an automatic 60/90-day wait.
9. Approximately 300 independent strong proposals with zero false-strong observations is the
   proposed roughly 1% one-sided statistical risk target, not current performance. C0 derives the
   burden limit. Destructive near-miss remains exactly zero.
10. Closing the initial window does not stop evidence, maintenance, drift checks, resolver/model
    observation, replay, or future recalibration.

### Accepted v3 correction

11. G0-V is a separate verification-authority child. It owns the noexec-compatible local-gate
    prerequisite, host command qualification, protected recipe-only delivery, and generated
    lock-only delivery as separate owner/repository/receipt boundaries. Final G0-R reconciliation
    starts only after G0-V and G0-C-AWA receipts exist; it records those receipts and leaves
    composite G0 in progress for a separate operator acceptance gate.

## Lean end-state architecture

### Authority map

| Component | Owns | Cannot own |
|---|---|---|
| Neutral router SSP | Frozen/additive schemas, registration validation, deterministic candidates, optional bounded reranking, proposal serialization, private State Controller, replay primitives, health | Host roster/identity, consumer execution, authorization, consequences, confirmation |
| Consumer package | Atomic operation registry, kernel, catalog/projection, parameters, live consequences, confirmation, execution, outcome, egress, consumer proofs | Router ranking policy, host membership, another consumer's verbs |
| Host fleet control plane | Repository identity, fleet membership, desired mode, exact registration digest, approved pins, prerequisites, rollout cohort, read-only conformance | Consumer semantics, router-private mutation/evidence, other fleet mutation |
| Router-private State Controller | Authorized raw/typed append, expiry/maintain, and later snapshot/restore/rebuild/promote/reverse/purge operations; receipts | Proposal ranking, consumer/kernel mutation, host authority |
| Independent authorities | PR verification/delivery, documentation governance, synchronization | Intent ranking/enrollment or mutation of each other |
| Operator surfaces | Plain proposal/explanation/status and exact review/promotion/reversal decisions | Hidden execution, reusable approval, raw content egress |

This repository contains no host roster or repository identity. The host joins a neutral
`consumer_id` to exact registration bytes. Consumer and host records cannot write router-private
state; only the State Controller can.

### Proposal path versus state path

**Proposal path**

1. Hear the exact request.
2. Resolve exact host-qualified registrations; before F1, only an explicitly supplied
   single-consumer catalog is active.
3. Validate registration/catalog digests and effective mode.
4. Generate deterministic `(consumer, verb)` candidates.
5. Apply collision/verdict rules.
6. In R2a, optionally shadow-rerank the same candidates only after provider entry gates pass.
7. Validate returned candidate IDs and immutable metadata.
8. Before F1, always return deterministic output. After F1/R2b, only an exact qualified read-only
   cohort may use a live reranked result.
9. Consumer kernel independently handles consequence, confirmation, authorization, execution, and
   verified outcome.

**State path**

1. An exact operator-authorized router-state verb or routine retention trigger enters the State
   Controller.
2. The controller validates root, ownership, operation identity, policy, preconditions, and current
   nondecreasing effective time.
3. It mutates only router-private state atomically.
4. It emits a non-raw receipt.
5. Proposal code, consumer kernels, host records, and independent authorities cannot call storage
   primitives directly.

Routine policy expiry needs no operator confirmation. An early purge is a separate destructive
State Controller verb with exact scope and literal confirmation.

## Contract hardening before additions

### Blocking G0-R0 freeze sub-gate

Before, or atomically with, any newly authoritative v1 optional field/enum:

1. lock every accepted optional field name→type mapping already present in frozen contracts;
2. lock current enum floors;
3. add negative tests that removal, rename, retype, narrowing, or enum-member removal fails;
4. begin with the verified `intent-feedback/v1` optional `correction` gap;
5. prove old fixtures/readers still parse;
6. run fresh `make verify` and `make status-verify`; and
7. record one exact G0-R0 receipt in the final router-owned G0-R PR, after the separately owned
   G0-V and G0-C-AWA receipts required by composite G0 exist.

No new typed writer, registration authority, or proposal metadata becomes authoritative until this
sub-gate passes. Additive-manifest phase labels may be updated only while preserving the meaning of
all existing passed tests; no completed proof is rewritten.

### Same-v1 compatibility rules

For every new v1 schema:

- `schema` and `version` constants are required.
- The required-key floor is immutable after first authoritative use.
- Adding/removing/retyping a required key requires v2.
- Optional fields may be added within v1.
- Readers ignore and preserve unknown optional top-level fields; unknown fields never affect
  routing, qualification, safety, or authorization.
- Writers emit only fields their schema revision declares.
- Closed safety-sensitive nested objects reject unknown members/enum values.
- Defaults apply only to absent optional fields and never synthesize missing required data.
- Instance revision is data revision, not schema version.
- Rollback readers tolerate unknown optional fields produced by newer writers.

## Proposed records and compatibility profiles

### Router-owned neutral registration v1

Schema constant: `intent-consumer-registration/v1`; `version: 1`.

The consumer-authored record intentionally contains no `repository_key`.

**Required floor**

| Field | Type |
|---|---|
| `schema` | constant `intent-consumer-registration/v1` |
| `version` | constant integer `1` |
| `consumer_id` | bounded stable string |
| `registration_revision` | positive integer instance revision |
| `catalog` | closed object: relative `path`, SHA-256 `digest`, `source`=`authored|generated` |
| `operation_registry` | closed object: relative `path`, SHA-256 `digest` |
| `kernel_proofs` | closed object: relative `path`, SHA-256 `digest` |
| `egress` | closed object: relative `path`, SHA-256 `digest` |
| `contracts` | closed object: catalog/proposal/feedback schema strings |
| `selection` | closed object with required plain `label` |
| `tests` | closed object with required non-empty `router_off`, `kernel_contamination`, `catalog_parity`, `outcome` test-ID arrays |

**Optional floor/defaults**

| Field | Type | Default |
|---|---|---|
| `selection.aliases` | bounded unique string array | `[]` |
| `deprecated` | boolean | `false` |
| `superseded_by` | consumer ID or null | `null` |
| `extensions` | object of namespaced optional values | `{}` |

`registration_revision` changes whenever authored registration meaning changes. It does not change
schema compatibility. Unknown optional top-level/extensions fields are ignored/preserved under the
same-v1 rule. Required-key addition/removal/retype is v2.

Validation rejects absolute/escaping/symlinked paths, executable values, duplicate consumer IDs,
unknown contract majors, bad digests, missing proof classes, and unsafe catalog/egress content.
Runnerless consumer verification—not the neutral parser—executes test IDs.

### Consumer-owned records

The consumer owns:

- `.intent-router/consumer.json`;
- its authored catalog or deterministic catalog projection;
- one semantic operation registry and kernel;
- proof manifest, goldens, outcome checks, and egress terms; and
- deprecation/successor meaning.

When an operation registry already exists, the catalog is generated; two editable semantic
authorities are forbidden.

### Host-owned fleet v1

Schema constant: `intent-fleet/v1`; `version: 1`. It is stored outside this repository.

**Required floor**

| Field | Type |
|---|---|
| `schema` | constant `intent-fleet/v1` |
| `version` | constant integer `1` |
| `repository_key` | host-owned UUID |
| `consumer_id` | exact neutral consumer ID |
| `registration_path` | bounded relative path |
| `registration_digest` | SHA-256 registration bytes |
| `catalog_digest` | SHA-256 catalog bytes |
| `operation_registry_digest` | SHA-256 operation authority |
| `proof_manifest_digest` | SHA-256 proof manifest |
| `egress_digest` | SHA-256 egress bytes |
| `router_release` | immutable release ID |
| `desired_mode` | `off|shadow|active|retired` |
| `approved_at` | UTC timestamp |
| `prerequisites` | closed typed array of authority/check/revision |

**Optional floor/defaults**

| Field | Type | Default |
|---|---|---|
| `cohort_id` | string or null | `null` |
| `retired_at` | UTC timestamp or null | `null` |
| `superseded_by` | consumer ID or null | `null` |
| `extensions` | namespaced object | `{}` |

Unknown optional fields are ignored/preserved. Unknown required/safety semantics cannot qualify.
Required-key evolution needs v2. No command, prompt, credential, raw request, or executable value
is allowed.

The host is the sole repository-identity authority. It joins `consumer_id` plus exact
`registration_digest`; no consumer-authored repository identity or onboarding cycle exists.

### Qualification and effective mode

Computed qualification:

- `qualified`: exact release/digests/proof receipts/prerequisites match;
- `drifted`: previously qualified bytes or prerequisite revision changed;
- `unavailable`: required record/authority cannot be read or verified;
- `under_evidenced`: structurally qualified mapping lacks activation/promotion evidence.

Effective order:

1. `retired` is off and cannot be locally enabled.
2. Local exact `off` narrows any host mode.
3. `drifted|unavailable` asks for that consumer.
4. `shadow` records comparison/evidence but cannot affect output.
5. Before F1, smart behavior is always shadow; supplied single-consumer routing stays deterministic.
6. After F1, `active+qualified` permits fleet deterministic routing.
7. After R2b, only exact `active+qualified+evidence-qualified` read-only mappings may use live
   reranking.

There is no local `on` override.

### Proposal-v1 optional additions and skew profile

The frozen eleven-key required floor stays unchanged.

**Optional fields**

| Field | Type | Default/absence |
|---|---|---|
| `catalog_version` | string | legacy unknown |
| `registration_digest` | SHA-256 string | not fleet-bound |
| `catalog_digest` | SHA-256 string | not fleet-bound |
| `behavior_version` | string | legacy deterministic |
| `candidate_set_digest` | SHA-256 string | no rerank provenance |
| `rerank_source` | `deterministic|llm` | `deterministic` |
| `rerank_revision` | string | absent |
| `provider_profile_digest` | SHA-256 string | absent |
| `redaction_profile_digest` | SHA-256 string | absent |
| `confidence_basis` | `deterministic_match_strength|reranked_match_strength|calibrated_probability` | `deterministic_match_strength` |
| `fallback_reason` | closed enum or null | `null` |

**Skew matrix**

| Writer → reader | Required behavior |
|---|---|
| New writer → old reader | Old reader ignores unknown optional fields; required floor remains valid |
| Old writer → new reader | New reader accepts absence as legacy deterministic proposal |
| Legacy proposal in explicit supplied single-consumer path | Remains valid deterministic input |
| Proposal missing/mismatching `registration_digest`, `catalog_digest`, or `behavior_version` in fleet path | Cannot qualify for active fleet use; degrade that mapping to ask/shadow |
| `rerank_source=llm` | Requires coherent group: candidate-set, rerank revision, provider profile, redaction profile, registration/catalog/behavior digests |
| Any coherent-group member present without valid group | Discard smart provenance/result and use deterministic fallback |

The existing `confidence` remains unchanged. Until calibrated, operator output calls it **match
strength**. No kernel consequence enters the proposal.

### Feedback-v1 legacy and typed profiles

Existing valid records remain parseable and replayable. They are **legacy**: without typed
provenance/version/independence fields they cannot count toward promotion or evidence qualification.
Rollback readers ignore unknown optional fields.

Typed records use optional discriminator `evidence_profile: "typed/v1"`.

**Typed common conditional group**

`event_id`, `raw_event_id`, `evidence_type`, `label_state`, `correlation_id`, `episode_id`,
`registration_digest`, `catalog_digest`, `policy_version`, `behavior_version`, `context_class`,
`independence_key`, and `attribution`.

Conditional requirements:

- `operator_correction` requires `target_verb` and `supersedes_event_id` when correcting a prior
  event.
- `system_outcome` requires `outcome_observer`, `outcome_revision`, and a correlation to the
  consumer kernel request.
- `model_revision` is required only when smart ranking participated.
- `label_state=abstained` uses `operator_choice=none`; it does **not** add enum value `abstain`.
- `unresolved` cannot count toward promotion.

Compatibility note: the current frozen enum observed on disk does not yet include `none`. G0-R0
must lock the current floor first; then reader support for additive `none` must land before any
writer emits a typed abstention. Until then, abstention is recorded in a non-promotable typed
observation outside the frozen feedback writer. No writer-first enum expansion is allowed.

The frozen required `utterance` value in longer-lived feedback is the constant content-free marker
`[raw-in-private-store]`, never normalized/free-form text. Exact wording lives only in the raw
store. Longer-lived evidence may contain only closed structured features proven by
PII/secret/non-reconstruction tests.

`raw_event_id` remains after expiry only as a non-dereferenceable tombstone. No raw content digest,
hash, embedding, token sketch, or commitment survives expiry.

The existing optional `consent_ref`, if retained, refers only to separately governed historical
import provenance; it never gates live capture.

## Router-private State Controller

### Boundary and verb semantics

All router-private mutation enters one controller outside the proposal path:

| Verb | Trigger/authorization | Semantics | First implementation phase |
|---|---|---|---|
| `append` | Router event trigger | Atomically append raw+typed event after expiry preflight | S0 |
| `expire` / `maintain` | Routine policy | Advance effective time; delete expired raw/derived classes | S0 |
| `snapshot` | Exact operator/state operation | Create non-raw projection snapshot | R-resilience-b |
| `restore` | Exact operator/state operation | Restore non-raw snapshot, then enforce current retention | R-resilience-b |
| `rebuild` | Exact operator/state operation | Deterministically rebuild projections from typed evidence | R-resilience-b |
| `promote` | Exact operator evidence decision | Activate exact read-only cohort manifest | C1 |
| `reverse` | Exact operator or hard gate | Restore exact last-good cohort behavior | R2b/C1 |
| `purge` | Literal-confirmed destructive operator verb | Delete in-scope unexpired raw early | S0 |

Every command declares `executes_consumer=false` and truthful
`mutates_router_state=true|false`. Map/explain/catalog-verify/doctor remain non-mutating; read-only
MCP exposes only non-mutating commands. Consumer kernels/host records cannot call controller
storage primitives.

### Raw record

| Field | Type |
|---|---|
| `event_id` | UUID |
| `captured_at` | UTC timestamp |
| `expires_at` | exactly captured time + 90 days |
| `consumer_id` | bounded string |
| `utterance` | exact request |

No persistent raw content digest is stored.

### Normative expiry state machine

Persist controller metadata:

- `time_high_water`: nondecreasing UTC timestamp;
- `retention_epoch`: monotonic integer;
- `state`: `healthy|quarantined`;
- `last_successful_expiry_at`;
- `oldest_retained_at`;
- `policy_version`.

For every raw read, append, provider call, startup, and maintenance:

1. validate state root/ownership and load metadata atomically;
2. compute `effective_now = max(time_high_water, trusted_wall_clock)`;
3. persist advanced high-water before raw access;
4. identify records with `expires_at <= effective_now`;
5. atomically replace the raw store without expired records;
6. persist retention epoch/status and non-raw receipt; then
7. allow the requested raw access/append/provider call.

Clock regression never moves the high-water backward. Interruption before replacement leaves the
old generation quarantined on restart; interruption after replacement replays idempotent metadata
commit. Partial/malformed generations quarantine. Expiry is idempotent.

If any expiry step fails:

- set/preserve `quarantined`;
- refuse raw read, raw append, and provider use;
- refuse raw-dependent evidence qualification;
- keep deterministic routing available without reading raw; and
- require successful repair/maintenance before leaving quarantine.

Receipts contain IDs, counts, epochs, policy revision, and structural state revision only—no raw
text or content commitment.

### Secondary-copy strategy

S0 chooses one lean enforceable strategy: **verified backup exclusion**.

- Router snapshots/backups/exports never include raw.
- The guarded raw path must be excluded from host backup/copy mechanisms, with a deterministic
  verification receipt.
- Restore treats any discovered raw generation as quarantined until expiry runs against the
  persisted high-water/current clock.
- If backup exclusion cannot be proven, S0 privacy proof fails; raw-dependent smart/evidence
  functionality cannot activate. Deterministic routing remains available.

Retention-epoch encryption is a valid future replacement, not a simultaneous requirement.

### Uninstall and lifecycle ownership

The install lifecycle records the active expiry owner. Product-feature rollback cannot remove or
disable expiry while raw exists.

Before removing the final expiry owner:

1. detect any unexpired raw;
2. show that final removal destroys all retained raw immediately;
3. require exact synchronous purge confirmation;
4. purge and persist a non-raw receipt; and
5. only then remove the owner.

If purge or receipt persistence fails, final removal refuses and leaves expiry ownership intact.
Ordinary 90-day expiry remains routine; only early/final-owner purge is destructive.

### Retention classes

- Raw: fixed rolling 90 days.
- Typed/derived evidence: starts at rolling 90 days.
- A later class-specific extension is forward-only, justified by measured recalibration need,
  explicitly operator-approved, and cannot extend raw.
- Frozen receipts/tombstones may retain minimal non-content lifecycle facts under a separately
  bounded governance policy.

## Provider privacy profile and R2a entry gate

No shadow/live provider call occurs until a reviewed immutable provider profile states:

| Field | Required meaning |
|---|---|
| `provider_id`, `profile_revision`, `digest` | Exact reviewed profile |
| `input_retention` | Provider retention duration |
| `training_use` | Whether inputs/outputs train provider models; must meet approved policy |
| `logging` | What provider/platform logs and for how long |
| `region` | Processing/storage regions |
| `deletion` | Available deletion mechanism/SLA |
| `credential_policy` | Deterministic secret/credential stripping version |
| `allowed_fields` | Closed current-request/candidate transformation |

Before each call:

1. State Controller expiry/quarantine preflight passes.
2. Transform only the **current** request and deterministic candidate IDs/bounded labels.
3. Strip credentials/secrets using a deterministic versioned redaction profile.
4. Validate against a closed input schema and record only profile/transformation digests.
5. Never read persisted raw history for provider input.

If profile, redaction, region/deletion policy, or preflight cannot be proven, the provider remains
off and routing stays local/deterministic. This is a blocking R2a entry gate. Persisting raw locally
never authorizes provider egress.

## Fleet selection and lifecycle

### Candidate selection/collision

- Flatten exact active/shadow registrations into `(consumer, verb)` candidates.
- Run the same deterministic normalization/scoring floor per catalog.
- R2a receives only non-zero deterministic candidates.
- Smart output is candidate IDs/scores only; unknown IDs, metadata changes, or malformed
  provenance discard the result.
- Close cross-consumer/same-label collisions become weak and ask in plain language.
- No composite verb or destructive parameter is invented.
- Missing params remain missing.

### Off/failure/drift

- Router absent/off: consumer asks and offers its explicit outcomes.
- Provider off/failed/invalid/quarantined: deterministic result.
- Host unavailable before/after F1: global routing asks; explicitly supplied single-consumer path
  remains deterministic.
- Registration/catalog/proof drift: only affected consumer asks/shadows.
- Typed state corrupt: catalog-only deterministic path; automatic learning off.
- Independent prerequisite failure blocks only dependent mapping and never triggers repair.

### Onboarding/update/retirement

1. Consumer implements one atomic kernel operation and router-absent behavior.
2. Consumer authors/generates catalog, registration, egress, goldens, and proof manifest.
3. Consumer-owned runnerless verification proves parity, contamination, outcome, and egress.
4. Host adds exact registration digest in `off`.
5. Independent conformance reports prerequisites without mutation.
6. Host moves exact qualified bytes to `shadow`.
7. Operator activates deterministic fleet mapping after F1.
8. R2b/C1 promotion is separately exact/read-only/evidence-bound.

Updates change registration revision/digests and return only affected mappings to shadow.
Deprecation prevents new activation; successor qualifies independently. Retirement is host
`retired`, locally non-overridable, with non-content tombstone/receipt. Frozen v1 entries use
additive `deprecated`/`superseded_by`, never silent deletion.

### Cross-fleet conformance

The host joins independent read-only projections by its own repository identity and reports intent
registration/mode/digests, PR delivery, documentation governance, synchronization prerequisite,
installed router release, and router-off proof. Each authority remains separate. Missing state
blocks only the dependent mapping.

## Smart/evidence lifecycle

### Deterministic and shadow stages

The current deterministic L0–L2+L5 floor remains sufficient and is always tested with smart off.
R2a can run only after G0-R0, S0 privacy proof, and provider-profile/redaction gates. Before F1 all
smart results are shadow-only.

Shadow compares deterministic and reranked outputs, with timeout/circuit breaker, exact
provider/config revision, injection isolation, and deterministic fallback. Smart ranking cannot
touch safety/authorization.

### Live stage after F1

F1 activates host fleet qualification first. R2b then may activate one exact evidence-qualified
read-only cohort. Writes/destructive stay deterministic proposals/review suggestions. Any
false-strong, destructive near-miss, burden breach, drift, provenance gap, or provider/privacy
failure returns affected mappings to shadow/ask.

### Typed arbitration/replay

- Partition by consumer, normalized intent, registration/catalog/behavior/model/policy versions,
  context class, and time.
- Operator correction and system outcome remain separate.
- System success does not prove intended meaning.
- Direct factual evidence can supersede a hypothesis, not rewrite prior intent.
- Correlated retries count once.
- Unresolved/destructive disagreement asks.
- Old evidence does not silently cross material versions.
- No half-life is chosen before adequate reversals/observation.

Replay uses frozen labels, chronological splits grouped by session/family, exact versions, and only
non-reconstructable typed features. Legacy records replay for historical integrity but do not count
for promotion. A golden regression, reconstruction-test failure, or label/provenance gap aborts.

### Exact assessment manifest

Every fifth-day/formal assessment freezes:

- assessment/cohort IDs;
- complete registered-universe snapshot;
- registration, catalog, operation registry, proof, behavior, model, provider-profile, redaction,
  evidence-policy, mapping, and cohort digests;
- included/excluded event IDs and independence keys;
- label revision and outcome-observer revision;
- baseline and measured burden; and
- gate results/deficits.

Later fleet additions appear in universe reporting but never enter a frozen denominator. A mapping
version change resets only that mapping. A shared behavior/model/policy change resets every affected
behavior stratum, not unrelated mappings.

### Forty-five-day sufficiency protocol

Assess days 5, 10, and every fifth day through 45. Time alone never proves sufficiency.

1. At least 300 independent strong proposals and zero false-strong for the exact cohort; zero
   destructive near-miss across the universe.
2. At least 30 independent strong proposals per promoted read-only mapping.
3. Every family representing at least 5% of eligible mapping traffic has at least 10 independent
   labeled proposals.
4. Count at most one strong proposal per three-hour episode for the same
   session/consumer/verb/target/family.
5. Every counted proposal has frozen disposition/provenance/versions; at least 90% of eligible
   cohort proposals have a usable final label.
6. Use the complete eligible stream and report every consumer/mapping/family/risk/abstention/
   exclusion/unknown.
7. Current and prior checkpoint show no new material under-covered segment, false-strong,
   destructive near-miss, or burden worse than deterministic baseline overall/per mapping.

Under-evidenced/new mappings remain shadow/ask without blocking qualified mappings. When gates pass,
the agent assesses depth, breadth, diversity, representativeness, independence, labels/outcomes,
safety, and burden, then recommends. The operator decides early exit.

At day 45, divide each count deficit by its corresponding independent-evidence rate over the latest
15 days; take the longest, round to the next fifth-day checkpoint, minimum five days. Zero rate
yields no invented date—repair collection or narrow cohort. Safety/quality failures need
remediation/fresh affected evidence, not waiting.

Exit ends the initial assessment window, not ongoing collection, maintenance, drift surveillance,
resolver/model observation, replay, or recalibration.

## Worked second consumer: `refresh_model_tiers`

### Atomic outcome

- Consumer: subagent orchestration
- Verb: `refresh_model_tiers`
- Inferred parameters: none
- Consequence: write/shared, computed live by consumer kernel
- Router: proposal only

### Flow and trust boundary

1. Host-qualified exact Skills-side registration/catalog yields the proposal.
2. Consumer adapter enters its kernel; router cannot invoke source control, verification, PR, or
   synchronization.
3. Cursor-side observer records live subagent enum, Cursor version, timestamp, and observation
   digest. Ordinary CI cannot independently obtain it; freshness/trust are explicit.
4. Kernel compares enum with catalog/checker/tests; no change is `noop`.
5. Safe worktree changes only catalog, checker, and tests in lockstep.
6. Full consumer gate checks enum, unavailable/superseded slugs, inherited placeholders,
   tier completeness, fallback, freshness, sibling assets, and install.
7. Governed runnerless PR proceeds without bypass/direct merge/pre-arming.
8. Kernel observes exact source head merged on live default.
9. It requests the independent sanctioned synchronization authority.
10. It verifies downstream governed bytes/digest.
11. Only then is outcome `converged`.

One operation advances idempotently:

`observed → source_ready → pr_open → merged → sync_requested → converged`

Receipts bind observation, source pre/post, exact PR head/merge, sync request, downstream digest,
and timestamps. Retries resume verified stage; changed inputs require new operation. The local
freshness monitor remains an alarm, not executor.

Provider reranking is irrelevant to this write verb's C1 eligibility: the router may propose it
deterministically, but initial automatic calibration cannot alter it.

## Verification, observability, privacy, and governance

### Runnerless ownership

| Owner | Gate |
|---|---|
| Router product authority | Local `make verify`, `make status-verify`, install, zero-link, no-execution, freeze-hardening, State Controller/privacy/replay |
| G0-V router prerequisite | One ordinary router PR makes `make verify` executable in the controller's `tmpfs,noexec` workspace by invoking scripts through interpreters and adds hermetic release-pointer/source/runtime/byte-integrity proof |
| Host verification control plane | In `KleinPerkins/dev`, reviews and exact-image-qualifies `["make", "verify"]`; owns the command mapping and qualification ledger in one host PR/receipt |
| Target protected-path owner | In this repository, merges one protected recipe-only PR through the sanctioned owner gate; no ordinary reviewer-App approval or pre-arming is claimed |
| Lock compiler/control plane | From the merged default-branch recipe, generates one lock-only target PR; the lock is never hand-edited or compiled from candidate recipe bytes |
| Verifier App | Executes unchanged required contexts `pr-automation / verify` and `pr-automation / job:repo.intent-router.m3-verify` on exact heads |
| Each consumer | Full router-absent verify plus exact-release seam, parity, consequence/outcome/egress |
| Host fleet authority | Fleet/digest/mode/prerequisite/qualification projection |
| Model-tier consumer | Live observation fixture plus full Skills source/install checks |
| Synchronization authority | Exact source-to-downstream convergence |

G0-V is a convergence child, not a mixed PR: each concrete delivery in the composite-G0 table below
keeps one owner, one repository, and one receipt. The final ordinary G0-R exact head is the first
target-repository canary required to prove the merged generated lock runs the strengthened
`make verify`; this is a G0-R entry-to-merge gate, not a reason for G0-V to depend on G0-R. Verifier
App owns exact-head checks. Reviewer App alone arms ordinary native merge automation; protected
automation paths remain owner-gated. Agents do not bypass/pre-arm. No paid runner is introduced.

### Observability

Plain status/dashboard reports all consumers, modes/qualification, deterministic/shadow/live,
fallbacks, label/outcome coverage, per-mapping/family depth, false-strong, burden,
conflicts/reversals, destructive near-miss, raw oldest/next-expiry/quarantine, provider profile/
redaction state, drift, replay, controller receipts, checkpoint deficits/rates, and exact
promotable cohort. It exposes no raw text or reconstructable feature.

### Security/privacy gates

- XDG-rooted owned regular paths: 0700 directories/0600 files; no writable symlink/special path.
- Expiry/quarantine precedes raw access/append/provider use.
- Verified host backup exclusion is mandatory for S0 privacy proof.
- Provider profile and deterministic secret stripping are mandatory for R2a.
- Raw never enters router snapshots/backups/exports/dashboard/logs/PRs/source/model training.
- Derived feedback utterance is fixed content-free marker; structured features pass
  PII/secret/non-reconstruction tests.
- Final expiry owner cannot uninstall before successful confirmed raw purge.
- Feature rollback never removes retention enforcement.
- Router is proposer, not sandbox; consumer residuals remain independent.

## Composite G0 checkpoint

G0 is a convergence checkpoint, not one PR or rollback.

### Child deliveries and order

| Child/delivery | Owner/repository | Delivery/gate | Receipt and rollback |
|---|---|---|---|
| G0-R0 freeze hardening | Router / `KleinPerkins/intent-router` | Merged first; optional name→type/enum floor locks and negative tests | Exact router receipt; revert only before dependent additions, otherwise forward-fix |
| G0-V-R local-gate prerequisite | Router / `KleinPerkins/intent-router` | One ordinary PR before command qualification; make canonical `make verify` noexec-compatible and prove hermetic release-pointer/source/runtime/byte integrity | Exact ordinary router PR/head/check receipt; router-owned revert before later G0-V dependencies, otherwise forward-fix |
| G0-V-H command authority | Host verification authority / `KleinPerkins/dev` | One host PR changes and exact-image-qualifies only the intent-router custom command to `make verify` | Exact host PR/head/check/qualification receipt; host-owned rollback |
| G0-V-P protected recipe | Target protected-path owner / `KleinPerkins/intent-router` | One protected recipe-only PR generated from merged host authority | Exact recipe PR/head/check/merge receipt; owner-gated target revert |
| G0-V-L generated lock | Target protected-path owner / `KleinPerkins/intent-router` | One lock-only PR using bytes generated by the qualified lock compiler/control plane from the merged default-branch recipe | Compiler/release/recipe provenance plus exact lock PR receipt; never hand-edit; reverse after dependent use only by governed forward-fix or authority-approved rollback |
| G0-C-AWA consumer child | Separate AWA repository authority | One separate AWA PR: exact router release seam, full router-absent verify, catalog/kernel/egress/proof digests, live counts, and trial/pin/egress prose | Exact AWA PR/head/check receipt linked to G0; AWA-owned revert |
| G0-H host projection, only if proven required | Host fleet authority | Separate host change only if that owner supplies evidence that a checkpoint projection is required | Host-owned receipt/rollback; absent proof means no G0-H delivery |
| G0-R final authority reconciliation | Router / `KleinPerkins/intent-router` | Starts only after G0-V and G0-C-AWA (plus required G0-H, if any) complete; records exact child receipts and corrects router authorities | Exact final ordinary router PR/head/check receipt; governed router rollback preserving proof meaning |

Required order is: merged G0-R0; accepted and delivered G0-V and G0-C-AWA in either order; optional
G0-H only if its owner proves it necessary; then final G0-R. G0-V itself is serial:
G0-V-R → G0-V-H → G0-V-P → G0-V-L. The G0-R ordinary exact head then proves the new generated lock
runs the strengthened canonical gate. This is acyclic: G0-V never waits for G0-R, and G0-R does not
start without G0-V's merged receipts.

The router cannot mutate AWA, host, delivery, lock-compiler, or synchronization authorities. G0-R
records their observed receipts but does not manufacture them. Every delivery preserves one owner,
one repository, one PR, and one rollback boundary. G0 remains `in_progress` after G0-R merges; a
separate operator acceptance gate observes the G0-R merge receipt and authorizes a later ledger
closeout. Child rollback is authority-owned; the checkpoint reopens if any required receipt no longer
matches.

G0 additive-manifest phase-label changes preserve existing passed-test meaning and require fresh
router `make verify`/`make status-verify`. No historical proof is renamed or fabricated.

## Source-of-truth reconciliation matrix

V3 does not edit these authorities. Under this accepted design, separately accepted G0 child
deliveries apply them in the required sequence:

| Authority | Intended correction | Owner/receipt |
|---|---|---|
| Router local canonical gate | Make `make verify` noexec-compatible; include hermetic install lifecycle and exact release-pointer/source/runtime/byte proof | G0-V-R ordinary router PR |
| Host custom-command map and qualification ledger | Change intent-router command from `bash tests/run-tests.sh` to `make verify` and qualify it against the exact controller image/limits | G0-V-H host PR in `KleinPerkins/dev` |
| Router protected recipe | Generate canonical `make verify` recipe from merged host authority; recipe-only change | G0-V-P protected owner-gated router PR |
| Router generated lock | Compile from merged default-branch recipe with qualified compiler/release; lock-only change | G0-V-L protected owner-gated router PR |
| Router `README.md` | Replace P0/stub/provisional claims with verified completed floor/current checkpoint | Final G0-R router PR |
| Router `RESUME.md` | Record merged egress and exact completed G0 children; phase-specific A0 proof; direct the next session to G0 acceptance rather than monolithic L3/L4 or missing-child work | Final G0-R |
| Router `status.yml` | Preserve completed IDs/commits; record exact G0-R0/G0-V/G0-C-AWA receipts in an in-progress composite G0 row; split future phases; reconcile K rows only to exact evidence | Final G0-R |
| Router architecture/constitution/contracts | Adopt accepted successor design; preserve locked rule meaning; only additive pending optional/enum declarations after G0-R0 | Final G0-R |
| Router additive manifest | Re-label split phases without changing prior test meaning; fresh verify/status proof | Final G0-R |
| Router security/rollback | Current runtime/runnerless truth; provider/raw/quarantine/uninstall; dependency-aware external-consumer-safe rollback | Final G0-R |
| Final canonical runnerless canary | Both unchanged required check contexts succeed on the final ordinary G0-R exact head, proving the merged generated lock executes strengthened `make verify` | Final G0-R exact-head receipt |
| AWA runnerless seam | Full router-absent verify plus exact router-release present seam | Same separate G0-C-AWA PR + exact linked receipt |
| AWA trial/egress/pin/catalog prose | Correct counts/wiring/merged state; frozen A0 baseline and exact pin | Same separate G0-C-AWA PR + exact linked receipt |
| Host checkpoint projection | Add only if host owner proves it required | Separate G0-H host receipt; otherwise absent by design |
| Delivery/synchronization authorities | No G0 mutation unless their owner identifies a required independent change | Separate authority receipt |

Review rechecked the local tree: no staged/unstaged `.github/pr-automation*` uncertainty exists.
The runnerless correction is deliberate G0-V work. Final G0-R excludes `.github` and host files and
only consumes their exact receipts.

## Revised phase ladder

Completed P0, R-core, A0 implementation, and egress remain unchanged.

| Phase/checkpoint | Production step | Proof/gate | Dependencies and rollback |
|---|---|---|---|
| G0 composite | Converged honest authorities across separately owned child deliveries | G0-R0; serial G0-V receipts; G0-C-AWA; optional G0-H only if proven; final G0-R; then separate operator acceptance | Current floor; authority-owned child reverts reopen checkpoint; G0 stays in progress through G0-R merge |
| A0-P | Frozen A0 real-PM proof | Trial names exact A0 baseline; proves A0 only | G0; controlled parallel; proof remains pending on failure |
| F0 | Neutral schemas/host interface/deterministic fleet selection | Compatibility, qualification, collision, drift, off, zero-link tests | G0-R0/G0; controlled parallel; revert to supplied single consumer |
| S0 | State Controller raw+typed append, correlation, 90-day raw/derived expiry, quarantine, receipts, deterministic replay primitive, backup exclusion | Atomic/clock/restart/failure/uninstall/non-reconstruction/privacy tests | G0-R0/G0; controlled parallel; disable evidence use but retain expiry owner |
| R2a | Provider profile/redaction plus bounded semantic shadow only | Provider/privacy entry gates; smart-off exact fallback; no product effect | G0-R0 + S0; controlled parallel; provider off |
| C0 | Review workflow, frozen assessment manifests, fifth-day report/deficit/exit assembly | Reproducible 45-day protocol; no automatic map change | F0+S0; R2a optional shadow; operator exit decisions |
| A1 | Exact AWA pin, persistent typed feedback, truthful surfaces/seam | Full AWA absent/present gates, A0-P attribution | A0-P+F0+S0; return mapping to deterministic/ask |
| R-resilience-a | Smart timeout/circuit breaker/last-good behavior | Fault fallback and atomic behavior reversal | R2a+S0; provider off/last-good |
| R-resilience-b | Operational snapshot/restore/rebuild, behavior hashes, re-heal | Raw excluded; restore enforces expiry/quarantine; corruption tests | S0+resilience-a; catalog-only deterministic |
| R-surface-a | Complete CLI/read-only MCP/thin rule-skill and wiring truth | Surface/egress and mutation-taxonomy tests | Resilience-b; remove optional surfaces |
| R-surface-complete | Immutable release, global binding, lifecycle enrollment, host handoff | Install/check/repair/uninstall, zero-link, exact provenance | Surface-a; unenroll/revert binding, preserve expiry |
| F1 | Activate host fleet with AWA managed deterministically | Host mode/digest/prerequisite/local-off/retire proofs | Surface-complete+A1; host off/supplied single consumer |
| R2b | First live rerank for exact qualified read-only cohort | Own frozen assessment, ~300/zero and per-segment gates, provider/privacy healthy | F1+C0+resilience-a; exact cohort to shadow |
| R2c | Deterministic typed low-risk resolvers; learned fields separately justified | Per-field/missing-param/CR9/smart-off proofs | R2b; disable resolver |
| B0 | `refresh_model_tiers` through converged downstream state | Live enum, full source gate, merge/sync/downstream receipts | F1+independent authorities; retire deterministic mapping/cancel before shared mutation |
| O0 | Dashboard/status projection only | No raw/reconstruction; all-universe/unknown state visible | F1+C0; rebuild/disable projection |
| C1 | Automatic calibration for exact qualified read-only mappings only | Exact manifest, accepted gates, zero destructive near-miss, operator promotion | F1+R2b+O0; reverse cohort to shadow/last-good |
| M0 | Migration/deprecation dry run | No duplicate authority; source/target/tombstone/rollback receipts | F1+B0+C1; discard projections |
| W1 | First qualified candidate wave | Per-consumer kernel-first/off/evidence/conformance | F1+O0; per-mapping retire/off |
| S2 | Local discovery suggestions | No autonomous catalog edit; privacy/precision proof | C1; disable suggestions |
| W2 | Qualified solid candidate rollout | Per-consumer exact proof; consequence gates remain | W1; per-mapping retire |
| S3 | Conditional supervised routing | Chronological holdout beats simpler stack without burden/safety regression | S2+labels; revert to bounded reranker |

Every phase has its own proof. R2b is after F1. Before F1 every smart result is shadow-only.

## Risks and non-goals

### Principal risks/controls

| Risk | Control |
|---|---|
| Optional contract drift | Blocking G0-R0 name→type/enum freeze and negative tests |
| Version skew | Explicit registration/host/proposal/feedback legacy profiles |
| Provider leaks current request | Reviewed profile, deterministic stripping, closed transformation, fallback |
| Expired raw remains readable | High-water expiry before access; quarantine on failure |
| Backups defeat retention | One mandatory verified backup-exclusion strategy |
| Final uninstall strands raw | Confirmed purge before final expiry owner removal; refusal on failure |
| Consumer identity duplicated | Repository key exists only in host fleet |
| Live smart precedes fleet authority | R2b depends on F1; pre-F1 shadow only |
| Global evidence hides weak mappings | Frozen exact manifests plus per-mapping/family/label gates |
| G0 crosses authority or cycles | G0-V-R→G0-V-H→G0-V-P→G0-V-L, independent G0-C-AWA, then final G0-R; separate owner/repository/PR/receipt/rollback per delivery |

### Non-goals

- No product implementation or authoritative mutation in this design pass.
- No model in safety/authorization/consequence/confirmation/destructive parameters.
- No online learning, reinforcement learning, vector database, remote raw storage, or raw training
  export.
- No autonomous catalog/fleet/PR/doc/synchronization mutation.
- No composite verbs or arbitrary commands.
- No paid runner or merge/check bypass.
- No shelf/global enrollment before surface-complete.
- No v2 contract by default.
- No global proof badge or time-only sufficiency.

## Smallest future implementation-plan bodies

Acceptance of v3 does not itself create or authorize any implementation body below. Each future
body requires its own accepted plan and implementation authority. G0-R0 is already delivered; it
remains listed for checkpoint traceability, not as future work.

1. G0-R0 router optional/enum freeze hardening — delivered receipt.
2. G0-V verification convergence, with separately bounded G0-V-R local prerequisite, G0-V-H host
   qualification, G0-V-P protected recipe-only, and G0-V-L generated lock-only deliveries.
3. G0-C-AWA separate consumer seam, proof-manifest, and prose correction.
4. G0-H host checkpoint projection only if host authority proves it required.
5. Final G0-R router authority reconciliation consuming the exact prior child receipts.
6. Composite G0 acceptance/ledger closeout after the final G0-R merge receipt exists.
7. A0-P frozen PM trial.
8. F0 neutral registration/host interface/deterministic fleet selection.
9. S0 State Controller append/expiry/quarantine/backup exclusion/replay primitive.
10. R2a provider profile/redaction and semantic shadow.
11. C0 assessment manifest/checkpoint/report/extension workflow.
12. A1 AWA maturation.
13. R-resilience-a smart fallback/last-good.
14. R-resilience-b snapshot/restore/rebuild/re-heal.
15. R-surface-a operator surfaces.
16. R-surface-complete immutable release/enrollment.
17. F1 host fleet activation.
18. R2b exact read-only live rerank.
19. R2c typed resolvers.
20. B0 model-tier consumer.
21. O0 dashboard projection.
22. C1 exact read-only automatic calibration.
23. M0 migration dry run.
24. W1 first candidate wave.
25. S2/W2/S3 separate conditional plans only when their entry evidence exists.

Each delivery keeps one phase/one PR in its owning repository. Cross-repository outcomes converge
through linked receipts, never a mixed commit. G0-V is a checkpoint over separate deliveries, not
an exception to that rule.

## Review provenance and resolution

V2 incorporates one deep review wave: topology probe; contract/compatibility, privacy/lifecycle,
architecture/dependencies, and governance/integration territories; then independent verification.
All returns passed their review schema.

The four independently confirmed P1 privacy blockers are resolved in design:

1. provider input is now transient, current-request-only, secret-redacted, profile-gated, and never
   sourced from persisted raw history;
2. longer-lived feedback stores a fixed content-free marker and non-reconstructable structured
   features; expired raw references become commitment-free tombstones;
3. expiry now has nondecreasing time, pre-access enforcement, atomic deletion, quarantine/fallback,
   backup exclusion, restore, clock, interruption, and partial-failure semantics; and
4. final expiry-owner removal now requires successful confirmed raw purge, while feature rollback
   cannot remove lifecycle enforcement.

Pre-fix shipping clearance failed as expected. V2 became the accepted design basis; that accepted
artifact remains immutable.

V3 adds only the source-confirmed G0 authority correction and its dependent consistency changes:

1. accepted G0-R0 v4 requires the later G0-R convergence PR to update durable ledgers only after all
   authority-owned children complete;
2. the verification control plane stages exactly one serial recipe or lock phase, compiles locks
   from merged default-branch recipe bytes, and assigns protected paths to an owner gate;
3. the current exact-image qualification contract uses a `tmpfs,noexec` workspace while the current
   `make verify` directly executes `./install.sh`, so G0-V needs a narrow router-owned local-gate
   prerequisite before host qualification; and
4. G0-V and G0-C-AWA therefore complete before final G0-R, whose exact ordinary head supplies the
   canonical runnerless canary and whose merge receipt goes to a separate composite-G0 acceptance
   gate.

No other accepted v2 architecture is reopened. These corrections are now accepted design; v2
remains immutable and superseded.

## Acceptance record

The operator accepted these exact v3 bytes on 2026-09-03. This acceptance supersedes v2 and makes v3
the design basis for the discrete future plans above and later authority-owned reconciliation. It
does not authorize implementation, G0-V host/protected-path mutations, G0-C-AWA work, G0-R
reconciliation, smart activation, fleet
enrollment, release, migration, C1 promotion, external mutation, or cross-authority writes.

Recorded decision:

> **Accepted Step 3 design v3 as the successor basis for G0-V/G0-C-AWA planning, final G0-R
> reconciliation, and later composite-G0 acceptance.**
