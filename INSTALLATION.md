# Installation

Choose one of three installation methods depending on your needs:

- **Docker** - Recommended for maximum compatibility across different Python environments
- **Local server** - Run the server directly without Docker
- **Standalone** - Serverless usage (see [`optional_standalone_no_server`](./optional_standalone_no_server) folder)

## Docker (Recommended)

Requires Docker with Compose.

### Build and start locally

```shell
docker compose up -d --build
```

Or on older systems:

```shell
docker-compose up -d --build
```

### Or pull pre-built image

```shell
docker pull docminus/decimer_api
```

Then edit `docker-compose.yml` to switch the `image:` line to `docker.io/docminus/decimer_api:latest` and run `docker compose up -d`.

Alternatively, use the Makefile for convenience:

```shell
make buildx
```

This builds for `linux/amd64` platform (recommended for TensorFlow compatibility).

### Install Python client

To access via the Python API, install the client package into your existind/desired environment:

```shell
pip install ./packages/decimerapi/
```

This is not required if you want to use plain HTTP requests.

### GPU Notes

- Docker doesn't support Mac GPU (Docker is Linux-only)
- Linux/Windows GPU support depends on your CUDA installation

---

## Local Installation

### Requirements

- Python >= 3.10 (3.10 recommended on Mac; newer versions not guaranteed to work)
- [uv](https://docs.astral.sh/uv/) package manager

Install uv:

- **macOS:** `brew install uv` or `pip install uv`
- **Linux:** `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Windows:** `irm https://astral.sh/uv/install.ps1 | iex`

Or simply: `pip install uv` in the existing environment

### Quick Install (All Platforms)

```shell
uv sync
```

This creates a `.venv` using Python 3.1x and installs all dependencies (including `decimer_image_classifier` and `decimerapi` packages).

### Mac Silicon GPU Support (Optional)

The base install uses standard `tensorflow` (CPU only on Mac). To enable Metal GPU acceleration:

```shell
uv pip install tensorflow-macos==2.15.0 tensorflow-metal==1.1.0
```

Then activate the environment:

```shell
source .venv/bin/activate
```

---

## EMF Support (Optional)

If you need to convert EMF files (typically from Word document extraction), install Inkscape. The API will ignore EMFs otherwise.

- **macOS:** `brew install --cask inkscape`
- **Linux:** `sudo apt-get install inkscape`
- **Windows:** Download from https://inkscape.org/release/
