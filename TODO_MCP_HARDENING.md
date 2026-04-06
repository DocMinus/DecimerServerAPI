# MCP / API Hardening Notes

These are intentionally non-breaking improvements to make DECIMER outputs easier to consume from MCP tool callers and API clients.

## Classifier threshold tightening

- Rename `IC_TRESHOLD` to `IC_THRESHOLD` and keep a compatibility alias if needed.
- Make threshold configurable via environment variable (`DECIMER_IC_THRESHOLD`) with default `0.3`.
- Include classifier metadata in `/image2smiles/` response:
  - `classifier_score`
  - `classifier_threshold`
  - `classifier_decision` (for example `structure_like` vs `not_structure_like`)

## Response semantics

- Keep existing `smiles` field for backward compatibility.
- Add explicit `reason` when `smiles` is `null`, for example:
  - `not_chemical_structure`
  - `prediction_failed`
  - `decode_failed`

## Input and safety controls

- Add request payload size guardrail for `encoded_image`.
- Return clear 4xx errors for malformed base64 and unsupported payload size.
- Keep temp-file cleanup in all execution paths.

## Optional compatibility improvements

- Support JSON request body in addition to form fields.
- Add a response model schema in FastAPI docs for stable client contracts.
