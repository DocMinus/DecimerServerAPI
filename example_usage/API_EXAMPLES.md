# API Examples

Requires a running DECIMER server.

For full request/response/error contract, see [`../API_ENDPOINTS.md`](../API_ENDPOINTS.md).
For script selection by experience level, see [`README.md`](./README.md).

## Using the `decimerapi` Python Package

See also: `decimer_server_usage_example.py`

```python
from pathlib import Path
from decimerapi.decimerapi import DecimerAPI

decimer_api = DecimerAPI()  # default host localhost, port 8099
# decimer_api = DecimerAPI("192.168.50.170", 8888)  # custom host/port
print(decimer_api.server_status())

current_file_path = Path(__file__).resolve()
input_image = current_file_path.parents[0] / "structure.png"
smiles = decimer_api.call_image2smiles(input_image, hand_drawn=False)
print(smiles)
```

## Using Direct HTTP Requests (No Python Wrapper)

See also: `decimer_naked_api_eg_docker_only_example.py`

### Python

Check server status:

```python
import requests

url = "http://localhost:8099"

try:
    response = requests.get(url)
    response.raise_for_status()
    print("Server is running.")
except requests.exceptions.ConnectionError:
    print("Error: Could not connect to server. Is the server/container running?")
    raise SystemExit(1)
except requests.exceptions.HTTPError as e:
    print(f"Error: Server returned {e.response.status_code}")
    raise SystemExit(1)
```

Convert image to SMILES:

```python
import base64
from pathlib import Path

import requests

url_i2s = "http://localhost:8099/image2smiles/"
input_image = "structure.png"
encoded_image = base64.b64encode(Path(input_image).read_bytes()).decode("utf-8")

data = {
    "encoded_image": encoded_image,  # required
    "is_hand_drawn": "false",      # optional
    "classify_image": "false",     # optional
}

response = requests.post(url_i2s, data=data)
if response.status_code != 200:
    print(f"Error: {response.status_code} -> {response.text}")
else:
    response_json = response.json()
    print(response_json["smiles"])
```

### Curl

Health check:

```shell
curl -X GET "http://localhost:8099/"
```

## Checking System Status & Hardware Acceleration

Query system information including hardware accelerator type (CPU/CUDA/Metal).

### Using the `decimerapi` Python Package

```python
from decimerapi import DecimerAPI

api = DecimerAPI()  # default localhost:8099
status = api.get_system_status()

if status:
    print(f"Server Status: {status['status']}")
    print(f"Accelerator: {status['accelerator_type']}")
    print(f"TensorFlow: {status['tensorflow_version']}")
else:
    print("Could not retrieve system status")

# Quick check for GPU availability
if status and status['accelerator_type'] != 'cpu':
    print(f"GPU acceleration available: {status['accelerator_type']}")
else:
    print("Running on CPU")
```

### Using Direct HTTP Requests

#### Python

```python
import requests

url = "http://localhost:8099/system/status"

try:
    response = requests.get(url)
    response.raise_for_status()
    status = response.json()
    print(f"Accelerator Type: {status['accelerator_type']}")
    print(f"TensorFlow Version: {status['tensorflow_version']}")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
```

#### Curl

```shell
curl -X GET "http://localhost:8099/system/status"
```

Expected response:

```json
{
  "status": "ready",
  "accelerator_type": "cuda",
  "tensorflow_version": "2.15.0"
}
```

Possible `accelerator_type` values:
- `cpu`: CPU-only processing
- `cuda`: NVIDIA CUDA GPU (Linux/Windows)
- `metal`: Apple Metal (macOS with M1-M4)
