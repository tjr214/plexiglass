"""
Tests for Utilities Demos.
"""

from unittest.mock import MagicMock

import pytest

from plexiglass.gallery.demos.utilities.get_download_url import GetDownloadURLDemo
from plexiglass.gallery.demos.utilities.get_thumbnail_url import GetThumbnailURLDemo


class TestGetDownloadURLDemo:
    """Test suite for GetDownloadURLDemo."""

    @pytest.fixture
    def demo(self):
        """Create a GetDownloadURLDemo instance."""
        return GetDownloadURLDemo()

    def test_demo_metadata(self, demo):
        """Test that demo has correct metadata."""
        assert demo.name == "Get Download URL"
        assert "download" in demo.description.lower() or "url" in demo.description.lower()
        assert demo.category == "Utilities"
        assert demo.operation_type == "READ"

    def test_get_parameters(self, demo):
        """Test parameter definition."""
        params = demo.get_parameters()
        assert len(params) == 1
        assert params[0]["name"] == "title"

    def test_get_code_example(self, demo):
        """Test code example generation."""
        code = demo.get_code_example()
        assert "download" in code.lower() or "url" in code.lower()

    def test_execute_without_server(self, demo):
        """Test execute without server returns error."""
        result = demo.execute(None, {})
        assert "error" in result
        assert "No server connection" in result["error"]

    def test_execute_success(self, demo):
        """Test successful download URL retrieval."""
        server = MagicMock()

        # Mock media item
        mock_item = MagicMock()
        mock_item.title = "Test Movie"
        mock_item.getDownloadURL.return_value = "http://server/download/123"

        server.search.return_value = [mock_item]

        result = demo.execute(server, {"title": "Test Movie"})

        assert "url" in result or "message" in result

    def test_execute_handles_exception(self, demo):
        """Test that exceptions are handled gracefully."""
        server = MagicMock()
        server.search.side_effect = Exception("Error")

        result = demo.execute(server, {"title": "test"})

        assert "error" in result


class TestGetThumbnailURLDemo:
    """Test suite for GetThumbnailURLDemo."""

    @pytest.fixture
    def demo(self):
        """Create a GetThumbnailURLDemo instance."""
        return GetThumbnailURLDemo()

    def test_demo_metadata(self, demo):
        """Test that demo has correct metadata."""
        assert demo.name == "Get Thumbnail URL"
        assert "thumbnail" in demo.description.lower() or "url" in demo.description.lower()
        assert demo.category == "Utilities"
        assert demo.operation_type == "READ"

    def test_get_parameters(self, demo):
        """Test parameter definition."""
        params = demo.get_parameters()
        assert len(params) == 1
        assert params[0]["name"] == "title"

    def test_get_code_example(self, demo):
        """Test code example generation."""
        code = demo.get_code_example()
        assert "thumb" in code.lower() or "art" in code.lower()

    def test_execute_without_server(self, demo):
        """Test execute without server returns error."""
        result = demo.execute(None, {})
        assert "error" in result
        assert "No server connection" in result["error"]

    def test_execute_success(self, demo):
        """Test successful thumbnail URL retrieval."""
        server = MagicMock()
        server.url.return_value = "http://server:32400"

        # Mock media item
        mock_item = MagicMock()
        mock_item.title = "Test Movie"
        mock_item.thumb = "/library/metadata/123/thumb/456"
        mock_item.art = "/library/metadata/123/art/789"

        server.search.return_value = [mock_item]

        result = demo.execute(server, {"title": "Test Movie"})

        assert "thumb" in result or "art" in result or "message" in result

    def test_execute_handles_exception(self, demo):
        """Test that exceptions are handled gracefully."""
        server = MagicMock()
        server.search.side_effect = Exception("Error")

        result = demo.execute(server, {"title": "test"})

        assert "error" in result
