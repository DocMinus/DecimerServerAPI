# API calls using decimerapi
```python
from pathlib import Path
from decimerapi.decimerapi import DecimerAPI

decimer_api = DecimerAPI()  # using default host localhost and port 8099
# decimer_api = DecimerAPI("192.168.50.170", 8888) # different port number
print(decimer_api.server_status())

current_file_path = Path(__file__).resolve()
input_image = current_file_path.parents[0] / "structure.png"
# both string or path can be used
# input_image = r"/Users/a/dev/DecimerAPI/structure.png"
smiles = decimer_api.call_image2smiles(input_image, hand_drawn=False)
print(smiles)
```


# API calls without decimerapi
should you want to use the local server directly, without using any package installs, here are 2 examples:<br>
Check the server status:
```python
import requests
url = "http://localhost:8099"

response = requests.get(url)
if response.status_code == 200:
    return "Server is running."
else:
    return "Server is not running."
```
Convert an image file which requires conversion to string (byte):
```python
import requests
import base64

url_i2s = "http://localhost:8099/image2smiles/"
encoded_image = base64.b64encode(input_image.read_bytes()).decode("utf-8")

data = {
    "encoded_image": encoded_image,                 # required, 
    "is_hand_drawn": str(hand_drawn).lower(),       # optional
    "classify_image": str(classify_image).lower(),  # optional
}
response = requests.post(url_i2s, data=data)
if response.status_code != 200:
    print(f"Error: {response.status_code}")
else:
    response_json = response.json()
    analyzed_smiles = response_json["smiles"]
    print(analyzed_smiles)
```