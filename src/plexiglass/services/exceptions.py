"""
Custom exceptions for service layer.
"""


class ServiceError(Exception):
    """Base exception for all service-layer errors."""

    pass


class ConnectionError(ServiceError):
    """
    Raised when there is an error connecting to a Plex server.

    This includes:
    - Unauthorized (invalid token)
    - Timeout errors
    - Network errors
    - Server unreachable
    """

    pass


class ServerNotFoundError(ServiceError):
    """
    Raised when a requested server is not found in the configuration.
    """

    pass
