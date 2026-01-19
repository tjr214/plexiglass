"""
List Users demo.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class ListUsersDemo(BaseDemo):
    """List users on the Plex account."""

    name = "List Users"
    description = "List users associated with the Plex account"
    category = "Users & Sharing"
    operation_type = "READ"

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        return """# List users
account = server.myPlexAccount()
for user in account.users():
    print(user.title, user.email)
"""

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        if server is None:
            return {"error": "No server connection available"}

        account = server.myPlexAccount()
        users = []
        for user in list(account.users()):
            users.append(
                {
                    "title": getattr(user, "title", "Unknown"),
                    "email": getattr(user, "email", None),
                    "id": getattr(user, "id", None),
                }
            )

        return {"users": users}
