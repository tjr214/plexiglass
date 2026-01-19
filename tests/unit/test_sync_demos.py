"""
Tests for Sync & Offline Demos.
"""

from unittest.mock import MagicMock

import pytest

from plexiglass.gallery.demos.sync.list_sync_items import ListSyncItemsDemo
from plexiglass.gallery.demos.sync.get_sync_status import GetSyncStatusDemo


class TestListSyncItemsDemo:
    """Test suite for ListSyncItemsDemo."""

    @pytest.fixture
    def demo(self):
        """Create a ListSyncItemsDemo instance."""
        return ListSyncItemsDemo()

    def test_demo_metadata(self, demo):
        """Test that demo has correct metadata."""
        assert demo.name == "List Sync Items"
        assert "sync items" in demo.description.lower()
        assert demo.category == "Sync & Offline"
        assert demo.operation_type == "READ"

    def test_get_parameters(self, demo):
        """Test parameter definition."""
        params = demo.get_parameters()
        assert len(params) == 0  # No parameters needed

    def test_get_code_example(self, demo):
        """Test code example generation."""
        code = demo.get_code_example()
        assert "syncItems" in code or "sync_items" in code
        assert "server" in code

    def test_execute_without_server(self, demo):
        """Test execute without server returns error."""
        result = demo.execute(None, {})
        assert "error" in result
        assert "No server connection" in result["error"]

    def test_execute_success(self, demo):
        """Test successful sync items listing."""
        # Mock server with sync items
        server = MagicMock()
        mock_sync1 = MagicMock()
        mock_sync1.title = "Movies for Travel"
        mock_sync1.clientIdentifier = "device123"
        mock_sync1.status = "complete"

        mock_sync2 = MagicMock()
        mock_sync2.title = "TV Shows Collection"
        mock_sync2.clientIdentifier = "device456"
        mock_sync2.status = "processing"

        server.syncItems.return_value = [mock_sync1, mock_sync2]

        # Execute demo
        result = demo.execute(server, {})

        # Verify results
        assert "sync_items" in result
        assert len(result["sync_items"]) == 2
        assert result["sync_items"][0]["title"] == "Movies for Travel"
        assert result["sync_items"][1]["status"] == "processing"

    def test_execute_empty_results(self, demo):
        """Test execution with no sync items."""
        server = MagicMock()
        server.syncItems.return_value = []

        result = demo.execute(server, {})

        assert "sync_items" in result
        assert len(result["sync_items"]) == 0

    def test_execute_handles_exception(self, demo):
        """Test that exceptions are handled gracefully."""
        server = MagicMock()
        server.syncItems.side_effect = Exception("Sync API error")

        result = demo.execute(server, {})

        assert "error" in result
        assert "Sync API error" in result["error"]


class TestGetSyncStatusDemo:
    """Test suite for GetSyncStatusDemo."""

    @pytest.fixture
    def demo(self):
        """Create a GetSyncStatusDemo instance."""
        return GetSyncStatusDemo()

    def test_demo_metadata(self, demo):
        """Test that demo has correct metadata."""
        assert demo.name == "Get Sync Status"
        assert "status" in demo.description.lower()
        assert demo.category == "Sync & Offline"
        assert demo.operation_type == "READ"

    def test_get_parameters(self, demo):
        """Test parameter definition."""
        params = demo.get_parameters()
        assert len(params) == 0

    def test_get_code_example(self, demo):
        """Test code example generation."""
        code = demo.get_code_example()
        assert "sync" in code.lower()
        assert "server" in code

    def test_execute_without_server(self, demo):
        """Test execute without server returns error."""
        result = demo.execute(None, {})
        assert "error" in result
        assert "No server connection" in result["error"]

    def test_execute_success(self, demo):
        """Test successful sync status retrieval."""
        server = MagicMock()

        # Mock sync items with various statuses
        mock_complete = MagicMock()
        mock_complete.status = "complete"

        mock_processing = MagicMock()
        mock_processing.status = "processing"

        mock_pending = MagicMock()
        mock_pending.status = "pending"

        server.syncItems.return_value = [mock_complete, mock_processing, mock_pending]

        result = demo.execute(server, {})

        assert "status_summary" in result
        assert result["status_summary"]["total"] == 3
        assert result["status_summary"]["complete"] == 1
        assert result["status_summary"]["processing"] == 1
        assert result["status_summary"]["pending"] == 1

    def test_execute_handles_exception(self, demo):
        """Test that exceptions are handled gracefully."""
        server = MagicMock()
        server.syncItems.side_effect = Exception("API error")

        result = demo.execute(server, {})

        assert "error" in result
        assert "API error" in result["error"]
