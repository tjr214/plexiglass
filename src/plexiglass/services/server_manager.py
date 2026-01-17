"""
Server Manager Service for PlexiGlass.

This module provides multi-server connection management including:
- Connection pooling for multiple Plex servers
- Health checking and status monitoring
- Connection caching
- Error handling for network/auth issues
"""

from typing import Any

from plexapi.exceptions import Unauthorized
from plexapi.server import PlexServer

from plexiglass.config.loader import ConfigLoader
from plexiglass.services.exceptions import ConnectionError, ServerNotFoundError


class ServerManager:
    """
    Manages connections to multiple Plex Media Servers.

    Features:
    - Multi-server connection pooling
    - Connection caching (lazy loading)
    - Health status monitoring
    - Read-only server protection
    - Graceful error handling

    Example:
        >>> from plexiglass.config.loader import ConfigLoader
        >>> loader = ConfigLoader(Path("config/servers.yaml"))
        >>> loader.load()
        >>> manager = ServerManager(loader)
        >>> server = manager.connect_to_default()
        >>> print(server.friendlyName)
    """

    def __init__(self, config_loader: ConfigLoader) -> None:
        """
        Initialize the ServerManager with a configuration loader.

        Args:
            config_loader: ConfigLoader instance with loaded configuration
        """
        self.config_loader = config_loader
        self._connection_pool: dict[str, PlexServer] = {}

    def connect_to_default(self) -> PlexServer:
        """
        Connect to the default Plex server.

        Returns the first server with default: true, or the first server if none
        are marked as default.

        Returns:
            PlexServer instance connected to the default server

        Raises:
            ConnectionError: If connection fails
            ServerNotFoundError: If no servers are configured
        """
        default_server_config = self.config_loader.get_default_server()

        if not default_server_config:
            raise ServerNotFoundError("No default server configured")

        server_name = default_server_config["name"]
        return self.connect_to_server(server_name)

    def connect_to_server(self, name: str) -> PlexServer:
        """
        Connect to a specific Plex server by name.

        If already connected, returns the cached connection.

        Args:
            name: Server name as defined in configuration

        Returns:
            PlexServer instance connected to the specified server

        Raises:
            ServerNotFoundError: If server name not found in configuration
            ConnectionError: If connection fails
        """
        # Return cached connection if available
        if name in self._connection_pool:
            return self._connection_pool[name]

        # Get server configuration
        server_config = self.config_loader.get_server_by_name(name)
        if not server_config:
            raise ServerNotFoundError(f"Server '{name}' not found in configuration")

        # Attempt connection
        try:
            server = PlexServer(
                baseurl=server_config["url"],
                token=server_config["token"],
                timeout=self.config_loader.get_settings()
                .get("performance", {})
                .get("connection_timeout", 30),
            )

            # Cache the connection
            self._connection_pool[name] = server

            return server

        except Unauthorized as e:
            raise ConnectionError(
                f"Unauthorized: Failed to connect to '{name}'. Check your Plex token. Error: {e}"
            ) from e
        except TimeoutError as e:
            raise ConnectionError(
                f"Connection timeout: Failed to connect to '{name}' at "
                f"{server_config['url']}. Error: {e}"
            ) from e
        except Exception as e:
            raise ConnectionError(f"Failed to connect to server '{name}': {e}") from e

    def disconnect_server(self, name: str) -> None:
        """
        Disconnect from a specific server.

        Removes the server from the connection pool.

        Args:
            name: Server name to disconnect
        """
        if name in self._connection_pool:
            del self._connection_pool[name]

    def disconnect_all(self) -> None:
        """
        Disconnect from all servers.

        Clears the entire connection pool.
        """
        self._connection_pool.clear()

    def get_connected_servers(self) -> list[str]:
        """
        Get list of currently connected server names.

        Returns:
            List of server names that are currently connected
        """
        return list(self._connection_pool.keys())

    def get_all_server_names(self) -> list[str]:
        """
        Get list of all configured server names (whether connected or not).

        Returns:
            List of all server names from configuration
        """
        servers = self.config_loader.get_servers()
        return [server["name"] for server in servers]

    def get_server_count(self) -> int:
        """
        Get the total number of configured servers.

        Returns:
            Number of servers in configuration
        """
        return len(self.config_loader.get_servers())

    def get_server_status(self, name: str) -> dict[str, Any]:
        """
        Get status information for a specific server.

        Args:
            name: Server name to check status

        Returns:
            Dictionary with status information:
            - connected: bool
            - version: str (if connected)
            - platform: str (if connected)
            - friendly_name: str (if connected)

        Raises:
            ServerNotFoundError: If server name not found in configuration
        """
        server_config = self.config_loader.get_server_by_name(name)
        if not server_config:
            raise ServerNotFoundError(f"Server '{name}' not found in configuration")

        status: dict[str, Any] = {
            "connected": name in self._connection_pool,
            "name": name,
            "url": server_config["url"],
            "session_count": 0,
            "now_playing": [],
        }

        if name in self._connection_pool:
            server = self._connection_pool[name]
            status["version"] = server.version
            status["platform"] = server.platform
            status["friendly_name"] = server.friendlyName

            sessions = self._safe_get_sessions(server)
            status["session_count"] = len(sessions)
            status["now_playing"] = [self._build_now_playing_entry(session) for session in sessions]

        return status

    @staticmethod
    def _safe_get_sessions(server: PlexServer) -> list[Any]:
        try:
            return list(server.sessions())
        except Exception:
            return []

    @staticmethod
    def _build_now_playing_entry(session: Any) -> dict[str, Any]:
        title = (
            getattr(session, "title", None)
            or getattr(session, "grandparentTitle", None)
            or "Unknown"
        )
        user = ServerManager._extract_session_user(session)
        state = getattr(session, "state", None) or "unknown"
        progress_percent = ServerManager._calculate_progress(session)

        return {
            "title": title,
            "user": user,
            "state": state,
            "progress_percent": progress_percent,
        }

    @staticmethod
    def _extract_session_user(session: Any) -> str:
        usernames = getattr(session, "usernames", None)
        if usernames:
            return str(usernames[0])

        user = getattr(session, "user", None)
        if user is not None:
            return str(getattr(user, "title", None) or getattr(user, "username", None) or user)

        players = getattr(session, "players", None)
        if players:
            player = players[0]
            return str(
                getattr(player, "title", None) or getattr(player, "username", None) or player
            )

        return "Unknown"

    @staticmethod
    def _calculate_progress(session: Any) -> int | None:
        view_offset = getattr(session, "viewOffset", None)
        duration = getattr(session, "duration", None)
        if view_offset is None or not duration:
            return None

        try:
            progress = int((float(view_offset) / float(duration)) * 100)
        except (TypeError, ValueError, ZeroDivisionError):
            return None

        return max(0, min(progress, 100))

    def is_server_read_only(self, name: str) -> bool:
        """
        Check if a server is marked as read-only in configuration.

        Args:
            name: Server name to check

        Returns:
            True if server is read-only, False otherwise

        Raises:
            ServerNotFoundError: If server name not found in configuration
        """
        server_config = self.config_loader.get_server_by_name(name)
        if not server_config:
            raise ServerNotFoundError(f"Server '{name}' not found in configuration")

        return bool(server_config.get("read_only", False))
