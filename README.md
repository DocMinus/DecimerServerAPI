# DECIMER V2 - API server, including Image Classifier, incl. Mac Silicone support

This package is an extension of [DECIMER V2](https://github.com/Kohulan/DECIMER-Image_Transformer) including the [DECIMER Image Classifier](https://github.com/Iagea/DECIMER-Image-Classifier):

- Served as an API either via (local) server, docker based server or standalone script without server requirement.
- Considers Mac Silicone (Darwin, aka Mac Mx models) and their specific Tensorflow setup to take advantage of their GPU (more of an excercise than really necessary).
- Linux/Win GPU support depends on your Cuda installs (not considered here), i.e. GPU possible.
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

- Instead of the true/false readout, a classifier score of <0.3 is used which allows reactions to still be classified as structures and thus not sorted out.
- The original package wasn't intended for reaction schemes, but that tweak seems to make it work with reactions as well. <br>
  Change that value in "decimer_server.py" (`IC_THRESHOLD`) as you see fit if it doesn't work well for you.
- Furhtermore, removed an unnecessary save_image command, and changed the keras calls to tf.keras

## Installation

You have the choice of three versions, or all, depening on your needs.

- The docker version. <br>
  With this you should be able to use any python environment, only need to add the decimerapi (see below).
- A (local) server version without need for docker, but a full environment install (see below).
- don't want server or docker? A standalone version is available as well (also requires full env install)

### For docker version

Requires Docker (with Compose).<br>

Build and start locally:

```shell
docker compose up -d --build
```

Or pull the pre-built image from dockerhub instead of building locally:

```shell
docker pull docminus/decimer_api
```

Then edit `docker-compose.yml` to switch the `image:` line to `docker.io/docminus/decimer_api:latest` and run `docker compose up -d`.<br>
<br>
\_important to note: the docker version unfortunately doesn't support mac-gpu since docker is solely linux based\_<br>
\_your linux/win GPU support depends on your Cuda and other environment installations\_<br>

To access via the API (recommended), install into any python version (>= 3.9 for linux max, 3.9/3.10 for Mac) that you might have: <br>

```shell
pip install ./packages/decimerapi/
```

### For local version (full install)

Note, that due to Tensorflow not all Python versions on Mac or Win seem to work without issues, although on Linux all >=3.9 should be fine.<br>
Esp. for Mac, Python 3.10 works best (for me) — this is pinned automatically via the `.python-version` file.

[uv](https://docs.astral.sh/uv/) is required. Quickest: `pip install uv`. Alternatively `brew install uv` (Mac/Linux) or see the [uv docs](https://docs.astral.sh/uv/getting-started/installation/) for other options.

#### All platforms:

```shell
uv sync
```

This creates a `.venv` using Python 3.10 and installs all dependencies (including the local `decimer_image_classifier` and `decimerapi` packages) in one step.

#### Mac Darwin/Silicon — GPU support (optional):

The base install above uses standard `tensorflow` (CPU only on Mac). To enable Metal GPU acceleration, additionally run:

```shell
uv pip install tensorflow-macos==2.15.0 tensorflow-metal==1.1.0
```

Then activate and run with:

```shell
source .venv/bin/activate
```

## Usage

### Docker

To start:

```shell
docker compose up -d
```

To stop:

```shell
docker compose down
```

### Local (non docker) server version

```shell
python decimer_server.py
```

### Example usage

The server runs on localhost:8099. This can be changed to ip-address:portnumber if you want to run another machine (or cloud even).<br>
`decimer_example.py` demonstrates calling the server via the `decimerapi` HTTP client — it works with both the docker and local server versions, and only requires `decimerapi` installed locally (not the full `uv sync`).<br>
Should you want to run a serverless app, check the [optional_standalone_no_server](./optional_standalone_no_server) folder.

### Important caveat

<span style="background-color: white; color:blue; font-weight:bold;">Although the classifier can be overriden, it is not recommended should you have non-molecule images, the system might crash. <br>
This seems to have to do with the decimer image to smiles implementation and is out of my control.</span>

### Of note:

<span style="background-color: white; color:blue; font-weight:bold;">First time start up might take a few minutes due to model download! (depending on your connection speed; this happens only once).</span>

### EMF support (optional)

Should you require conversion of EMF files (which most likely stem from a Word-document extraction), you require Inkscape to be installed. The API will ignore EMFs otherwise.

- mac:
  brew install --cask inkscape
- linux:
  sudo apt-get install inkscape
- windows:
  download from official website: https://inkscape.org/release/

## API Documentation

See the separate readme file [readme_api_calls.md](readme_api_calls.md).

## Author:

[DocMinus](https://github.com/DocMinus) <br>
First development during October-December 2024

## License

MIT license, based on inheritance from Decimer Transfomer and Classifier which are both MIT license.
<br>

### Uninstalling

Should you want/need to uninstall, after removing any app folder and environment, check your homefolder for ".data" folder where Decimer stores its models, delete this folder as well.
