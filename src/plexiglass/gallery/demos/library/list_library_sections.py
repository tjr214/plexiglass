"""
List Library Sections demo.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class ListLibrarySectionsDemo(BaseDemo):
    """List library sections for the server."""

    name = "List Library Sections"
    description = "List available library sections on the server"
    category = "Library Management"
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

        sections = []
        for section in list(server.library.sections()):
            sections.append(
                {
                    "title": getattr(section, "title", "Unknown"),
                    "type": getattr(section, "type", None),
                    "uuid": getattr(section, "uuid", None),
                    "total_items": getattr(section, "totalSize", 0),
                }
            )

        return {"sections": sections}
