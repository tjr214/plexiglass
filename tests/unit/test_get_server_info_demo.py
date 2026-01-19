"""
Tests for the GetServerInfoDemo sample gallery demo.

This is a proof-of-concept demo to validate the BaseDemo and Registry systems.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from plexiglass.gallery.demos.server.get_server_info import GetServerInfoDemo


class TestGetServerInfoDemo:
    """Test suite for GetServerInfoDemo class."""

    def test_demo_has_correct_metadata(self) -> None:
        """Demo should have correct name, description, category, and operation type."""
        demo = GetServerInfoDemo()

        assert demo.name == "Get Server Info"
        assert demo.description == "Retrieve basic server information and status"
        assert demo.category == "Server & Connection"
        assert demo.operation_type == "READ"

    def test_demo_provides_code_example(self) -> None:
        """Demo should provide a code example showing how to use the API."""
        demo = GetServerInfoDemo()
        code = demo.get_code_example()

        assert isinstance(code, str)
        assert len(code) > 0
        assert "PlexServer" in code
        assert "friendlyName" in code or "version" in code

    def test_demo_execute_with_mock_server(self) -> None:
        """Demo should execute and return server information."""
        # Create a mock PlexServer
        mock_server = MagicMock()
        mock_server.friendlyName = "My Plex Server"
        mock_server.version = "1.32.8.7639"
        mock_server.platform = "Linux"
        mock_server.platformVersion = "6.1.0"
        mock_server.machineIdentifier = "abc123xyz"

        demo = GetServerInfoDemo()
        result = demo.execute(server=mock_server, params={})

        # Verify result structure
        assert isinstance(result, dict)
        assert "friendlyName" in result
        assert "version" in result
        assert "platform" in result

        # Verify values
        assert result["friendlyName"] == "My Plex Server"
        assert result["version"] == "1.32.8.7639"
        assert result["platform"] == "Linux"

    def test_demo_handles_none_server_gracefully(self) -> None:
        """Demo should handle None server gracefully."""
        demo = GetServerInfoDemo()
        result = demo.execute(server=None, params={})

        # Should return error or empty result
        assert isinstance(result, dict)
        assert "error" in result or len(result) == 0

    def test_demo_get_parameters_returns_empty_list(self) -> None:
        """Demo should have no parameters (reads server info directly)."""
        demo = GetServerInfoDemo()
        params = demo.get_parameters()

        assert isinstance(params, list)
        assert len(params) == 0

    def test_demo_validate_params_always_valid(self) -> None:
        """Demo should validate successfully with any params (no required params)."""
        demo = GetServerInfoDemo()

        # Empty params should be valid
        is_valid, error = demo.validate_params({})
        assert is_valid is True
        assert error is None

        # Any params should be valid
        is_valid, error = demo.validate_params({"foo": "bar"})
        assert is_valid is True
        assert error is None

    def test_demo_get_metadata(self) -> None:
        """Demo should provide consolidated metadata."""
        demo = GetServerInfoDemo()
        metadata = demo.get_metadata()

        assert metadata["name"] == "Get Server Info"
        assert metadata["category"] == "Server & Connection"
        assert metadata["operation_type"] == "READ"
        assert "description" in metadata

    def test_demo_result_includes_multiple_server_properties(self) -> None:
        """Demo should return multiple server properties for comprehensive info."""
        mock_server = MagicMock()
        mock_server.friendlyName = "Test Server"
        mock_server.version = "1.0.0"
        mock_server.platform = "Windows"
        mock_server.platformVersion = "10.0"
        mock_server.machineIdentifier = "test123"

        demo = GetServerInfoDemo()
        result = demo.execute(server=mock_server, params={})

        # Should return at least 3-4 properties
        assert len(result) >= 3
        assert all(isinstance(k, str) for k in result.keys())
        assert all(isinstance(v, str) for v in result.values() if v is not None)
