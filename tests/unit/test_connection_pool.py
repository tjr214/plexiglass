"""
Unit tests for Enhanced Connection Pooling in ServerManager.

Tests advanced connection pooling features including health checking,
statistics tracking, and pool management.
"""

from unittest.mock import MagicMock, patch

import pytest
from plexapi.exceptions import Unauthorized

from plexiglass.config.loader import ConfigLoader
from plexiglass.services.exceptions import ConnectionError, ServerNotFoundError


@pytest.fixture
def mock_server():
    """Create a mock PlexServer instance."""
    server = MagicMock()
    server.friendlyName = "Test Server"
    server.version = "1.0.0"
    server.platform = "Linux"
    server.sessions.return_value = []
    server.library.sections.return_value = []
    return server


@pytest.fixture
def mock_config():
    """Create a mock ConfigLoader with test configuration."""
    config = MagicMock(spec=ConfigLoader)
    config.get_servers.return_value = [
        {
            "name": "test_server",
            "url": "http://localhost:32400",
            "token": "test_token",
        }
    ]
    config.get_default_server.return_value = config.get_servers.return_value[0]
    config.get_server_by_name.side_effect = lambda name: next(
        (s for s in config.get_servers.return_value if s["name"] == name), None
    )
    config.get_settings.return_value = {
        "performance": {
            "connection_timeout": 30,
            "pool_max_size": 10,
        }
    }
    return config


class TestConnectionHealthChecking:
    """Test connection health checking."""

    def test_health_check_with_healthy_connection(self, mock_config, mock_server):
        """Test health check with valid connection."""
        from plexiglass.services.server_manager import ServerManager

        manager = ServerManager(mock_config)

        with patch("plexiglass.services.server_manager.PlexServer") as mock_plex:
            mock_plex.return_value = mock_server

            manager.connect_to_server("test_server")
            is_healthy = manager.check_connection_health("test_server")

            assert is_healthy is True

    def test_health_check_for_nonexistent_connection(self, mock_config):
        """Test health check for non-existent connection."""
        from plexiglass.services.server_manager import ServerManager

        manager = ServerManager(mock_config)
        is_healthy = manager.check_connection_health("nonexistent")

        assert is_healthy is False


class TestConnectionPoolStatistics:
    """Test connection pool statistics tracking."""

    def test_get_pool_statistics_empty(self, mock_config):
        """Test getting pool statistics when empty."""
        from plexiglass.services.server_manager import ServerManager

        manager = ServerManager(mock_config)
        stats = manager.get_pool_statistics()

        assert stats["pool_size"] == 0
        assert stats["connected_servers"] == []
        assert stats["max_pool_size"] == 10

    def test_get_pool_statistics_with_connection(self, mock_config, mock_server):
        """Test getting pool statistics with active connections."""
        from plexiglass.services.server_manager import ServerManager

        manager = ServerManager(mock_config)

        with patch("plexiglass.services.server_manager.PlexServer") as mock_plex:
            mock_plex.return_value = mock_server

            manager.connect_to_server("test_server")
            stats = manager.get_pool_statistics()

            assert stats["pool_size"] == 1
            assert stats["connected_servers"] == ["test_server"]
            assert stats["max_pool_size"] == 10

    def test_pool_statistics_update_on_multiple_connections(self, mock_config, mock_server):
        """Test that statistics update as connections change."""
        from plexiglass.services.server_manager import ServerManager

        manager = ServerManager(mock_config)

        with patch("plexiglass.services.server_manager.PlexServer") as mock_plex:
            mock_plex.return_value = mock_server

            # Add second server
            mock_config.get_servers.return_value.append(
                {"name": "server2", "url": "http://localhost:32400", "token": "token"}
            )

            stats1 = manager.get_pool_statistics()
            manager.connect_to_server("test_server")
            manager.connect_to_server("server2")
            stats2 = manager.get_pool_statistics()

            assert stats2["pool_size"] > stats1["pool_size"]
            assert len(stats2["connected_servers"]) > len(stats1["connected_servers"])


class TestConnectionReuse:
    """Test connection reuse for efficiency."""

    def test_reuses_existing_connection(self, mock_config, mock_server):
        """Test that existing connection is reused instead of creating new."""
        from plexiglass.services.server_manager import ServerManager

        manager = ServerManager(mock_config)

        with patch("plexiglass.services.server_manager.PlexServer") as mock_plex:
            mock_plex.return_value = mock_server

            server1 = manager.connect_to_server("test_server")
            server2 = manager.connect_to_server("test_server")

            assert server1 is server2  # Same instance
            assert mock_plex.call_count == 1  # Only created once

    def test_clear_connection_pool(self, mock_config, mock_server):
        """Test clearing the connection pool."""
        from plexiglass.services.server_manager import ServerManager

        manager = ServerManager(mock_config)

        with patch("plexiglass.services.server_manager.PlexServer") as mock_plex:
            mock_plex.return_value = mock_server

            manager.connect_to_server("test_server")
            assert manager.get_pool_statistics()["pool_size"] == 1

            manager.clear_connection_pool()
            assert manager.get_pool_statistics()["pool_size"] == 0

    def test_disconnect_removes_from_pool(self, mock_config, mock_server):
        """Test that disconnect removes server from pool."""
        from plexiglass.services.server_manager import ServerManager

        manager = ServerManager(mock_config)

        with patch("plexiglass.services.server_manager.PlexServer") as mock_plex:
            mock_plex.return_value = mock_server

            manager.connect_to_server("test_server")
            manager.disconnect_server("test_server")

            assert "test_server" not in manager._connection_pool
            assert manager.get_pool_statistics()["pool_size"] == 0

    def test_clear_all_synonym(self, mock_config, mock_server):
        """Test that disconnect_all is synonym for clear_connection_pool."""
        from plexiglass.services.server_manager import ServerManager

        manager = ServerManager(mock_config)

        with patch("plexiglass.services.server_manager.PlexServer") as mock_plex:
            mock_plex.return_value = mock_server

            manager.connect_to_server("test_server")
            assert manager.get_pool_statistics()["pool_size"] == 1

            manager.disconnect_all()
            assert manager.get_pool_statistics()["pool_size"] == 0
