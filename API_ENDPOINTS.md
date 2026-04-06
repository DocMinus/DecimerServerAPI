# API Endpoints

This document describes the HTTP endpoints exposed by `decimer_server.py`.

Base URL (default local): `http://localhost:8099`

## `GET /`

Simple health/status endpoint.

### Response `200`

```json
{
  "Message": "Image2smiles converter is up and running."
}
```

## `POST /image2smiles/`

Convert a base64-encoded image into a SMILES string.

### Request formats

Supported content types:
- `application/x-www-form-urlencoded`
- `multipart/form-data`
- `application/json`

Fields:
- `encoded_image` (required, string): base64-encoded image bytes
- `is_hand_drawn` (optional, bool or bool-like string, default `false`)
- `classify_image` (optional, bool or bool-like string, default `true`)

Accepted bool-like strings: `true/false`, `1/0`, `yes/no`, `on/off`.

### Successful response `200`

`smiles` remains present for backward compatibility.

```json
{
  "smiles": "CCO",
  "reason": null,
  "classifier_score": 0.12,
  "classifier_threshold": 0.3,
  "classifier_decision": "structure_like",
  "threshold": 0.3,
  "decision": "structure_like"
}
```

When classification says image is not structure-like:

```json
{
  "smiles": null,
  "reason": "not_chemical_structure",
  "classifier_score": 0.88,
  "classifier_threshold": 0.3,
  "classifier_decision": "not_structure_like",
  "threshold": 0.3,
  "decision": "not_structure_like"
}
```

Possible `reason` values when `smiles` is `null`:
- `not_chemical_structure`
- `decode_failed`
- `prediction_failed`

### Validation and error responses

- `400` malformed request payload (invalid JSON/form)
- `400` invalid base64 in `encoded_image`
- `413` `encoded_image` payload too large
- `422` missing/empty/invalid field values (for example missing `encoded_image`)

Error body format:

```json
{
  "message": "<error detail>"
}
```

## Environment Variables

- `DECIMER_IC_THRESHOLD` (float, default `0.3`): classifier decision threshold
- `DECIMER_IC_TRESHOLD` (legacy alias): compatibility alias for typo in older setups
- `DECIMER_MAX_ENCODED_IMAGE_BYTES` (int, default `6291456`): max encoded payload size in bytes
