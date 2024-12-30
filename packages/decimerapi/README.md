# FILE: /decimerapi/README.md
# This file contains documentation for the DECIMER API.

# DECIMER API
The DECIMER API is a Python module extending the DECIMER image transformer and classifier when using it server based.

Not required for the standalone version.

## Installation
Should be handled from main level installation of the repo.

## Usage
```python
from decimerapi.decimerapi import DecimerAPI
decimer_api = DecimerAPI()
smiles = decimer_api.call_image2smiles(input_image)
print(smiles)
```
Default values for hand_drawn and classify_image are False, respectively True: i.e. `decimer_api.call_image2smiles(input_image, hand_drawn=False, classifiy_image=True)`

You can set a different portnumber or IP address should you change from default localhost:8099 with `DecimerAPI("192.x.x.x", 8099)`.

To check if the server is up and running at all: `print(decimer_api.server_status())`.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Author
[DocMinus](https://github.com/DocMinus)
