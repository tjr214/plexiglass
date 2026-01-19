"""
List Playback Sessions demo.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class ListPlaybackSessionsDemo(BaseDemo):
    """List active playback sessions with client context."""

    name = "List Playback Sessions"
    description = "List active playback sessions with client info"
    category = "Playback & Clients"
    operation_type = "READ"

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        return """# List playback sessions
sessions = server.sessions()
for session in sessions:
    player = session.players[0] if session.players else None
    print(session.title, player.title if player else "Unknown")
"""

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        if server is None:
            return {"error": "No server connection available"}

        sessions = []
        for session in list(server.sessions()):
            player = None
            players = getattr(session, "players", None)
            if players:
                player = players[0]
            sessions.append(
                {
                    "title": getattr(session, "title", "Unknown"),
                    "player": getattr(player, "title", None) if player else None,
                    "state": getattr(session, "state", "unknown"),
                }
            )

        return {"sessions": sessions}
