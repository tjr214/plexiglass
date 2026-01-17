"""
Test suite for sample module.

This demonstrates the TDD Red-Green-Refactor cycle:
1. RED: Write a failing test
2. GREEN: Write minimal code to pass
3. REFACTOR: Improve the code
"""

import pytest
from plex_test.sample import hello_plex


class TestHelloPlex:
    """Test cases for hello_plex function."""

    def test_hello_plex_default(self):
        """Test hello_plex with default argument."""
        # Arrange & Act
        result = hello_plex()

        # Assert
        assert result == "Hello, Plex!"

    def test_hello_plex_custom_name(self):
        """Test hello_plex with custom name."""
        # Arrange
        custom_name = "World"

        # Act
        result = hello_plex(custom_name)

        # Assert
        assert result == "Hello, World!"

    def test_hello_plex_empty_string(self):
        """Test hello_plex with empty string."""
        # Arrange & Act
        result = hello_plex("")

        # Assert
        assert result == "Hello, !"

    @pytest.mark.parametrize(
        "name,expected",
        [
            ("Plex", "Hello, Plex!"),
            ("Tim", "Hello, Tim!"),
            ("Media Server", "Hello, Media Server!"),
        ],
    )
    def test_hello_plex_parametrized(self, name, expected):
        """Test hello_plex with multiple inputs using parametrize."""
        # Act
        result = hello_plex(name)

        # Assert
        assert result == expected


class TestTDDDemonstration:
    """
    Demonstration of TDD workflow.

    Example TDD cycle for a new feature:

    🔴 RED (Write failing test first):
    def test_connect_to_plex_server(self):
        client = PlexClient("http://localhost:32400", "token")
        assert client.is_connected() is True

    🟢 GREEN (Write minimal code to pass):
    class PlexClient:
        def __init__(self, url, token):
            self.url = url
            self.token = token

        def is_connected(self):
            return True  # Minimal implementation

    🔵 REFACTOR (Improve while keeping tests green):
    class PlexClient:
        def __init__(self, url, token):
            self.url = url
            self.token = token
            self._server = None

        def is_connected(self):
            try:
                from plexapi.server import PlexServer
                self._server = PlexServer(self.url, self.token)
                return True
            except Exception:
                return False
    """

    def test_sample_passes(self):
        """This test always passes - demonstrating green state."""
        assert True

    @pytest.mark.skip(reason="Example of RED state - test not yet implemented")
    def test_feature_not_yet_implemented(self):
        """
        This would be a RED test - failing until feature is implemented.

        When you're ready to implement a new feature:
        1. Remove the @pytest.mark.skip decorator
        2. Run the test - it should FAIL (RED)
        3. Implement the minimal code to make it pass (GREEN)
        4. Refactor as needed (REFACTOR)
        """
        # This test is skipped - remove skip marker to enter RED state
        pass
