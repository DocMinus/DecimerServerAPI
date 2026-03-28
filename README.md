# DECIMER V2 - API Server

An extension of [DECIMER V2](https://github.com/Kohulan/DECIMER-Image_Transformer) including the [DECIMER Image Classifier](https://github.com/Iagea/DECIMER-Image-Classifier) — served as an API via Docker, local server, or standalone script.

Supports Mac Silicon (M1-4) GPU acceleration, Linux/Windows with CUDA, and reaction scheme image classification.

## Features

- Convert images of chemical structures to SMILES format
- Supports hand-drawn and digital images
- Classification also works with reaction schemes
- Fast recognition via server-based one-time model loading
- Easy Python API integration

## Quick Start

### Docker (Recommended)

```shell
docker compose up -d --build
```

Then install the Python client:

```shell
pip install ./packages/decimerapi/
```

### Local Server

```shell
uv sync
uv run python decimer_server.py
```

The server runs on `localhost:8099`. See [`example_usage`](./example_usage) for complete examples.

## Documentation

- [Installation Guide](./INSTALLATION.md) - Docker, local, and standalone setup
- [API Reference](./readme_api_calls.md) - HTTP and Python API usage
- [Differences](./DIFFERENCES.md) - Changes from original DECIMER packages
- [FAQ](./FAQ.md) - Common questions and important caveats

## License

MIT License — see [LICENSE](./LICENSE) file.
