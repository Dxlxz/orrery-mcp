# mypy: disable-error-code="type-abstract"
from unittest.mock import MagicMock, patch

import pytest
from orrery.ingestion.graph.client import OrreryGraph
from orrery.sdk.main_client import OrreryClient

from orrery_integrations.mcp.mcp_server import (
    MCPContext,
    get_orrery_client,
    get_mcp_context,
    with_orrery_client,
)
from orrery_integrations.mcp.tool_context import ToolContext
from orrery_integrations.mcp.view_helpers import (
    _user_view_cache,
    fetch_user_default_view,
)
from orrery_integrations.mcp.view_preference import (
    CustomView,
    NoView,
    UseDefaultView,
    ViewPreference,
)

_PATCH_USER = "orrery_integrations.mcp.view_preference.fetch_user_default_view"
_PATCH_GLOBAL = "orrery_integrations.mcp.view_preference.fetch_global_default_view"


@pytest.fixture
def mock_graph() -> MagicMock:
    return MagicMock(spec=OrreryGraph)


@pytest.fixture
def mock_client(mock_graph: MagicMock) -> MagicMock:
    client = MagicMock(spec=OrreryClient)
    client._graph = mock_graph
    return client


class TestViewPreference:
    def test_no_view_returns_none(self, mock_graph: MagicMock) -> None:
        assert NoView().get_view(mock_graph) is None

    def test_custom_view_returns_urn(self, mock_graph: MagicMock) -> None:
        urn = "urn:li:orreryView:my-view"
        assert CustomView(urn=urn).get_view(mock_graph) == urn

    @patch(_PATCH_GLOBAL)
    @patch(_PATCH_USER)
    def test_use_default_view_prefers_user_view(
        self,
        mock_user: MagicMock,
        mock_global: MagicMock,
        mock_graph: MagicMock,
    ) -> None:
        mock_user.return_value = "urn:li:orreryView:user-default"
        mock_global.return_value = "urn:li:orreryView:global-default"
        result = UseDefaultView().get_view(mock_graph)
        assert result == "urn:li:orreryView:user-default"
        mock_user.assert_called_once_with(mock_graph)
        mock_global.assert_not_called()

    @patch(_PATCH_GLOBAL)
    @patch(_PATCH_USER)
    def test_use_default_view_falls_back_to_global(
        self,
        mock_user: MagicMock,
        mock_global: MagicMock,
        mock_graph: MagicMock,
    ) -> None:
        mock_user.return_value = None
        mock_global.return_value = "urn:li:orreryView:global-default"
        result = UseDefaultView().get_view(mock_graph)
        assert result == "urn:li:orreryView:global-default"
        mock_user.assert_called_once_with(mock_graph)
        mock_global.assert_called_once_with(mock_graph)

    @patch(_PATCH_GLOBAL)
    @patch(_PATCH_USER)
    def test_use_default_view_returns_none_when_no_defaults(
        self,
        mock_user: MagicMock,
        mock_global: MagicMock,
        mock_graph: MagicMock,
    ) -> None:
        mock_user.return_value = None
        mock_global.return_value = None
        assert UseDefaultView().get_view(mock_graph) is None

    def test_custom_view_is_frozen(self) -> None:
        view = CustomView(urn="urn:li:orreryView:test")
        with pytest.raises(AttributeError):
            view.urn = "something-else"  # type: ignore[misc]

    def test_no_view_is_frozen(self) -> None:
        view = NoView()
        with pytest.raises(AttributeError):
            view.foo = "bar"  # type: ignore[attr-defined]


def _me_response(view_urn: str) -> dict:
    """Build the nested ``me`` GraphQL response for a given default view URN."""
    return {
        "me": {"corpUser": {"settings": {"views": {"defaultView": {"urn": view_urn}}}}}
    }


class TestFetchUserDefaultView:
    @pytest.fixture(autouse=True)
    def _clear_cache(self) -> None:
        _user_view_cache.clear()

    @patch("orrery_integrations.mcp.view_helpers.graphql_helpers")
    def test_returns_user_default_view_urn(
        self, mock_gql: MagicMock, mock_graph: MagicMock
    ) -> None:
        mock_gql.execute_graphql.return_value = _me_response(
            "urn:li:orreryView:user-view"
        )
        assert fetch_user_default_view(mock_graph) == "urn:li:orreryView:user-view"

    @patch("orrery_integrations.mcp.view_helpers.graphql_helpers")
    def test_returns_none_when_no_settings(
        self, mock_gql: MagicMock, mock_graph: MagicMock
    ) -> None:
        mock_gql.execute_graphql.return_value = {"me": {"corpUser": {"settings": None}}}
        assert fetch_user_default_view(mock_graph) is None

    @patch("orrery_integrations.mcp.view_helpers.graphql_helpers")
    def test_returns_none_when_no_default_view(
        self, mock_gql: MagicMock, mock_graph: MagicMock
    ) -> None:
        mock_gql.execute_graphql.return_value = {
            "me": {"corpUser": {"settings": {"views": {"defaultView": None}}}}
        }
        assert fetch_user_default_view(mock_graph) is None

    @patch("orrery_integrations.mcp.view_helpers.graphql_helpers")
    def test_returns_none_when_me_is_empty(
        self, mock_gql: MagicMock, mock_graph: MagicMock
    ) -> None:
        mock_gql.execute_graphql.return_value = {"me": None}
        assert fetch_user_default_view(mock_graph) is None

    @patch("orrery_integrations.mcp.view_helpers.graphql_helpers")
    def test_returns_none_on_graphql_error(
        self, mock_gql: MagicMock, mock_graph: MagicMock
    ) -> None:
        mock_gql.execute_graphql.side_effect = RuntimeError("unauthorized")
        assert fetch_user_default_view(mock_graph) is None

    @patch("orrery_integrations.mcp.view_helpers.DISABLE_DEFAULT_VIEW", True)
    def test_returns_none_when_feature_disabled(self, mock_graph: MagicMock) -> None:
        assert fetch_user_default_view(mock_graph) is None

    @patch("orrery_integrations.mcp.view_helpers.graphql_helpers")
    def test_caches_result_per_graph_instance(
        self, mock_gql: MagicMock, mock_graph: MagicMock
    ) -> None:
        mock_gql.execute_graphql.return_value = _me_response(
            "urn:li:orreryView:cached"
        )
        assert fetch_user_default_view(mock_graph) == "urn:li:orreryView:cached"
        assert fetch_user_default_view(mock_graph) == "urn:li:orreryView:cached"
        mock_gql.execute_graphql.assert_called_once()

    @patch("orrery_integrations.mcp.view_helpers.graphql_helpers")
    def test_separate_cache_per_graph(self, mock_gql: MagicMock) -> None:
        graph_a = MagicMock(spec=OrreryGraph)
        graph_b = MagicMock(spec=OrreryGraph)

        mock_gql.execute_graphql.side_effect = [
            _me_response("urn:li:orreryView:user-a"),
            _me_response("urn:li:orreryView:user-b"),
        ]

        assert fetch_user_default_view(graph_a) == "urn:li:orreryView:user-a"
        assert fetch_user_default_view(graph_b) == "urn:li:orreryView:user-b"
        assert mock_gql.execute_graphql.call_count == 2


class TestToolContext:
    def test_get_by_base_type(self) -> None:
        ctx = ToolContext([NoView()])
        result = ctx.get(ViewPreference)
        assert isinstance(result, NoView)

    def test_first_match_wins(self) -> None:
        ctx = ToolContext([NoView(), CustomView(urn="urn:li:orreryView:second")])
        result = ctx.get(ViewPreference)
        assert isinstance(result, NoView)

    def test_returns_default_when_missing(self) -> None:
        ctx = ToolContext([])
        default = UseDefaultView()
        result = ctx.get(ViewPreference, default)
        assert result is default

    def test_returns_none_when_missing_no_default(self) -> None:
        ctx = ToolContext([])
        assert ctx.get(ViewPreference) is None

    def test_empty_bag(self) -> None:
        ctx = ToolContext()
        assert ctx.get(ViewPreference) is None

    def test_exact_type_match(self) -> None:
        view = CustomView(urn="urn:li:orreryView:test")
        ctx = ToolContext([view])
        assert ctx.get(CustomView) is view

    def test_unrelated_types_not_found(self) -> None:
        ctx = ToolContext(["a string", 42])
        assert ctx.get(ViewPreference) is None


class TestMCPContext:
    def test_defaults_to_empty_tool_context(self, mock_client: MagicMock) -> None:
        ctx = MCPContext(client=mock_client)
        assert ctx.tool_context.get(ViewPreference) is None

    def test_accepts_tool_context_with_view(self, mock_client: MagicMock) -> None:
        view = NoView()
        ctx = MCPContext(client=mock_client, tool_context=ToolContext([view]))
        assert ctx.tool_context.get(ViewPreference) is view


class TestWithOrreryClient:
    def test_sets_and_resets_context(self, mock_client: MagicMock) -> None:
        with with_orrery_client(mock_client):
            ctx = get_mcp_context()
            assert ctx.client is mock_client
            assert ctx.tool_context.get(ViewPreference) is None
        with pytest.raises(LookupError):
            get_mcp_context()

    def test_passes_tool_context_through(self, mock_client: MagicMock) -> None:
        tc = ToolContext([NoView()])
        with with_orrery_client(mock_client, tool_context=tc):
            ctx = get_mcp_context()
            assert isinstance(ctx.tool_context.get(ViewPreference), NoView)

    def test_get_orrery_client_returns_client(self, mock_client: MagicMock) -> None:
        with with_orrery_client(mock_client):
            assert get_orrery_client() is mock_client

    def test_defaults_to_empty_tool_context_when_none(
        self, mock_client: MagicMock
    ) -> None:
        with with_orrery_client(mock_client, tool_context=None):
            ctx = get_mcp_context()
            assert ctx.tool_context.get(ViewPreference) is None

    def test_nested_contexts_restore_correctly(self, mock_client: MagicMock) -> None:
        outer_tc = ToolContext([NoView()])
        inner_tc = ToolContext([CustomView(urn="urn:li:orreryView:inner")])

        with with_orrery_client(mock_client, tool_context=outer_tc):
            assert isinstance(
                get_mcp_context().tool_context.get(ViewPreference), NoView
            )

            with with_orrery_client(mock_client, tool_context=inner_tc):
                assert isinstance(
                    get_mcp_context().tool_context.get(ViewPreference), CustomView
                )

            assert isinstance(
                get_mcp_context().tool_context.get(ViewPreference), NoView
            )
