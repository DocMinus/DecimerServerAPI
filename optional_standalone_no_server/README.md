# DECIMER V2 - Standalone version including Image Classifier, incl. Mac Silicone support
For details check the [Main README](../README.md)

## Installation
If you haven't followed the main readme file, here a recap:<br>
Best results with python3.10, at least on Mac M models if you want to use GPU support.<br>
Other python versions on Linux according to DECIMER authors should be fine.<br>
```shell
conda create --name decimerapi python=3.10.0
conda activate decimerapi
```
Linux/Windows: ```pip install -r requirements.txt``` <br>
Mac Darwin/Silicon: ```pip install -r requirements_mac.txt``` <br>
<br>
Finally (from top level of this repo): ```python ./packages/decimer_ic/setup.py install``` 
<br>

## Running
`python decimer_standalone_no_server.py`<br>

### Important caveat
<span style="background-color: white; color:blue; font-weight:bold;">Althoug the classifier can be overriden, it is not recommended should you have non-molecule images, the system might crash. This seems to have to do with the decimer image to smiles implementation and is out of my control.</span>

### Of note:
<span style="background-color: white; color:blue; font-weight:bold;">First time start up might take a few minutes due to model download! (depending on your connection speed; this happens only once).</span>

## Author: 
[DocMinus](https://github.com/DocMinus) <br>
First development during October-December 2024

## License
MIT license, based on inheritance from Decimer Transfomer and Classifier which are both MIT license. 