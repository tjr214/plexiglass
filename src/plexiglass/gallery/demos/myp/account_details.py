"""
MyPlex Account Details demo.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class MyPlexAccountDetailsDemo(BaseDemo):
    """Show MyPlex account details."""

    name = "MyPlex Account Details"
    description = "Show account identity details"
    category = "MyPlex Account"
    operation_type = "READ"

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        return """# Get MyPlex account details
account = server.myPlexAccount()
print(account.title, account.username, account.email)
"""

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        if server is None:
            return {"error": "No server connection available"}

        account = server.myPlexAccount()
        return {
            "account": {
                "title": getattr(account, "title", "Unknown"),
                "username": getattr(account, "username", None),
                "email": getattr(account, "email", None),
                "id": getattr(account, "id", None),
            }
        }
