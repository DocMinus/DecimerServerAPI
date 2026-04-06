"""
Mini-server for Decimer image to SMILES conversion
@author: Alexander Minidis (DocMinus)

license: MIT
Copyright (c) 2024 DocMinus
V0.0.1 - basic code for working server.
V0.0.2 - added the actual decimer conversion
V0.0.3 - added image classifier if actually a chemical structure or not
V0.0.4 - added image classifier based on score <0.3 instead of the True/False
V0.1.0 - V bump, now with encoding instead of file upload, works better with docker
V0.2.0 - one server version only that includes the classifier as optional
V0.2.1 - added threshold as variable
V0.3.0 - API hardening (threshold env config, metadata, reason codes, input validation)
2026-04-06
See Readme / requirements for dependencies
works on Linux and Windows, also Mac with GPU
"""

import base64
import binascii
import os
import tempfile

import uvicorn
from DECIMER.decimer import *
from decimer_image_classifier import DecimerImageClassifier
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

decimer_classifier = DecimerImageClassifier()


def _get_classifier_threshold() -> float:
    """Returns configured classifier threshold with safe default fallback."""

    default_threshold = 0.3
    configured_threshold = os.getenv("DECIMER_IC_THRESHOLD")
    if configured_threshold is None:
        configured_threshold = os.getenv("DECIMER_IC_TRESHOLD")
    if configured_threshold is None:
        return default_threshold

    try:
        return float(configured_threshold)
    except ValueError:
        return default_threshold


def _get_max_payload_size() -> int:
    """Returns max allowed encoded payload size in bytes."""

    default_limit = 6 * 1024 * 1024
    configured_limit = os.getenv("DECIMER_MAX_ENCODED_IMAGE_BYTES")
    if configured_limit is None:
        return default_limit

    try:
        limit = int(configured_limit)
    except ValueError:
        return default_limit

    return limit if limit > 0 else default_limit


IC_THRESHOLD: float = _get_classifier_threshold()
# Compatibility alias for previous typo-based variable name.
IC_TRESHOLD: float = IC_THRESHOLD
MAX_ENCODED_IMAGE_BYTES: int = _get_max_payload_size()


def _predict_smiles(encoded_image: any, hand_drawn: bool = False) -> str | None:
    """Predicts smiles representation of a molecule depicted in the given image.
    Taken from DECIMER.decimer and modified.

    Args:
        encoded_image (any): encoded image
        hand_drawn (bool): Flag to indicate whether the molecule in the image is hand-drawn

    Returns:
        str | None: smiles representation of the molecule in the input image, or None if prediction fails
    """

    model = DECIMER_Hand_drawn if hand_drawn else DECIMER_V2
    predicted_tokens, confidence_values = model(tf.constant(encoded_image))
    try:
        predicted_smiles = utils.decoder(detokenize_output(predicted_tokens))
    except:
        return None

    return predicted_smiles


app = FastAPI()


def _parse_bool(value, field_name: str, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized_value = value.strip().lower()
        if normalized_value in {"true", "1", "yes", "on"}:
            return True
        if normalized_value in {"false", "0", "no", "off"}:
            return False

    raise HTTPException(
        status_code=422,
        detail=(
            f"Field '{field_name}' must be a boolean or boolean-like string "
            "(true/false)."
        ),
    )


def _build_response(
    smiles,
    reason,
    classifier_score,
    threshold,
    decision,
):
    normalized_score = classifier_score
    if normalized_score is not None:
        try:
            normalized_score = float(normalized_score)
        except (TypeError, ValueError):
            if hasattr(normalized_score, "item"):
                normalized_score = float(normalized_score.item())

    return {
        "smiles": smiles,
        "reason": reason,
        "classifier_score": normalized_score,
        "classifier_threshold": threshold,
        "classifier_decision": decision,
        "threshold": threshold,
        "decision": decision,
    }


async def _extract_request_params(request: Request):
    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type.lower():
        try:
            payload = await request.json()
        except Exception:
            raise HTTPException(status_code=400, detail="Malformed JSON payload.")

        if not isinstance(payload, dict):
            raise HTTPException(
                status_code=400,
                detail="JSON payload must be an object.",
            )
    else:
        try:
            payload = dict(await request.form())
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Malformed form payload.",
            )

    encoded_image = payload.get("encoded_image")
    if encoded_image is None:
        raise HTTPException(
            status_code=422, detail="Field 'encoded_image' is required."
        )
    if not isinstance(encoded_image, str):
        raise HTTPException(
            status_code=422,
            detail="Field 'encoded_image' must be a base64 string.",
        )

    encoded_image = encoded_image.strip()
    if not encoded_image:
        raise HTTPException(
            status_code=422,
            detail="Field 'encoded_image' must not be empty.",
        )

    if len(encoded_image.encode("utf-8")) > MAX_ENCODED_IMAGE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=(
                "Payload too large for 'encoded_image'. "
                f"Maximum allowed size is {MAX_ENCODED_IMAGE_BYTES} bytes."
            ),
        )

    try:
        decoded_bytes = base64.b64decode(encoded_image, validate=True)
    except (binascii.Error, ValueError):
        raise HTTPException(
            status_code=400,
            detail="Field 'encoded_image' is not valid base64.",
        )

    if not decoded_bytes:
        raise HTTPException(
            status_code=422,
            detail="Field 'encoded_image' decodes to empty content.",
        )

    is_hand_drawn = _parse_bool(payload.get("is_hand_drawn"), "is_hand_drawn", False)
    classify_image = _parse_bool(payload.get("classify_image"), "classify_image", True)

    return decoded_bytes, is_hand_drawn, classify_image


@app.get("/")
async def root():
    return {"Message": "Image2smiles converter is up and running."}


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """catches general (e.g. Python) exceptions"""
    return JSONResponse(
        status_code=500,
        content={
            "message": "An unspecified general error in image2smiles API occurred."
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """catches HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc.detail)},
    )


@app.post("/image2smiles/")
async def image_to_smiles(
    request: Request,
):
    """
    This function uses encoded image, makes a temporary file and does the conversion to SMILES.
    Here, the image is first checked if it is a chemical structure.

    encoded_image: base64 encoded image (as string)
    is_hand_drawn: Boolean indicating if the image is hand-drawn
    classify_image: Boolean indicating if the image should be classified
    """

    decoded_bytes, is_hand_drawn, classify_image = await _extract_request_params(
        request
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_file.write(decoded_bytes)
        temporaryfile = temp_file.name

    try:
        classifier_score = None
        classifier_decision = "not_checked"

        if classify_image:
            classifier_score = decimer_classifier.get_classifier_score(temporaryfile)
            if classifier_score < IC_THRESHOLD:
                classifier_decision = "structure_like"
            else:
                classifier_decision = "not_structure_like"
                return _build_response(
                    smiles=None,
                    reason="not_chemical_structure",
                    classifier_score=classifier_score,
                    threshold=IC_THRESHOLD,
                    decision=classifier_decision,
                )

        try:
            decoded_image = config.decode_image(temporaryfile)
        except Exception:
            return _build_response(
                smiles=None,
                reason="decode_failed",
                classifier_score=classifier_score,
                threshold=IC_THRESHOLD,
                decision=classifier_decision,
            )

        smiles = _predict_smiles(decoded_image, is_hand_drawn)
        if smiles is None:
            return _build_response(
                smiles=None,
                reason="prediction_failed",
                classifier_score=classifier_score,
                threshold=IC_THRESHOLD,
                decision=classifier_decision,
            )

        return _build_response(
            smiles=smiles,
            reason=None,
            classifier_score=classifier_score,
            threshold=IC_THRESHOLD,
            decision=classifier_decision,
        )
    finally:
        if os.path.exists(temporaryfile):
            os.remove(temporaryfile)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8099)
