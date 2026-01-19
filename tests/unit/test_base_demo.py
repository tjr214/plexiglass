"""
Tests for the BaseDemo class.

The BaseDemo class provides the foundation for all gallery demos,
handling common functionality like metadata, code examples, and execution.
"""

from __future__ import annotations

import pytest

from plexiglass.gallery.base_demo import BaseDemo


class TestBaseDemo:
    """Test suite for BaseDemo class."""

    def test_demo_has_required_metadata(self) -> None:
        """Demo should have name, description, and category metadata."""

        class SampleDemo(BaseDemo):
            name = "Sample Demo"
            description = "A sample demonstration"
            category = "Server & Connection"
            operation_type = "READ"

            def execute(self, server, params):
                return {"result": "success"}

        demo = SampleDemo()
        assert demo.name == "Sample Demo"
        assert demo.description == "A sample demonstration"
        assert demo.category == "Server & Connection"
        assert demo.operation_type == "READ"

    def test_demo_has_code_example(self) -> None:
        """Demo should provide a code example string."""

        class SampleDemo(BaseDemo):
            name = "Get Server Info"
            description = "Get server information"
            category = "Server & Connection"
            operation_type = "READ"

            def get_code_example(self, params=None):
                return "server = PlexServer(url, token)\nprint(server.version)"

            def execute(self, server, params):
                return {"version": "1.0.0"}

        demo = SampleDemo()
        code = demo.get_code_example()
        assert "PlexServer" in code
        assert "server.version" in code

    def test_demo_execute_returns_result(self) -> None:
        """Demo execute method should return a result dictionary."""

        class SampleDemo(BaseDemo):
            name = "List Libraries"
            description = "List all library sections"
            category = "Library Management"
            operation_type = "READ"

            def execute(self, server, params):
                return {"libraries": ["Movies", "TV Shows", "Music"]}

        demo = SampleDemo()
        result = demo.execute(server=None, params={})
        assert "libraries" in result
        assert len(result["libraries"]) == 3

    def test_demo_has_parameters(self) -> None:
        """Demo should define supported parameters."""

        class SampleDemo(BaseDemo):
            name = "Search Library"
            description = "Search for media in library"
            category = "Library Management"
            operation_type = "READ"

            def get_parameters(self):
                return [
                    {"name": "query", "type": "str", "required": True},
                    {"name": "library", "type": "str", "required": False},
                ]

            def execute(self, server, params):
                return {"results": []}

        demo = SampleDemo()
        params = demo.get_parameters()
        assert len(params) == 2
        assert params[0]["name"] == "query"
        assert params[0]["required"] is True

    def test_demo_supports_write_operation_type(self) -> None:
        """Demo should support WRITE operation type."""

        class SampleDemo(BaseDemo):
            name = "Update Metadata"
            description = "Update media metadata"
            category = "Media Operations"
            operation_type = "WRITE"

            def execute(self, server, params):
                return {"updated": True}

        demo = SampleDemo()
        assert demo.operation_type == "WRITE"

    def test_demo_cannot_be_instantiated_without_required_fields(self) -> None:
        """Demo must have required fields: name, description, category, operation_type."""

        class IncompleteDemo(BaseDemo):
            def execute(self, server, params):
                return {}

        demo = IncompleteDemo()
        # Should raise AttributeError when accessing required fields
        with pytest.raises(AttributeError):
            _ = demo.name

    def test_demo_get_metadata(self) -> None:
        """Demo should provide consolidated metadata."""

        class SampleDemo(BaseDemo):
            name = "Sample Demo"
            description = "A sample demonstration"
            category = "Server & Connection"
            operation_type = "READ"

            def execute(self, server, params):
                return {}

        demo = SampleDemo()
        metadata = demo.get_metadata()
        assert metadata["name"] == "Sample Demo"
        assert metadata["description"] == "A sample demonstration"
        assert metadata["category"] == "Server & Connection"
        assert metadata["operation_type"] == "READ"

    def test_demo_validate_params_checks_required_fields(self) -> None:
        """Demo should validate that required parameters are provided."""

        class SampleDemo(BaseDemo):
            name = "Search"
            description = "Search media"
            category = "Library Management"
            operation_type = "READ"

            def get_parameters(self):
                return [{"name": "query", "type": "str", "required": True}]

            def execute(self, server, params):
                return {}

        demo = SampleDemo()
        # Missing required parameter
        is_valid, error = demo.validate_params({})
        assert is_valid is False
        assert "query" in error

        # With required parameter
        is_valid, error = demo.validate_params({"query": "test"})
        assert is_valid is True
        assert error is None
