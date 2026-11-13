# MCP Server Sync Status — 2026-04-10

## Repositories

- **OSS**: `orrery-mcp` (standalone MCP server)
- **Cloud**: `orrery-fork` → `orrery-integrations-service/src/orrery_integrations/mcp/`

## Last Full Sync Point

Commit `23dc142` (2026-03-11) — "Sync MCP server from fork: modular tools architecture (#91)"

## OSS Commits Since Last Sync

| Commit | Date | Description | Applied to Cloud? |
|--------|------|-------------|-------------------|
| `54d8886` | 2026-03-16 | feat: capture MCP client identity in telemetry events (#96) | **No** — touches `_telemetry.py` which is OSS-only; cloud has its own `mcp_telemetry.py` with SaaS-specific telemetry via `track_saas_event` |
| `d1d18e3` | 2026-04-06 | Fixes: Gemini GenAI API 400 error — revert `keywords` type (#98) | **Yes** — applied to cloud `entities.py`: `Optional[List[str] \| str]` → `Optional[List[str]]` |
| `ba7100b` | 2026-04-10 | Exclude fakeredis 2.35.0 to fix startup crash/hang (#111) | **No** — only touches OSS `pyproject.toml`; cloud manages dependencies separately |
| `790eac2` | 2026-04-10 | add readOnlyHint to read tools in mcp (#105) | **Yes** — applied `@read_only` decorator + `readOnlyHint` annotation to cloud |

## Cloud-Only Changes (Present in Cloud, Not Yet in OSS)

These are changes in the cloud fork that need to be synced to OSS (direction: Cloud → OSS).

### Shared File Divergences

1. **`mcp_server.py`**
   - Cloud uses `from orrery_integrations.mcp.fastmcp_helpers import list_mcp_tools_sync` instead of `mcp._tool_manager._tools.values()` for tool listing
   - Cloud imports `FastMCPTool` from `fastmcp.tools` (not `fastmcp.tools.tool`)
   - Cloud removed `cachetools`, `OrreryGraph`, `graphql_helpers` imports (view config moved to `view_helpers`)
   - Cloud adds ask_orrery_tools registration block
   - Cloud uses `string.Template` for `$FILTER_DOCS` substitution in lineage docstring

2. **`graphql_helpers.py`**
   - Cloud adds `SubEntityResolver` from `sub_entity_urls` for URL resolution
   - Cloud handles `None` URL values by omitting the url field

3. **`search_filter_parser.py`**
   - Cloud adds structured property filter documentation
   - Cloud adds `_normalize_sp_field()` for URN vs qualifiedName handling
   - Cloud adds boolean field aliases and `_normalize_boolean()` / `_make_boolean_filter()` helpers
   - Cloud adds `_BOOLEAN_FIELDS` set

4. **`document_tools_middleware.py`**
   - Cloud updates docstring to use `list_mcp_tools_sync()` instead of `_tool_manager`

5. **`view_preference.py`**
   - Cloud adds two-tier view fallback (user default → org global default) via `view_helpers`

6. **`tools/assertions.py`**
   - Cloud adds sub-entity URL injection using `SUB_ENTITY_CONFIGS` and `make_sub_entity_url()`

7. **`tools/lineage.py`**
   - Cloud uses `string.Template` for `$FILTER_DOCS` injection into docstring
   - Cloud imports `FILTER_DOCS` from `search_filter_parser`

8. **`tools/save_document.py`**
   - Cloud adds `create_user_scoped_document()` for private user-scoped memory documents
   - Cloud adds `TYPE_CHECKING` conditional import and `CorpUserUrn`

### Cloud-Only Files (Not Shared)

These files exist only in cloud and are not synced to OSS:

- `router.py` — FastAPI routing with token auth and SSE endpoints
- `mcp_telemetry.py` — SaaS event tracking via `track_saas_event`
- `fastmcp_helpers.py` — `list_mcp_tools_sync()` compat bridge for FastMCP v3+
- `view_helpers.py` — Default view resolution with TTL caching
- `sub_entity_urls.py` — Sub-entity URL resolution for assertions/incidents

## OSS-Only Files (Not Shared)

- `__main__.py` — Standalone entry point
- `_telemetry.py` — OSS telemetry with MCP client identity capture (commit `54d8886`)
- `_version.py` — Auto-generated from git tags via setuptools-scm

## Next Steps

1. Run `sync-mcp-server` skill to bring cloud changes → OSS
2. The sync will handle the shared file updates and create a compatibility shim for cloud-only imports
