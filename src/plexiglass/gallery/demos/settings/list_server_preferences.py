"""
List Server Preferences demo.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class ListServerPreferencesDemo(BaseDemo):
    """List server preferences."""

    name = "List Server Preferences"
    description = "List server preference values"
    category = "Settings"
    operation_type = "READ"

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        return """# List server preferences
prefs = server.preferences()
for pref in prefs:
    print(pref.id, pref.value)
"""

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        if server is None:
            return {"error": "No server connection available"}

        prefs = []
        preferences_method = getattr(server, "preferences", None)
        if preferences_method is None:
            return {"error": "Server does not support preferences"}

        for pref in list(preferences_method()):
            prefs.append(
                {
                    "id": getattr(pref, "id", None),
                    "value": getattr(pref, "value", None),
                    "summary": getattr(pref, "summary", None),
                }
            )

        return {"preferences": prefs}
