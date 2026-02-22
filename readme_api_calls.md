# API calls using installed decimerapi package
Requires installed server. if no local server running, docker can still be used if run within this decimerapi package (see README.md).

See also the script `decimer_server_usage_example.py`

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


# API calls without decimerapi usage
Should you want to use the local server directly, without using any api package usage, or if you are using only the docker version without any installed decimer packages.<br>

See also the script `decimer_naked_api_eg_docker_only_example`

## Python
Check the server status:
```python
import requests
url = "http://localhost:8099"

response = requests.get(url)
try:
    response = requests.get(url)
    response.raise_for_status()
    print("Server is running.")
except requests.exceptions.ConnectionError:
    print("Error: Could not connect to server. Is the Docker container running?")
    exit(1)
except requests.exceptions.HTTPError as e:
    print(f"Error: Server returned {e.response.status_code}")
    exit(1)
```

Convert an image file which requires conversion to string (byte):
```python
import requests
import base64
from pathlib import Path

url_i2s = "http://localhost:8099/image2smiles/"
encoded_image = base64.b64encode(Path(input_image).read_bytes()).decode("utf-8")
input_image = "structure.png"
hand_drawn = False
classify_image = False

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
```

## Curl
To test the server, on cmd line use:
```Shell
curl -X GET "http://localhost:8099/"
```