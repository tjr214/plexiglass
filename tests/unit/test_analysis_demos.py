"""
Tests for Media Analysis Demos.
"""

from unittest.mock import MagicMock

import pytest

from plexiglass.gallery.demos.analysis.get_media_streams import GetMediaStreamsDemo
from plexiglass.gallery.demos.analysis.analyze_codec_info import AnalyzeCodecInfoDemo


class TestGetMediaStreamsDemo:
    """Test suite for GetMediaStreamsDemo."""

    @pytest.fixture
    def demo(self):
        """Create a GetMediaStreamsDemo instance."""
        return GetMediaStreamsDemo()

    def test_demo_metadata(self, demo):
        """Test that demo has correct metadata."""
        assert demo.name == "Get Media Streams"
        assert "stream" in demo.description.lower()
        assert demo.category == "Media Analysis"
        assert demo.operation_type == "READ"

    def test_get_parameters(self, demo):
        """Test parameter definition."""
        params = demo.get_parameters()
        assert len(params) == 1
        assert params[0]["name"] == "title"
        assert params[0]["type"] == "str"
        assert params[0]["required"] is True

    def test_get_code_example(self, demo):
        """Test code example generation."""
        code = demo.get_code_example()
        assert "stream" in code.lower()
        assert "media" in code.lower()

    def test_execute_without_server(self, demo):
        """Test execute without server returns error."""
        result = demo.execute(None, {})
        assert "error" in result
        assert "No server connection" in result["error"]

    def test_execute_without_title(self, demo):
        """Test execute without title parameter."""
        server = MagicMock()
        result = demo.execute(server, {})
        assert "error" in result
        assert "title" in result["error"].lower()

    def test_execute_success(self, demo):
        """Test successful media stream retrieval."""
        server = MagicMock()

        # Mock media item with streams
        mock_item = MagicMock()
        mock_item.title = "Test Movie"

        # Mock video stream
        mock_video_stream = MagicMock()
        mock_video_stream.streamType = 1  # video
        mock_video_stream.codec = "h264"
        mock_video_stream.bitrate = 5000

        # Mock audio stream
        mock_audio_stream = MagicMock()
        mock_audio_stream.streamType = 2  # audio
        mock_audio_stream.codec = "aac"
        mock_audio_stream.bitrate = 192

        mock_item.media = [
            MagicMock(parts=[MagicMock(streams=[mock_video_stream, mock_audio_stream])])
        ]

        server.search.return_value = [mock_item]

        result = demo.execute(server, {"title": "Test Movie"})

        assert "streams" in result or "message" in result

    def test_execute_handles_exception(self, demo):
        """Test that exceptions are handled gracefully."""
        server = MagicMock()
        server.search.side_effect = Exception("Search error")

        result = demo.execute(server, {"title": "test"})

        assert "error" in result


class TestAnalyzeCodecInfoDemo:
    """Test suite for AnalyzeCodecInfoDemo."""

    @pytest.fixture
    def demo(self):
        """Create an AnalyzeCodecInfoDemo instance."""
        return AnalyzeCodecInfoDemo()

    def test_demo_metadata(self, demo):
        """Test that demo has correct metadata."""
        assert demo.name == "Analyze Codec Info"
        assert "codec" in demo.description.lower()
        assert demo.category == "Media Analysis"
        assert demo.operation_type == "READ"

    def test_get_parameters(self, demo):
        """Test parameter definition."""
        params = demo.get_parameters()
        assert len(params) == 1
        assert params[0]["name"] == "title"

    def test_get_code_example(self, demo):
        """Test code example generation."""
        code = demo.get_code_example()
        assert "codec" in code.lower()

    def test_execute_without_server(self, demo):
        """Test execute without server returns error."""
        result = demo.execute(None, {})
        assert "error" in result
        assert "No server connection" in result["error"]

    def test_execute_success(self, demo):
        """Test successful codec analysis."""
        server = MagicMock()

        # Mock media item
        mock_item = MagicMock()
        mock_item.title = "Test Movie"

        server.search.return_value = [mock_item]

        result = demo.execute(server, {"title": "Test Movie"})

        assert "message" in result or "codecs" in result or "info" in result

    def test_execute_handles_exception(self, demo):
        """Test that exceptions are handled gracefully."""
        server = MagicMock()
        server.search.side_effect = Exception("Error")

        result = demo.execute(server, {"title": "test"})

        assert "error" in result
