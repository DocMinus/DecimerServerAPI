"""
Standalone for Decimer image to SMILES conversion
@author: Alexander Minidis (DocMinus)

license: MIT
Copyright (c) 2024 DocMinus
V0.2.0 - following the decimer_server.py version

Main difference: aside from no server, imagepath is used directly instead of base64 encoding

!beware: this version does not check for large image sizes or correct file types as the server version together with the API does
!It also doesn't support emf files as the use of the API would, but is in principle possible.

2024-12-22
"""

from DECIMER.decimer import *
from decimer_image_classifier import DecimerImageClassifier

decimer_classifier = DecimerImageClassifier()


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
    image_path: str, is_hand_drawn: bool = False, classify_image: bool = True
) -> str:
    """
    This function reads the image file from the provided path and does the conversion to SMILES.
    Here, the image is first checked if it is a chemical structure.

    temporaryfile: Path to the image file
    is_hand_drawn: Boolean indicating if the image is hand-drawn
    """

    if classify_image:
        if decimer_classifier.get_classifier_score(image_path) < 0.3:
            decoded_image = config.decode_image(image_path)
            smiles = _getdecimersmiles(decoded_image, is_hand_drawn)
            if smiles is not None:
                return smiles
    else:
        decoded_image = config.decode_image(image_path)
        smiles = _getdecimersmiles(decoded_image, is_hand_drawn)
        if smiles is not None:
            return smiles

    return None


def main():
    smiles = predict_smiles(
        "/Users/a/dev/DecimerAPI/structure.png",
        is_hand_drawn=False,
        classify_image=True,
    )
    print(smiles)


if __name__ == "__main__":
    main()
