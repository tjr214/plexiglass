"""
List Server Sessions demo.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class ListServerSessionsDemo(BaseDemo):
    """List active sessions on the server."""

    name = "List Server Sessions"
    description = "List active sessions currently playing on the server"
    category = "Server & Connection"
    operation_type = "READ"

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        return """# List current sessions
sessions = server.sessions()
for session in sessions:
    print(session.title, session.usernames)
"""

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        if server is None:
            return {"error": "No server connection available"}

        sessions = []
        for session in list(server.sessions()):
            sessions.append(
                {
                    "title": getattr(session, "title", "Unknown"),
                    "user": (getattr(session, "usernames", None) or ["Unknown"])[0],
                    "state": getattr(session, "state", "unknown"),
                    "progress": self._calculate_progress(session),
                }
            )

        return {"sessions": sessions}

    @staticmethod
    def _calculate_progress(session: Any) -> int | None:
        view_offset = getattr(session, "viewOffset", None)
        duration = getattr(session, "duration", None)
        if view_offset is None or not duration:
            return None
        try:
            return int((float(view_offset) / float(duration)) * 100)
        except (TypeError, ValueError, ZeroDivisionError):
            return None
