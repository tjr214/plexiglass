"""
Tests for ListPlayQueuesDemo.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from plexiglass.gallery.demos.playback.list_play_queues import ListPlayQueuesDemo


class TestListPlayQueuesDemo:
    """Unit tests for ListPlayQueuesDemo."""

    def test_demo_metadata(self):
        demo = ListPlayQueuesDemo()

        assert demo.name == "List Play Queues"
        assert demo.category == "Playback & Clients"
        assert demo.operation_type == "READ"

    def test_demo_execute_with_none_server(self):
        demo = ListPlayQueuesDemo()

        result = demo.execute(server=None, params={})

        assert "error" in result

    def test_demo_execute_returns_queues(self):
        demo = ListPlayQueuesDemo()

        queue = MagicMock()
        queue.playQueueID = 101
        queue.playQueueTotalCount = 12
        queue.mediaType = "video"

        server = MagicMock()
        server.playQueues.return_value = [queue]

        result = demo.execute(server=server, params={})

        assert "queues" in result
        assert result["queues"][0]["queue_id"] == 101
        assert result["queues"][0]["total_count"] == 12
