# Installation

Choose one of two primary paths:

- **Docker** - Recommended for maximum compatibility across different Python environments
- **Local server (no Docker)** - Run the server directly with `uv`

Advanced/optional modes (for experienced users) are listed later in this file.

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
- Linux/Windows GPU support depends on host NVIDIA/CUDA runtime setup
- This project does not auto-provision NVIDIA drivers/CUDA; TensorFlow uses GPU only if your system is already configured for it
- If GPU runtime is unavailable, TensorFlow falls back to CPU automatically

---

## Local Installation (No Docker)

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
uv run python decimer_server.py
```

This creates a `.venv` using Python 3.1x and installs all dependencies (including `decimer_image_classifier` and `decimerapi` packages).

On Apple Silicon (`darwin` + `arm64`), this project now pins `tensorflow-macos==2.15.0` and includes `tensorflow-metal` automatically via `pyproject.toml`, so no extra TensorFlow install step is required after `uv sync`.

### Mac Silicon GPU Support (Optional Recovery)

If your environment was created before the TensorFlow platform pins were added, or if TensorFlow import fails after sync, reinstall the Mac runtime packages:

```shell
uv pip install tensorflow-macos==2.15.0 tensorflow-metal>=1.1.0
```

Then activate the environment:

```shell
source .venv/bin/activate
```

---

## Advanced / Optional Topics

### Standalone Mode (No Server)

Use the standalone script in `example_usage` if you explicitly want serverless local inference:

- `example_usage/decimer_standalone_no_server.py`

For most users, the server mode above is simpler to operate and integrate.

### Python Client Package

If you want the lightweight client wrapper in a separate environment:

```shell
pip install ./packages/decimerapi/
```

This is optional; direct HTTP calls work without it.

### API Examples by Experience Level

- Beginner local client usage: `example_usage/decimer_server_usage_example.py`
- Direct raw API call (Docker/local server): `example_usage/decimer_naked_api_eg_docker_only_example.py`
- Standalone, no server mode: `example_usage/decimer_standalone_no_server.py`

---

## EMF Support (Optional)

If you need to convert EMF files (typically from Word document extraction), install Inkscape. The API will ignore EMFs otherwise.

- **macOS:** `brew install --cask inkscape`
- **Linux:** `sudo apt-get install inkscape`
- **Windows:** Download from https://inkscape.org/release/
