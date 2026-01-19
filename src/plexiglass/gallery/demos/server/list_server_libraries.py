"""
List Server Libraries demo.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class ListServerLibrariesDemo(BaseDemo):
    """List library sections available on the server."""

    name = "List Server Libraries"
    description = "List all library sections available on the server"
    category = "Server & Connection"
    operation_type = "READ"

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        return """# List library sections
sections = server.library.sections()
for section in sections:
    print(section.title, section.type)
"""

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        if server is None:
            return {"error": "No server connection available"}

        libraries = []
        for section in list(server.library.sections()):
            libraries.append(
                {
                    "title": getattr(section, "title", "Unknown"),
                    "type": getattr(section, "type", None),
                    "uuid": getattr(section, "uuid", None),
                }
            )

        return {"libraries": libraries}
