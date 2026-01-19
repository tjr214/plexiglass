"""
Tests for Advanced Features Demos.
"""

from unittest.mock import MagicMock

import pytest

from plexiglass.gallery.demos.advanced.get_server_capabilities import GetServerCapabilitiesDemo
from plexiglass.gallery.demos.advanced.list_server_activities import ListServerActivitiesDemo


class TestGetServerCapabilitiesDemo:
    """Test suite for GetServerCapabilitiesDemo."""

    @pytest.fixture
    def demo(self):
        """Create a GetServerCapabilitiesDemo instance."""
        return GetServerCapabilitiesDemo()

    def test_demo_metadata(self, demo):
        """Test that demo has correct metadata."""
        assert demo.name == "Get Server Capabilities"
        assert "capabilit" in demo.description.lower()
        assert demo.category == "Advanced Features"
        assert demo.operation_type == "READ"

    def test_get_parameters(self, demo):
        """Test parameter definition."""
        params = demo.get_parameters()
        assert len(params) == 0

    def test_get_code_example(self, demo):
        """Test code example generation."""
        code = demo.get_code_example()
        assert "capabilit" in code.lower() or "feature" in code.lower()

    def test_execute_without_server(self, demo):
        """Test execute without server returns error."""
        result = demo.execute(None, {})
        assert "error" in result
        assert "No server connection" in result["error"]

    def test_execute_success(self, demo):
        """Test successful capabilities retrieval."""
        server = MagicMock()
        server.machineIdentifier = "test123"
        server.version = "1.32.0"

        result = demo.execute(server, {})

        assert "capabilities" in result or "info" in result or "features" in result

    def test_execute_handles_exception(self, demo):
        """Test that exceptions are handled gracefully."""
        server = MagicMock()
        server.version.side_effect = Exception("Error")

        result = demo.execute(server, {})

        assert "error" in result or "capabilities" in result


class TestListServerActivitiesDemo:
    """Test suite for ListServerActivitiesDemo."""

    @pytest.fixture
    def demo(self):
        """Create a ListServerActivitiesDemo instance."""
        return ListServerActivitiesDemo()

    def test_demo_metadata(self, demo):
        """Test that demo has correct metadata."""
        assert demo.name == "List Server Activities"
        assert "activit" in demo.description.lower()
        assert demo.category == "Advanced Features"
        assert demo.operation_type == "READ"

    def test_get_parameters(self, demo):
        """Test parameter definition."""
        params = demo.get_parameters()
        assert len(params) == 0

    def test_get_code_example(self, demo):
        """Test code example generation."""
        code = demo.get_code_example()
        assert "activit" in code.lower()

    def test_execute_without_server(self, demo):
        """Test execute without server returns error."""
        result = demo.execute(None, {})
        assert "error" in result
        assert "No server connection" in result["error"]

    def test_execute_success(self, demo):
        """Test successful activities listing."""
        server = MagicMock()

        # Mock activities
        mock_activity = MagicMock()
        mock_activity.title = "Scanning library"
        mock_activity.progress = 50

        server.activities.return_value = [mock_activity]

        result = demo.execute(server, {})

        assert "activities" in result or "message" in result

    def test_execute_handles_exception(self, demo):
        """Test that exceptions are handled gracefully."""
        server = MagicMock()
        server.activities.side_effect = Exception("Error")

        result = demo.execute(server, {})

        assert "error" in result or "message" in result
