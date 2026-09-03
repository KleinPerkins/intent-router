# G0-R0 contract-freeze hardening plan v3

**Status:** ACCEPTED — 2026-09-02
**Plan-type:** agentic-execution
**Supersedes:** `docs/plans/g0-r0-contract-freeze-hardening-v2.md` (preserved byte-for-byte as
accepted basis; SHA-256:
`d417c5b26742816be4349a8b8a31331c67bfbab0517f232ef2a7846950b0c76b`)
**Correction:** T2 cross-reference for `enum_extensions` bootstrap validation corrected from
brittle `§5.2 step 10` to stable `§5.4 (enum_extensions bootstrap validation)`; no substantive
content changed.
**Purpose:** Zero-context-executable implementer-grade plan for the G0-R0 child delivery inside
the composite G0-R convergence checkpoint. Implementation is not yet authorized.

---

## 1. Child-delivery identity and boundary

G0-R0 is a **child delivery** inside the composite G0-R convergence checkpoint, not a
standalone repository phase. G0-R0 closes one verified guard gap before any new authoritative v1
optional field or enum member lands. The G0-R convergence PR — distinct and later — updates
`status.yml`, `RESUME.md`, and the roadmap ledger only after all authority-owned G0 child
deliveries are complete.

**In scope:**

- `contracts/additive-manifest.json` — add complete `frozen_behavior` and `enum_extensions`
- `checks/intent-contract-freeze.sh` — bootstrap/fail-closed manifest validation; exact
  required/optional/nested/enum/content-floor comparison; `INTENT_CONTRACT_DIR` test-only override
- `tests/test_contract_freeze.py` — shipped-checker adversarial matrix including manifest
  negative tests
- `tests/test_additive_compat.py` — path-qualified additive promotion identity; bidirectional
  `enum_extensions` validation
- `tests/freeze_helpers.py` (new required module: `validate_additive_bundle(contracts_root: Path)`)
- `AGENTS.md` — narrow truth correction of stale freeze-timing sentence

**Out of scope (do not touch):**

- Any product contract field, enum member, or content
- `status.yml`, `RESUME.md`, `ARCHITECTURE.md`, `CONSTITUTION.md`
- `.github/pr-automation*`, `Makefile`, `tests/run-tests.sh`
- Any AWA, host, consumer, State Controller, provider, or synchronization file
- Design journals, roadmap revision documents, or `docs/plans/` other than the README update
  that accompanies plan acceptance

**Accepted design authority:**
`docs/plans/roadmap-revision-step-3-design-v2.md`, accepted digest
`9f1098920e531818d1e845f7f11ed3480a7d86ffb738326c98f819835fc8afb1`.

---

## 2. Confirmed ground truth

### 2.1 Reproduced defect

The shipped checker (`checks/intent-contract-freeze.sh`) currently freezes:

- five hard-coded schema IDs and their corresponding filenames/status in `EXPECTED` (a
  schema → `(filename, expected_status)` dict that will be replaced by a pure schema-ID set
  after T2; the manifest alone will own filenames and status declarations);
- exact top-level required keys in `FLOOR`;
- one nested required map in `NESTED_FLOOR` (catalog `param` required keys only); and
- a partial set of enum floors in `ENUM_FLOOR`.

It does **not** compare top-level `optional_keys`, any nested `optional_keys`, or the following
enum sets: `intent-feedback/v1.verdict`, `intent-catalog/v1.param.type`,
`intent-catalog/v1.param.source`, `intent-constitution/v1.machine_check.status`.

The defect was reproduced on 2026-09-02 through the existing
`tests.test_contract_freeze._run_checker_against` harness:

1. copy the real contracts into a temporary `INTENT_HOME`;
2. remove `intent-feedback.v1.json.optional_keys.correction`; and
3. run the shipped checker.

Observed result: exit code `0`, all five contracts `PASS`, `intent-contract-freeze: OK`.

Intended post-delivery result: exit non-zero with a diagnostic naming the dropped frozen optional.

### 2.2 Exact five-contract frozen inventory (ground truth from disk)

This table drives the `frozen_behavior` declaration in T1. Do not infer it dynamically — copy it
exactly from disk.

| Contract | Required floor (name:type) | Top optional floor | Nested required/optional | Enum floors (path: members) |
|---|---|---|---|---|
| `intent-catalog/v1` | `verb:string`; `aliases:array`; `examples:array`; `param_schema:array<param>`; `preconditions:array`; `safety_class:enum`; `tool_path:enum`; `start_point_rules:object`; `plain_label:string`; `consequence_copy:string` | none | `param.required={name:string, type:enum, required:bool}`; `param.optional={enum:array, source:enum}` | `safety_class:{read,write,destructive}`; `tool_path:{cli,mcp,hook}`; `param.type:{string,int,number,bool,enum,path,ref}`; `param.source:{literal,regex,enum,repo-resolver,llm}` |
| `intent-map/v1` | `intent_key:string`; `utterance_examples:array`; `target_verb:string`; `param_bindings:object`; `weight:number`; `confidence:number`; `hit_count:int`; `last_used:string\|null`; `outcome_stats:object`; `source:enum`; `version:int` | none | none | `source:{seed,manual,feedback}` |
| `intent-feedback/v1` | `ts:string`; `consumer:string`; `catalog_version:string`; `utterance:string`; `proposal:object`; `operator_choice:enum`; `verdict:enum`; `confidence:number`; `outcome:enum`; `session_id:string` | `correction:object\|null` | none | `operator_choice:{accept,correct,reject,clarify,abort}`; `outcome:{success,refused,failed,noop,unknown}`; `verdict:{strong,weak,none}` |
| `intent-constitution/v1` | `rules:array<rule>`; `kernel_invariants:array<invariant>`; `machine_checks:object`; `banned_terms:object`; `operator_outcomes:array` | none | none | `machine_check.status:{active,spec}` |
| `intent-proposal/v1` | `consumer:string`; `verb:string`; `params:object`; `start_point:string`; `safety_class:enum`; `tool_path:enum`; `confidence:number`; `verdict:enum`; `why:array`; `missing_params:array`; `requires_confirmation:bool` | none | none | `verdict:{strong,weak,none}`; `safety_class:{read,write,destructive}`; `tool_path:{cli,mcp,hook}` |

**Constitution content floors (from disk — exact set equality everywhere except metadata):**

| Surface | Floor semantics |
|---|---|
| `rules` | Actual rule ID set must **equal** the manifest `rules` ID set (no unrecorded IDs, no dropped IDs); exact `rule` text per ID. Sanctioned additions update both contract and manifest in one PR. |
| `kernel_invariants` | Actual invariant ID set must **equal** manifest ID set; exact `invariant` text per ID. Same sanctioned-addition rule. |
| `banned_terms.tier_a_generic_mechanism` | Actual array must **equal** the manifest floor array (order-insensitive exact set); sanctioned additions update both. |
| `banned_terms.tier_b_git_workflow` | Same exact-set semantics. |
| `banned_terms.tier_c_consumer_contributed` | Actual scalar value must **equal** the manifest exact-scalar floor value. |
| `banned_terms_optional_entries` | Map of authoritative `banned_terms.optional` additions (currently `{}`); `tier_a_consumer_contributed` is **pending** (absent from actual `banned_terms` and from this map). |
| `operator_outcomes` | Actual array must **equal** the manifest floor array (order-insensitive exact set); sanctioned additions update both. |
| `machine_checks` per-entry `status` | **NOT frozen** — `spec→active` transitions are intentional lifecycle; only the enum floor `{active,spec}` is frozen. |

Copy exact rule/invariant texts and array members verbatim from `contracts/intent-constitution.v1.json`
at implementation time; do not paraphrase or abbreviate. `banned_terms.note` is tolerated metadata
and is not frozen.

### 2.3 Checker gap catalog

The following accepted behaviors are NOT currently enforced by the shipped checker:

| Gap | Defect class |
|---|---|
| `intent-feedback/v1.optional_keys.correction` removal | The primary reproduced defect |
| `intent-catalog/v1.param.optional_keys.enum` removal | Nested optional, not checked |
| `intent-catalog/v1.param.optional_keys.source` removal | Nested optional, not checked |
| `intent-feedback/v1.enums.verdict` member removal | Enum floor absent from ENUM_FLOOR |
| `intent-catalog/v1.enums.param.type` member removal | Enum floor absent from ENUM_FLOOR |
| `intent-catalog/v1.enums.param.source` member removal | Enum floor absent from ENUM_FLOOR |
| `intent-constitution/v1.enums.machine_check.status` member removal | Enum floor absent |
| Constitution rule text changed | Content floor not checked |
| Constitution invariant removed or text changed | Content floor not checked |
| `operator_outcomes` member removed | Content floor not checked |
| `banned_terms` tier array member removed | Content floor not checked |
| Manifest structural validity | Not bootstrap-validated before iteration |
| Extra/duplicate manifest schema or filename | Not checked |
| Wrong-type manifest section (e.g. array instead of object) | Not checked |

### 2.4 Existing protections (updated)

- Required-key set equality and required type equality bite.
- `intent-catalog/v1` nested `param` required keys bite.
- Partial enum-floor subset (`safety_class`, `tool_path`, `source`, `operator_choice`, `outcome`,
  `verdict` in proposal, `safety_class`/`tool_path` in proposal) bite.
- Freeze status/date/exemption and schema/version/freeze strings bite.
- `intent-proposal/v1` is **frozen** as of A0 (frozen date recorded; `freeze_exempt: false`);
  the checker and contracts are already correct.   Three locations contain stale present-tense PROVISIONAL claims that postdate the A0 freeze:
  `AGENTS.md` (line ~21, agent entrypoint), `ARCHITECTURE.md` (contract-status table, lines 83–92),
  and `intent_router/proposal.py` (lines 5–7, source comment). Only `AGENTS.md` is corrected by
  this delivery (T-AGENTS) because it is the mandatory agent entrypoint; `ARCHITECTURE.md` and
  `intent_router/proposal.py` are deliberately deferred to the later G0-R authority-honesty child
  delivery. The regression test (T-AGENTS) checks AGENTS.md only and does not scan the deferred files.
- `tests/test_additive_compat.py` checks deferred-addition/manifest agreement and prevents some
  key collisions/removals; its global key flattening (unqualified) will be replaced with
  path-qualified identity in T4.
- `make verify` runs `tests/run-tests.sh`, the shell checker, strict status verification, and
  install static preflight.
- The runnerless job `repo.intent-router.m3-verify` is **configured** (lock file verified) to run
  `bash tests/run-tests.sh`, but execution is **paused/unproven** as of 2026-09-02 (PR #53 merged
  with empty `statusCheckRollup`). New unittest regressions will run remotely once the controller
  resumes, without recipe changes.

---

## 3. Objective

After G0-R0:

1. One existing declarative artifact (`contracts/additive-manifest.json`) contains the complete
   expected frozen behavior for all five v1 contracts, including optional fields, nested optional
   fields, all enum floors, and constitution content floors.
2. The shipped checker validates the manifest's structure before iterating; missing/unreadable/
   invalid/structurally wrong manifests fail with controlled deterministic diagnostics.
3. The checker compares actual contracts to that floor: removal, rename, retype, type-union
   narrowing of required, optional, and nested fields fails; removal of any accepted enum member
   fails; rule/invariant text change or member removal fails; individual machine_check `status`
   transitions do NOT fail (only the enum floor `{active,spec}` is frozen).
4. Unrecorded optional/enum additions fail; actual enum members must equal the complete
   `frozen_behavior.enum_floors` set (exact equality, order-insensitive); a sanctioned addition
   updates all coordinated surfaces coherently before any writer emits the new field or member.
5. All old fixtures/readers and completed-phase tests still pass.
6. Path-qualified additive identity replaces unqualified global key flattening.
7. `enum_extensions` in the manifest is the provenance index for all declared enum extension
   members; current state is empty maps for all schemas (no `deferred_additions` entry has
   `target` beginning with `enum.`).
8. Both the shell checker and the Python additive validator can be aimed at the same temporary
   bundle via `INTENT_CONTRACT_DIR`.
9. AGENTS.md's stale freeze-timing sentence is corrected with a regression test.
10. The remote proof path is verified live (configuration confirmed, both required check contexts
    identified); if the controller is still paused at delivery the PR stays draft until both checks
    complete successfully on the exact head SHA.

---

## 4. Locked invariants and non-goals

### Locked

- CR1/CR2: router still proposes only and never authorizes.
- CR4: additive within v1; no required removal/rename/retype/addition.
- CR5: contract/catalog content remains data.
- KI1: consumer remains safe with router absent.
- Zero-link remains green.
- All five v1 contracts remain frozen (no product field change).
- One G0-R0 child delivery, one router PR.
- No paid or Actions runner.

### Non-goals

- No new optional field or enum member in any product contract.
- No F0 registration/fleet schema.
- No proposal/feedback typed-event additions.
- No State Controller, raw store, provider, smart ranking, AWA, host, or synchronization change.
- No authoritative architecture/security/rollback reconciliation (belongs to G0-R authority
  honesty child delivery).
- No runner recipe/lock change.
- No broad ledger/RESUME rewrite.
- No v2 contract.

---

## 5. Hardened freeze model

### 5.1 Manifest as sole declarative expected floor

Extend `contracts/additive-manifest.json` with two new top-level objects:

- **`frozen_behavior`**: keyed by the five schema strings; each entry records the complete
  expected freeze floor for one contract.
- **`enum_extensions`**: path-qualified provenance index for all declared enum extension members
  (pending or authoritative) across all contracts; currently `{}` for each schema because no
  contract `deferred_additions` entry has a `target` beginning with `enum.`.

The additive manifest already owns the cross-contract additive roadmap. It becomes the one
declarative **expected** baseline. Contract JSON remains the **actual** declared shape; checker
Python compares actual to expected. The checker no longer owns duplicate `FLOOR`, `NESTED_FLOOR`,
`ENUM_FLOOR`, or content-floor constants.

### 5.2 Manifest bootstrap/fail-closed validation

The checker's hard-coded bootstrap anchor is **only the exact set of five schema ID strings**;
it owns no filename or status knowledge. The manifest alone owns filenames, per-schema status
declarations, and all floors. Before iteration the checker validates the manifest file itself;
any structural defect halts with a deterministic diagnostic. Validation order:

1. `contracts/additive-manifest.json` exists and is readable → fail: `manifest MISSING or unreadable`
2. Parses as valid JSON **with duplicate-key rejection** (e.g. `object_pairs_hook` raising on
   duplicate keys) → fail: `manifest not valid JSON` (malformed) or `manifest duplicate key <key>`
   (dup key). Every loaded contract is also parsed with duplicate-key rejection → fail:
   `contract <schema> not valid JSON` / `contract <schema> duplicate key <key>`.
3. `manifest["schema"] == "intent-additive-manifest/v1"` (exact string) → fail:
   `manifest schema header invalid: expected intent-additive-manifest/v1`
4. `manifest["version"] == 1` (integer one, not just truthy) → fail:
   `manifest version header invalid: expected integer 1`
5. Top-level `frozen_behavior` key exists and is an object → fail: `frozen_behavior missing or not an object`
6. Top-level `enum_extensions` key exists and is an object → fail: `enum_extensions missing or not an object`
7. `frozen_behavior` keys match **exactly** the five bootstrap schema IDs (no missing, no extra)
   → fail: `frozen_behavior missing schema <id>` or `frozen_behavior unexpected schema <id>`
8. For each schema entry — validate all child shapes recursively:
   - `file` is a **nonempty** string, basename-only safe: no `/` or `\`, `Path(file).name == file`,
     ends with `.v1.json`, and `(contracts_root / file).resolve()` is directly under
     `contracts_root.resolve()` → fail: `frozen_behavior[<schema>].file unsafe: <file>`
   - `status` is the **literal string `"frozen"`** → fail with schema-scoped diagnostic
   - `required_keys` is an object; every key is a nonempty string; every value is a nonempty string
     → fail: `frozen_behavior[schema].required_keys invalid`
   - `optional_keys` is an object; every key is a nonempty string; every value is a nonempty string
     → fail: `frozen_behavior[schema].optional_keys invalid`
   - `nested` is an object; every key (container name) is a nonempty string; every value is an
     object containing **both** `required_keys` and `optional_keys` sub-keys, each itself a valid
     type map (object with nonempty-string keys and nonempty-string values); missing sub-key or
     wrong type fails → fail: `frozen_behavior[schema].nested[container] invalid`
   - `enum_floors` is an object; every key (path) is a nonempty string; every value is a unique
     nonempty-string array → fail: `frozen_behavior[schema].enum_floors[path] invalid`
   - `content_floors` is either `null` (non-constitution schemas) or an object (constitution) that
     contains **exactly** these required children, each with the validated shape below; wrong type
     or missing child fails → fail: `frozen_behavior[schema].content_floors invalid`
9. No duplicate `file` value across the five entries → fail: `frozen_behavior duplicate filename <file>`
10. Constitution `content_floors` recursive validation (exact required children, no others required):
    - `rules`: object; every key is a nonempty string (rule ID); every value is a nonempty string
      (exact rule text) → fail: `content_floors.rules invalid`
    - `kernel_invariants`: object; every key is a nonempty string (invariant ID); every value is
      a nonempty string (exact invariant text) → fail: `content_floors.kernel_invariants invalid`
    - `banned_terms_exact_values`: object; every key is a nonempty string (tier name); every
      value is a unique nonempty-string array → fail: `content_floors.banned_terms_exact_values invalid`
    - `banned_terms_exact_scalars`: object; every key is a nonempty string; every value is a
      nonempty string → fail: `content_floors.banned_terms_exact_scalars invalid`
    - `banned_terms_optional_entries`: object; every key is a nonempty string; every value is a
      nonempty string (direct value, not a wrapper object) → fail: `content_floors.banned_terms_optional_entries invalid`
    - `operator_outcomes_exact_members`: unique nonempty-string array → fail: `content_floors.operator_outcomes_exact_members invalid`
11. `enum_extensions` has exactly the five bootstrap schema IDs as keys, each value is an object;
    for any non-empty child object, every key (path) is a nonempty string and every value is a
    unique nonempty-string array → fail: `enum_extensions missing schema <id>` /
    `enum_extensions[schema][path] not a unique string array`
13. `required_additive_phases` is a unique-string array → fail: `required_additive_phases invalid`
14. `deferred_phases` is an object; each phase key is a nonempty string; each phase spec is an
    object with `kind` equal to exactly `"additive"` or `"no-schema-change"`. For `"additive"`:
    `contracts` is a nonempty object keyed only by schema IDs within `FROZEN_SCHEMAS`, each value
    a unique nonempty-string array. For `"no-schema-change"`: `reason` is a nonempty string.
    Every phase in `required_additive_phases` must exist in `deferred_phases` → fail with
    phase-scoped diagnostics.
15. For each contract loaded, `deferred_additions` (if present) is an object; each phase value is
    an array; each entry is an object with nonempty string `key`, `type`, and `target`; `target`
    is one of the four supported values (`top.optional`, `nested.<container>.optional`,
    `enum.<path>`, `banned_terms.optional`) → fail: `contract <schema> deferred declaration invalid: <diagnostic>`

After bootstrap validation, for each schema the checker loads the manifest-declared `file`
from `frozen_behavior[schema]["file"]`, opens `contracts_root / file`, and verifies:
- `contract["schema"] == schema` and `contract["status"] == "frozen"`

This verifies the manifest's self-declared mapping without hard-coded schema→filename constants.

Top-level manifest keys `schema`, `version`, `rationale` and any unrecognized metadata keys are
tolerated beyond the validated keys above. `required_additive_phases` and `deferred_phases` are
**validated** (steps 13–14), not merely tolerated.

### 5.3 Complete `frozen_behavior` structure per schema

```
"frozen_behavior": {
  "<schema-id>": {
    "file": "<filename>",
    "status": "frozen",
    "required_keys": { "<name>": "<type>", ... },
    "optional_keys": { "<name>": "<type>", ... },   // {} if none
    "nested": {
      "<container>": {
        "required_keys": { "<name>": "<type>", ... },
        "optional_keys": { "<name>": "<type>", ... } // {} if none
      }
    },                                               // {} if no nested
    "enum_floors": {
      "<path>": ["<member>", ...]                    // path = enum field name or dotted path
    },                                               // {} if no enums
    "content_floors": null                           // object for intent-constitution/v1; null for all others; must be present
  }
}
```

For `intent-constitution/v1`, `content_floors` is:

```
"content_floors": {
  "rules": { "<rule-id>": "<exact rule text>", ... },
  "kernel_invariants": { "<invariant-id>": "<exact invariant text>", ... },
  "banned_terms_exact_values": {
    "tier_a_generic_mechanism": ["<exact member>", ...],
    "tier_b_git_workflow": ["<exact member>", ...]
  },
  "banned_terms_exact_scalars": {
    "tier_c_consumer_contributed": "<exact text>"
  },
  "banned_terms_optional_entries": {},
  "operator_outcomes_exact_members": ["accept", "correct", "reject", "clarify", "abort"]
}
```

Field semantics (all exact equality; no "extensions allowed" subset semantics):

- `rules`: map of `{rule-id → exact rule text}`. Actual rule ID set must **equal** this ID set.
- `kernel_invariants`: same ID-set equality + exact text.
- `banned_terms_exact_values`: for each tier name, actual array must **equal** the recorded array (order-insensitive). Covers `tier_a_generic_mechanism` and `tier_b_git_workflow`.
- `banned_terms_exact_scalars`: for each scalar key, actual string value must **equal** exactly. Covers `tier_c_consumer_contributed`.
- `banned_terms_optional_entries`: map of authoritative `banned_terms.optional` additions (nonempty-string keys → nonempty-string values). Currently `{}`. When `tier_a_consumer_contributed` is promoted, this map gains the key with its direct string value. Pending state: key absent from both actual `banned_terms` and this map. Authoritative state: key present in both actual `banned_terms` and this map with identical nonempty string values (`actual[key] == floor[key]`).
- `operator_outcomes_exact_members`: actual `operator_outcomes` must **equal** this array (order-insensitive exact set).

`banned_terms.note` is tolerated metadata and is not covered by any floor sub-map. Individual
`machine_checks[key]["status"]` values are **not** recorded here — only the enum floor
`machine_check.status: [active, spec]` appears in `enum_floors`.

### 5.4 Enum extensions (path-qualified provenance index, currently empty)

Top-level `enum_extensions` in the manifest is the provenance index for **all** declared enum
extension members, whether pending or authoritative:

```
"enum_extensions": {
  "intent-catalog/v1": {},
  "intent-map/v1": {},
  "intent-feedback/v1": {},
  "intent-constitution/v1": {},
  "intent-proposal/v1": {}
}
```

`enum_extensions[schema][path]` is an ordered unique string array of enum member values that have
been declared via a deferred addition targeting `enum.<path>`. Currently all maps are empty
because no contract has a `deferred_additions` entry with `target` starting `enum.`.

**Exact deferred entry shape for enum additions:**

```json
{"key": "<member-value>", "type": "enum-member", "target": "enum.<path>"}
```

For example, adding member `none` to `intent-feedback/v1.enums.operator_choice` would require:
```json
{"key": "none", "type": "enum-member", "target": "enum.operator_choice"}
```

**Five-surface state machine:**

| State | Condition | Valid? |
|---|---|---|
| Pending | Member in `deferred_additions` + manifest phase record + `enum_extensions[schema][path]`; absent from actual `enums[path]` AND `frozen_behavior.enum_floors[path]` | Valid |
| Authoritative | All five surfaces agree: deferred declaration, manifest phase record, `enum_extensions[schema][path]`, actual `enums[path]`, and `frozen_behavior.enum_floors[path]` | Valid |
| Any partial state | Any surface has the member while another does not | Invalid — fail |

Current state for all schemas: all five surfaces are empty/absent (no enum extension targets),
which is a valid consistent state.

**Bootstrap validation for `enum_extensions`** (step 11 of §5.2 — enum_extensions validation):
- Exactly the five bootstrap schema IDs as keys; each child value is an object.
- Any non-empty child object: every key is a nonempty string (path), every value is a unique-string array.
- Checker negative tests: missing schema key, extra schema key, child value not an object,
  path value not an array, duplicate member in array, non-string member.

When a future phase adds an enum member, all five surfaces update coherently in one PR:

1. `contract.deferred_additions[phase]` gains `{"key":"<m>","type":"enum-member","target":"enum.<path>"}`.
2. The manifest `deferred_phases[phase]` records the phase participation.
3. `enum_extensions[schema][path]` records `<m>` (pending state).
4. When the member becomes authoritative: `contract.enums[path]` gains `<m>` AND
   `frozen_behavior[schema].enum_floors[path]` gains `<m>`.

Any partial state fails both the checker and the additive validator.

### 5.5 Constitution content floors

The checker enforces **exact set equality** for all content floor surfaces of `intent-constitution/v1`.
"Extensions allowed" semantics are replaced by coordinated floor-update semantics everywhere.

- **Rule ID-set and text exact equality:** actual `rules` array ID-set must **equal** `content_floors.rules`
  key set exactly. Unrecorded actual IDs fail (`unrecorded rule ID <id>`); dropped IDs or changed
  `rule` text fail. Sanctioned rule additions update both the contract `rules` array and
  `content_floors.rules` in one PR before any writer uses the new ID.
- **Invariant ID-set and text exact equality:** actual `kernel_invariants` array ID-set must
  **equal** `content_floors.kernel_invariants` key set exactly; exact `invariant` text per ID.
  Same sanctioned-addition coordination required.
- **Banned term tier array exact set equality:** for each tier name in
  `content_floors.banned_terms_exact_values`, actual `banned_terms[tier_name]` array must
  **equal** the floor array (order-insensitive). Unrecorded extra members fail (`unrecorded
  banned_term member <tier>.<value>`); dropped members fail. `banned_terms.note` is tolerated
  metadata and is not floor-checked.
- **Banned term tier_c exact scalar equality:** actual `banned_terms["tier_c_consumer_contributed"]`
  value must **equal** `content_floors.banned_terms_exact_scalars["tier_c_consumer_contributed"]`
  exactly.
- **Banned term optional entries:** `content_floors.banned_terms_optional_entries` maps each
  authoritative optional key to a direct nonempty string (the expected value). Currently `{}`.
  Checker validation: (1) for each key in `banned_terms_optional_entries`, the key must exist in
  actual `banned_terms` and `actual[key]` must equal `floor[key]` exactly (both nonempty strings)
  → fail: `banned_terms.optional key <key> value mismatch` or `missing from actual`; (2) for each
  key in actual `banned_terms` that is not one of the required tier keys and not `note`, the key
  must appear in `banned_terms_optional_entries` → fail: `unrecorded banned_terms.optional key <key>`.
  The current `tier_a_consumer_contributed` deferred declaration is pending: key absent from both
  actual `banned_terms` and `banned_terms_optional_entries` → valid, does NOT fail.
- **Operator outcomes exact set equality:** actual `operator_outcomes` array must **equal**
  `content_floors.operator_outcomes_exact_members` (order-insensitive). Sanctioned additions
  update both surfaces.
- **machine_check.status NOT frozen per entry:** the checker must NOT record or assert individual
  machine check `status` values. Only the enum floor `machine_check.status: [active, spec]`
  is frozen. A `spec→active` transition must PASS.

### 5.6 Exact comparison rules

- Required map: exact key set and exact type strings.
- Optional map: exact key set and exact type strings (top-level and nested).
- Nested required/optional maps: exact container set, exact key set, exact type strings.
- Enum floors: the actual contract `enums[path]` member set must **equal** the complete
  `frozen_behavior.enum_floors[path]` set (order-insensitive, unique strings). Missing floor
  members fail (`dropped frozen value`); extra actual members without a coordinated floor update
  also fail (`unrecorded enum member`). The contract is additive because a sanctioned extension
  updates `frozen_behavior.enum_floors[path]` before any writer emits the new member; existing
  members can never be dropped.
- Type strings are semantic atoms. Exact equality catches union narrowing:
  `object|null → object` and `string|null → string` both fail.
- Extra optional key in contract without a `frozen_behavior` record → fail: `ADD unrecorded optional`.
- `deferred_additions` presence remains required and is still cross-checked.

### 5.7 Path-qualified additive promotion identity

The current `test_additive_compat.py::_added_keys_by_contract()` returns
`{phase: {unqualified_key_names}}`, losing path information and risking ambiguity when two
contracts declare same-named keys at different paths.

**Scope boundary:** The existing frozen optional/nested keys already declared in
`frozen_behavior.optional_keys` (e.g. `correction:object|null` in intent-feedback/v1) are
**base frozen fields**, NOT deferred additions. They have no `deferred_additions` entry and no
manifest phase record. The promotion-state machinery applies only to `deferred_additions` entries;
base frozen fields are validated solely by the floor-comparison checks in §5.6. This distinction
prevents false "missing deferred declaration" failures on existing frozen optionals.

**Provenance guarantee (narrowed):** A self-contained repository checker cannot distinguish a
coordinated actual+floor addition with all provenance omitted from a pre-existing baseline without
embedding a second immutable baseline. G0-R0 deliberately does not embed one. What G0-R0 proves:
(a) current actual shape exactly equals the current authoritative floor; (b) every *declared*
deferred declaration and its manifest phase record are bidirectionally consistent and path/type-aware;
(c) every *declared* deferred addition is either fully pending or fully authoritative (no partial
state); (d) `enum_extensions` is bidirectional for declared enum additions. A future promotion PR
is responsible for proving every diff-added identity has a declared provenance record — that is a
review/phase gate, not a claim made by this checker. Original frozen base fields (e.g. `correction`,
existing enum members) are governed by exact actual-vs-floor equality and do NOT require deferred
provenance records.

**Canonical join (bidirectional, over the three provenance sources):** The validator iterates the
full union of three sources: every `(phase, schema, key)` triple in
`manifest.deferred_phases[phase].contracts[schema]`, every `deferred_additions[phase][i]`
declaration in every contract, and every entry in `enum_extensions[schema][path]`. The join
resolves declared provenance only — it does NOT scan actual/floor for identities absent from all
three sources and does NOT claim provenance completeness over arbitrary coordinated edits.

Every manifest phase-record `(phase, schema, key)` must resolve to **exactly one** declaration in
`contract.deferred_additions[phase]` where `declaration["key"] == key` — zero matches fails as
**orphan manifest record**; multiple matches fails as **ambiguous declaration**. Conversely, every
declaration in `contract.deferred_additions[phase]` must resolve back to **exactly one** manifest
phase record — zero matches fails as **orphan declaration**. For enum targets, every member in
`enum_extensions[schema][path]` must resolve to exactly one deferred declaration and vice versa;
orphans in either direction fail.

Canonical path-qualified identity: `declaration["target"] + "." + declaration["key"]`, e.g.
`top.optional.catalog_version`, `nested.param.optional.extractor`, `enum.outcome.test_ext`,
`banned_terms.optional.tier_a_consumer_contributed`.

Supported `target` values: `top.optional`, `nested.<container>.optional`, `enum.<path>`,
`banned_terms.optional`. A target not matching one of these four patterns is invalid (fail:
`unsupported target <target>`).

**Type rules per target:**

| Target | `declaration.type` requirement | Pending condition | Authoritative condition |
|---|---|---|---|
| `top.optional` | Must exactly equal both the actual optional field type and the `frozen_behavior` floor type when authoritative | Absent from both actual `optional_keys` and `frozen_behavior.optional_keys` | Present in both with identical type string |
| `nested.<container>.optional` | Same as top.optional, scoped to the container | Absent from both nested optional surfaces | Present in both with identical type |
| `enum.<path>` | Must equal literal `"enum-member"`; `key` must be a string (the member value) | Absent from actual `enums[path]` AND `frozen_behavior.enum_floors[path]` AND `enum_extensions[schema][path]` contains the member (pending registration) — five-surface state per §5.4 | All five surfaces agree |
| `banned_terms.optional` | `declaration.type` must equal `"note"`; actual `banned_terms[key]` must be a nonempty string; `floor.banned_terms_optional_entries[key]` must be a nonempty string; `actual[key] == floor[key]` | Key absent from actual `banned_terms` AND absent from `content_floors.banned_terms_optional_entries` | Key present in both with identical nonempty-string values |

Unknown `declaration.type` or unknown `target` → fail immediately.

**State tables (applying the type rules above):**

| State | Condition | Valid? |
|---|---|---|
| Pending (optional/nested) | Deferred declaration + manifest record; absent from both actual optional/nested AND frozen floor | Valid |
| Authoritative (optional/nested) | Deferred declaration + manifest record; present in both actual AND frozen floor; type strings identical | Valid |
| Any partial (optional/nested) | One surface has it, the other does not; or types disagree | Invalid — fail |
| Pending (enum) | Deferred declaration + manifest record + `enum_extensions` entry; absent from actual `enums[path]` AND `enum_floors[path]` | Valid |
| Authoritative (enum) | All five surfaces agree | Valid |
| Any partial (enum) | Any surface has/lacks inconsistently | Invalid — fail |
| Pending (banned_terms.optional) | Deferred declaration + manifest record; absent from actual `banned_terms` AND `banned_terms_optional_entries` | Valid |
| Authoritative (banned_terms.optional) | Deferred declaration + manifest record; key present in actual `banned_terms` AND `banned_terms_optional_entries`; both values are nonempty strings and `actual[key] == floor[key]` | Valid |
| Any partial (banned_terms.optional) | Present in one surface but not the other | Invalid — fail |

**Current state on real tree:**
- `tier_a_consumer_contributed` at `banned_terms.optional` (egress phase): **pending** — deferred
  declaration present; manifest egress phase record present; key absent from actual `banned_terms`
  and from `banned_terms_optional_entries: {}`. `validate_additive_bundle` must accept this without error.
- All other deferred additions (A0, R2, C1, R-resilience, R-surface): **pending** — keys absent
  from actual optional fields and frozen floors (none are authoritative yet; floors are not yet declared).
  C0 has `kind: no-schema-change` — it has no `deferred_additions` entries and is not subject to
  the promotion-state machinery.
  After T1 adds the manifest floors, these pending states remain valid (keys remain absent from floors).
- All enum surfaces: currently empty; no enum extension declarations exist.

### 5.8 Producer/reader skew boundary

Schema-level additive validation alone does not prove that old consumers tolerate unknown optional
fields or enum members. G0-R0's temporary sanctioned-addition fixture proves **checker and
metadata acceptance only** — it does not prove runtime compatibility.

State explicitly in T4 acceptance criteria and stop conditions:

- A new optional field may not be emitted by any writer until old-reader tolerance is proven for
  every affected consumer (reader-first/writer-last ordering).
- An enum extension is treated as modifying unless unknown-member tolerance is explicitly proven
  for every old reader.
- If consumer-side old-reader evidence cannot be produced, do not claim v1 compatibility; version
  the contract instead.
- G0-R0 does not produce reader-compatibility evidence; that burden falls on each future phase
  that promotes an addition from pending to authoritative and activates a writer.

---

## 6. One injectable validation path

**Shell checker override:** Add `INTENT_CONTRACT_DIR` environment variable support to
`checks/intent-contract-freeze.sh`. Change the `CONTRACTS` resolution line to:

```bash
CONTRACTS="${INTENT_CONTRACT_DIR:-"$INTENT_HOME/contracts"}"
```

`INTENT_CONTRACT_DIR` is a **test-only** override that points directly to a contracts directory
root. It is never set in production (production always resolves via `INTENT_HOME`). The checker
comments must document: "INTENT_CONTRACT_DIR is test-only; production default is fail-closed to
INTENT_HOME/contracts."

**Python validator:** `tests/freeze_helpers.py` is required (see §7). Its exported function
`validate_additive_bundle(contracts_root: Path)` performs the same logical validation as the
manifest-loading portion of the shell checker — loads and validates the manifest, checks
structural correctness, and verifies frozen_behavior against actual contracts. It accepts
`contracts_root` as an argument; it must not use any hardcoded path. Existing `TestAdditiveCompat`
wrappers call it or its focused helpers on the real root.

**Test coherence requirement:** The shell checker and the Python validator always read the same
`cdir`. No fixture may split the directory seen by the two validators.

- **Sanctioned passing fixtures** (coherent): mutate all coordinated surfaces in the same `cdir`
  so both validators accept the result. Run shell checker with `INTENT_CONTRACT_DIR=str(cdir)` then
  call `validate_additive_bundle(cdir)` on the same path.
- **Negative fixtures** (intentionally one-sided): mutate exactly one surface to induce a failure.
  Both validators still read the same `cdir`; only one surface is wrong, so both validators see
  the same broken state and must both fail (or the shell checker alone is tested for shipped-checker
  negatives).

---

## 7. Implementation-file allowlist

The G0-R0 child PR's changed path set must equal **exactly** the following required set:

| Path | Change |
|---|---|
| `contracts/additive-manifest.json` | Add `frozen_behavior` and `enum_extensions` |
| `checks/intent-contract-freeze.sh` | Add manifest bootstrap validation; extend comparison; add `INTENT_CONTRACT_DIR` |
| `tests/test_contract_freeze.py` | Manifest negative tests; full adversarial matrix |
| `tests/test_additive_compat.py` | Path-qualified identity; `enum_extensions` bidirectional validation |
| `tests/freeze_helpers.py` | Required new module: `validate_additive_bundle(contracts_root: Path)` |
| `AGENTS.md` | Narrow freeze-timing truth correction (one sentence) |

All six paths are required. No other paths may appear. Do **not** invent `.github/` evidence.
Do **not** include `status.yml`, `RESUME.md`, `Makefile`, `tests/run-tests.sh`, `docs/plans/`, or
any other file. The T5 changed-path proof must assert the exact required set (see §10/T5).

---

## 8. Execution task blocks

Tasks run in dependency order: **T1 → T2 → T4 → T3 → T-AGENTS → T5**. T2 requires T1 staged
or complete. T4 (shared validator and path semantics) must complete before T3 (adversarial matrix),
because T3 imports `tests/freeze_helpers.py` and calls `validate_additive_bundle`. T-AGENTS is
independent and may run alongside T4/T3. All land atomically in one PR (no partial T state).

---

### Task G0-R0-T1 — Declare complete frozen behavior

**Purpose:** Extend the additive manifest to be the sole declarative expected floor.

**Files:**
- `contracts/additive-manifest.json`

**Steps:**

- [ ] Add `frozen_behavior` object with exactly five schema keys per §5.3.
  - `intent-catalog/v1`: required_keys (10 entries per §2.2), optional_keys `{}`, nested `param`
    with required `{name:string, type:enum, required:bool}` and optional `{enum:array, source:enum}`,
    enum_floors `{safety_class:[read,write,destructive], tool_path:[cli,mcp,hook], param.type:[string,int,number,bool,enum,path,ref], param.source:[literal,regex,enum,repo-resolver,llm]}`, content_floors `null`
  - `intent-map/v1`: required_keys (11 entries per §2.2), optional_keys `{}`, nested `{}`,
    enum_floors `{source:[seed,manual,feedback]}`, content_floors `null`
  - `intent-feedback/v1`: required_keys (10 entries per §2.2), optional_keys `{correction:object|null}`,
    nested `{}`, enum_floors `{operator_choice:[accept,correct,reject,clarify,abort], outcome:[success,refused,failed,noop,unknown], verdict:[strong,weak,none]}`, content_floors `null`
  - `intent-constitution/v1`: required_keys (5 entries per §2.2), optional_keys `{}`, nested `{}`,
    enum_floors `{machine_check.status:[active,spec]}`, content_floors per §5.3/§5.5 with
    verbatim `rules` (CR1–CR10 id→text), `kernel_invariants` (KI1–KI4 id→text),
    `banned_terms_exact_values` (tier_a and tier_b arrays verbatim),
    `banned_terms_exact_scalars` (tier_c value verbatim),
    `banned_terms_optional_entries: {}`,
    `operator_outcomes_exact_members` (verbatim array) — all copied exactly from disk
  - `intent-proposal/v1`: required_keys (11 entries per §2.2), optional_keys `{}`, nested `{}`,
    enum_floors `{verdict:[strong,weak,none], safety_class:[read,write,destructive], tool_path:[cli,mcp,hook]}`, content_floors `null`
- [ ] Add `enum_extensions` object with five schema keys each mapping to `{}` (no deferred enum
  targets exist).
- [ ] Preserve all existing `required_additive_phases`, `deferred_phases`, `schema`, `version`,
  and `rationale` fields byte-for-byte (formatting aside).
- [ ] Run `python3 -m json.tool contracts/additive-manifest.json > /dev/null` to confirm valid JSON.

**Pre-T2 coexistence check:** The checker still reads only `FLOOR`/`NESTED_FLOOR`/`ENUM_FLOOR`
at this point; T1 is a manifest-only additive change. Run the unchanged checker to confirm it
remains GREEN before proceeding to T2.

```
bash checks/intent-contract-freeze.sh
```

Expected: exit 0 (existing checker not yet rewired; backward-compatible manifest addition).

**Acceptance:**
- Manifest parses; `frozen_behavior` covers all five schemas; `enum_extensions` is present.
- Existing `deferred_phases` tests retain their meaning.
- Checker still passes (backward-compatible addition).

**Rollback:** Revert this manifest change independently before T2 depends on it. After T2 lands
atomically in the same PR, roll back T1+T2 together only before any later authoritative optional
addition depends on the floor.

**Dependencies:** Accepted design; no code dependency.

---

### Task G0-R0-T2 — Rewire shipped checker with bootstrap validation

**Purpose:** Make the production freeze gate enforce the declarative floor; add fail-closed
manifest bootstrap validation.

**Files:**
- `checks/intent-contract-freeze.sh`

**Steps:**

- [ ] Add `INTENT_CONTRACT_DIR` override line immediately after the existing `CONTRACTS`
  assignment: `CONTRACTS="${INTENT_CONTRACT_DIR:-"$INTENT_HOME/contracts"}"`.
  Add comment: `# INTENT_CONTRACT_DIR is test-only; production default is fail-closed to INTENT_HOME/contracts.`
- [ ] Replace the existing `EXPECTED` schema→`(filename, status)` dict with a **plain set of
  five schema ID strings** (the bootstrap anchor). Example:
  ```python
  FROZEN_SCHEMAS = {
      "intent-catalog/v1", "intent-map/v1", "intent-feedback/v1",
      "intent-constitution/v1", "intent-proposal/v1",
  }
  ```
  The manifest alone owns filenames and status declarations; the checker owns only this ID set.
- [ ] Load `$CONTRACTS/additive-manifest.json`; apply all bootstrap validation checks from §5.2
  in order. Each step on failure prints a deterministic diagnostic to stderr and exits 1. Use
  `FROZEN_SCHEMAS` to validate that `frozen_behavior` has exactly those five keys (no more, no
  fewer). Validate each entry's `status == "frozen"` (literal), `file` nonempty string,
  `required_keys`/`optional_keys`/`nested`/`enum_floors` objects, `content_floors` object or null
  (present for all five, null for the four non-constitution schemas), and no duplicate `file`
  value. Validate `enum_extensions` per §5.4 (enum_extensions bootstrap validation).
- [ ] For each schema, load the contract from `contracts_dir / frozen_behavior[schema]["file"]`;
  verify `contract["schema"] == schema` and `contract["status"] == frozen_behavior[schema]["status"]`.
- [ ] Replace embedded `FLOOR`, `NESTED_FLOOR`, and `ENUM_FLOOR` constants: derive
  `required_keys`, `optional_keys`, `nested`, and `enum_floors` from
  `manifest["frozen_behavior"][schema]` for each schema.
- [ ] Add optional-key comparison: compare contract `optional_keys` against
  `frozen_behavior[schema]["optional_keys"]` using exact key set and exact type equality.
  Emit `DROPPED frozen optional`, `RETYPED frozen optional`, `ADD unrecorded optional`.
- [ ] Add nested optional-key comparison: for each container in `frozen_behavior[schema]["nested"]`,
  compare `contract["nested"][container]["optional_keys"]` against the floor. Same diagnostic scheme.
- [ ] Add complete enum floor comparison using `frozen_behavior[schema]["enum_floors"]` (covers
  previously-absent `feedback.verdict`, `catalog.param.type`, `catalog.param.source`,
  `constitution.machine_check.status`). Enum comparison: actual `enums[path]` member set must
  **equal** `frozen_behavior.enum_floors[path]` (order-insensitive, unique strings). Missing floor
  member → `enum <path> dropped frozen value <member>`; extra actual member →
  `enum <path> unrecorded member <member>`.
- [ ] Add **bidirectional promotion validation for ALL declared target types** using the canonical
  join over the three provenance sources (§5.7): for each resolved `(phase, schema, key, target)`
  declaration (obtained from the bidirectional join), apply the per-target type rules from §5.7:
  - `top.optional`: type string must match actual optional_key type when authoritative; fail on
    partial (key in one surface but not the other) or type mismatch.
  - `nested.<container>.optional`: same, scoped to the container's optional_keys.
  - `banned_terms.optional`: type must equal `"note"`; authoritative value must be nonempty string;
    fail on partial.
  - `enum.<path>`: handled by five-surface state validation below.
  Orphan manifest records and orphan declarations fail as described in §5.7.
- [ ] Add `enum_extensions` five-surface state validation: for each schema, for each path in
  `manifest["enum_extensions"][schema]` (currently `{}` — a no-op loop):
  - For each member `m` in `enum_extensions[schema][path]`, locate the deferred declaration
    (`contract.deferred_additions[phase][target="enum.<path>", key=m]`) and the manifest
    phase record. Then classify the state:
    - **Pending**: `m` absent from `contract["enums"][path]` AND absent from
      `frozen_behavior[schema]["enum_floors"][path]` → **valid**, emit no error.
    - **Authoritative**: `m` present in `contract["enums"][path]` AND present in
      `frozen_behavior[schema]["enum_floors"][path]` → **valid**, emit no error.
    - **Partial**: `m` present in one but not both → **fail** with `enum <path> partial state
      for member <m>`.
    - Missing deferred declaration or manifest phase record for any `enum_extensions` entry
      → **fail** with `enum_extensions[schema][path] member <m> has no deferred declaration`.
  - Must not require `m` to be in `contract["enums"]` in pending state.
  - Must not crash on empty `{}` map.
  The ordinary actual-vs-floor enum comparison (§5.6 exact equality) is **separate** and
  still runs: it compares `contract["enums"][path]` against `frozen_behavior.enum_floors[path]`
  and fails on any member that is neither a floor member nor an `enum_extensions` pending member.
- [ ] Add constitution content floor enforcement per §5.5 (exact set equality throughout):
  rule ID-set equality + exact text; invariant ID-set equality + exact text;
  `banned_terms_exact_values` exact array equality per tier; `banned_terms_exact_scalars` exact
  scalar equality;   `banned_terms_optional_entries` authoritative-key presence check + value equality check
  (`actual[key] == floor[key]`, both nonempty strings) + unrecorded-extra-key check
  (excluding `note` metadata); `operator_outcomes_exact_members`
  exact array equality. Do **NOT** assert individual `machine_checks[key]["status"]` values.
- [ ] Emit path-specific diagnostics with `DROPPED`, `ADD`, `RETYPED` prefixes; include schema
  and dotted path, e.g. `intent-feedback/v1 optional_keys.correction DROPPED`.
- [ ] Update checker comment header: "Frozen behavior authority is
  `contracts/additive-manifest.json::frozen_behavior`. Contract JSON is the actual declared
  shape. `FROZEN_SCHEMAS` is the bootstrap trust anchor (schema IDs only); manifest owns
  filenames and status."
- [ ] **Retain/derive all existing checker protections** (do not remove; derive from manifest or
  keep as is where manifest supplies the value):
  - `contract["version"] == 1` (integer) → fail: `version not 1`
  - `contract["schema"]` appears in `contract["freeze_strings"]` list → fail: `freeze_strings missing schema`
  - `contract["freeze_exempt"] is False` (boolean False, not just falsy) → fail: `freeze_exempt must be false`
  - `contract["frozen"]` is a nonempty string → fail: `frozen date missing or empty`
  - Contract JSON is valid (duplicate-key-rejected parse, per §5.2 step 2) → already guaranteed
    by the manifest bootstrap contract-load step
  - `contract["schema"] == schema` (matches manifest-declared schema ID) → already in step above
  - `contract["status"] == "frozen"` (matches manifest-declared status) → already in step above
- [ ] Retain `deferred_additions` object presence check.
- [ ] Check for **unexpected `*.v1.json` files**: after loading the five declared contracts, scan
  `contracts_root` for any `*.v1.json` file whose filename is **not** one of the five manifest-declared
  filenames; reject every such file unconditionally, regardless of its internal schema → fail:
  `undeclared contract file: <name>`. This applies whether the file's internal `schema` field is in
  `FROZEN_SCHEMAS`, duplicates a known schema, or is entirely unknown — the presence of any
  undeclared `*.v1.json` file is the failure condition, not the schema it claims.
- [ ] Remove dead provisional branch logic (the checker had a code path handling `freeze_exempt: true`
  or non-frozen status separately); semantics are now covered by the explicit `freeze_exempt is False`
  and `status == "frozen"` checks derived above — remove the unreachable branch.
- [ ] Remove the now-redundant embedded `FLOOR`, `NESTED_FLOOR`, and `ENUM_FLOOR` constants.

**Tests:**

```bash
bash checks/intent-contract-freeze.sh    # must pass on real tree
```

**Acceptance:**
- Current repository passes (exit 0).
- Removing `correction` now fails with `DROPPED` in output.
- No embedded floor constants remain: `rg 'NESTED_FLOOR|ENUM_FLOOR|^FLOOR\s*=' checks/intent-contract-freeze.sh`
  returns nothing.
- `rg 'EXPECTED' checks/intent-contract-freeze.sh` returns nothing (replaced by `FROZEN_SCHEMAS`).

**Rollback:** T1+T2 governed revert before any later optional/enum authority depends on this
floor. After dependency, forward-fix only.

**Dependencies:** T1 must be staged or complete.

---

### Task G0-R0-T4 — Shared validator and path-qualified additive semantics

**Execution order note:** T4 runs **before T3**. T3's adversarial matrix imports
`tests/freeze_helpers.py` and calls `validate_additive_bundle`; T4 creates both.

**Purpose:** Create the shared pure Python validator; replace unqualified key flattening with
path-qualified identity; add bidirectional `enum_extensions` validation.

**Files:**
- `tests/freeze_helpers.py` (new, required)
- `tests/test_additive_compat.py`

**Steps:**

- [ ] Create `tests/freeze_helpers.py` exporting `validate_additive_bundle(contracts_root: Path) -> list[str]`.
  This function mirrors the manifest-loading and frozen_behavior validation logic of the shell
  checker: loads and bootstrap-validates the manifest, then for each schema checks required_keys,
  optional_keys, nested, enum_floors, enum_extensions (five-surface state per §5.4), and
  content_floors (exact set equality per §5.5, including `banned_terms_optional_entries`
  pending-state acceptance) against the actual contract. For `banned_terms.optional` deferred
  targets, accepts pending state (key absent from both surfaces) without error. Returns a list
  of error strings (empty means valid). Calls from test code pass the real `_CONTRACTS` path
  or a temp bundle path; no hardcoded paths. Running on the current real contracts root must
  return `[]` (including passing the `tier_a_consumer_contributed` pending declaration).
- [ ] In `tests/test_additive_compat.py`, import and use `validate_additive_bundle` on the real
  contracts root to ensure the real bundle passes the Python validator (as a class-level check).
- [ ] Replace `_added_keys_by_contract()` with a **bidirectional canonical join** over the
  UNION of all sources (§5.7): iterate the full union of manifest phase records AND contract
  declarations AND enum_extensions entries. For each manifest `(phase, schema, key)` find
  exactly one declaration in `contract.deferred_additions[phase]` where `declaration["key"] == key`
  (zero → orphan manifest record; multiple → ambiguous). For each contract declaration find
  exactly one manifest record (zero → orphan declaration). For each enum_extensions member
  find exactly one enum declaration and vice versa. Never iterate only one side.
  Canonical path-qualified identity: `declaration["target"] + "." + key`.
  Supported `target` values: `top.optional`, `nested.<container>.optional`, `enum.<path>`,
  `banned_terms.optional`. Unknown target → fail immediately.
  Apply type rules per §5.7 per-target table; type mismatches fail with specific diagnostic.
  Scope boundary: base frozen fields in `frozen_behavior.optional_keys` (e.g. `correction`) are
  NOT deferred additions; skip them in the join — their coverage comes from §5.6 floor comparison.
  Update all call sites and their diagnostics.
- [ ] Update `test_manifest_and_contracts_agree` to use path-qualified keys in diagnostics.
- [ ] Update `test_every_deferred_addition_is_genuinely_additive` to use path-qualified keys.
- [ ] Add `test_promotion_state_semantics`: for each deferred optional/nested addition across all
  contracts, assert the path-qualified key is either fully absent from both `frozen_behavior`
  optional/nested floors AND actual contract optional/nested keys (pending), or fully present in
  both with matching types (authoritative). For `banned_terms.optional` targets: pending state
  means key absent from actual `banned_terms` AND from `content_floors.banned_terms_optional_entries`;
  authoritative state means key present in both with matching semantic type. Any partial state
  must fail. Verify that `tier_a_consumer_contributed` at `banned_terms.optional` is in valid
  pending state on the current real tree.
- [ ] Add `test_enum_extensions_bidirectional`: for each schema, verify
  `manifest["enum_extensions"][schema]` and `contract.deferred_additions[*][target=enum.*]` are
  mutually consistent; assert both are currently empty (`{}`).
- [ ] Add `test_enum_extensions_is_an_object`: assert `manifest["enum_extensions"]` is a dict
  with exactly the five schema keys, each value a dict (may be empty).
- [ ] Add `test_frozen_behavior_coverage`: assert `frozen_behavior` has exactly the five schema
  keys; each entry has `required_keys`, `optional_keys`, `nested`, `enum_floors`, `content_floors`
  keys; each is the correct type (object or null).
- [ ] Add `test_pending_deferred_additions_absent_from_floor`: every deferred optional/nested
  addition whose key is absent from the actual contract optional/nested keys must also be absent
  from `frozen_behavior` optional/nested floors (confirms pending state).
- [ ] Preserve all existing `TestAdditiveCompat` tests; update internal helpers to use
  path-qualified keys where needed.
- [ ] **Skew boundary comment:** add a comment block: "These tests prove checker and metadata
  acceptance only. Runtime reader-compatibility evidence for optional fields and enum extensions
  is required separately before any writer emits an addition."
- [ ] If the full suite fails for any reason other than the guard becoming too strict on
  already-valid data, **stop and return to the operator**.

**Tests:**

```bash
python3 -m unittest tests.test_additive_compat
```

**Acceptance:**
- `tests/freeze_helpers.py` created; `validate_additive_bundle` callable; returns `[]` on real
  contracts root.
- Path-qualified diagnostics name the full dotted path in every error.
- `enum_extensions` validated bidirectionally; currently asserts `{}` for all schemas.
- Full existing `TestAdditiveCompat` suite unchanged-green.

**Rollback:** Governed revert before dependencies; forward-fix after.

**Dependencies:** T1–T2.

---

### Task G0-R0-T3 — Generate adversarial freeze matrix

**Execution order note:** T3 runs **after T4** (requires `tests/freeze_helpers.py`).

**Purpose:** Prove every accepted field/member bites through the shipped checker; add shipped-
checker-level manifest negative tests; run one coherent optional fixture and one coherent enum
fixture invoking both validators on the same bundle.

**Files:**
- `tests/test_contract_freeze.py`
- `tests/freeze_helpers.py` (import from T4)

**Shared helper pattern:** Extend `_run_checker_against` to accept an optional `mutate_manifest`
callable alongside `mutate`. Both receive the temp contracts directory `cdir`. Set
`INTENT_CONTRACT_DIR=str(cdir)` (not `INTENT_HOME`) in the subprocess env. After running the
shell checker, call `validate_additive_bundle(cdir)` on the same `cdir` for coherent bundle
fixtures. No fixture may split: the shell checker and Python validator must always see the same
directory.

**Manifest bootstrap negative tests (shipped-checker level):**

Protocol header:
- [ ] Manifest `schema` field missing or wrong value → fail; output contains `schema header invalid`
- [ ] Manifest `version` field missing, wrong type (string `"1"`), or wrong value (`2`) → fail; contains `version header invalid`

Duplicate-key rejection:
- [ ] Manifest with a duplicate top-level JSON key (e.g. `"frozen_behavior"` twice) → fail; contains `duplicate key`
- [ ] Contract file with a duplicate JSON key → fail; contains `duplicate key`

File existence and JSON validity:
- [ ] Manifest file not valid JSON (e.g. truncated/malformed) → fail; output contains `not valid JSON`
- [ ] Missing/unreadable manifest file → fail; output contains `manifest MISSING`

Filename safety:
- [ ] `file` value contains a `/` (e.g. `"sub/intent-catalog.v1.json"`) → fail; contains `unsafe`
- [ ] `file` value is an absolute path (e.g. `"/tmp/intent-catalog.v1.json"`) → fail; contains `unsafe`
- [ ] `file` value is `".."` or `"../"` → fail; contains `unsafe`
- [ ] `file` set to an empty string `""` → fail
- [ ] `file` set to a non-string (e.g. integer `1`) → fail
- [ ] `file` value does not end with `.v1.json` → fail; contains `unsafe`

`frozen_behavior` structure:
- [ ] Remove `frozen_behavior` from manifest → fail; output contains `frozen_behavior missing`
- [ ] Set `frozen_behavior` to an array → fail; output contains `not an object`
- [ ] Add an extra schema key to `frozen_behavior` → fail; output contains `unexpected schema`
- [ ] Remove one schema key from `frozen_behavior` → fail; output contains `missing schema`
- [ ] Two entries with the same `file` value → fail; output contains `duplicate filename`
- [ ] `status` set to a non-`"frozen"` string (e.g. `"provisional"`) → fail
- [ ] `optional_keys` key absent from a `frozen_behavior` entry → fail
- [ ] Set `frozen_behavior[schema].required_keys` to an array → fail; names schema and bad type
- [ ] Set a `nested` container's `optional_keys` to `null` → fail
- [ ] Set an `enum_floors` entry to a non-array → fail
- [ ] Set an `enum_floors` entry to an array containing a non-string member → fail
- [ ] `content_floors` key absent from a `frozen_behavior` entry → fail
- [ ] `content_floors` set to `null` for `intent-constitution/v1` (must be an object) → fail
- [ ] `content_floors` set to a non-null value (e.g. `{}`) for a non-constitution schema (must be null) → fail
- [ ] `required_keys` map has an empty-string key → fail
- [ ] `required_keys` map has an empty-string value → fail
- [ ] `optional_keys` map has an integer value (wrong type, not nonempty string) → fail
- [ ] `nested` container value missing `required_keys` sub-key → fail
- [ ] `nested` container value missing `optional_keys` sub-key → fail
- [ ] `nested` container `optional_keys` set to `null` → fail
- [ ] `enum_floors` path key is an empty string → fail
- [ ] `content_floors.rules` set to an array instead of object → fail
- [ ] `content_floors.kernel_invariants` has an empty-string key → fail
- [ ] `content_floors.banned_terms_exact_values` set to a non-object (e.g. array) → fail
- [ ] `content_floors.banned_terms_exact_scalars` has an empty-string value → fail
- [ ] `content_floors.banned_terms_optional_entries` entry value is a non-string (e.g. object `{"type":"note","value":"x"}`) → fail
- [ ] `content_floors.banned_terms_optional_entries` entry value is an empty string `""` → fail
- [ ] `content_floors.operator_outcomes_exact_members` set to a non-array → fail
- [ ] `content_floors.operator_outcomes_exact_members` contains a duplicate string → fail

`enum_extensions` structure:
- [ ] `enum_extensions` missing one of the five schema keys → fail
- [ ] `enum_extensions` containing an extra (sixth) schema key → fail
- [ ] `enum_extensions[schema]` set to a non-object (e.g. array) → fail
- [ ] `enum_extensions[schema][path]` path key is an empty string → fail
- [ ] `enum_extensions[schema][path]` value is a non-array (e.g. string) → fail
- [ ] `enum_extensions[schema][path]` array containing a duplicate string member → fail
- [ ] `enum_extensions[schema][path]` containing a non-string member → fail

`required_additive_phases` / `deferred_phases` structure:
- [ ] `required_additive_phases` set to a non-array → fail
- [ ] `deferred_phases` set to a non-object → fail
- [ ] Phase spec `kind` set to an unsupported value (e.g. `"breaking"`) → fail
- [ ] Additive phase with `contracts` object containing an unknown schema key → fail
- [ ] Required phase listed in `required_additive_phases` missing from `deferred_phases` → fail

Deferred declaration validation:
- [ ] Contract `deferred_additions[phase]` set to a non-array → fail
- [ ] Declaration entry missing `target` field → fail; contains `deferred declaration invalid`
- [ ] Declaration entry with unsupported `target` (e.g. `"unknown.target"`) → fail

**Existing-protection adversarial tests (shipped-checker level):**

- [ ] Contract `version` changed from `1` to `2` → fail; output contains `version not 1`
- [ ] `freeze_strings` list does not contain the schema ID → fail; contains `freeze_strings missing schema`
- [ ] `freeze_exempt` set to `true` → fail; contains `freeze_exempt must be false`
- [ ] `frozen` date field set to empty string `""` → fail; contains `frozen date missing`
- [ ] `frozen` date field removed entirely → fail; contains `frozen date missing`
- [ ] Contract file is invalid JSON → fail; contains `not valid JSON` for that contract
- [ ] Manifest-declared `file` value references a file that does not exist in `cdir` → fail;
  contains `missing` or file not found diagnostic
- [ ] Add an undeclared `*.v1.json` file to `cdir` whose internal `schema` is an unknown string
  not in `FROZEN_SCHEMAS` → fail; output contains `undeclared contract file`
- [ ] Add an undeclared `*.v1.json` file to `cdir` whose internal `schema` duplicates one of the
  five `FROZEN_SCHEMAS` values → fail; output contains `undeclared contract file` (the filename
  check fires before schema inspection; both variants must fail)

**Table-driven required/optional field tests:**

- [ ] For every required key across all five contracts (`@subTest` loop enumerating
  `frozen_behavior`): remove the key → fail with `DROPPED` and schema/key path.
- [ ] For every required key: retype to `"__sentinel__"` → fail with `RETYPED`.
- [ ] Add a new required key (top-level and one nested representative) → fail with `ADD`.
- [ ] Remove `intent-feedback/v1.optional_keys.correction` (explicit named test, not only table
  entry) → fail with `DROPPED` and `correction` in output.
- [ ] Retype `correction` from `object|null` to `object` (union narrowing) → fail with `RETYPED`
  including both original and narrowed types.
- [ ] Remove `intent-catalog/v1.nested.param.optional_keys.enum` → fail.
- [ ] Remove `intent-catalog/v1.nested.param.optional_keys.source` → fail.

**Enum member tests:**

- [ ] For every enum floor entry across all five contracts (subTest loop): remove one floor member
  → fail with `dropped frozen value`.
- [ ] Explicit cases: `feedback.verdict`; `catalog.param.type`; `catalog.param.source`;
  `constitution.machine_check.status` member removals.
- [ ] Add an extra member to a contract's `enum` without updating `frozen_behavior.enum_floors`
  → fail with `unrecorded member` (extra actual member fails exact equality).
- [ ] **Allowed transition:** update a constitution machine_check entry's `status` from `spec` to
  `active` without mutating `enum_floors` → must PASS.

**Constitution content floor tests:**

- [ ] Change CR1 rule text → fail with rule-ID and `text CHANGED`.
- [ ] Remove rule CR2 from rules array → fail (dropped ID).
- [ ] Add a rule ID to actual rules without updating `content_floors.rules` → fail (`unrecorded rule ID`).
- [ ] Change KI1 invariant text → fail.
- [ ] Remove a member from `banned_terms.tier_a_generic_mechanism` → fail.
- [ ] Add an extra member to actual `tier_a_generic_mechanism` without updating floor → fail (`unrecorded`).
- [ ] Remove `abort` from `operator_outcomes` → fail.
- [ ] Add extra member to actual `operator_outcomes` without updating floor → fail.
- [ ] Change actual `tier_c_consumer_contributed` scalar value → fail.

**Sanctioned content extension fixture (coherent; both validators):**

- [ ] **Content extension fixture:** in the temp bundle:
  1. Add `{"id":"CR99","rule":"<exact test rule text>","enforcement":"no_execution_path"}` to
     `intent-constitution.v1.json.rules` (all three fields required by the real rule schema).
  2. Add `"CR99": "<exact test rule text>"` to `manifest.frozen_behavior["intent-constitution/v1"].content_floors.rules`.
  Run shell checker (`INTENT_CONTRACT_DIR=cdir`) → exit 0. Run `validate_additive_bundle(cdir)` → no errors.
  This confirms sanctioned content additions work when both surfaces are updated coherently.

**Table-driven promotion-state tests (same-cdir, both validators, all supported targets):**

For each supported target type, test the following states using synthetic temp entries (real bundle
lacks authoritative promotions today; use temp bundles only, never committed contracts):

- [ ] **top.optional — pending valid:** declaration in contract `deferred_additions` + manifest
  record + absent from actual `optional_keys` + absent from `frozen_behavior.optional_keys` →
  shell checker exit 0, `validate_additive_bundle` returns `[]`.
- [ ] **top.optional — authoritative valid:** all surfaces agree (declaration + record + actual
  optional_key + floor optional_key, same type) → both validators pass.
- [ ] **top.optional — actual-only partial fails:** key in actual `optional_keys` but not in floor
  → `ADD unrecorded optional` from both validators (same cdir).
- [ ] **top.optional — floor-only partial fails:** key in floor `optional_keys` but not in actual
  → `DROPPED frozen optional` from both validators.
- [ ] **top.optional — type mismatch fails:** key in both, type differs between actual and floor
  → `RETYPED` from both validators.
- [ ] **top.optional — missing manifest record fails:** declaration in contract but no manifest
  phase record → `orphan declaration` fail.
- [ ] **top.optional — orphan manifest record fails:** manifest record but no contract declaration
  → `orphan manifest record` fail.
- [ ] **nested.<container>.optional — pending valid:** declaration + manifest record; key absent
  from both nested actual optional_keys and nested frozen floor → both validators pass.
- [ ] **nested.<container>.optional — authoritative valid:** all surfaces agree → both pass.
- [ ] **nested.<container>.optional — actual-only partial fails:** key in nested actual but not
  floor → both validators fail.
- [ ] **nested.<container>.optional — floor-only partial fails:** key in nested floor but not
  actual → both validators fail.
- [ ] **nested.<container>.optional — type mismatch fails:** key in both, types differ → both fail.
- [ ] **nested.<container>.optional — missing manifest record fails** → `orphan declaration` fail.
- [ ] **nested.<container>.optional — orphan manifest record fails** → `orphan manifest record` fail.
- [ ] **enum — pending valid, authoritative valid, actual-only partial, floor-only partial,
  missing enum_extensions entry, orphan enum_extensions entry:** as above, adapted for five-surface
  state (both validators same cdir).
- [ ] **banned_terms.optional — pending valid (current real state):** `validate_additive_bundle`
  on real tree returns `[]` for `tier_a_consumer_contributed` pending declaration.
- [ ] **banned_terms.optional — authoritative valid:** key in actual `banned_terms` (nonempty
  string value) and identical nonempty string in `banned_terms_optional_entries[key]` → both pass.
- [ ] **banned_terms.optional — value mismatch fails:** key present in both surfaces but values
  differ → both validators fail (mismatch between actual and floor string).
- [ ] **banned_terms.optional — actual-only partial:** key in actual `banned_terms` but not in
  `banned_terms_optional_entries` → fail (unrecorded optional key).
- [ ] **banned_terms.optional — floor-only partial:** key in `banned_terms_optional_entries` but
  not in actual `banned_terms` → fail (authoritative entry without actual key).

**Unrecorded optional addition:**

- [ ] Add key to a contract's `optional_keys` without updating `frozen_behavior` → fail with
  `ADD unrecorded optional`.

**Sanctioned coherent fixtures (one optional, one enum — each invokes both validators):**

- [ ] **Optional fixture:** in the temp bundle:
  1. Add `{"key":"test_sanctioned","type":"string","target":"top.optional"}` to
     `intent-map.v1.json.deferred_additions.test_phase`.
  2. Add `test_sanctioned: string` to `intent-map.v1.json.optional_keys`.
  3. Add `test_sanctioned: string` to `manifest.frozen_behavior["intent-map/v1"].optional_keys`.
  4. Add `manifest.deferred_phases.test_phase` = `{"kind":"additive","contracts":{"intent-map/v1":["test_sanctioned"]}}`.
  Run shell checker (`INTENT_CONTRACT_DIR=cdir`) → exit 0. Run `validate_additive_bundle(cdir)` → no errors.

- [ ] **Enum fixture:** in the temp bundle:
  1. Add `{"key":"test_ext","type":"enum-member","target":"enum.outcome"}` to
     `intent-feedback.v1.json.deferred_additions.test_enum_phase`.
  2. Add `test_ext` to `intent-feedback.v1.json.enums.outcome`.
  3. Add `test_ext` to `manifest.frozen_behavior["intent-feedback/v1"].enum_floors.outcome`.
  4. Add `manifest.enum_extensions["intent-feedback/v1"].outcome = ["test_ext"]`.
  5. Add `manifest.deferred_phases.test_enum_phase` = `{"kind":"additive","contracts":{"intent-feedback/v1":["test_ext"]}}`.
  Run shell checker → exit 0. Run `validate_additive_bundle(cdir)` → no errors.

Both fixtures use only temp bundles; they never touch committed contract files.

**Existing regression suite:**

- [ ] All existing `TestContractFreeze` and `TestContractFreezeRegression` tests pass unchanged.

**Tests:**

```bash
python3 -m unittest tests.test_contract_freeze
```

**Acceptance:**
- Every inventory field is covered by the table-driven loop or an explicit named test.
- `correction` defect closed by a named test.
- Sanctioned optional and enum fixtures pass both validators on the same bundle.
- machine_check activation passes.
- Every enumerated bootstrap/protection negative row above has exactly one shipped-checker test
  (no numeric floor count; the exhaustive row list is the requirement).
- Promotion-state table-driven tests cover all four supported targets (top.optional,
  nested.<container>.optional, enum, banned_terms.optional) with pending/authoritative/partial/
  type-mismatch/orphan cases through the same cdir for both validators.

**Rollback:** Same dependency rule as T2.

**Dependencies:** T1, T2, T4.

---

### Task G0-R0-T-AGENTS — Fix AGENTS.md stale freeze-timing sentence

**Purpose:** Narrow documentation truth correction. The freeze-timing block in `AGENTS.md` (line
21) states `intent-proposal/v1` is `PROVISIONAL — do NOT freeze it until A0 exercises it`. This
is factually wrong: the contract is already frozen (status `"frozen"`, `freeze_exempt: false`,
`frozen` date recorded) as proven by `tests.test_contract_freeze.test_proposal_is_frozen` and the
checker itself. Correct the sentence so the document matches reality.

**Files:**
- `AGENTS.md`

**Steps:**

- [ ] Locate the freeze-timing block (around line 21). The current sentence is:
  `contract are FROZEN. \`intent-proposal/v1\` is PROVISIONAL — do NOT freeze it until A0exercises it`
  (exact text may have minor formatting differences on disk; verify before editing).
- [ ] Replace it with:
  `contract are FROZEN. \`intent-proposal/v1\` is FROZEN — held provisional through P0/R-core and frozen in A0 after the first-consumer seam exercised it.`
  Keep the surrounding sentence structure intact; do not alter any other line.
- [ ] Add a regression test in `tests/test_contract_freeze.py`:

  ```python
  def test_agents_md_freeze_timing_is_current(self):
      """AGENTS.md must not contain the stale 'intent-proposal/v1 is PROVISIONAL' claim."""
      agents_md = (_REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
      self.assertNotIn(
          "intent-proposal/v1` is PROVISIONAL",
          agents_md,
          "AGENTS.md contains stale freeze-timing claim; intent-proposal/v1 is frozen",
      )
      # Consistency: the contract itself must also be frozen.
      c = json.loads((_CONTRACTS / "intent-proposal.v1.json").read_text(encoding="utf-8"))
      self.assertEqual(c["status"], "frozen", "contract status must be frozen")
      self.assertIs(c.get("freeze_exempt"), False)
  ```

- [ ] Run `python3 -m unittest tests.test_contract_freeze.TestContractFreeze.test_agents_md_freeze_timing_is_current`
  before and after the edit to confirm it fails before and passes after.

**Tests:**

```bash
python3 -m unittest tests.test_contract_freeze.TestContractFreeze.test_agents_md_freeze_timing_is_current
```

**Acceptance:**
- The stale "PROVISIONAL" sentence is gone from `AGENTS.md`.
- The replacement sentence accurately reflects the frozen state.
- The regression test passes.
- No other AGENTS.md content is changed.

**Rollback:** Revert the one-sentence edit; forward-fix the regression test separately.

**Dependencies:** None (independent of T1–T4; may run in parallel).

---

### Task G0-R0-T5 — Deliver one router PR (child delivery)

**Purpose:** Establish the G0-R0 child receipt without claiming broader G0 completion.

**Files:** All allowlisted files from T1–T4 and T-AGENTS; no `.github/*`, `status.yml`,
`RESUME.md`, `Makefile`, `tests/run-tests.sh` changes.

**Steps:**

- [ ] Run focused tests, `make verify`, `make status-verify`, and `git diff --check`.
- [ ] Local preflight (before opening PR): verify changed-path isolation.
  ```bash
  git fetch origin main
  BASE=$(git merge-base HEAD origin/main)
  git diff --name-only "$BASE"...HEAD | sort
  git status --porcelain
  ```
  Assert diff shows **exactly** the six required §7 paths (no more, no fewer); `docs/plans/` must
  not appear; working tree must be clean. Stop if either assertion fails.
- [ ] Confirm no product contract content changed:
  ```bash
  git diff "$BASE"...HEAD -- contracts/intent-*.v1.json
  ```
  Must show no diff (fixtures are temp-bundle-only; no committed contract file changes).
- [ ] Confirm zero-link green: `python3 -m unittest tests.test_zero_link`.
- [ ] Open one **Draft** G0-R0 router PR. Do not pre-arm or bypass automation.
- [ ] Run governed review cadence: `/loop /review-bugbot` until no actionable findings remain.
- [ ] Capture the PR's metadata before merge and assert `baseRefName == main`:
  ```bash
  gh pr view <PR-number> --json baseRefName,baseRefOid,headRefOid,url
  ```
  Assert `baseRefName == "main"` — fail if not (wrong base branch). Record `baseRefOid` (PR base
  SHA) and `headRefOid` (PR head SHA). Note: `make status-verify` independently proves PR existence
  and merge-commit ancestry via `status.yml`, but does NOT prove GitHub PR-to-merge linkage; that
  linkage is verified separately in the child receipt below. Verify both required checks
  appear on the exact `headRefOid`:
  ```bash
  gh api repos/KleinPerkins/intent-router/commits/<headRefOid>/check-runs \
    --jq '.check_runs[] | {name:.name, conclusion:.conclusion, head_sha:.head_sha}'
  ```
  Required: both `pr-automation / verify` AND `pr-automation / job:repo.intent-router.m3-verify`
  must show `conclusion: success` against `<headRefOid>`. If either check is absent, queued, or
  non-success — **keep PR in Draft, do not arm auto-merge, stop for controller authority**.
- [ ] Confirm the six-path diff between `baseRefOid` and `headRefOid` via GitHub:
  ```bash
  gh api repos/KleinPerkins/intent-router/compare/<baseRefOid>...<headRefOid> \
    --jq '[.files[].filename] | sort'
  ```
  Must equal the exact six §7 paths.
- [ ] After the governed merge, capture the merge commit SHA:
  ```bash
  gh pr view <PR-number> --json mergeCommit --jq '.mergeCommit.oid'
  ```
  Verify it is an ancestor of fetched `origin/main`:
  ```bash
  git fetch origin main
  git merge-base --is-ancestor <mergeCommitSHA> origin/main && echo "ancestor: OK"
  ```
- [ ] Capture the exact child receipt (all three SHAs required):
  - PR URL
  - PR base SHA (`baseRefOid`)
  - PR head SHA (`headRefOid`)
  - Merge commit SHA
  - Both check names and `conclusion: success` against exact head SHA
  - Manifest digest: `shasum -a 256 contracts/additive-manifest.json`
  - Checker digest: `shasum -a 256 checks/intent-contract-freeze.sh`
  - Test evidence: focused tests + `make verify` + `make status-verify` output
- [ ] Hand the receipt to G0-R; do not claim composite G0 or G0-R closed.

**Tests:**

```bash
python3 -m unittest tests.test_contract_freeze tests.test_additive_compat
make verify
make status-verify
```

**Acceptance:**
- Exact merged receipt exists.
- No later additive authority has landed ahead of G0-R0.
- No runner configuration changed.
- No product contract content changed.
- Changed-path assertion passes (only allowlisted paths differ).

**Rollback:** Before dependent additions, governed revert of the G0-R0 PR is allowed. Once a
later v1 optional/enum authority depends on the guard, weakening or revert is forbidden;
forward-fix in a new PR is the only safe response.

**Dependencies:** T1, T2, T4, T3, T-AGENTS; operator approval to implement/merge (this DRAFT
plan grants neither).

---

## 9. Ledger and resume handling

G0-R0 is a **child delivery** inside the composite G0-R convergence checkpoint, not a standalone
repository phase. The G0-R0 implementation PR does **not** touch `status.yml` or `RESUME.md`.

Why this complies with AGENTS.md phase-ledger policy:

- `status.yml` entries encode the phase ladder; `tests.test_status_verify._ALL_PHASES` recomputes
  every `done` claim against disk + tests.
- A `done` row requires a real PR URL, an exact resolvable/ancestor merge commit, and passing
  `passed_test_ids`. Those artifacts do not exist until after the implementation PR merges.
- Marking a phase `done` before the merge commit exists is exactly the class of ledger dishonesty
  that `make status-verify` was built to catch.
- `current_phase` in `status.yml` must equal the first non-done router phase; changing it before
  the commit exists would create a stale `current_phase` that `make status-verify` would reject.

Therefore:

1. G0-R0 PR changes only freeze metadata/checker/tests/AGENTS.md.
2. Its merge/check receipt proves the child delivery.
3. The subsequent G0-R authority-honesty PR adds the `G0-R0` done row, updates the phase
   parser/test expected IDs, introduces the composite G0 checkpoint, and regenerates `RESUME.md`.
4. The row may be `done` only when it pins the real merged G0-R0 commit, PR, files, and passing
   test IDs.
5. Completed P0/R-core/A0/egress evidence is preserved exactly; no historical test meaning
   changes.

---

## 10. Runnerless remote proof

**Confirmed live configuration (verified 2026-09-02 from `.github/pr-automation.json` and
`.github/pr-automation.lock.json`):**

- Aggregate check name: `pr-automation / verify` — owned by verifier App 4274739
- Job IDs in lock: `canned.repository-contract.v1` (runs first) and `repo.intent-router.m3-verify`
  (depends on first; runs `bash tests/run-tests.sh`)
- Live branch rules require **both** contexts from verifier App 4274739:
  `pr-automation / verify` AND `pr-automation / job:repo.intent-router.m3-verify`
- Unittest discovery in `bash tests/run-tests.sh`: every `tests/test_*.py`

**Execution status:** PR #53 (https://github.com/KleinPerkins/intent-router/pull/53) merged with
empty `statusCheckRollup` — the configuration is present and locked but execution is **not
live-proven**. The controller remains paused as of 2026-09-02.

**Remote-proof requirement:** Before claiming remote proof complete:

1. Fetch live branch rules using the ruleset-aware endpoint (the classic `branches/main/protection`
   endpoint returns 404 for ruleset-governed repos):
   ```bash
   gh api repos/KleinPerkins/intent-router/rules/branches/main \
     --jq '.[] | select(.type == "required_status_checks") | .parameters.required_status_checks'
   ```
   Parse/select the `required_status_checks` rule; assert **both** contexts are present with
   integration 4274739: `pr-automation / verify` AND `pr-automation / job:repo.intent-router.m3-verify`.
2. Require **both** `pr-automation / verify` AND `pr-automation / job:repo.intent-router.m3-verify`
   to appear with `conclusion: success` on the **exact PR head SHA** (not a prior commit).
3. If the controller remains paused, checks are absent, queued, or either context is not
   `success` on the exact head: **keep the PR in Draft, do not arm auto-merge, and stop for
   controller authority**. Do not edit protected runner config, recipe lock, or `.github/` files.

Local `make verify` is mandatory because it separately executes the shell freeze checker, strict
status verification, and install static check. Local `make status-verify` is rerun explicitly as
part of T5 evidence. Local proof stands independently of remote proof status.

Canonical remote recipe hardening to `make verify` belongs to the G0-R authority honesty child
delivery, not this phase.

---

## 11. Acceptance ledger and traceability

Every criterion maps to an exact command, assertion, or artifact. Tautological exact-schema-set
assertions (e.g. "the manifest has exactly five schemas and the contracts have exactly five schemas
— therefore they agree") are not retained as independent proof; the cross-validation tests provide
the actual evidence.

| Requirement | Deterministic evidence |
|---|---|
| Reproduced defect closed | `python3 -m unittest tests.test_contract_freeze.TestContractFreeze.test_dropping_correction_optional_fails` → non-zero with `correction` in diagnostic |
| All five contracts covered | `python3 -m unittest tests.test_additive_compat.TestAdditiveCompat.test_frozen_behavior_coverage` passes on real tree |
| Required floors preserved | Table-driven `@subTest` loop in `tests.test_contract_freeze.TestContractFreeze` covers every required remove/retype |
| Top optional floors frozen | `tests.test_contract_freeze.TestContractFreeze.test_dropping_correction_optional_fails` (named) + subTest loop |
| Nested optional floors frozen | `tests.test_contract_freeze.TestContractFreeze` explicit tests for `catalog.param.enum`, `catalog.param.source` removal |
| All enum floors frozen | Table-driven subTest loop covers every enum floor including `feedback.verdict`, `catalog.param.type`, `catalog.param.source`, `constitution.machine_check.status` |
| Union narrowing fails | `correction: object\|null → object` retype test in `tests.test_contract_freeze.TestContractFreeze` |
| Protocol header validation | `tests.test_contract_freeze.TestContractFreeze` negatives for schema/version header |
| Duplicate-key rejection | `tests.test_contract_freeze.TestContractFreeze` negatives for manifest and contract dup keys |
| Filename traversal prevention | `tests.test_contract_freeze.TestContractFreeze` negatives for `/`, absolute, `..` filenames |
| Bootstrap fail-closed | One shipped-checker test per enumerated negative row in T3 (exhaustive row list is the requirement) |
| Existing protections retained | Adversarial tests: version change, freeze_strings removal, freeze_exempt true, missing frozen date, invalid contract JSON, missing declared file, unexpected v1 schema |
| deferred_phases validation | `tests.test_contract_freeze.TestContractFreeze` negatives for malformed phase spec, unknown schema, missing required phase |
| Constitution content floors — exact rule/invariant ID-set | Rule removed → fail; unrecorded rule ID added → fail |
| Constitution content floors — banned/outcome exact sets | banned_term member removed + extra unrecorded → fail; tier_c scalar changed → fail; operator_outcome removed → fail |
| Sanctioned content extension works | Content extension fixture (CR99 with `enforcement` field) passes both validators on same bundle |
| `banned_terms.optional` pending state | `python3 -m unittest tests.test_additive_compat.TestAdditiveCompat.test_promotion_state_semantics` → `validate_additive_bundle` on real tree returns `[]` |
| machine_check activation allowed | `tests.test_contract_freeze.TestContractFreeze.test_machine_check_spec_to_active_passes` must PASS |
| Unrecorded optional addition fails | Optional key added without `frozen_behavior` update → `ADD unrecorded optional` |
| Unrecorded enum member fails | Extra actual enum member without floor update → `unrecorded member` |
| Sanctioned optional addition works | T3 optional fixture passes both validators on same cdir |
| Sanctioned enum extension works | T3 enum fixture passes both validators on same cdir |
| Promotion-state table-driven | All four targets (top.optional, nested.&lt;container&gt;.optional, enum, banned_terms.optional): pending/authoritative/partial/type-mismatch/orphan cases for each; same-cdir both validators |
| Bidirectional canonical join | `tests.test_additive_compat.TestAdditiveCompat` join iterates union of all sources; orphan manifest records and orphan declarations fail |
| Path-qualified identity | `tests.test_additive_compat.TestAdditiveCompat` diagnostics include full dotted path; (phase,schema,key) resolves uniquely |
| enum_extensions currently empty | `tests.test_additive_compat.TestAdditiveCompat.test_enum_extensions_bidirectional` asserts `{}` for all schemas |
| No embedded floor constants | `rg 'NESTED_FLOOR\|ENUM_FLOOR\|^FLOOR\s*=' checks/intent-contract-freeze.sh` returns nothing |
| No EXPECTED schema→filename dict | `rg 'EXPECTED' checks/intent-contract-freeze.sh` returns nothing |
| Legacy compatibility | `python3 -m unittest tests.test_contract_freeze tests.test_additive_compat` + `make verify` pass |
| CR1/CR2/CR5/KI1 unchanged | `make verify`; no runtime/consumer files changed |
| CR4/zero-link | `python3 -m unittest tests.test_zero_link`; additive/freeze tests pass |
| AGENTS.md stale claim corrected | `python3 -m unittest tests.test_contract_freeze.TestContractFreeze.test_agents_md_freeze_timing_is_current` passes |
| Changed-path isolation | Local: `git diff --name-only "$BASE"...HEAD`; GitHub: `gh api compare` — both show exactly the six §7 paths |
| Honest phase evidence | G0-R0 child receipt (base SHA + head SHA + merge SHA + both check conclusions); G0-R ledger row only after real merge |
| Local proof | Focused tests + `make verify` + `make status-verify` + `git diff --check` |
| Remote proof | `gh api repos/KleinPerkins/intent-router/rules/branches/main` confirms both required contexts; both show `conclusion: success` against exact head SHA; if controller paused, record absence and keep PR draft |
| One G0-R0 child/one PR | One G0-R0 router PR; no mixed G0-R changes |
| Skew boundary documented | `tests.test_additive_compat.TestAdditiveCompat` class comment; T5 confirms no product file diff |

---

## 12. Stop conditions and operator gates

Stop implementation and return to the operator if:

- Any fix requires changing a five-contract product field or member.
- Checker hardening rejects currently valid fixtures or readers without a metadata error.
- One declarative manifest cannot represent an existing contract's actual type semantics.
- A required test needs runtime, AWA, host, provider, State Controller, or registry work.
- Either `pr-automation / verify` or `pr-automation / job:repo.intent-router.m3-verify` is absent,
  queued, or non-success on the exact PR head SHA (controller paused; do not claim remote proof,
  do not edit `.github/` files or protected runner config; keep PR draft and stop for controller authority).
- Remote proof cannot be obtained without editing protected runner configuration.
- Zero-link fails.
- Completed phase evidence would need rewriting.
- An authoritative optional/enum addition has landed before the guard is in place.
- A far-reaching compatibility decision appears.
- A reviewer claims the checker must prove provenance completeness for arbitrary future
  coordinated edits (it cannot without an immutable baseline; stop and clarify the narrowed
  guarantee rather than silently adding a duplicate baseline).
- Constitution content floor requires freezing `machine_checks` per-entry status values
  (it does not; only the enum floor is frozen — but if a reviewer dispute arises, stop and
  clarify rather than guess).
- Any deferred optional field or enum member is being promoted to a writer before old-reader
  tolerance is proven for every affected consumer (§5.8 skew boundary).
- Sanctioned-addition or enum-extension test fixtures accidentally mutate real committed contract
  files (fixtures must be temp-bundle-only).
- `git diff --name-only "$BASE"...HEAD` shows any path outside the §7 required set, or shows
  fewer than the six required paths (both over- and under-delivery are stop conditions).
- The manifest has duplicate filenames across `frozen_behavior` entries or structurally invalid
  `enum_extensions` and the fix requires changing more than metadata/checker/tests.

Operator gates:

1. Accept/revise this plan before implementation.
2. Explicitly authorize the G0-R0 implementation PR.
3. Follow the repository's governed review/merge gate.
4. Accept the merged G0-R0 child receipt into composite G0/G0-R reconciliation.

---

## 13. Implementation-agent recommendation and cadence

Use the **deep** model tier with maximum available reasoning. Recommended concrete model:
`claude-opus-4-8-thinking-max`.

Rationale: the code change is small but mutates a frozen compatibility guard. The agent must
reason across shell-embedded Python, five declarative contract shapes, manifest bootstrap
validation, path-qualified additive state, enum extension tracking, constitution content floors
with exactly-scoped freezing (avoiding over-freezing lifecycle), generated adversarial testing,
coherent bundle injection, changed-path isolation, rollback semantics, and child-delivery ledger
policy. Economy/standard execution is not proportionate to that irreversibility risk.

Expected cadence after plan acceptance:

1. Implement T1 (manifest); confirm pre-T2 checker still passes.
2. Implement T2 (checker) in the same working branch; run `bash checks/intent-contract-freeze.sh`.
3. Implement T4 (freeze_helpers.py + path-qualified additive semantics); run
   `python3 -m unittest tests.test_additive_compat`.
4. Implement T3 (adversarial matrix, imports freeze_helpers); run
   `python3 -m unittest tests.test_contract_freeze`.
5. Implement T-AGENTS; run the regression test before and after the edit.
6. Run `make verify` and `make status-verify`; confirm all gates pass.
7. Open one **Draft** G0-R0 PR.
8. Run `/loop /review-bugbot` until no actionable findings remain.
9. Confirm exact-head runnerless verification.
10. Merge only through the governed operator/reviewer gate.
11. Capture the exact G0-R0 child receipt using `shasum -a 256` (macOS-compatible).
12. Stop before G0-R authority-honesty planning/reconciliation.

No implementation agent is launched by this plan.

---

## 14. Plan acceptance checkpoint

Accepting this plan authorizes neither code changes nor delivery. It approves G0-R0's exact
implementation scope, manifest structure, checker design, test strategy, and evidence model as
the basis for a future explicitly authorized one-PR implementation.

Decision:

> **Accept, revise, or reject `g0-r0-contract-freeze-hardening-v2.md` for a later explicitly
> authorized one-PR implementation.**
