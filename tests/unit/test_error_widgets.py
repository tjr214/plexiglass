"""
Tests for error display widgets (Toast and ErrorModal).
"""

import pytest
from textual.app import App
from plexiglass.ui.widgets.error_toast import ErrorToast
from plexiglass.ui.widgets.error_modal import ErrorModal
from plexiglass.services.error_handler import ErrorSeverity


class TestErrorToast:
    """Test suite for ErrorToast widget."""

    @pytest.mark.asyncio
    async def test_error_toast_creation(self):
        """Test ErrorToast can be created."""
        toast = ErrorToast(message="Test error message", severity=ErrorSeverity.WARNING)
        assert toast is not None
        assert toast.message == "Test error message"
        assert toast.severity == ErrorSeverity.WARNING

    @pytest.mark.asyncio
    async def test_error_toast_default_severity(self):
        """Test ErrorToast defaults to WARNING severity."""
        toast = ErrorToast(message="Test message")
        assert toast.severity == ErrorSeverity.WARNING

    @pytest.mark.asyncio
    async def test_error_toast_critical_severity(self):
        """Test ErrorToast with CRITICAL severity."""
        toast = ErrorToast(message="Critical error", severity=ErrorSeverity.CRITICAL)
        assert toast.severity == ErrorSeverity.CRITICAL

    @pytest.mark.asyncio
    async def test_error_toast_info_severity(self):
        """Test ErrorToast with INFO severity."""
        toast = ErrorToast(message="Info message", severity=ErrorSeverity.INFO)
        assert toast.severity == ErrorSeverity.INFO

    @pytest.mark.asyncio
    async def test_error_toast_auto_dismiss(self):
        """Test ErrorToast auto-dismiss configuration."""
        toast = ErrorToast(message="Test", auto_dismiss=True, dismiss_delay=3.0)
        assert toast.auto_dismiss is True
        assert toast.dismiss_delay == 3.0

    @pytest.mark.asyncio
    async def test_error_toast_no_auto_dismiss(self):
        """Test ErrorToast without auto-dismiss."""
        toast = ErrorToast(message="Test", auto_dismiss=False)
        assert toast.auto_dismiss is False

    @pytest.mark.asyncio
    async def test_error_toast_has_css_classes(self):
        """Test ErrorToast applies correct CSS classes."""
        toast_warning = ErrorToast("Test", severity=ErrorSeverity.WARNING)
        toast_critical = ErrorToast("Test", severity=ErrorSeverity.CRITICAL)
        toast_info = ErrorToast("Test", severity=ErrorSeverity.INFO)

        assert "error-toast" in toast_warning.classes
        assert "error-toast" in toast_critical.classes
        assert "error-toast" in toast_info.classes


class TestErrorModal:
    """Test suite for ErrorModal widget."""

    @pytest.mark.asyncio
    async def test_error_modal_creation(self):
        """Test ErrorModal can be created."""
        modal = ErrorModal(
            title="Error Occurred", message="Something went wrong", severity=ErrorSeverity.CRITICAL
        )
        assert modal is not None
        assert modal.title == "Error Occurred"
        assert modal.message == "Something went wrong"
        assert modal.severity == ErrorSeverity.CRITICAL

    @pytest.mark.asyncio
    async def test_error_modal_default_title(self):
        """Test ErrorModal with default title."""
        modal = ErrorModal(message="Test message")
        assert modal.title == "Error"

    @pytest.mark.asyncio
    async def test_error_modal_with_details(self):
        """Test ErrorModal with additional details."""
        modal = ErrorModal(message="Main error", details="Stack trace or additional info")
        assert modal.details == "Stack trace or additional info"

    @pytest.mark.asyncio
    async def test_error_modal_without_details(self):
        """Test ErrorModal without details."""
        modal = ErrorModal(message="Test")
        assert modal.details is None or modal.details == ""

    @pytest.mark.asyncio
    async def test_error_modal_has_severity(self):
        """Test ErrorModal stores severity correctly."""
        modal = ErrorModal(message="Test", severity=ErrorSeverity.CRITICAL)
        assert modal.severity == ErrorSeverity.CRITICAL

    @pytest.mark.asyncio
    async def test_error_modal_dismissible(self):
        """Test ErrorModal can be dismissed."""
        modal = ErrorModal(message="Test", dismissible=True)
        assert modal.dismissible is True

    @pytest.mark.asyncio
    async def test_error_modal_not_dismissible(self):
        """Test ErrorModal for critical errors not dismissible."""
        modal = ErrorModal(message="Critical", severity=ErrorSeverity.CRITICAL, dismissible=False)
        assert modal.dismissible is False
