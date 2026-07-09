# Golden sets (scaffold — populated in R-core / A0)

This directory holds the router's **golden utterance sets**: the executable evaluation surface that
pins deterministic behavior. It is a scaffold in P0 (no routing logic yet) and is filled by:

- **R-core** — a first deterministic golden set proving L0–L2+L5 produce a valid conservative
  proposal with LLM OFF.
- **A0** — the AWA consumer golden set (25–30 utterances): ambiguous / destructive / injection /
  negative cases + cross-session re-entry + "is everything okay?" + calibration-review utterances.

## Locked format (decided in P0)

Each golden set is a JSON file: `<consumer>.golden.json`

```json
{
  "schema": "intent-golden/v1",
  "consumer": "<consumer id>",
  "catalog_version": "intent-catalog/v1",
  "cases": [
    {
      "utterance": "put this work somewhere safe",
      "expect_verb": "<verb or null>",
      "expect_verdict": "strong|weak|none",
      "expect_safety_class": "read|write|destructive",
      "expect_requires_confirmation": true,
      "notes": "why this case exists"
    }
  ]
}
```

## Locked invariant (decided in P0)

**Calibration must never regress the golden set.** Any calibration pass (C0 reviewable, C1
automatic) that would drop a previously-passing golden case ABORTS and keeps the last-good map.
This invariant is frozen now; its enforcing test is written in C0/C1 (see
`tests/test_deferred_spec.py` and the `spec` machine-checks in the constitution contract).
