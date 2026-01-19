"""
List Movies demo.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class ListMoviesDemo(BaseDemo):
    """List movie items in a library section."""

    name = "List Movies"
    description = "List movies in a specific library section"
    category = "Media Operations"
    operation_type = "READ"

    def get_parameters(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "section_name",
                "type": "str",
                "required": True,
                "description": "Movie library section name (e.g. Movies)",
            }
        ]

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        section_name = "Movies"
        if params and params.get("section_name"):
            section_name = str(params["section_name"])
        return (
            """# List movies
section = server.library.section("""
            f'"{section_name}"' + ")\n"
            "movies = section.all()\n"
            "for movie in movies:\n"
            "    print(movie.title, movie.year)\n"
        )

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        if server is None:
            return {"error": "No server connection available"}

        section_name = params.get("section_name")
        if not section_name:
            return {"error": "Missing required parameter: section_name"}

        section = server.library.section(section_name)
        movies = []
        for item in list(section.all()):
            movies.append(
                {
                    "title": getattr(item, "title", "Unknown"),
                    "year": getattr(item, "year", None),
                    "ratingKey": getattr(item, "ratingKey", None),
                }
            )

        return {"movies": movies}
