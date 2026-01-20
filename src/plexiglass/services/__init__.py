"""
Services module for PlexiGlass.

This module provides service-level functionality including:
- Server connection management
- Multi-server coordination
- Request caching with TTL
- Service-level error handling
"""

from plexiglass.services.cache_service import CacheService
from plexiglass.services.exceptions import (
    ConnectionError,
    ServerNotFoundError,
    ServiceError,
)
from plexiglass.services.server_manager import ServerManager
from plexiglass.services.undo_service import UndoService

__all__ = [
    "CacheService",
    "ServerManager",
    "UndoService",
    "ServiceError",
    "ConnectionError",
    "ServerNotFoundError",
]
