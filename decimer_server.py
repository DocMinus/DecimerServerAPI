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
2024-12-28
See Readme / requirements for dependencies
works on Linux and Windows, also Mac with GPU
"""

import uvicorn
import base64
import tempfile
import os
from DECIMER.decimer import *
from decimer_image_classifier import DecimerImageClassifier
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import JSONResponse

decimer_classifier = DecimerImageClassifier()
IC_TRESHOLD: float = 0.3


def _predict_smiles(encoded_image: any, hand_drawn: bool = False) -> str:
    """Predicts smiles representation of a molecule depicted in the given image.
    Taken from DECIMER.decimer and modified.

    Args:
        encoded_image (any): encoded image
        hand_drawn (bool): Flag to indicate whether the molecule in the image is hand-drawn

    Returns:
        str: smiles representation of the molecule in the input image
    """

    model = DECIMER_Hand_drawn if hand_drawn else DECIMER_V2
    predicted_tokens, confidence_values = model(tf.constant(encoded_image))
    try:
        predicted_smiles = utils.decoder(detokenize_output(predicted_tokens))
    except:
        return None

    return predicted_smiles


app = FastAPI()


@app.get("/")
async def root():
    return {"Message": "Image2smiles converter is up and running."}


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """catches general (e.g. Python) exceptions"""
    return JSONResponse(
        status_code=500,
        content={
            "message": "An unspecified general eerror in image2smiles API occurred."
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
    encoded_image: str = Form(...),
    is_hand_drawn: bool = Form(False),
    classify_image: bool = Form(True),
):
    """
    This function uses encoded image, makes a temporary file and does the conversion to SMILES.
    Here, the image is first checked if it is a chemical structure.

    encoded_image: bae64 encoded image (as string)
    is_hand_drawn: Boolean indicating if the image is hand-drawn
    classify_image: Boolean indicating if the image should be classified
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_file.write(base64.b64decode(encoded_image))
        temporaryfile = temp_file.name

    try:
        if classify_image:
            if decimer_classifier.get_classifier_score(temporaryfile) < IC_TRESHOLD:
                decoded_image = config.decode_image(temporaryfile)
                smiles = _predict_smiles(decoded_image, is_hand_drawn)
                if smiles is None:
                    return JSONResponse(
                        status_code=400,
                        content={"message": "Image conversion error"},
                    )
                return {"smiles": smiles}
            else:
                return {"smiles": None}
        else:
            decoded_image = config.decode_image(temporaryfile)
            smiles = _predict_smiles(decoded_image, is_hand_drawn)
            if smiles is None:
                return JSONResponse(
                    status_code=400,
                    content={"message": "Image conversion error"},
                )
            return {"smiles": smiles}
    finally:
        os.remove(temporaryfile)


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8099)

