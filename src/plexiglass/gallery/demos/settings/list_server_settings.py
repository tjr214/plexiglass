"""
List Server Settings demo.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class ListServerSettingsDemo(BaseDemo):
    """List Plex server settings."""

    name = "List Server Settings"
    description = "List available server settings with current values"
    category = "Settings"
    operation_type = "READ"

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        return """# List server settings
settings = server.settings()
for setting in settings:
    print(setting.id, setting.value)
"""

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        if server is None:
            return {"error": "No server connection available"}

        settings = []
        for setting in list(server.settings()):
            settings.append(
                {
                    "id": getattr(setting, "id", None),
                    "value": getattr(setting, "value", None),
                    "summary": getattr(setting, "summary", None),
                }
            )

        return {"settings": settings}
