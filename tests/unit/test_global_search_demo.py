"""
Tests for Global Search Demo.
"""

from unittest.mock import MagicMock

import pytest

from plexiglass.gallery.demos.search.global_search import GlobalSearchDemo


class TestGlobalSearchDemo:
    """Test suite for GlobalSearchDemo."""

    @pytest.fixture
    def demo(self):
        """Create a GlobalSearchDemo instance."""
        return GlobalSearchDemo()

    def test_demo_metadata(self, demo):
        """Test that demo has correct metadata."""
        assert demo.name == "Global Search"
        assert demo.description == "Search across all libraries for any media"
        assert demo.category == "Search & Discovery"
        assert demo.operation_type == "READ"

    def test_get_parameters(self, demo):
        """Test parameter definition."""
        params = demo.get_parameters()
        assert len(params) == 1
        assert params[0]["name"] == "query"
        assert params[0]["type"] == "str"
        assert params[0]["required"] is True

    def test_get_code_example(self, demo):
        """Test code example generation."""
        code = demo.get_code_example()
        assert "server.search" in code
        assert "search" in code.lower()

    def test_get_code_example_with_params(self, demo):
        """Test code example with custom params."""
        code = demo.get_code_example({"query": "Star Wars"})
        assert "Star Wars" in code

    def test_execute_without_server(self, demo):
        """Test execute without server returns error."""
        result = demo.execute(None, {})
        assert "error" in result
        assert "No server connection" in result["error"]

    def test_execute_without_query(self, demo):
        """Test execute without query param."""
        server = MagicMock()
        result = demo.execute(server, {})
        assert "error" in result
        assert "query" in result["error"].lower()

    def test_execute_success(self, demo):
        """Test successful search execution."""
        # Mock server with search results
        server = MagicMock()
        mock_result1 = MagicMock()
        mock_result1.title = "Star Wars: A New Hope"
        mock_result1.type = "movie"
        mock_result1.ratingKey = 123

        mock_result2 = MagicMock()
        mock_result2.title = "Star Wars: Empire Strikes Back"
        mock_result2.type = "movie"
        mock_result2.ratingKey = 456

        server.search.return_value = [mock_result1, mock_result2]

        # Execute demo
        result = demo.execute(server, {"query": "Star Wars"})

        # Verify results
        assert "results" in result
        assert len(result["results"]) == 2
        assert result["results"][0]["title"] == "Star Wars: A New Hope"
        assert result["results"][0]["type"] == "movie"
        assert result["results"][1]["title"] == "Star Wars: Empire Strikes Back"

        # Verify search was called with correct query
        server.search.assert_called_once_with("Star Wars")

    def test_execute_empty_results(self, demo):
        """Test execution with no search results."""
        server = MagicMock()
        server.search.return_value = []

        result = demo.execute(server, {"query": "NonexistentMovie12345"})

        assert "results" in result
        assert len(result["results"]) == 0

    def test_execute_handles_exception(self, demo):
        """Test that exceptions are handled gracefully."""
        server = MagicMock()
        server.search.side_effect = Exception("Search failed")

        result = demo.execute(server, {"query": "test"})

        assert "error" in result
        assert "Search failed" in result["error"]

    def test_validate_params_missing_query(self, demo):
        """Test parameter validation with missing query."""
        is_valid, error = demo.validate_params({})
        assert is_valid is False
        assert "query" in error

    def test_validate_params_with_query(self, demo):
        """Test parameter validation with valid query."""
        is_valid, error = demo.validate_params({"query": "test"})
        assert is_valid is True
        assert error is None
