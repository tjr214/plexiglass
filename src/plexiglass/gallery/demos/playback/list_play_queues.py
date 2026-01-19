"""
List Play Queues demo.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class ListPlayQueuesDemo(BaseDemo):
    """List active play queues."""

    name = "List Play Queues"
    description = "List recent play queues on the server"
    category = "Playback & Clients"
    operation_type = "READ"

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        return """# List play queues
queues = server.playQueues()
for queue in queues:
    print(queue.playQueueID, queue.playQueueTotalCount)
"""

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        if server is None:
            return {"error": "No server connection available"}

        queues = []
        queues_method = getattr(server, "playQueues", None)
        if queues_method is None:
            return {"error": "Server does not support play queues"}

        for queue in list(queues_method()):
            queues.append(
                {
                    "queue_id": getattr(queue, "playQueueID", None),
                    "total_count": getattr(queue, "playQueueTotalCount", None),
                    "media_type": getattr(queue, "mediaType", None),
                }
            )

        return {"queues": queues}
