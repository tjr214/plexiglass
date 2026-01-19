"""
List Server Activities Demo.

Demonstrates listing current server activities and background tasks.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class ListServerActivitiesDemo(BaseDemo):
    """
    Demonstration of server activities listing.

    This is a READ operation that shows current server background
    tasks and activities like library scans, downloads, etc.
    """

    name = "List Server Activities"
    description = "View current server activities and background tasks"
    category = "Advanced Features"
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
        Provide code example for activities listing.

        Args:
            params: Optional parameters (not used)

        Returns:
            Python code string demonstrating activities listing
        """
        return """# List server activities
from plexapi.server import PlexServer

# Initialize connection
server = PlexServer(baseurl, token)

# Get current activities
activities = server.activities()

print(f"Current server activities:")
for activity in activities:
    print(f"  {activity.title}")
    print(f"    Progress: {activity.progress}%")
    print(f"    Type: {activity.type}")
"""

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        """
        Execute activities listing.

        Args:
            server: PlexServer instance (or None)
            params: Parameters (not used)

        Returns:
            Dictionary containing activities or error
        """
        if server is None:
            return {"error": "No server connection available"}

        try:
            # Get server activities
            activities_list = []

            try:
                activities = server.activities()
                for activity in activities:
                    activities_list.append(
                        {
                            "title": getattr(activity, "title", "Unknown"),
                            "type": getattr(activity, "type", "unknown"),
                            "progress": getattr(activity, "progress", 0),
                        }
                    )
            except (AttributeError, Exception):
                # activities() may not be available on all server versions
                pass

            if activities_list:
                return {"activities": activities_list, "count": len(activities_list)}
            else:
                return {
                    "message": "No active server activities",
                    "info": "Server has no background tasks running currently",
                }

        except Exception as e:
            return {"error": f"Failed to list activities: {str(e)}"}
