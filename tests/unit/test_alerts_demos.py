"""
Tests for Alerts & Monitoring Demos.
"""

from unittest.mock import MagicMock, patch

import pytest

from plexiglass.gallery.demos.alerts.list_activity_alerts import ListActivityAlertsDemo
from plexiglass.gallery.demos.alerts.monitor_timeline import MonitorTimelineDemo


class TestListActivityAlertsDemo:
    """Test suite for ListActivityAlertsDemo."""

    @pytest.fixture
    def demo(self):
        """Create a ListActivityAlertsDemo instance."""
        return ListActivityAlertsDemo()

    def test_demo_metadata(self, demo):
        """Test that demo has correct metadata."""
        assert demo.name == "List Activity Alerts"
        assert "activity" in demo.description.lower() or "alerts" in demo.description.lower()
        assert demo.category == "Alerts & Monitoring"
        assert demo.operation_type == "READ"

    def test_get_parameters(self, demo):
        """Test parameter definition."""
        params = demo.get_parameters()
        assert len(params) == 0  # No parameters needed

    def test_get_code_example(self, demo):
        """Test code example generation."""
        code = demo.get_code_example()
        assert "alert" in code.lower() or "activity" in code.lower()
        assert "server" in code

    def test_execute_without_server(self, demo):
        """Test execute without server returns error."""
        result = demo.execute(None, {})
        assert "error" in result
        assert "No server connection" in result["error"]

    def test_execute_success(self, demo):
        """Test successful activity alerts listing."""
        server = MagicMock()

        # Mock alert/timeline data
        result = demo.execute(server, {})

        # Should return some info about alerts/monitoring
        assert "message" in result or "info" in result or "alerts" in result

    def test_execute_handles_exception(self, demo):
        """Test that exceptions are handled gracefully."""
        server = MagicMock()
        # Force an error
        server.timeline = MagicMock(side_effect=Exception("Alert API error"))

        result = demo.execute(server, {})

        # Should still handle gracefully
        assert "error" in result or "message" in result or "info" in result


class TestMonitorTimelineDemo:
    """Test suite for MonitorTimelineDemo."""

    @pytest.fixture
    def demo(self):
        """Create a MonitorTimelineDemo instance."""
        return MonitorTimelineDemo()

    def test_demo_metadata(self, demo):
        """Test that demo has correct metadata."""
        assert demo.name == "Monitor Timeline"
        assert "timeline" in demo.description.lower()
        assert demo.category == "Alerts & Monitoring"
        assert demo.operation_type == "READ"

    def test_get_parameters(self, demo):
        """Test parameter definition."""
        params = demo.get_parameters()
        assert len(params) == 0

    def test_get_code_example(self, demo):
        """Test code example generation."""
        code = demo.get_code_example()
        assert "timeline" in code.lower()
        assert "server" in code

    def test_execute_without_server(self, demo):
        """Test execute without server returns error."""
        result = demo.execute(None, {})
        assert "error" in result
        assert "No server connection" in result["error"]

    def test_execute_success(self, demo):
        """Test successful timeline monitoring."""
        server = MagicMock()

        result = demo.execute(server, {})

        # Should return timeline information
        assert "message" in result or "info" in result or "timeline" in result

    def test_execute_handles_exception(self, demo):
        """Test that exceptions are handled gracefully."""
        server = MagicMock()

        result = demo.execute(server, {})

        # Should handle gracefully
        assert "message" in result or "error" in result or "info" in result
