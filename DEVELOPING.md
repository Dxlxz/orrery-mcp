## Developing

### Setup

Requires [`uv`](https://docs.astral.sh/uv/) - see the [project README](README.md) for installation instructions.

```bash
make setup

# <authentication is the same as in production>
```

### Run using the MCP inspector

```bash
uv run fastmcp dev src/orrery_mcp/__main__.py:create_app --with-editable .
```

In the inspector UI, add environment variables for `ORRERY_GMS_URL` and `ORRERY_GMS_TOKEN`, then click Connect.

> **Note:** Use `fastmcp dev` (not `mcp dev`), since this project uses the standalone FastMCP package.

### Run using an MCP client

Use this configuration in your MCP client e.g. Claude Desktop, Cursor, etc.

```js
{
  "mcpServers": {
    "orrery": {
      "command": "<full-path-to-uv>",  // e.g. /Users/hsheth/.local/bin/uv
      "args": [
        "--directory",
        "path/to/orrery-mcp",  // update this with an absolute path
        "run",
        "orrery-mcp"
      ],
      "env": {  // required if ~/.orreryenv does not exist
        "ORRERY_GMS_URL": "<your-orrery-url>",
        "ORRERY_GMS_TOKEN": "<your-orrery-token>"
      }
    }
  }
}
```

### Run linting

```bash
# Check linting
make lint-check

# Fix linting
make lint
```

### Run tests

```bash
make test
```

Most of the suite runs offline against mocked GraphQL responses and needs no Orrery
instance. The integration tests in `tests/test_mcp_integration.py` do require a live
Orrery and credentials — they skip automatically when none are configured.

## Publishing

We use setuptools-scm to manage the version number.

CI will automatically publish a new release to PyPI when a GitHub release is created.
