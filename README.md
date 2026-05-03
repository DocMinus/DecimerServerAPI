# DECIMER V2 - API Server

An extension of [DECIMER V2](https://github.com/Kohulan/DECIMER-Image_Transformer) including the [DECIMER Image Classifier](https://github.com/Iagea/DECIMER-Image-Classifier) — served as an API via Docker, local server, or standalone script.

Supports Mac Silicon (M1-4) GPU acceleration, Linux/Windows TensorFlow GPU usage when the host is configured accordingly, and reaction scheme image classification.

> GPU availability is environment-dependent. On Linux/Windows with NVIDIA hardware, GPU acceleration is used when system drivers/runtime are correctly set up; otherwise processing falls back to CPU.

## Features

- Convert images of chemical structures to SMILES format
- Supports hand-drawn and digital images
- Classification also works with reaction schemes
- Fast recognition via server-based one-time model loading
- Easy Python API integration

## Start Here

If you are new, choose one of these two paths:

### Path A: Docker (recommended)

```shell
# Use pre-built Docker Hub image (default compose file)
docker compose up -d

# Build locally from this repository
docker compose -f docker-compose.yml -f docker-compose.local.yml up -d --build
```

For reproducible deployments, pin the image tag in `docker-compose.yml` (for example `docker.io/docminus/decimer_api:1.4.0`) instead of `:latest`.

### Path B: No Docker (local Python)

```shell
uv sync
uv run python decimer_server.py
```

Server URL in both cases: `http://localhost:8099`

For details and troubleshooting, use the docs linked below.

## Documentation

- [Installation Guide](./INSTALLATION.md) - Guided setup (Docker or no-Docker), plus optional advanced topics
- [API Endpoints](./API_ENDPOINTS.md) - Canonical endpoint contract (request/response/error semantics)
- [API Examples](./example_usage/API_EXAMPLES.md) - Practical request examples (Python and curl)
- [Example Scripts](./example_usage/README.md) - Which script to use by audience and scenario
- Latest addition: `decimerapi` now provides both `call_image2smiles(...)` (smiles-only, backwards compatible) and `call_image2smiles_with_meta(...)` (full response JSON with metadata). See [decimerapi README](./packages/decimerapi/README.md)
- [Differences](./DIFFERENCES.md) - Changes from original DECIMER packages
- [FAQ](./FAQ.md) - Common questions and important caveats


## Related Projects
A MCP-Server building on this is also available here: [https://github.com/DocMinus/DecimerMCPServer](https://github.com/DocMinus/DecimerMCPServer).

## Contributions
Idea and implementation: Docminus

Recent updates include endpoint hardening and improved MCP-oriented usage/documentation.
AI-assisted coding was used for parts of this work (via OpenCode / GPT-based tooling), with manual review and integration by the maintainer.

## License

MIT License — see [LICENSE](./LICENSE) file.
