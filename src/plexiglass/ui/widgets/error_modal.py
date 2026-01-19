"""
Error Modal Widget - Modal dialog for displaying errors.

Used for critical errors that require user acknowledgment.
"""

from textual.screen import ModalScreen
from textual.widgets import Static, Button
from textual.containers import Container, Vertical, Horizontal
from plexiglass.services.error_handler import ErrorSeverity


class ErrorModal(ModalScreen):
    """
    Modal dialog for displaying errors.

    Features:
    - Blocks interaction until dismissed
    - Shows detailed error information
    - Color-coded by severity
    - Optional details section
    """

    DEFAULT_CSS = """
    ErrorModal {
        align: center middle;
    }
    
    .error-modal {
        width: 70%;
        height: auto;
        max-height: 80%;
        background: $panel;
        border: tall $error;
        padding: 2 3;
    }
    
    .error-modal.critical {
        border: tall $error;
    }
    
    .error-modal.warning {
        border: tall $warning;
    }
    
    .error-modal.info {
        border: tall $accent;
    }
    
    .modal-title {
        text-style: bold;
        color: $error;
        margin-bottom: 1;
    }
    
    .modal-message {
        margin-bottom: 1;
    }
    
    .modal-details {
        margin-top: 1;
        padding: 1;
        background: $surface;
        border: tall $primary;
        color: $text-muted;
    }
    
    .modal-actions {
        margin-top: 2;
        align: center middle;
    }
    """

    def __init__(
        self,
        message: str,
        title: str = "Error",
        severity: ErrorSeverity = ErrorSeverity.WARNING,
        details: str = None,
        dismissible: bool = True,
        **kwargs,
    ):
        """
        Initialize ErrorModal.

        Args:
            message: Main error message
            title: Modal title
            severity: Error severity level
            details: Additional error details (optional)
            dismissible: Whether modal can be dismissed
        """
        super().__init__(**kwargs)
        self.title = title
        self.message = message
        self.severity = severity
        self.details = details
        self.dismissible = dismissible

    def compose(self):
        """Compose the modal content."""
        with Container(classes=f"error-modal {self.severity.value}"):
            yield Static(self.title, classes="modal-title")
            yield Static(self.message, classes="modal-message")

            if self.details:
                yield Static(self.details, classes="modal-details")

            if self.dismissible:
                with Horizontal(classes="modal-actions"):
                    yield Button("OK", variant="primary", id="dismiss-button")

    def on_button_pressed(self, event: Button.Pressed):
        """Handle button press - dismiss modal."""
        if event.button.id == "dismiss-button":
            self.dismiss()
