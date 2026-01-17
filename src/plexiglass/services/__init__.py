"""
Services module for PlexiGlass.

This module provides service-level functionality including:
- Server connection management
- Multi-server coordination
- Service-level error handling
"""

from plexiglass.services.exceptions import (
    ConnectionError,
    ServerNotFoundError,
    ServiceError,
)
from plexiglass.services.server_manager import ServerManager

__all__ = ["ServerManager", "ServiceError", "ConnectionError", "ServerNotFoundError"]
