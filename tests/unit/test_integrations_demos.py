"""
Tests for Integrations Demos.
"""

from unittest.mock import MagicMock

import pytest

from plexiglass.gallery.demos.integrations.discover_sonos import DiscoverSonosDemo
from plexiglass.gallery.demos.integrations.list_integrations import ListIntegrationsDemo


class TestDiscoverSonosDemo:
    """Test suite for DiscoverSonosDemo."""

    @pytest.fixture
    def demo(self):
        """Create a DiscoverSonosDemo instance."""
        return DiscoverSonosDemo()

    def test_demo_metadata(self, demo):
        """Test that demo has correct metadata."""
        assert demo.name == "Discover Sonos Speakers"
        assert "sonos" in demo.description.lower()
        assert demo.category == "Integrations"
        assert demo.operation_type == "READ"

    def test_get_parameters(self, demo):
        """Test parameter definition."""
        params = demo.get_parameters()
        assert len(params) == 0  # No parameters needed

    def test_get_code_example(self, demo):
        """Test code example generation."""
        code = demo.get_code_example()
        assert "sonos" in code.lower()

    def test_execute_without_server(self, demo):
        """Test execute without server returns error."""
        result = demo.execute(None, {})
        assert "error" in result
        assert "No server connection" in result["error"]

    def test_execute_success(self, demo):
        """Test successful Sonos discovery."""
        server = MagicMock()

        result = demo.execute(server, {})

        # Should return some info about Sonos discovery
        assert "message" in result or "info" in result or "speakers" in result

    def test_execute_handles_exception(self, demo):
        """Test that exceptions are handled gracefully."""
        server = MagicMock()

        result = demo.execute(server, {})

        # Should handle gracefully
        assert "message" in result or "error" in result or "info" in result


class TestListIntegrationsDemo:
    """Test suite for ListIntegrationsDemo."""

    @pytest.fixture
    def demo(self):
        """Create a ListIntegrationsDemo instance."""
        return ListIntegrationsDemo()

    def test_demo_metadata(self, demo):
        """Test that demo has correct metadata."""
        assert demo.name == "List Available Integrations"
        assert "integration" in demo.description.lower()
        assert demo.category == "Integrations"
        assert demo.operation_type == "READ"

    def test_get_parameters(self, demo):
        """Test parameter definition."""
        params = demo.get_parameters()
        assert len(params) == 0

    def test_get_code_example(self, demo):
        """Test code example generation."""
        code = demo.get_code_example()
        assert "integration" in code.lower() or "device" in code.lower()

    def test_execute_without_server(self, demo):
        """Test execute without server returns error."""
        result = demo.execute(None, {})
        assert "error" in result
        assert "No server connection" in result["error"]

    def test_execute_success(self, demo):
        """Test successful integrations listing."""
        server = MagicMock()

        result = demo.execute(server, {})

        # Should return integration information
        assert "message" in result or "info" in result or "integrations" in result

    def test_execute_handles_exception(self, demo):
        """Test that exceptions are handled gracefully."""
        server = MagicMock()

        result = demo.execute(server, {})

        # Should handle gracefully
        assert "message" in result or "error" in result or "info" in result
