"""This is an example of how to use the image2smiles API via a Docker container.
Make sure to have the Docker container running before executing this code.
Only requires the `requests` library: pip install requests
"""

import requests
import base64
from pathlib import Path

SERVER = "http://localhost:8099/"

# check if server is running
try:
    response = requests.get(SERVER)
    response.raise_for_status()
    print("Server is running.")
except requests.exceptions.ConnectionError:
    print("Error: Could not connect to server. Is the Docker container running?")
    exit(1)
except requests.exceptions.HTTPError as e:
    print(f"Error: Server returned {e.response.status_code}")
    exit(1)


# load image, encode it, and send it to the server
input_image = "structure.png"
hand_drawn = False
classify_image = False

url_i2s = SERVER + "image2smiles/"
encoded_image = base64.b64encode(Path(input_image).read_bytes()).decode("utf-8")

data = {
    "encoded_image": encoded_image,  # required,
    "is_hand_drawn": str(hand_drawn).lower(),  # optional
    "classify_image": str(classify_image).lower(),  # optional
}
response = requests.post(url_i2s, data=data)
if response.status_code != 200:
    print(f"Error: {response.status_code}")
else:
    response_json = response.json()
    analyzed_smiles = response_json["smiles"]
    print(analyzed_smiles)
