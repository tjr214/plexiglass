"""
Error handling service with user-friendly messages, retry logic, and graceful degradation.

This module provides comprehensive error handling capabilities:
- User-friendly error message transformation
- Automatic retry with exponential backoff
- Error severity categorization
- Error history tracking
- Graceful degradation support
"""

import asyncio
from enum import Enum
from typing import Any, Callable, TypeVar, Optional
from datetime import datetime
from collections import deque

from plexiglass.services.exceptions import ServiceError, ConnectionError, ServerNotFoundError
from plexiglass.config.exceptions import ConfigurationError


class ErrorSeverity(Enum):
    """Error severity levels for UI display."""

    CRITICAL = "critical"  # Blocks app functionality
    WARNING = "warning"  # Degraded functionality
    INFO = "info"  # Informational, no action needed


T = TypeVar("T")


class ErrorHandler:
    """
    Comprehensive error handling service.

    Provides:
    - User-friendly error message transformation
    - Automatic retry with exponential backoff
    - Error categorization by severity
    - Error history tracking
    """

    def __init__(
        self, retry_count: int = 3, retry_delay: float = 1.0, max_error_history: int = 100
    ):
        """
        Initialize ErrorHandler.

        Args:
            retry_count: Number of retry attempts for retryable errors
            retry_delay: Base delay between retries (seconds)
            max_error_history: Maximum number of errors to keep in history
        """
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.max_error_history = max_error_history
        self._error_history: deque = deque(maxlen=max_error_history)

    def get_user_friendly_message(self, error: Exception) -> str:
        """
        Convert exception to user-friendly message.

        Args:
            error: The exception to convert

        Returns:
            Human-readable error message
        """
        if isinstance(error, ConnectionError):
            return (
                "Unable to connect to the Plex server. "
                "Please check that the server is running and accessible."
            )

        if isinstance(error, ServerNotFoundError):
            return (
                "The requested server doesn't exist in your configuration. "
                "Please check your server settings."
            )

        if isinstance(error, ConfigurationError):
            return (
                "There's a problem with your configuration file. "
                "Please check your settings and try again."
            )

        if isinstance(error, ServiceError):
            return "A service error occurred. The operation couldn't be completed at this time."

        # Generic fallback
        return f"An unexpected error occurred: {type(error).__name__}"

    def categorize_error(self, error: Exception) -> ErrorSeverity:
        """
        Categorize error by severity level.

        Args:
            error: The exception to categorize

        Returns:
            ErrorSeverity level
        """
        # Critical errors block app functionality
        if isinstance(error, ConfigurationError):
            return ErrorSeverity.CRITICAL

        # Connection errors are warnings (app can continue)
        if isinstance(error, ConnectionError):
            return ErrorSeverity.WARNING

        # Server not found is informational
        if isinstance(error, ServerNotFoundError):
            return ErrorSeverity.INFO

        # Default to warning for unknown errors
        return ErrorSeverity.WARNING

    async def execute_with_retry(
        self, func: Callable[[], T], use_exponential_backoff: bool = False
    ) -> T:
        """
        Execute async function with automatic retry on transient failures.

        Args:
            func: Async function to execute
            use_exponential_backoff: Use exponential backoff for retries

        Returns:
            Result of successful function execution

        Raises:
            Original exception if all retries exhausted or error is non-retryable
        """
        last_error = None

        for attempt in range(self.retry_count):
            try:
                result = await func()
                return result
            except Exception as e:
                last_error = e

                # Don't retry non-retryable errors
                if not self.is_retryable_error(e):
                    raise

                # If this was the last attempt, raise
                if attempt >= self.retry_count - 1:
                    raise

                # Calculate delay
                if use_exponential_backoff:
                    delay = self.retry_delay * (2**attempt)
                else:
                    delay = self.retry_delay

                # Wait before retry
                await asyncio.sleep(delay)

        # Should never reach here, but just in case
        if last_error:
            raise last_error

    def is_retryable_error(self, error: Exception) -> bool:
        """
        Determine if an error is retryable.

        Args:
            error: The exception to check

        Returns:
            True if error is retryable, False otherwise
        """
        # Configuration errors are not retryable (need user intervention)
        if isinstance(error, ConfigurationError):
            return False

        # Server not found is not retryable (need config change)
        if isinstance(error, ServerNotFoundError):
            return False

        # Connection errors are retryable (transient)
        if isinstance(error, ConnectionError):
            return True

        # Generic service errors are retryable
        if isinstance(error, ServiceError):
            return True

        # Default to not retryable for unknown errors
        return False

    def format_error_for_display(self, error: Exception) -> dict[str, Any]:
        """
        Format error for UI display.

        Args:
            error: The exception to format

        Returns:
            Dictionary with formatted error information
        """
        return {
            "message": self.get_user_friendly_message(error),
            "severity": self.categorize_error(error).value,
            "timestamp": datetime.now().isoformat(),
            "type": type(error).__name__,
        }

    def record_error(self, error: Exception) -> None:
        """
        Record error in history.

        Args:
            error: The exception to record
        """
        error_data = self.format_error_for_display(error)
        self._error_history.append(error_data)

    def get_error_history(self) -> list[dict[str, Any]]:
        """
        Get error history.

        Returns:
            List of formatted errors
        """
        return list(self._error_history)

    def clear_error_history(self) -> None:
        """Clear all error history."""
        self._error_history.clear()
