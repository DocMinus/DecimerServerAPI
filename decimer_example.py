"""
Example code for using the DECIMER Server & API to convert an image to SMILES.
@author: Alexander Minidis (DocMinus)

license: MIT
Copyright (c) 2024 DocMinus
V0.3.1b - updated example code
2024-12-23

"""

from pathlib import Path

from decimerapi.decimerapi import DecimerAPI


def main():
    decimer_api = DecimerAPI()  # using default host locahost on port 8099
    print(decimer_api.server_status())

    current_directory = Path(__file__).resolve()
    input_image = current_directory.parents[0] / "structure.png"
    # both string or path can be used
    # input_image = r"/Users/a/dev/DecimerAPI/structure.png"
    smiles = decimer_api.call_image2smiles(input_image, hand_drawn=False)
    print(smiles)
    input_image = current_directory.parents[0] / "not_structure.gif"
    smiles = decimer_api.call_image2smiles(input_image, hand_drawn=False)
    print(smiles)


if __name__ == "__main__":
    main()
