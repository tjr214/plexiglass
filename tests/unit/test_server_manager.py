"""
Tests for Server Manager Service (TDD Red Phase)

This module tests the server management system including:
- Multi-server connection pool
- Server health checking
- Connection management
- Server switching
- Error handling
"""

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from plexapi.exceptions import Unauthorized
from plexapi.server import PlexServer


class TestServerManager:
    """Test suite for the ServerManager class."""

    def test_initialization_with_config_loader(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should initialize with a ConfigLoader instance.

        Expected behavior:
        - Accept ConfigLoader in constructor
        - Load server configurations
        - No connections established yet (lazy loading)
        """
        # Arrange
        from plexiglass.config.loader import ConfigLoader
        from plexiglass.services.server_manager import ServerManager

        loader = ConfigLoader(sample_config_path)
        loader.load()

        # Act
        manager = ServerManager(loader)

        # Assert
        assert manager is not None
        assert manager.get_server_count() > 0

    def test_connect_to_default_server(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should connect to the default server.

        Expected behavior:
        - Find default server from config
        - Establish connection to PlexServer
        - Store connection in pool
        - Return PlexServer instance
        """
        # Arrange
        from plexiglass.config.loader import ConfigLoader
        from plexiglass.services.server_manager import ServerManager

        loader = ConfigLoader(sample_config_path)
        loader.load()
        manager = ServerManager(loader)

        # Act
        with patch("plexiglass.services.server_manager.PlexServer") as mock_plex:
            mock_server = MagicMock()
            mock_server.friendlyName = "Home Server"
            mock_plex.return_value = mock_server

            server = manager.connect_to_default()

        # Assert
        assert server is not None
        assert server.friendlyName == "Home Server"
        mock_plex.assert_called_once()

    def test_connect_to_server_by_name(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should connect to a specific server by name.

        Expected behavior:
        - Find server config by name
        - Establish connection
        - Store in connection pool
        - Return PlexServer instance
        """
        # Arrange
        from plexiglass.config.loader import ConfigLoader
        from plexiglass.services.server_manager import ServerManager

        loader = ConfigLoader(sample_config_path)
        loader.load()
        manager = ServerManager(loader)

        # Act
        with patch("plexiglass.services.server_manager.PlexServer") as mock_plex:
            mock_server = MagicMock()
            mock_server.friendlyName = "Test Server"
            mock_plex.return_value = mock_server

            server = manager.connect_to_server("Test Server")

        # Assert
        assert server is not None
        assert server.friendlyName == "Test Server"

    def test_connect_to_nonexistent_server_raises_error(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should raise error when connecting to nonexistent server.

        Expected behavior:
        - Attempt to find server by name
        - Raise ServerNotFoundError if not in config
        """
        # Arrange
        from plexiglass.config.loader import ConfigLoader
        from plexiglass.services.server_manager import ServerManager
        from plexiglass.services.exceptions import ServerNotFoundError

        loader = ConfigLoader(sample_config_path)
        loader.load()
        manager = ServerManager(loader)

        # Act & Assert
        with pytest.raises(ServerNotFoundError, match="Nonexistent Server"):
            manager.connect_to_server("Nonexistent Server")

    def test_connection_caching(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should cache server connections (not reconnect each time).

        Expected behavior:
        - First call establishes connection
        - Subsequent calls return cached connection
        - PlexServer constructor called only once per server
        """
        # Arrange
        from plexiglass.config.loader import ConfigLoader
        from plexiglass.services.server_manager import ServerManager

        loader = ConfigLoader(sample_config_path)
        loader.load()
        manager = ServerManager(loader)

        # Act
        with patch("plexiglass.services.server_manager.PlexServer") as mock_plex:
            mock_server = MagicMock()
            mock_plex.return_value = mock_server

            server1 = manager.connect_to_default()
            server2 = manager.connect_to_default()

        # Assert
        assert server1 is server2  # Same instance
        mock_plex.assert_called_once()  # Only one call to PlexServer

    def test_unauthorized_connection_raises_error(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should handle unauthorized (bad token) gracefully.

        Expected behavior:
        - Attempt connection with invalid token
        - Catch Unauthorized exception from plexapi
        - Raise ConnectionError with helpful message
        """
        # Arrange
        from plexiglass.config.loader import ConfigLoader
        from plexiglass.services.server_manager import ServerManager
        from plexiglass.services.exceptions import ConnectionError as ConnError

        loader = ConfigLoader(sample_config_path)
        loader.load()
        manager = ServerManager(loader)

        # Act & Assert
        with patch("plexiglass.services.server_manager.PlexServer") as mock_plex:
            mock_plex.side_effect = Unauthorized("Invalid token")

            with pytest.raises(ConnError, match="Unauthorized"):
                manager.connect_to_default()

    def test_connection_timeout_raises_error(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should handle connection timeout gracefully.

        Expected behavior:
        - Attempt connection to unreachable server
        - Catch connection timeout
        - Raise ConnectionError with helpful message
        """
        # Arrange
        from plexiglass.config.loader import ConfigLoader
        from plexiglass.services.server_manager import ServerManager
        from plexiglass.services.exceptions import ConnectionError as ConnError

        loader = ConfigLoader(sample_config_path)
        loader.load()
        manager = ServerManager(loader)

        # Act & Assert
        with patch("plexiglass.services.server_manager.PlexServer") as mock_plex:
            mock_plex.side_effect = TimeoutError("Connection timeout")

            with pytest.raises(ConnError, match="timeout"):
                manager.connect_to_default()

    def test_get_connected_servers(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should return list of currently connected servers.

        Expected behavior:
        - Track which servers are connected
        - Return list of server names
        """
        # Arrange
        from plexiglass.config.loader import ConfigLoader
        from plexiglass.services.server_manager import ServerManager

        loader = ConfigLoader(sample_config_path)
        loader.load()
        manager = ServerManager(loader)

        # Act
        with patch("plexiglass.services.server_manager.PlexServer") as mock_plex:
            mock_server = MagicMock()
            mock_plex.return_value = mock_server

            manager.connect_to_server("Home Server")
            manager.connect_to_server("Test Server")

            connected = manager.get_connected_servers()

        # Assert
        assert "Home Server" in connected
        assert "Test Server" in connected
        assert len(connected) == 2

    def test_disconnect_server(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should disconnect from a specific server.

        Expected behavior:
        - Remove server from connection pool
        - Clean up resources
        - Server no longer in connected list
        """
        # Arrange
        from plexiglass.config.loader import ConfigLoader
        from plexiglass.services.server_manager import ServerManager

        loader = ConfigLoader(sample_config_path)
        loader.load()
        manager = ServerManager(loader)

        # Act
        with patch("plexiglass.services.server_manager.PlexServer") as mock_plex:
            mock_server = MagicMock()
            mock_plex.return_value = mock_server

            manager.connect_to_default()
            assert len(manager.get_connected_servers()) == 1

            manager.disconnect_server("Home Server")

        # Assert
        assert len(manager.get_connected_servers()) == 0

    def test_disconnect_all_servers(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should disconnect from all servers.

        Expected behavior:
        - Close all active connections
        - Clear connection pool
        - No servers in connected list
        """
        # Arrange
        from plexiglass.config.loader import ConfigLoader
        from plexiglass.services.server_manager import ServerManager

        loader = ConfigLoader(sample_config_path)
        loader.load()
        manager = ServerManager(loader)

        # Act
        with patch("plexiglass.services.server_manager.PlexServer") as mock_plex:
            mock_server = MagicMock()
            mock_plex.return_value = mock_server

            manager.connect_to_server("Home Server")
            manager.connect_to_server("Test Server")
            assert len(manager.get_connected_servers()) == 2

            manager.disconnect_all()

        # Assert
        assert len(manager.get_connected_servers()) == 0

    def test_get_server_status(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should get server status/health information.

        Expected behavior:
        - Query server for status
        - Return dict with: connected, version, platform, etc.
        """
        # Arrange
        from plexiglass.config.loader import ConfigLoader
        from plexiglass.services.server_manager import ServerManager

        loader = ConfigLoader(sample_config_path)
        loader.load()
        manager = ServerManager(loader)

        # Act
        with patch("plexiglass.services.server_manager.PlexServer") as mock_plex:
            mock_server = MagicMock()
            mock_server.version = "1.40.0.7775"
            mock_server.platform = "Linux"
            mock_server.sessions.return_value = []
            mock_server.library.sections.return_value = []
            mock_plex.return_value = mock_server

            manager.connect_to_default()
            status = manager.get_server_status("Home Server")

        # Assert
        assert status is not None
        assert status["connected"] is True
        assert "version" in status
        assert "platform" in status
        assert status["session_count"] == 0
        assert status["library_count"] == 0
        assert status["library_items"] == 0

    def test_get_server_status_includes_now_playing(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should include now-playing sessions with progress.

        Expected behavior:
        - Include session_count
        - Include now_playing entries with title, user, state, progress
        """
        # Arrange
        from plexiglass.config.loader import ConfigLoader
        from plexiglass.services.server_manager import ServerManager

        loader = ConfigLoader(sample_config_path)
        loader.load()
        manager = ServerManager(loader)

        session = MagicMock()
        session.title = "The Matrix"
        session.usernames = ["neo"]
        session.user = None
        session.players = []
        session.state = "playing"
        session.viewOffset = 30_000
        session.duration = 120_000

        # Act
        with patch("plexiglass.services.server_manager.PlexServer") as mock_plex:
            mock_server = MagicMock()
            mock_server.version = "1.40.0.7775"
            mock_server.platform = "Linux"
            mock_server.sessions.return_value = [session]
            mock_server.library.sections.return_value = [MagicMock(totalSize=12)]
            mock_plex.return_value = mock_server

            manager.connect_to_default()
            status = manager.get_server_status("Home Server")

        # Assert
        assert status["session_count"] == 1
        assert status["now_playing"][0]["title"] == "The Matrix"
        assert status["now_playing"][0]["user"] == "neo"
        assert status["now_playing"][0]["state"] == "playing"
        assert status["now_playing"][0]["progress_percent"] == 25
        assert status["library_count"] == 1
        assert status["library_items"] == 12

    def test_get_all_server_names(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should return all server names from config.

        Expected behavior:
        - Return list of all configured servers (not just connected)
        """
        # Arrange
        from plexiglass.config.loader import ConfigLoader
        from plexiglass.services.server_manager import ServerManager

        loader = ConfigLoader(sample_config_path)
        loader.load()
        manager = ServerManager(loader)

        # Act
        names = manager.get_all_server_names()

        # Assert
        assert "Home Server" in names
        assert "Test Server" in names

    def test_is_server_read_only(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should check if server is marked as read-only.

        Expected behavior:
        - Check read_only flag from config
        - Return True if read_only, False otherwise
        """
        # Arrange
        from plexiglass.config.loader import ConfigLoader
        from plexiglass.services.server_manager import ServerManager

        loader = ConfigLoader(sample_config_path)
        loader.load()
        manager = ServerManager(loader)

        # Act - "Home Server" has read_only: false
        is_readonly = manager.is_server_read_only("Home Server")

        # Assert
        assert is_readonly is False


# Fixtures


@pytest.fixture
def sample_config_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Create a sample configuration file for testing."""
    monkeypatch.setenv("PLEX_TOKEN_HOME", "home-token-12345")
    monkeypatch.setenv("PLEX_TOKEN_TEST", "test-token-67890")

    config_content = """
servers:
  - name: "Home Server"
    description: "Main home Plex server"
    url: "http://192.168.1.100:32400"
    token: "${PLEX_TOKEN_HOME}"
    default: true
    read_only: false
    tags: ["production", "home"]
    
  - name: "Test Server"
    description: "Development and testing server"
    url: "http://localhost:32400"
    token: "${PLEX_TOKEN_TEST}"
    default: false
    read_only: false
    tags: ["development", "testing"]

settings:
  ui:
    theme: "dark"
    refresh_interval: 5
    
  performance:
    connection_timeout: 30
"""

    config_file = tmp_path / "servers.yaml"
    config_file.write_text(config_content)

    return config_file
