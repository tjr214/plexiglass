"""
List Recent Plays demo.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class ListRecentPlaysDemo(BaseDemo):
    """List recently played items."""

    name = "List Recent Plays"
    description = "List recently played items on the server"
    category = "Playback & Clients"
    operation_type = "READ"

    def get_parameters(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "limit",
                "type": "int",
                "required": False,
                "default": 10,
                "description": "Limit number of recent plays",
            }
        ]

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        limit = 10
        if params and params.get("limit"):
            limit = int(params["limit"])
        return (
            """# List recent plays
entries = server.history(maxresults="""
            f"{limit}" + ")\n"
            "for entry in entries:\n"
            "    print(entry.title, entry.viewedAt)\n"
        )

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        if server is None:
            return {"error": "No server connection available"}

        limit = params.get("limit", 10)
        try:
            limit_value = int(limit)
        except (TypeError, ValueError):
            limit_value = 10

        plays = []
        for entry in list(server.history(maxresults=limit_value)):
            viewed_at = getattr(entry, "viewedAt", None)
            timestamp = None
            if viewed_at:
                try:
                    timestamp = datetime.fromtimestamp(viewed_at).isoformat()
                except (TypeError, ValueError, OSError):
                    timestamp = None
            plays.append(
                {
                    "title": getattr(entry, "title", "Unknown"),
                    "type": getattr(entry, "type", None),
                    "viewed_at": timestamp,
                }
            )

        return {"recent_plays": plays}
