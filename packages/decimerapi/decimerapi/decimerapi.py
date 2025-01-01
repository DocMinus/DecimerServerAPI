"""
module: decimerapi.py
@author: Alexander Minidis (DocMinus)

license: MIT
Copyright (c) 2024/25 DocMinus
Tools for server usage, basically independet from used environment, only requires the server running somehwere

working tools implementation, now as class to submitt a different port
typo fixed; host added to __init__ method, allows to run not just locally
V 0.5.0, 2025-01-01 
now automatic EMF to PNG conversion based on Inkscape presence. See readme for installation instructions.
Also some minor improvements in error handling and status check.
"""

import base64
import imghdr
import subprocess
from pathlib import Path
from shutil import which

import requests

# determine if Inkscape is installed. If not, EMF conversion will be disabled.
INKSCAPE = True if which("inkscape") is not None else False


class DecimerAPI:
    """
    DecimerAPI class for interacting with the DECIMER image-to-SMILES server.

    Attributes:
        DECIMER_URL (str): The URL of the DECIMER API endpoint.

    Methods:
        __init__(host: str = "localhost", port: int = 8099):
            Initializes the DecimerAPI instance with the specified host and port, defaulting to localhost 8099.

        _is_valid_image_type(encoded_image: bytes) -> bool:
            Checks if the base64-encoded image is of type JPG, PNG, GIF, EMF.

        _convert_emf2png(input_path: Path) -> Path:
            Converts an EMF file to PNG using Inkscape.

        call_image2smiles_api(input_image: Path, hand_drawn: bool = False, classify_image: bool = True) -> str:
            Calls the DECIMER API to convert an image to a SMILES string.
                input_image (Path): Path to the image file.
                hand_drawn (bool): Boolean indicating if the image is hand-drawn.
                classify_image (bool): Boolean indicating if the image should be classified.
                Note that when using non-structure images, classifyt should be set to TRUE (default!
            Returns:
                str: The SMILES string if the API call is successful, None otherwise.
    """

    def __init__(self, host: str = "localhost", port: int = 8099):
        self.DECIMER_URL = f"http://{host}:{port}"

    def _is_valid_image_type(self, encoded_image: bytes) -> tuple[bool, bool]:
        """Checks if the base64-encoded image is of type JPG, PNG, GIF or EMF.
        Returns a tuple of two booleans: (is_emf, is_valid_image)
        """

        decoded_image = base64.b64decode(encoded_image)
        image_type = imghdr.what(None, h=decoded_image)
        # emf requires separate check, as imghdr does not support it
        # could one check file ending? possibly, but not reliable
        if INKSCAPE and image_type is None and decoded_image[:4] == b"\x01\x00\x00\x00":
            image_type = "emf"

        is_emf = image_type == "emf"
        return is_emf, image_type in ["jpeg", "png", "gif", "emf"]

    def _convert_emf2png(self, input_path: Path) -> Path:
        """Converts an EMF file to PNG using Inkscape."""
        output_path = input_path.with_suffix(".png")
        subprocess.run(
            [
                "inkscape",
                str(input_path),
                f"--export-filename={str(output_path)}",
                "--export-type=png",
            ],
            check=True,
        )
        return output_path

    def call_image2smiles(
        self,
        input_image: Path | str,
        hand_drawn: bool = False,
        classify_image: bool = True,
    ) -> str:
        """Calls decimer Server to convert an image to a SMILES string.

        Checks for correct image type and size before sending the image to the server.
        Converts EMF images to PNG if Inkscape is installed.
        Args:
            input_image: Path (or string) to the image file
            hand_drawn: Boolean indicating if the image is hand-drawn
            classify_image: Boolean indicating if the image should be classified
        """
        if isinstance(input_image, str):
            input_image = Path(input_image)

        if input_image.stat().st_size > 4 * 1024 * 1024:
            print("Error: Image file size is too large.")
            return None  # return error would be better

        encoded_image = base64.b64encode(input_image.read_bytes()).decode("utf-8")

        is_emf, is_valid_image = self._is_valid_image_type(encoded_image)

        if not is_valid_image:
            print(
                "Error: Invalid image type. Only JPG, PNG, GIF and EMF are supported."
            )
            return None  # return error would be better

        if is_emf:
            new_input_image = self._convert_emf2png(input_image)
            encoded_image = base64.b64encode(new_input_image.read_bytes()).decode(
                "utf-8"
            )

        data = {
            "encoded_image": encoded_image,
            "is_hand_drawn": str(hand_drawn).lower(),
            "classify_image": str(classify_image).lower(),
        }

        response = requests.post(f"{self.DECIMER_URL}/image2smiles/", data=data)
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
