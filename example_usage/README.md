# Example Usage Guide

Use this quick guide to choose the right example script.

For direct API call snippets (Python/curl), see [`API_EXAMPLES.md`](./API_EXAMPLES.md).

## Beginner

- `decimer_server_usage_example.py`
  - Use when you run the DECIMER server and want a simple Python client call.
  - Best first script for local development.

## Intermediate

- `decimer_naked_api_eg_docker_only_example.py`
  - Use when you want direct HTTP requests without the `decimerapi` wrapper.
  - Works with Docker or local server, as long as the endpoint is reachable.

## Advanced / Special Case

- `decimer_standalone_no_server.py`
  - Use when you intentionally want standalone local inference without running the API server.
  - Requires full local ML runtime setup.

## Sample Input Files

- `structure.png` - molecule image example
- `not_structure.gif` - non-structure image example
