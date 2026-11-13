# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Model Context Protocol (MCP) server implementation for Orrery. The server provides tools for searching entities, fetching metadata, traversing lineage graphs, and listing SQL queries. It's built using the FastMCP framework and integrates with Orrery's GraphQL API.

## Development Commands

See [DEVELOPING.md](DEVELOPING.md) and [Makefile](Makefile) for more details.

A quick summary is below:

- `make setup` - Set up development environment (requires uv)
- `make lint` - Run ruff formatting, linting and type checking
- `make test` - Run pytest tests (most run offline; only the integration tests need a live Orrery instance)
- `make clean` - Clean up build artifacts

## Testing

- Run all tests: `make test`
- Single test file: `uv run pytest tests/test_mcp/test_search_documents.py`
- Most tests run offline against mocked GraphQL responses — no Orrery instance needed.
- The integration tests in `tests/test_mcp_integration.py` require a live Orrery instance
  with authentication (`ORRERY_GMS_URL` / `ORRERY_GMS_TOKEN`, or `~/.orreryenv`). They
  skip automatically when no credentials are available.

## Development Setup

Run the server using MCP inspector for development:

```bash
uv run fastmcp dev src/orrery_mcp/__main__.py --with-editable .
```

> **Note:** Use `fastmcp dev` (not `mcp dev`), since this project uses the standalone FastMCP package.

## Architecture

### Core Components

- **mcp_server.py**: Main server implementation with MCP tools

  - `get_entity()`: Fetch entity metadata by URN
  - `search()`: Search across Orrery entities with filters
  - `get_dataset_queries()`: Get SQL queries for datasets
  - `get_lineage()`: Traverse upstream/downstream lineage

- **GraphQL Integration**: Uses GraphQL fragments for efficient queries

  - `gql/search.gql`: Search queries
  - `gql/entity_details.gql`: Entity metadata queries
  - `gql/queries.gql`: SQL query retrieval

- **Client Management**: Context-aware Orrery client handling
  - Uses contextvars for thread-safe client management
  - Supports both Orrery Cloud and on-premise instances

### Key Patterns

- All tools return cleaned GraphQL responses (removes `__typename` fields)
- Orrery Cloud instances get URL injection for entities
- Filter compilation uses Orrery SDK's `compile_filters()`
- Lineage traversal supports configurable hop limits (1-3+ degrees)

## Authentication

Server requires Orrery authentication via:

- Environment variables: `ORRERY_GMS_URL`, `ORRERY_GMS_TOKEN`
- Or `~/.orreryenv` configuration file

## Version Management

Uses setuptools-scm for dynamic versioning from git tags. Version file is auto-generated at `src/orrery_mcp/_version.py`.
