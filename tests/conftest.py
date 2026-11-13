"""Test configuration with compatibility layer for cross-repo testing."""

import os
import sys
from pathlib import Path

import pytest

# === Compatibility Layer for Cross-Repo Testing ===
# This allows tests to use orrery_integrations imports in both repos
repo_root = Path(__file__).resolve().parents[1]

possible_locations = [
    # Integrations service structure
    repo_root / "src" / "orrery_integrations",
    # OSS structure
    repo_root / "src" / "orrery_mcp",
]

# Find which package structure exists
using_oss = False
for loc in possible_locations:
    if loc.exists() and loc.name == "orrery_mcp":
        using_oss = True
        break

# If in OSS repo, create orrery_integrations compatibility shim
if using_oss:
    import types

    # Create orrery_integrations package
    orrery_integrations = types.ModuleType("orrery_integrations")
    sys.modules["orrery_integrations"] = orrery_integrations

    # Create orrery_integrations.mcp submodule
    mcp_module = types.ModuleType("orrery_integrations.mcp")
    sys.modules["orrery_integrations.mcp"] = mcp_module
    orrery_integrations.mcp = mcp_module  # type: ignore[attr-defined]  # Dynamic attribute

    # Import and expose mcp_server
    from orrery_mcp import mcp_server

    mcp_module.mcp_server = mcp_server  # type: ignore[attr-defined]  # Dynamic attribute
    sys.modules["orrery_integrations.mcp.mcp_server"] = mcp_server

    # Import and expose document_tools_middleware
    from orrery_mcp import document_tools_middleware

    mcp_module.document_tools_middleware = document_tools_middleware  # type: ignore[attr-defined]
    sys.modules["orrery_integrations.mcp.document_tools_middleware"] = (
        document_tools_middleware
    )

    # Import and expose version_requirements
    from orrery_mcp import version_requirements

    mcp_module.version_requirements = version_requirements  # type: ignore[attr-defined]
    sys.modules["orrery_integrations.mcp.version_requirements"] = version_requirements

    # Import and expose graphql_helpers
    from orrery_mcp import graphql_helpers

    mcp_module.graphql_helpers = graphql_helpers  # type: ignore[attr-defined]
    sys.modules["orrery_integrations.mcp.graphql_helpers"] = graphql_helpers

    # Import and expose search_filter_parser
    from orrery_mcp import search_filter_parser

    mcp_module.search_filter_parser = search_filter_parser  # type: ignore[attr-defined]
    sys.modules["orrery_integrations.mcp.search_filter_parser"] = search_filter_parser

    # Import and expose tool_context
    from orrery_mcp import tool_context

    mcp_module.tool_context = tool_context  # type: ignore[attr-defined]
    sys.modules["orrery_integrations.mcp.tool_context"] = tool_context

    # Import and expose view_preference
    from orrery_mcp import view_preference

    mcp_module.view_preference = view_preference  # type: ignore[attr-defined]
    sys.modules["orrery_integrations.mcp.view_preference"] = view_preference

    # Import and expose search_flags
    from orrery_mcp import search_flags

    mcp_module.search_flags = search_flags  # type: ignore[attr-defined]
    sys.modules["orrery_integrations.mcp.search_flags"] = search_flags

    # Import and expose fastmcp_helpers
    from orrery_mcp import fastmcp_helpers

    mcp_module.fastmcp_helpers = fastmcp_helpers  # type: ignore[attr-defined]
    sys.modules["orrery_integrations.mcp.fastmcp_helpers"] = fastmcp_helpers

    # Import and expose arg_validation
    from orrery_mcp import arg_validation

    mcp_module.arg_validation = arg_validation  # type: ignore[attr-defined]
    sys.modules["orrery_integrations.mcp.arg_validation"] = arg_validation

    # Import and expose sub_entity_urls
    from orrery_mcp import sub_entity_urls

    mcp_module.sub_entity_urls = sub_entity_urls  # type: ignore[attr-defined]
    sys.modules["orrery_integrations.mcp.sub_entity_urls"] = sub_entity_urls

    # Import and expose view_helpers
    from orrery_mcp import view_helpers

    mcp_module.view_helpers = view_helpers  # type: ignore[attr-defined]
    sys.modules["orrery_integrations.mcp.view_helpers"] = view_helpers

    # Import and expose _token_estimator
    from orrery_mcp import _token_estimator

    mcp_module._token_estimator = _token_estimator  # type: ignore[attr-defined]
    sys.modules["orrery_integrations.mcp._token_estimator"] = _token_estimator

    # Create orrery_integrations.mcp.tools submodule
    tools_module = types.ModuleType("orrery_integrations.mcp.tools")
    sys.modules["orrery_integrations.mcp.tools"] = tools_module
    mcp_module.tools = tools_module  # type: ignore[attr-defined]

    # Import tool modules directly and get from sys.modules to avoid __init__.py shadowing
    # The __init__.py re-exports functions which shadows the module names

    # Get actual module objects from sys.modules (not the shadowed function refs)
    descriptions_module = sys.modules["orrery_mcp.tools.descriptions"]
    documents_module = sys.modules["orrery_mcp.tools.documents"]
    domains_module = sys.modules["orrery_mcp.tools.domains"]
    get_me_module = sys.modules["orrery_mcp.tools.get_me"]
    owners_module = sys.modules["orrery_mcp.tools.owners"]
    save_document_module = sys.modules["orrery_mcp.tools.save_document"]
    structured_properties_module = sys.modules[
        "orrery_mcp.tools.structured_properties"
    ]
    tags_module = sys.modules["orrery_mcp.tools.tags"]
    terms_module = sys.modules["orrery_mcp.tools.terms"]

    assertions_module = sys.modules["orrery_mcp.tools.assertions"]
    dataset_queries_module = sys.modules["orrery_mcp.tools.dataset_queries"]
    entities_module = sys.modules["orrery_mcp.tools.entities"]
    lineage_module = sys.modules["orrery_mcp.tools.lineage"]
    search_module = sys.modules["orrery_mcp.tools.search"]

    tools_module.assertions = assertions_module  # type: ignore[attr-defined]
    tools_module.dataset_queries = dataset_queries_module  # type: ignore[attr-defined]
    tools_module.descriptions = descriptions_module  # type: ignore[attr-defined]
    tools_module.documents = documents_module  # type: ignore[attr-defined]
    tools_module.domains = domains_module  # type: ignore[attr-defined]
    tools_module.entities = entities_module  # type: ignore[attr-defined]
    tools_module.get_me = get_me_module  # type: ignore[attr-defined]
    tools_module.lineage = lineage_module  # type: ignore[attr-defined]
    tools_module.owners = owners_module  # type: ignore[attr-defined]
    tools_module.save_document = save_document_module  # type: ignore[attr-defined]
    tools_module.search = search_module  # type: ignore[attr-defined]
    tools_module.structured_properties = structured_properties_module  # type: ignore[attr-defined]
    tools_module.tags = tags_module  # type: ignore[attr-defined]
    tools_module.terms = terms_module  # type: ignore[attr-defined]

    sys.modules["orrery_integrations.mcp.tools.assertions"] = assertions_module
    sys.modules["orrery_integrations.mcp.tools.dataset_queries"] = (
        dataset_queries_module
    )
    sys.modules["orrery_integrations.mcp.tools.descriptions"] = descriptions_module
    sys.modules["orrery_integrations.mcp.tools.documents"] = documents_module
    sys.modules["orrery_integrations.mcp.tools.domains"] = domains_module
    sys.modules["orrery_integrations.mcp.tools.entities"] = entities_module
    sys.modules["orrery_integrations.mcp.tools.get_me"] = get_me_module
    sys.modules["orrery_integrations.mcp.tools.lineage"] = lineage_module
    sys.modules["orrery_integrations.mcp.tools.owners"] = owners_module
    sys.modules["orrery_integrations.mcp.tools.save_document"] = save_document_module
    sys.modules["orrery_integrations.mcp.tools.search"] = search_module
    sys.modules["orrery_integrations.mcp.tools.structured_properties"] = (
        structured_properties_module
    )
    sys.modules["orrery_integrations.mcp.tools.tags"] = tags_module
    sys.modules["orrery_integrations.mcp.tools.terms"] = terms_module

# === End Compatibility Layer ===

os.environ["ORRERY_TELEMETRY_ENABLED"] = "false"


@pytest.fixture(scope="module")
def anyio_backend() -> str:
    return "asyncio"
