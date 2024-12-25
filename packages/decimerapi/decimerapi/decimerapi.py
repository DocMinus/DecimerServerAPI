"""
module: decimerapi.py
@author: Alexander Minidis (DocMinus)

license: MIT
Copyright (c) 2024 DocMinus
V 0.3.1 - working tools implementation, now as class to submitt a different port
2024-12-25 typo fixed

tools server usage

#TODO figure out a way to accept and convert emf images
"""

import requests
import base64
import imghdr
from pathlib import Path

# from PIL import Image
# import emf2svg


class DecimerAPI:
    """
    DecimerAPI class for interacting with the DECIMER image-to-SMILES API.

    Attributes:
        DECIMER_URL (str): The URL of the DECIMER API endpoint.

    Methods:
        __init__(port: int = 8099):
            Initializes the DecimerAPI instance with the specified port, defaulting to 8099.

        _is_valid_image_type(encoded_image: bytes) -> bool:
            Checks if the base64-encoded image is of type JPG, PNG, GIF (EMF not yet supported).

        call_image2smiles_api(input_image: Path, hand_drawn: bool = False, classify_image: bool = True) -> str:
            Calls the DECIMER API to convert an image to a SMILES string.
                input_image (Path): Path to the image file.
                hand_drawn (bool): Boolean indicating if the image is hand-drawn.
                classify_image (bool): Boolean indicating if the image should be classified.
                Note that when using non-structure images, classifyt shoudl be set to TRUE!
            Returns:
                str: The SMILES string if the API call is successful, None otherwise.
    """

    def __init__(self, port: int = 8099):
        self.DECIMER_URL = f"http://localhost:{port}"
        self.DECIMER_I2S = f"{self.DECIMER_URL}/image2smiles/"

    def _is_valid_image_type(self, encoded_image: bytes) -> bool:
        """Check if the base64-encoded image is of type JPG, PNG, or EMF."""
        image_type = imghdr.what(None, h=base64.b64decode(encoded_image))
        return image_type in ["jpeg", "png", "gif"]  # "emf" not yet supported

    # def _convert_emf_to_png(self, encoded_image: bytes) -> bytes:
    #     """Convert EMF image to PNG format."""
    #     emf_image = emf2svg.EMF(base64.b64decode(encoded_image))
    #     png_image = emf_image.to_png()
    #     return base64.b64encode(png_image)

    def call_image2smiles(
        self,
        input_image: Path | str,
        hand_drawn: bool = False,
        classify_image: bool = True,
    ) -> str:
        """calls decimer API, requires decimer server running

        Args:
            input_image: Path (or string) to the image file
            hand_drawn: Boolean indicating if the image is hand-drawn
            classify_image: Boolean indicating if the image should be classified
        """
        if isinstance(input_image, str):
            input_image = Path(input_image)
        encoded_image = base64.b64encode(input_image.read_bytes()).decode("utf-8")

        if len(encoded_image) > 4 * 1024 * 1024:
            print("Image file size is too large.")
            return None  # return error would be better

        if not self._is_valid_image_type(encoded_image):
            print("Invalid image type. Only JPG, PNG, and GIF are supported.")
            return None  # return error would be better

        # image_type = imghdr.what(None, h=base64.b64decode(encoded_image))
        # if image_type == "emf":
        #     encoded_image = self._convert_emf_to_png(encoded_image)

        data = {
            "encoded_image": encoded_image,
            "is_hand_drawn": str(hand_drawn).lower(),
            "classify_image": str(classify_image).lower(),
        }

        response = requests.post(self.DECIMER_I2S, data=data)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return None
        else:
            response_json = response.json()
            analyzed_smiles = response_json["smiles"]
            return analyzed_smiles

    def server_status(self) -> str:
        """Check the status of the DECIMER server."""
        response = requests.get(self.DECIMER_URL)
        if response.status_code == 200:
            return "Server is running."
        else:
            return "Server is not running."
