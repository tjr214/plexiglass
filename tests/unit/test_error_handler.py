"""
Tests for ErrorHandler service.

This module tests the error handling, user-friendly messages,
retry logic, and graceful degradation functionality.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from plexiglass.services.error_handler import ErrorHandler, ErrorSeverity
from plexiglass.services.exceptions import ServiceError, ConnectionError, ServerNotFoundError
from plexiglass.config.exceptions import ConfigurationError


class TestErrorHandler:
    """Test suite for ErrorHandler service."""

    def test_error_handler_initialization(self):
        """Test ErrorHandler can be instantiated."""
        handler = ErrorHandler()
        assert handler is not None
        assert handler.retry_count == 3
        assert handler.retry_delay == 1.0

    def test_custom_retry_configuration(self):
        """Test ErrorHandler with custom retry configuration."""
        handler = ErrorHandler(retry_count=5, retry_delay=2.0)
        assert handler.retry_count == 5
        assert handler.retry_delay == 2.0

    def test_get_user_friendly_message_connection_error(self):
        """Test user-friendly message for ConnectionError."""
        handler = ErrorHandler()
        error = ConnectionError("Failed to connect to http://localhost:32400")
        message = handler.get_user_friendly_message(error)

        assert "connect" in message.lower()
        assert "plex server" in message.lower()
        assert message != str(error)  # Should be transformed

    def test_get_user_friendly_message_server_not_found(self):
        """Test user-friendly message for ServerNotFoundError."""
        handler = ErrorHandler()
        error = ServerNotFoundError("Server 'test' not found")
        message = handler.get_user_friendly_message(error)

        assert "server" in message.lower()
        assert "not found" in message.lower() or "doesn't exist" in message.lower()

    def test_get_user_friendly_message_config_error(self):
        """Test user-friendly message for ConfigurationError."""
        handler = ErrorHandler()
        error = ConfigurationError("Invalid YAML syntax")
        message = handler.get_user_friendly_message(error)

        assert "configuration" in message.lower()
        assert "settings" in message.lower() or "config" in message.lower()

    def test_get_user_friendly_message_generic_error(self):
        """Test user-friendly message for generic exceptions."""
        handler = ErrorHandler()
        error = ValueError("Invalid value")
        message = handler.get_user_friendly_message(error)

        assert "error" in message.lower()
        assert len(message) > 0

    def test_categorize_error_severity_critical(self):
        """Test error categorization - critical errors."""
        handler = ErrorHandler()
        error = ConfigurationError("No config file")
        severity = handler.categorize_error(error)

        assert severity == ErrorSeverity.CRITICAL

    def test_categorize_error_severity_warning(self):
        """Test error categorization - warning level."""
        handler = ErrorHandler()
        error = ConnectionError("Timeout")
        severity = handler.categorize_error(error)

        assert severity == ErrorSeverity.WARNING

    def test_categorize_error_severity_info(self):
        """Test error categorization - info level."""
        handler = ErrorHandler()
        error = ServerNotFoundError("Server not found")
        severity = handler.categorize_error(error)

        assert severity == ErrorSeverity.INFO

    @pytest.mark.asyncio
    async def test_execute_with_retry_success_first_try(self):
        """Test retry logic succeeds on first attempt."""
        handler = ErrorHandler(retry_count=3, retry_delay=0.01)

        mock_func = AsyncMock(return_value="success")
        result = await handler.execute_with_retry(mock_func)

        assert result == "success"
        assert mock_func.call_count == 1

    @pytest.mark.asyncio
    async def test_execute_with_retry_success_after_failures(self):
        """Test retry logic succeeds after transient failures."""
        handler = ErrorHandler(retry_count=3, retry_delay=0.01)

        # Fail twice, then succeed
        mock_func = AsyncMock(
            side_effect=[ConnectionError("Timeout"), ConnectionError("Timeout"), "success"]
        )

        result = await handler.execute_with_retry(mock_func)

        assert result == "success"
        assert mock_func.call_count == 3

    @pytest.mark.asyncio
    async def test_execute_with_retry_exhausts_retries(self):
        """Test retry logic exhausts all retries and fails."""
        handler = ErrorHandler(retry_count=3, retry_delay=0.01)

        # Always fail
        mock_func = AsyncMock(side_effect=ConnectionError("Always fails"))

        with pytest.raises(ConnectionError):
            await handler.execute_with_retry(mock_func)

        assert mock_func.call_count == 3

    @pytest.mark.asyncio
    async def test_execute_with_retry_non_retryable_error(self):
        """Test retry logic doesn't retry non-retryable errors."""
        handler = ErrorHandler(retry_count=3, retry_delay=0.01)

        # ConfigurationError should not be retried
        mock_func = AsyncMock(side_effect=ConfigurationError("Bad config"))

        with pytest.raises(ConfigurationError):
            await handler.execute_with_retry(mock_func)

        # Should fail immediately, no retries
        assert mock_func.call_count == 1

    @pytest.mark.asyncio
    async def test_execute_with_retry_exponential_backoff(self):
        """Test retry logic uses exponential backoff."""
        handler = ErrorHandler(retry_count=3, retry_delay=0.01)

        mock_func = AsyncMock(side_effect=ConnectionError("Timeout"))

        with patch("asyncio.sleep") as mock_sleep:
            with pytest.raises(ConnectionError):
                await handler.execute_with_retry(mock_func, use_exponential_backoff=True)

            # Should have called sleep with increasing delays
            assert mock_sleep.call_count == 2  # Sleep between retries
            # First sleep should be ~0.01, second should be ~0.02
            calls = [call.args[0] for call in mock_sleep.call_args_list]
            assert calls[1] > calls[0]  # Exponential increase

    def test_is_retryable_error_connection_errors(self):
        """Test retryable error detection - connection errors are retryable."""
        handler = ErrorHandler()

        assert handler.is_retryable_error(ConnectionError("Timeout"))
        assert handler.is_retryable_error(ServiceError("Service unavailable"))

    def test_is_retryable_error_non_retryable(self):
        """Test retryable error detection - config errors not retryable."""
        handler = ErrorHandler()

        assert not handler.is_retryable_error(ConfigurationError("Bad config"))
        assert not handler.is_retryable_error(ServerNotFoundError("Not found"))

    def test_format_error_for_display(self):
        """Test error formatting for UI display."""
        handler = ErrorHandler()
        error = ConnectionError("Failed to connect")

        display_error = handler.format_error_for_display(error)

        assert "message" in display_error
        assert "severity" in display_error
        assert "timestamp" in display_error
        assert display_error["message"] == handler.get_user_friendly_message(error)
        assert display_error["severity"] in [s.value for s in ErrorSeverity]

    def test_error_history_tracking(self):
        """Test error history is tracked."""
        handler = ErrorHandler(max_error_history=5)

        errors = [
            ConnectionError("Error 1"),
            ServerNotFoundError("Error 2"),
            ConfigurationError("Error 3"),
        ]

        for error in errors:
            handler.record_error(error)

        history = handler.get_error_history()
        assert len(history) == 3

    def test_error_history_max_limit(self):
        """Test error history respects max limit."""
        handler = ErrorHandler(max_error_history=2)

        for i in range(5):
            handler.record_error(ConnectionError(f"Error {i}"))

        history = handler.get_error_history()
        assert len(history) == 2  # Only keeps last 2

    def test_clear_error_history(self):
        """Test clearing error history."""
        handler = ErrorHandler()

        handler.record_error(ConnectionError("Error"))
        assert len(handler.get_error_history()) == 1

        handler.clear_error_history()
        assert len(handler.get_error_history()) == 0
