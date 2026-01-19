"""
Tests for ListLibrarySectionsDemo.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from plexiglass.gallery.demos.library.list_library_sections import ListLibrarySectionsDemo


class TestListLibrarySectionsDemo:
    """Unit tests for ListLibrarySectionsDemo."""

    def test_demo_metadata(self):
        demo = ListLibrarySectionsDemo()

        assert demo.name == "List Library Sections"
        assert demo.category == "Library Management"
        assert demo.operation_type == "READ"

    def test_demo_code_example(self):
        demo = ListLibrarySectionsDemo()
        code = demo.get_code_example()

        assert "sections" in code

    def test_demo_execute_with_none_server(self):
        demo = ListLibrarySectionsDemo()

        result = demo.execute(server=None, params={})

        assert "error" in result

    def test_demo_execute_returns_sections(self):
        demo = ListLibrarySectionsDemo()

        section = MagicMock()
        section.title = "Movies"
        section.type = "movie"
        section.uuid = "uuid-123"
        section.totalSize = 100

        server = MagicMock()
        server.library.sections.return_value = [section]

        result = demo.execute(server=server, params={})

        assert "sections" in result
        assert result["sections"][0]["title"] == "Movies"
        assert result["sections"][0]["total_items"] == 100
