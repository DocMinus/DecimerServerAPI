# DECIMER V2 - Standalone version including Image Classifier, incl. Mac Silicone support
For details check the [Main README](../README.md)

## Installation
If you haven't followed the main readme file, here a recap:<br>
Best results with Python 3.10, at least on Mac M models if you want to use GPU support.<br>
Other Python versions on Linux according to DECIMER authors should be fine.<br>

[uv](https://docs.astral.sh/uv/) is required. Quickest: `pip install uv`. Alternatively `brew install uv` (Mac/Linux) or see the [uv docs](https://docs.astral.sh/uv/getting-started/installation/) for other options.<br>

From the **root of the repository**, run:

```shell
uv sync
source .venv/bin/activate
```

This creates a `.venv` using Python 3.10 (pinned via `.python-version`) and installs all dependencies including the local classifier package.

#### Mac Darwin/Silicon — GPU support (optional):

```shell
uv pip install tensorflow-macos==2.15.0 tensorflow-metal==1.1.0
```

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