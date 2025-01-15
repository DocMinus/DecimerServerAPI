"""
Standalone for Decimer image to SMILES conversion
@author: Alexander Minidis (DocMinus)

license: MIT
Copyright (c) 2024 DocMinus
V0.2.1 - following the decimer_server.py version

Main difference: aside from no server, imagepath is used directly instead of base64 encoding

!beware: this version does not check for large image sizes or correct file types as the server version together with the API does
!It also doesn't support emf files as the use of the API would, but is in principle possible.
!Remember: startup time may be long due to model loading

2024-12-22 / 2025-01-15
"""

from pathlib import Path

from DECIMER.decimer import *
from decimer_image_classifier import DecimerImageClassifier

decimer_classifier = DecimerImageClassifier()
IC_TRESHOLD: float = 0.3


def _getdecimersmiles(
    encoded_image: config.decode_image, hand_drawn: bool = False
) -> str:
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


def predict_smiles(
    image_name: str, is_hand_drawn: bool = False, classify_image: bool = True
) -> str:
    """
    This function reads the image file from the provided path and does the conversion to SMILES.
    Here, the image is first checked if it is a chemical structure.

    temporaryfile: Path to the image file
    is_hand_drawn: Boolean indicating if the image is hand-drawn
    """

    if classify_image:
        if decimer_classifier.get_classifier_score(image_name) < IC_TRESHOLD:
            decoded_image = config.decode_image(image_name)
            smiles = _getdecimersmiles(decoded_image, is_hand_drawn)
            if smiles is not None:
                return smiles
    else:
        decoded_image = config.decode_image(image_name)
        smiles = _getdecimersmiles(decoded_image, is_hand_drawn)
        if smiles is not None:
            return smiles

    return None


def main():
    current_directory = Path(__file__).resolve()
    # 1 for folder level above (0 for same level)
    input_image = str(current_directory.parents[1] / "structure.png")
    smiles = predict_smiles(
        input_image,
        is_hand_drawn=False,
        classify_image=True,
    )
    print(smiles)


if __name__ == "__main__":
    main()
