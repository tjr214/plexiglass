"""
Tests for ListMoviesDemo.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from plexiglass.gallery.demos.media.list_movies import ListMoviesDemo


class TestListMoviesDemo:
    """Unit tests for ListMoviesDemo."""

    def test_demo_metadata(self):
        demo = ListMoviesDemo()

        assert demo.name == "List Movies"
        assert demo.category == "Media Operations"
        assert demo.operation_type == "READ"

    def test_demo_parameters(self):
        demo = ListMoviesDemo()
        params = demo.get_parameters()

        assert params
        assert params[0]["name"] == "section_name"

    def test_demo_execute_with_none_server(self):
        demo = ListMoviesDemo()

        result = demo.execute(server=None, params={})

        assert "error" in result

    def test_demo_execute_returns_movies(self):
        demo = ListMoviesDemo()

        item = MagicMock()
        item.title = "Movie"
        item.type = "movie"
        item.ratingKey = "123"

        section = MagicMock()
        section.all.return_value = [item]

        server = MagicMock()
        server.library.section.return_value = section

        result = demo.execute(server=server, params={"section_name": "Movies"})

        assert "movies" in result
        assert result["movies"][0]["title"] == "Movie"
