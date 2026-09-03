# Intent-router roadmap revision — Step 2 ecosystem and learning evidence journal

**Status:** DRAFT — 2026-09-02  
**Plan-type:** standard  
**Purpose:** Evidence journal and recommendation input for Step 3. This is not an ADR, final design,
execution plan, or implementation authorization.

## Scope and evidence boundaries

This journal combines:

1. the Step 1 repository audit;
2. read-only inspection of the live capability, fleet, consumer, scheduling, and synchronization
   authorities; and
3. a machine-local transcript study reported only as aggregate findings.

Verified facts and recommendations are labeled separately. No raw transcript text, transcript
identifier, secret, or unique private anecdote is retained here. The router remains proposal-only;
consumer kernels decide and execute. CR1–CR10, KI1–KI4, additive-within-v1 contracts, zero-link,
machine-local private state, and runnerless verification remain constraints.

## Accepted operator inputs

These are accepted design inputs, not open questions:

1. A0 remains implementation `done`. Human usability proof is earned separately per phase, not as
   one all-or-nothing product state.
2. The first smart layer is bounded reranking for ambiguous requests, always with deterministic
   fallback.
3. Operator corrections and attributable system outcomes are stored separately and reviewably.
   Neither timelessly outranks the other; thresholds wait for transcript-pattern and C0 evidence.
4. Retain raw request history as the sole behavior, machine-locally and privately under CR3, with a
   rolling 90-day policy and deterministic lifecycle enforcement. There is no consent toggle,
   alternate default, or indefinite retention. Derived/non-raw evidence may persist longer under
   its own bounded policy.
5. Run the A0 real-PM trial and smart-layer work in controlled parallel. Test A0 against a frozen A0
   baseline and prove every phase separately. No later smart phase inherits A0 proof or earns
   promotion without its own evidence and gates.
6. Fleet authority lives in the host-owned control plane. The router ships neutral schemas and
   validation; independent governance remains separately authoritative.
7. The revised controlled-parallel ladder is accepted as the Step 3 planning basis, with names and
   details refinable during design review.
8. Initial C1 automatic calibration may affect read-only verbs only. Writes and destructive actions
   remain review suggestions.
9. The proposed C1 quality target is approximately 300 independent strong proposals with zero
   false-strong observations, interpreted as a roughly 1% one-sided statistical risk target rather
   than current performance. C0 evidence determines review-burden limits; zero destructive
   near-miss remains absolute.
10. The initial evidence horizon is 45 days, assessed at fifth-day checkpoints. Objective
    sufficiency may support operator-approved early exit; deficits determine any extension. Closing
    the initial window does not stop ongoing evidence collection, maintenance, drift checks, or
    recalibration.

## Verified ecosystem evidence

### Router

- Repository `main` and the inspected worktree resolve to `427c1344`; `make verify` passes 264 tests
  with four deliberate future-phase skips, and `make status-verify` passes.
- All five v1 contracts are frozen. Future smart fields must remain optional/additive.
- The built pipeline is deterministic L0–L2 plus L5: token normalization, per-catalog candidate
  scoring, fixed verdict thresholds, and schema-shaped proposal.
- Current mapping requires one caller-supplied consumer catalog. Fleet-wide consumer selection is
  not built.
- The numeric `confidence` field is a deterministic score projection, not empirically calibrated
  correctness probability.
- No L3 semantic reranker, L4 parameter extraction, persistent feedback writer, calibration,
  snapshot writer, or recovery implementation exists.
- The local runtime is installed, but no live Cursor rule, hook, or MCP registration, no global
  shelf binding, and no lifecycle enrollment were found.
- Installed source/contracts match current bytes, but the release pointer records an older source
  commit. Installation content and provenance can therefore drift separately.
- The runnerless verification recipe executes `tests/run-tests.sh`, not canonical `make verify`.
- The freeze checker does not fully protect every optional frozen field, and strict status
  verification proves referenced PR existence rather than exact merge/commit semantics.

### CLI taxonomy inconsistency

`intent_router/cli.py` labels every future command `read_only=True`, including feedback append,
phrasebook apply, snapshot, restore, and rebuild operations that necessarily mutate router-private
state. This is harmless while they are stubs but is an incorrect boundary for C0.

**Recommendation:** replace the overloaded label with two independent properties:

- `executes_consumer=false` for every router command; and
- `mutates_router_state=true|false` according to the command.

CR1 forbids consumer execution and authorization. It does not forbid bounded writes to the router's
own private state.

### AWA, first consumer

- AWA carries the only verified real `intent-catalog/v1` found: six operator outcomes and seven
  verbs across read, write, and destructive classes.
- Its operator loop already preserves router-off behavior, kernel-owned consequence computation,
  deterministic confirmation, execution, real-outcome verification, plain narration, and
  feedback-shaped output.
- Feedback is returned in memory but not persisted.
- A real-PM trial kit and harness exist, but no completed human trial result exists.
- The consumer pin follows a mutable branch while recording an explanatory base commit. Current
  runnerless verification does not exercise the co-installed router seam or the full canonical AWA
  verification gate.
- Supporting prose still contains stale action counts and obsolete verification-surface claims.

### Existing fleet and governance patterns

- The runnerless PR-verification fleet contains 18 targets, all currently assigned local coverage.
  Its authority model separates central fleet roster, repository recipe, immutable catalog/profile
  references, generated lock, and repository-local policy.
- Its controller has a typed operation service, consequence metadata, confirmation, exact request
  binding, durable receipts, and an optional proposal-router adapter. The adapter is explicitly
  inactive and its catalog schema is not `intent-catalog/v1`.
- Doc governance has active typed policy, repository configuration, deterministic previews,
  operation-bound receipts, reconciliation, and trigger records. Its logical fleet discovery
  currently reads the PR fleet roster; this is discovery reuse, not a sound precedent for collapsing
  enrollment authority.
- New-repository setup already stages doc governance and PR verification independently. It has no
  intent-consumer onboarding path.
- Operator Voice provides another useful precedent: one typed operation registry generates
  surfaces, while 32 operations have deterministic plain-language aliases and router-off fallback.
  It has 60 total operations across safe, reversible, and consequential postures.

### Model-tier maintenance

- The source catalog is current against the observed 2026-09-01 Cursor subagent enum. Its checker
  records ten concrete available slugs; the four tiers contain eight candidate slots and six unique
  selected slugs.
- Source verification validates freshness, known unavailable/superseded slugs, tier completeness,
  and cross-provider fallback. Its tests and declared-sibling installation regression are active.
- A 09:00 local freshness job is enabled and loaded. It was installed after its prior daily window;
  the scheduler reports zero scheduled launches. Its two recorded runs were manual CLI runs: one
  failure followed by one success.
- The job runs the checker against the installed catalog. A pass proves catalog/checker
  self-consistency and age; it does not independently fetch the current Cursor enum.
- The source refresh merged through the governed PR path, but the downstream governed copy still
  carries the 2026-07-28 catalog. No post-refresh synchronization completed.
- No Skills-side intent catalog, typed refresh operation, or consumer kernel was found. The existing
  documentation describes an agent-driven workflow, not implemented kernel authority.

**Finding:** the freshness job is a useful alarm, not the consumer executor. The missing product
boundary is one operation that owns detection, live-enum observation, governed source update,
merge observation, sanctioned synchronization request, and end-state verification.

## Verified transcript evidence

### Dataset and limits

- 1,327 unique parent transcripts and 14,707 user-role records were parsed from 2026-04-25 through
  2026-09-02. System-injected records mean 14,707 is not a human-interaction denominator.
- Forty-seven correction-enriched candidates were manually adjudicated.
- Direct production-router evidence remains zero: no persisted feedback events, empty router state,
  and synthetic golden tests.
- The correction-enriched sample has no accepted or negative control set. True-positive and
  true-negative rates, current precision, recall, false-strong rate, and calibration cannot be
  estimated from it.

### Adjudicated patterns

- Fifteen agent/operator disagreements were retained: 13 high-confidence and two medium-confidence.
- Six concerned action or target interpretation, six concerned scope/policy/semantic framing, and
  three concerned stale state or context.
- Two explicit operator reversals and one non-contradictory scope update were observed.
- Twenty-nine search hits were excluded after adjudication.
- No sampled case showed a verified system outcome legitimately overriding an explicit
  operator-intent correction.
- One factual operator hypothesis was withdrawn after contrary analysis. This supports a typed
  distinction: direct evidence may supersede factual belief without retroactively redefining what
  the operator intended.
- The fifteen errors are false-positive-like for the proposed meaning and false-negative-like for
  the corrected meaning. They are not a production error rate.

### Timing evidence

- Eighteen episodes had usable intervals: median 4 minutes, mean 26.9 minutes, range 1–131 minutes.
- A 5-minute window captured 56%; 30 minutes 67%; 60 minutes 83%; 90 minutes 94%; and 180 minutes
  100%.
- One correction remained valid and outcome-confirmed 36.7 days later, rejecting blanket 30-day
  expiration.
- The two observed reversals occurred at approximately one minute and 2.2 hours. This is far too
  sparse for a survival curve or learned half-life.

**Evidence-supported use:** a provisional three-hour interval may group C0 review episodes. It must
not decide which evidence wins. No automatic freshness threshold is currently supportable.

## Accepted intent-fleet authority model

### Authority separation

1. **Router SSP:** neutral schemas, ranking, validation, local evidence processing, and read-only
   proposal surfaces. It contains no host repository roster.
2. **Consumer repository:** operation registry, kernel, catalog or deterministic catalog projection,
   consequences, confirmation, execution, outcome verification, egress terms, and golden cases.
3. **Host control plane:** repository/workspace identity, fleet roster, approved digests,
   qualification evidence, rollout mode, and cross-fleet prerequisites.
4. **Machine-local router state:** evidence, map projections, metrics, and snapshots only.
5. **Independent authorities:** PR delivery, doc governance, and ecosystem synchronization remain
   separately owned. A read-only report joins their states; no fleet enrolls or repairs another.

This placement preserves zero-link: neutral schemas may live in intent-router, while host identities
and repository literals live only in the host control plane.

### Proposed records

**Neutral registration schema:** `intent-consumer-registration/v1`, owned by intent-router.

**Consumer record:** `.intent-router/consumer.json`, containing:

- stable consumer ID and repository UUID; nullable remote repository ID;
- relative paths to catalog, golden set, egress contract, and kernel proof manifest;
- compatible contract versions;
- router-off, contamination, catalog-to-operation parity, and outcome-proof test IDs;
- authored or deterministically generated catalog provenance;
- no free-form commands, prompts, credentials, or executable configuration.

**Host fleet record:** one source-tracked fleet file containing:

- repository/consumer identity and registration path;
- approved registration, catalog, golden, and egress digests;
- exact router release pin;
- desired mode `off | shadow | active | retired`;
- rollout cohort and required external authorities.

**Local runtime projection:** rebuildable fleet index and observations beneath private router state.

**Local override:** exact per-consumer `off` always narrows effective mode. `on` cannot override an
unqualified or retired host record.

Qualification (`qualified | drifted | unavailable`) is computed from evidence, not manually stored
as another ambiguous lifecycle state.

### Fleet-wide selection

The current per-consumer path remains valid. A new global path flattens active
`(consumer, verb)` candidates and adds bounded consumer-level aliases/description from registration.
Generic verb collisions remain weak or unresolved and therefore ask. The router never composes two
verbs into a new action.

### Onboarding and verb lifecycle

1. Build an explicit kernel operation and prove router-off behavior.
2. Add registration/catalog in `off`; do not create empty intent scaffolds in every repository.
3. Validate schemas, bounded paths, catalog-to-kernel parity, egress, goldens, contamination, and
   runnerless proof coverage.
4. Merge consumer authority, then pin its exact digests in the host fleet.
5. Run shadow; review quality, safety, privacy, and fallback evidence.
6. Activate only exact qualified bytes.
7. Add a new verb additively: kernel path first or in the same consumer PR, then catalog entry,
   proofs, host repin, shadow, and activation.
8. A catalog/registration digest mismatch degrades only that consumer to ask.
9. Repair may rebuild derived local projections or reinstall exact releases. It never rewrites
   catalog/kernel meaning.
10. Immediate local off remains available. Retirement first turns routing off, then marks verbs
    `deprecated:true`, retains an audit tombstone, and removes projections. V1 entries are not
    silently deleted.
11. Existing typed operation registries may generate a deterministic intent-catalog projection,
    avoiding duplicate semantic authorities.

### Cross-fleet conformance

Join independent projections by stable repository identity and report:

- intent registration/mode/digests;
- required PR-delivery capability;
- required doc-governance capability;
- required synchronization authority;
- installed release and router-off proof state.

Requirements are consumer-specific. A read-only verb need not be PR-enrolled; a source-changing
consumer such as model-tier refresh must be. Missing prerequisites block intent activation only and
never trigger cross-fleet mutation.

## Worked second consumer: refresh the model-tier catalog

### Proposed atomic operation

- **Consumer:** subagent orchestration
- **Verb:** `refresh_model_tiers`
- **User value:** replace recurring technical maintenance with one governed request
- **Parameters from wording:** none
- **Safety class:** write; the consumer kernel determines shared-reference consequence
- **Kernel owner:** Skills-side subagent-orchestration package

### Recommended flow

1. The fleet mapper proposes only `refresh_model_tiers`.
2. The Skills-side adapter validates consumer, verb, catalog digest, freshness, and uncertainty,
   then enters its own kernel.
3. A Cursor-side observer supplies a bounded, timestamped model-enum observation from the live
   subagent tool schema. Ordinary CI cannot independently obtain this enum.
4. The kernel compares that observation with the source catalog/checker. No change returns `noop`.
5. A safe worktree updates exactly the catalog, checker, and checker tests in lockstep.
6. The kernel validates enum membership, no inherited placeholder, unavailable/superseded slugs,
   cross-provider fallback, tier completeness, freshness, targeted tests, and the full Skills gate.
7. It delivers a governed PR without directly enabling or bypassing merge automation.
8. It observes an exact merged head on the source default branch.
9. It requests capability synchronization through the sanctioned independent synchronization
   authority. It never writes the downstream edge itself.
10. It verifies that the downstream governed copy carries the new enum revision before returning
    end-to-end success.
11. Feedback records operator choice separately from source-merge and downstream outcomes.

One operation may have staged receipts (`observed`, `source_ready`, `merged`, `sync_requested`,
`converged`) while remaining one atomic operator outcome. Retries resume by operation ID and do not
open duplicate PRs.

## Recommended staged SMART collection

### Build now

- Preserve the deterministic catalog retrieval/verdict floor unchanged.
- Add host-aware flattened candidate indexing and reviewed synonyms/phrasebook inputs.
- Add typed event correlation, aggregate metrics, replay, frozen labels, shadow output, and
  last-good rollback. Retain raw requests only within the mandatory bounded local lifecycle.
- Build one bounded semantic reranker over existing non-zero top candidates for ambiguous cases,
  always with deterministic fallback and initially without product effect.
- Add optional proposal metadata such as `confidence_basis`, `catalog_digest`, and rerank provenance;
  all additions remain optional within v1.
- Label the existing score in operator-facing output as **match strength**, not accuracy or
  calibrated confidence.

### Promote only after phase evidence

- Any reranker effect on live proposals waits for that phase's own shadow evidence and promotion
  gates; A0 proof cannot be reused as smart-layer proof.
- Selective prediction: below an evidence-backed risk threshold, abstain/ask.
- Reliability buckets and confidence intervals before any fitted calibrator.
- Monotonic calibration only when direct labels and class coverage support it.
- Local/offline clustering of repeated none/clarify/correction cases for discovery suggestions.

### Later and conditional

- Supervised routing only after stable classes, independent adjudicated labels, chronological
  holdout improvement, and learning-curve evidence.
- Parameter learning only for eligible low-risk fields. Destructive parameters remain literal,
  enum, regex, or deterministic live-resolver sourced, or require literal confirmation.

### Reject or defer

- No learned or LLM component in authorization, safety classification, consequence, confirmation,
  or kernel disposition.
- No reinforcement learning, online gradient updates, autonomous source/catalog editing, vector
  database, multiple simultaneous model stacks, or agent swarm in the routing path.
- No remote raw-wording store and no inference that local retention authorizes model egress.
- No automatic conflict winner, decay threshold, or half-life before evidence supports it.

## Evidence arbitration recommendation

Use a deterministic typed evidence ledger, not an ML adjudicator.

Evidence types:

- operator intent/correction;
- factual observation;
- attributable system outcome;
- hypothesis/preference;
- clarification, rejection, abort, and abstention.

Partition evidence by consumer, normalized intent, catalog/policy/model/behavior versions, and
relevant context. Old evidence remains auditable but does not silently cross version boundaries.
Deduplicate correlated retries so one incident does not masquerade as independent support.

Rules before C1:

- unresolved or destructive disagreement abstains/asks;
- conflict produces a review suggestion only;
- system success does not prove intent correctness;
- direct factual evidence may overturn a factual hypothesis but does not rewrite prior intent;
- operator locks may be date- or version-bounded, and expiration reopens review rather than flipping
  a mapping.

Candidate future weighting, only after sufficient direct labels:

`weight = quality × independence × 2^(-age / learned_half_life)`

Learn half-lives by evidence stratum. A one-vs-rest Bayesian support model is a valid simpler
alternative. Neither should be selected until each evidence stratum has enough reversals and
observation duration.

## Privacy and retention recommendation

- Raw request history is always retained machine-locally/private under CR3; there is no consent
  toggle or alternate raw-history mode.
- Keep exact raw wording in a separate mode-0600 lifecycle store keyed by event ID. Keep derived
  counts, explicit corrections, typed evidence, and version/context attribution in the append-only
  evidence record under its own bounded policy so ordinary raw expiry does not erase the evidence
  trail.
- **Accepted policy:** a rolling 90-day raw-history window. This retains the observed 36.7-day
  correction context while bounding exposure; it is separate from the 45-day initial evidence
  horizon. Do not infer that enforcement is already implemented.
- Enforce expiry deterministically on append and startup/doctor maintenance, with oldest-retained
  and expired-backlog status, idempotent deletion receipts, and tests for boundary time, restart,
  partial failure, and clock handling. Snapshots and backups must not silently extend the limit.
- Normal policy-driven expiry is expected lifecycle processing and does not require destructive
  confirmation. An explicitly requested purge before scheduled expiry is a separate destructive
  operation with exact scope, confirmation, receipt, and honest irreversibility copy.
- Historical transcript mining remains separately governed; live-router retention does not by
  itself authorize unrelated historical mining or model egress.

## Measurement and promotion evidence

### Required event coverage

Collect accepted, corrected, rejected, clarified, aborted, and abstained cases—not correction-only.
Record operator evidence and attributable system outcome separately.

### Evaluation method

- Freeze labels before evaluation.
- Use chronological rolling splits grouped by session and utterance family.
- Run shadow replay against exact catalog/model/policy versions.
- Report per-consumer and per-verb precision/recall, false-strong rate, selective risk/coverage,
  calibration, clarification/review burden, conflict/reversal rates, and outcome-attribution
  coverage.
- Exclude unresolved/unknown outcomes from accuracy numerators while reporting their coverage.
- Track latency, provider failure/fallback, deterministic replay, drift, egress, and state recovery.
- Never expose raw wording in dashboards, PRs, shared logs, or fleet records.

### Promotion evidence

Hard gates:

- deterministic and router-off behavior unchanged;
- zero destructive near-miss;
- zero golden/injection/egress regression;
- provider failure always falls back deterministically;
- exact rollback to last-good state;
- runnerless proof covers the canonical verification path.

### Accepted 45-day checkpoint and exit protocol

Assess cumulative evidence on days 5, 10, and every fifth day through day 45. Time alone never
proves sufficiency. At any checkpoint where the objective gates below are met, run a formal
assessment; the agent recommends exit or continuation with reasons, and the operator decides.

**Exact promotion cohort and moving universe**

- Every registered consumer appears in the checkpoint report with registration/catalog digests,
  lifecycle mode, risk classes, event counts, label coverage, and qualification state.
- Automatic promotion is scoped to an immutable cohort of exact qualified read-only
  `(consumer, verb, catalog/policy/model/behavior version)` mappings.
- New, changed, or under-evidenced mappings remain shadow/ask. They neither block a qualified cohort
  nor enter its denominator silently. A material version change resets only the affected mapping's
  promotion evidence; prior evidence remains auditable.

**Objective exit gates**

1. **Quality and safety:** the exact cohort contains at least 300 independent strong proposals and
   zero false-strong observations, supporting the proposed roughly 1% one-sided statistical risk
   target rather than claiming current performance. Destructive near-miss is zero across the full
   registered universe. Writes and destructive actions remain review suggestions.
2. **Depth and breadth by consumer/verb:** each promoted mapping contributes at least 30 independent
   strong proposals. A mapping below that floor remains shadow/ask without blocking other mappings.
3. **Utterance-family diversity:** for each promoted mapping, every family representing at least 5%
   of its observed eligible traffic has at least 10 independent labeled proposals. List all smaller
   families and unknown/none cases even when they do not gate promotion. These are coverage floors,
   not per-family confidence claims.
4. **Independence:** deduplicate retries and correlated records; count at most one strong proposal
   per three-hour episode for the same session, consumer, verb, target, and utterance family. The
   three-hour rule groups review evidence only and never decides which evidence wins.
5. **Label and outcome quality:** 100% of counted proposals have frozen disposition, provenance,
   exact version/context, and reviewable attribution; at least 90% of all eligible cohort proposals
   have a usable final label. Report unresolved and unavailable outcomes rather than imputing them.
6. **Representativeness:** assess the complete eligible cohort stream rather than a convenience
   sample; report every consumer, verb, family, risk class, abstention, and exclusion. No global
   count substitutes for the per-mapping and material-family gates.
7. **Stability and burden:** at the current and immediately preceding fifth-day checkpoint, there is
   no new material family or qualified mapping below its coverage floor, no false-strong or
   destructive near-miss, and review/clarification burden is no worse than the frozen deterministic
   baseline overall or for any promoted mapping. C0 observations establish the numeric burden
   baseline and any later improvement target.

**Day-45 extension**

If the gates are not met on day 45, compute each countable deficit against the gates above and divide
it by the corresponding independent-evidence collection rate observed over the latest 15 days.
Round the largest resulting duration up to the next five-day checkpoint, with a minimum five-day
extension. If a required segment has a zero rate, do not invent a date: keep it shadow/ask and repair
collection or narrow the proposed cohort. Safety, label-quality, or representativeness failures
require remediation and fresh affected-mapping evidence, not passive waiting.

Closing the initial window—early or at/after day 45—does not stop evidence collection, observation,
algorithm/model/deterministic-resolver maintenance, drift checks, or future recalibration.
Freshness estimation still needs at least 20 reversals per evidence stratum, preferably 50 conflict
episodes, and observation for at least twice any tested half-life; no automatic freshness threshold
is implied by the 45-day horizon.

## Candidate priority after core infrastructure

### STRONG

| Candidate | User value | Kernel owner | Data/feedback | Safety | Prerequisite / rationale |
|---|---|---|---|---|---|
| Existing AWA catalog maturation | Makes the first real consumer human-proven and learnable without new verbs | AWA | Real loop, synthetic goldens, pending PM trial; no persisted production feedback | Mixed | Exact runnerless seam, PM trial, C0 persistence; strongest because kernel already exists |
| `refresh_model_tiers` | Removes recurring catalog drift and technical PM work | Skills-side subagent orchestration | Repeated source refreshes, local checker events, observable source/downstream state | Write/shared | Live-enum observation, typed kernel, exact-path PR, sanctioned sync; strongest second consumer |
| `repair_job` | Turns a diagnosed local scheduling problem into one bounded repair | Local-jobs | Typed job records, events, drift diagnosis, real outcome checks | Reversible write | Kernel-resolved managed job ID and preview; excludes arbitrary command execution |

### SOLID

| Candidate | User value | Kernel owner | Data/feedback | Safety | Defer rationale |
|---|---|---|---|---|---|
| `retry_verification` | Retries a failed governed check | PR controller | Durable requests/receipts and check outcomes | Write | Catalog currently marks it unavailable pending a same-head retry canary |
| `recover` | Repairs controller-owned state | PR controller | Mature preflight, confirmation and receipts | Destructive-capable | Prove a lower-risk verb first |
| `reconciliation_preview` | Explains document-governance drift before change | Doc governance | Typed records, previews, receipts, trigger | Read | Low observed intent volume; independent fleet enrollment still needs clarity |
| Targeted capability synchronization | Closes stale shared capability copies | Synchronization authority | Existing registry, digests, PR outcomes | Write/shared | Exact capability target and authority-bound confirmation required |
| Capability repair | Restores a capability across supported clients | Capability lifecycle owner | Doctors and install verification exist | Reversible write | Current surface is an agent playbook, not one typed kernel |
| Operator Voice `context.get` | Maps ordinary drafting requests to a high-value read | Operator Voice | Typed registry, deterministic aliases, local feedback | Read/private | Existing fallback already works; privacy raises incremental cost |

### WEAK / REJECT

| Candidate | Reason |
|---|---|
| Generic “run/fix all local jobs” | Composite and may expose arbitrary command execution |
| Generic “write/update this document” | Broad authoring intent must be narrowed by its existing skill/kernel |
| Approve, merge, arm, bypass, or disarm automation | Forbidden or unavailable under current authority |
| Workspace routing through intent-router | A separate capability already owns workspace selection; router-of-router complexity adds little |
| Autonomous catalog/fleet repair | Violates consumer ownership and content-as-data |
| Outcome-only tier/model policy changes | Operational success is not sufficient intent or policy evidence |

## Accepted revised complete phase ladder — Step 3 planning basis

Completed history remains unchanged: P0, R-core, A0 implementation, and egress. Existing consumer
kernel lanes are reconciled against live evidence rather than silently rewritten.

### Near term

1. **G0 — baseline honesty and proof hardening:** reconcile stale prose/ledger, optional-field
   freeze, CLI taxonomy, release provenance, canonical router verification, and exact AWA seam.
2. **Controlled parallel wave, with separate baselines and proof:**
   - **A0-P — real-PM proof:** freeze the A0 baseline, run the trial, and record sanitized A0
     evidence separately from implementation completion and every later phase.
   - **F0 — neutral fleet substrate:** registration/fleet schemas, host-owned roster, fleet-wide
     selection, digest qualification, local off, and independent conformance; no global enrollment.
   - **S0 — smart evidence foundation:** typed derived evidence, correlation, telemetry, replay,
     frozen labels, shadow, rollback, and bounded raw-history lifecycle enforcement.
   - **R2a — bounded semantic shadow:** rerank only ambiguous top-candidate sets, always fall back
     deterministically, isolate injection-like content, and produce no product effect.
3. **C0 — reviewable calibration:** append-only evidence, manual phrasebook, conflict review,
   three-hour episode grouping, and the accepted 45-day fifth-day checkpoint/exit protocol.
4. **A1 — AWA maturation:** exact pin, persistent feedback, real-surface evidence, and first shadow
   evaluation.
5. **R-resilience-a — live-smart safety:** timeout/circuit breaker, deterministic fallback,
   corruption fallback, and last-good rollback.
6. **R2b — selective live reranking:** empirically gated by its own evidence, non-authorizing, and
   initially narrow risk.
7. **R2c — typed parameters:** deterministic resolvers first; learned extraction only when justified;
    destructive literal-confirm remains fixed.

### Medium term

8. **R-resilience-b — full recovery:** behavior hashes, rebuild, snapshots, restore, drift and
    re-heal.
9. **R-surface-a — production surfaces:** complete CLI, read-only MCP, thin rule/skill and
    production-wired egress proof.
10. **R-surface-complete — release and enrollment:** immutable release, Flavor-2 global binding,
    lifecycle enrollment, and host overlay.
11. **F1 — host fleet activation:** activate the host control plane and onboard AWA as the first
    managed consumer.
12. **B0 — second consumer:** model-tier refresh through source PR, merge observation, sanctioned
    synchronization and downstream verification.
13. **O0 — fleet observability:** quality/safety/privacy/drift dashboard and scheduled backstops.
14. **C1 — automatic calibration:** only qualified read-only mappings after their direct evidence,
    accepted thresholds, zero destructive near-miss, and rollback proof; writes/destructive remain
    review suggestions.
15. **M0 — migration design and dry run:** registry adapters, deprecation, retirement, tombstones,
    rollback inventory, and no automatic migration.
16. **W1 — STRONG rollout:** qualified local-job repair and low-risk PR operation.

### Long term

17. **S2 — discovery intelligence:** local clustering and review suggestions.
18. **W2 — SOLID rollout:** qualified doc, capability, synchronization, and private-context verbs.
19. **S3 — supervised routing, conditional:** only if learning curves and chronological holdouts
    prove durable benefit over retrieval/reranking.

**Explicit changes to the old pending ladder:** A0 stays done and gains phase-specific A0-P; A0-P
and smart-layer construction run in controlled parallel against separate frozen baselines; R2 splits
into foundation/shadow/live/parameters; resilience and surface split; C0 precedes learned promotion;
C1 leaves the critical path until labels exist. Every phase earns proof separately.

## Major ADR/design topics for Step 3 or later

These are proposed topics, not final ADRs:

1. Fleet authority placement, zero-link boundary, and independent conformance.
2. Consumer registration, digest qualification, local off, deprecation, retirement, and migration.
3. Fleet-wide candidate selection and collision/abstention behavior.
4. Smart-provider boundary, match-strength semantics, calibration, and deterministic fallback.
5. Typed evidence, privacy, version partitioning, conflict arbitration, and operator locks.
6. Runnerless cross-repository seams, exact pins, provenance, and canonical gates.
7. Model-tier refresh kernel, live enum observation, staged receipts, and sync handoff.
8. Metrics, promotion evidence, drift, rollback, and C1 activation.

Likely execution-plan bodies after design acceptance:

- G0 verification and evidence-semantics reconciliation;
- A0-P trial;
- F0/S0/C0 foundations, including bounded raw-history expiry, early-purge separation, registered-
  universe reporting, and the fifth-day checkpoint/exit protocol;
- split R2 and resilience;
- A1 maturation;
- production surface/release/enrollment;
- F1/B0/O0;
- C1 activation;
- migration and candidate waves.

## Step 3 recommendation

Use this journal and its accepted decisions as input to one revised roadmap/design pass. Step 3
should:

1. reconcile existing architecture, status, resume, security, and rollback prose against accepted
   evidence without changing completed phase history;
2. define the neutral fleet/evidence schemas and phase acceptance criteria;
3. encode the accepted raw-retention, moving-universe, checkpoint, early-exit, extension, and C1
   promotion boundaries;
4. run a proportional architecture review before any implementation plan; and
5. produce discrete implementation plans only after the revised design is accepted.

After G0 establishes exact baselines, run the A0 PM trial and bounded smart-layer work in controlled
parallel. Keep their evidence isolated: A0 trial results prove only frozen A0, while every smart
phase must satisfy its own shadow, safety, quality, and promotion gates.

## Remaining operator decisions

No additional roadmap-design choice remains from this evidence batch. At any fifth-day checkpoint
that meets the objective gates, the agent must recommend exit or continuation and the operator must
decide whether to close the initial window early. Any later C1 promotion remains a separate
operator-gated decision bound to the exact qualified read-only cohort and evidence assessment.

## Remaining contradictions and dependencies

- PM trial proof is still absent, while existing phase prose disagrees on whether it blocks R2.
  Controlled parallelism now settles the intended order: trial frozen A0 while smart work proceeds
  against separate baselines. Source-of-truth docs remain to be reconciled in G0/Step 3.
- “Seven surfaces” currently mixes contract compatibility with production wiring. Step 3 should
  define and report those states separately.
- The consumer seam has no exact live runnerless owner today.
- Cursor exposes the model enum to an agent-facing tool schema, not an ordinary stable CI API. The
  live observation trust boundary needs explicit design.
- Source merge and downstream convergence are separate outcomes; the current model-tier state proves
  the distinction.
- Current transcript evidence supports instrumentation and abstention, not automatic decay,
  arbitration, or production quality claims.
- The raw-history duration, C1 scope, initial evidence horizon/checkpoints, quality target, host
  control plane, and controlled-parallel ladder are accepted. Step 3 must translate them into
  testable design and plan acceptance criteria without reopening them.

## Sources inspected

- `AGENTS.md`, `ARCHITECTURE.md`, `CONSTITUTION.md`, `RESUME.md`, `status.yml`, `SECURITY.md`,
  `ROLLBACK.md`, `meta.yml`, `install.sh`, contracts, runtime modules, tests, and runnerless records.
- AWA consumer catalog, operator loop, translators, egress contract, trial kit, router pin, kernel
  tests, and live remote change metadata.
- Skills subagent-orchestration rule, catalog, checker, tests, sibling-asset ADR/plan, installer,
  regression, and repository verification.
- Host local-job registry, command instance, events, installed launch record, and live scheduler
  state.
- Runnerless fleet roster, assignments, profiles, recipes, locks, operation catalog/service,
  proposal adapter, and current remote records.
- Doc-governance policy, config schema, trigger catalog, transaction/reconciliation code, and fleet
  inventory.
- Synchronization registry, relationship authority, payload logic, status history, and live
  downstream catalog bytes.
- Ecosystem manifest/standalone-system paradigms, new-repository scaffolding, capability playbook,
  and Operator Voice operation/intent registries.
- Aggregate transcript-evidence report supplied for this synthesis.

