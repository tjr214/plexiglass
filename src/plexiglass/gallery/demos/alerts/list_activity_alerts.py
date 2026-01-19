"""
List Activity Alerts Demo.

Demonstrates monitoring activity and alerts on the Plex server.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class ListActivityAlertsDemo(BaseDemo):
    """
    Demonstration of monitoring server activity and alerts.

    This is a READ operation that provides information about
    activity monitoring on the Plex server.
    """

    name = "List Activity Alerts"
    description = "Monitor server activity and alert information"
    category = "Alerts & Monitoring"
    operation_type = "READ"

    def get_parameters(self) -> list[dict[str, Any]]:
        """
        Get parameter definitions for this demo.

        Returns:
            Empty list (no parameters needed)
        """
        return []

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        """
        Provide code example for monitoring activity.

        Args:
            params: Optional parameters (not used)

        Returns:
            Python code string demonstrating activity monitoring
        """
        return """# Monitor server activity
from plexapi.server import PlexServer

# Initialize connection
server = PlexServer(baseurl, token)

# Note: Activity monitoring requires WebSocket connections
# which are handled by the Alert listener in plexapi

# Get current sessions (active streams)
sessions = server.sessions()
print(f"Active sessions: {len(sessions)}")

for session in sessions:
    user = session.usernames[0] if session.usernames else "Unknown"
    print(f"  {user} watching {session.title}")
"""

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        """
        Execute activity monitoring on the server.

        Args:
            server: PlexServer instance (or None)
            params: Parameters (not used)

        Returns:
            Dictionary containing activity information or error
        """
        if server is None:
            return {"error": "No server connection available"}

        try:
            # Get current sessions as a proxy for activity
            sessions = server.sessions()

            # Format activity info
            activities = []
            for session in sessions:
                user = (
                    session.usernames[0]
                    if hasattr(session, "usernames") and session.usernames
                    else "Unknown"
                )
                title = getattr(session, "title", "Unknown")
                activities.append(
                    {
                        "user": user,
                        "title": title,
                        "type": getattr(session, "type", "unknown"),
                    }
                )

            return {
                "info": "Activity monitoring via sessions (WebSocket alerts require listener setup)",
                "active_count": len(sessions),
                "alerts": activities,
            }

        except Exception as e:
            return {"error": f"Failed to get activity: {str(e)}"}
