# DECIMER V2 - API server, including Image Classifier, incl. Mac Silicone support
This package is an extension of [DECIMER V2](https://github.com/Kohulan/DECIMER-Image_Transformer) including the [DECIMER Image Classifier](https://github.com/Iagea/DECIMER-Image-Classifier):
- Served as an API either via local server, docker based server or standalone script without server requirement.
- Considers Mac Silicone (Darwin, aka Mac Mx models) and their specific Tensorflow setup to take advantage of their GPU (more of an excercise than really necessary).
- The classifier now also classifies reaction scheme images rather well by using the decimer_classifier.get_classifier_score().

## Why this version of Decimer (detailed explanation)
- The original decimer repos where at times a pain to install due to their dependencies, depending on which system it was installed.
- No self-deployable server version otherwise avaialabe
- The docker version (recommended) allows this to be even more "robust" if you have environments of differing python versions or installations giving issues with the original repo dependencies. 
- The startup of the scripts with calling the decimer dependencies and model loading can take quite some time, especially for frequent usage it can become a time-sink.<br> 
When starting a server, model loading is done only once. Comes in handy if you routinely switch scripts, have large batches, etc.<br>
Using the classifier also sorts out wrong images speeding up the process even more.

## Features in brief
- Convert images of chemical structures to SMILES format.
- Support for both hand-drawn and digital images.
- Classification that also supports reactions.
- Speedier start up and recognition process
- Easy integration with existing Python projects.


## Changes compared to using the Decimer transformer package directly
- Installation also considers Mac Silicone Tensorflow version (and GPU support) - _local install only, not docker version_.<br>
- The server version uses json calls, the standalone version overrides the original `predict_smiles()`. <br>
Although, ignoring any of the enclosed code, just using the decimer python packages installation, the original decimer function can be still be used as well.<br>
- An API is provided to facilitate the server based calls.

## Changes compared to using the classifier package
Instead of the true/false readout, a classifier score of <0.3 is used which allows reactions to still be classified as structures and thus not sorted out.<br>
The original package wasn't intended for reaction schemes, but that tweak seems to make it work with reactions as well. Change that value as you see fit if it doesn't work well for you.<br>


## Installation
You have the choice of three versions, or all, depening on your needs.

* The docker version. <br>
With this u should be able to use any python environment, only need to add the decimerapi (see below).
* A local server version without need for docker, but a full environment install (see below).
* don't want server or docker? A standalone version is available as well (also requires full env install)

### For docker version
Requires docker... doh!<br>
Windows cmd: ´win_make.bat´<br>
Mac/Linux: ´Make build´<br>
_important to note: the docker version unfortunately doesn't support mac-gpu since it can only be linux based_<br>
It will nevertheless be sufficiently fast. You could always compare the time for local versus docker version?
To access via the API (recommended), install into any python version (>= 3.8) you might have: <br>
```pip install ./packages/decimerapi/``` <br>

### For local version (full install)
Best results with python3.10, at least on Mac M models. Py 3.9 on Mac with gpu support doesn't seenm to work (for me), the non GPU version should be fine on any Py version.<br>
Other python versions on Linux according to DECIMER authors should be fine?<br>
```shell
conda create --name decimerapi python=3.10.0  # or other if you don't want/need Mac GPU support
conda activate decimerapi
```
Linux/Windows: ```pip install -r requirements.txt``` <br>
Mac Darwin/Silicon: ```pip install -r requirements_mac.txt``` <br>

## Usage
### Docker
`docker-compose up -d` to start the API server, ´docker-compose down´ to stop. <br>
(depending on your install it might be ´docker compose (space, no -))´.<br>

### Local (non docker) server version
`python decimer_server.py`<br>

### Example usage
The `python decimer_example.py` shows how to call the server, works for both, docker and local server versions.<br>
(note, if you have both running (for testing?) at the same time, you will need to change the port in the local server version)<br>
Should you want to run a serverless app, check the [optional_standalone_no_server](./optional_standalone_no_server) folder.

### Important caveat
<span style="background-color: white; color:blue; font-weight:bold;">Although the classifier can be overriden, it is not recommended should you have non-molecule images, the system might crash. <br>
This seems to have to do with the decimer image to smiles implementation and is out of my control.</span>

### Of note:
<span style="background-color: white; color:blue; font-weight:bold;">First time start up might take a few minutes due to model download! (depending on your connection speed; this happens only once).</span>

## API Documentation
See the separate readme file [readme_api_calls.md](readme_api_calls.md).

## Author: 
[DocMinus](https://github.com/DocMinus) <br>
First development during October-December 2024

## License
MIT license, based on inheritance from Decimer Transfomer and Classifier which are both MIT license. 
<br>

#TODO Option to change the threshold of image classifier via API

#TODO create a readily available image on dockerhub
