"""
Error Toast Widget - Non-intrusive error notifications.

Displays temporary error messages that auto-dismiss.
"""

from textual.widget import Widget
from textual.widgets import Static
from textual.containers import Container
from plexiglass.services.error_handler import ErrorSeverity


class ErrorToast(Container):
    """
    Toast notification widget for displaying errors.

    Features:
    - Auto-dismiss after configurable delay
    - Color-coded by severity
    - Non-intrusive positioning
    """

    DEFAULT_CSS = """
    ErrorToast {
        dock: top;
        height: auto;
        width: 60%;
        margin: 1 2;
        padding: 1 2;
        background: $panel;
        border: tall $warning;
    }
    
    ErrorToast.critical {
        border: tall $error;
        background: $error 20%;
    }
    
    ErrorToast.warning {
        border: tall $warning;
        background: $warning 20%;
    }
    
    ErrorToast.info {
        border: tall $accent;
        background: $accent 20%;
    }
    """

    def __init__(
        self,
        message: str,
        severity: ErrorSeverity = ErrorSeverity.WARNING,
        auto_dismiss: bool = True,
        dismiss_delay: float = 5.0,
        **kwargs,
    ):
        """
        Initialize ErrorToast.

        Args:
            message: Error message to display
            severity: Error severity level
            auto_dismiss: Whether to auto-dismiss
            dismiss_delay: Delay before auto-dismiss (seconds)
        """
        super().__init__(**kwargs)
        self.message = message
        self.severity = severity
        self.auto_dismiss = auto_dismiss
        self.dismiss_delay = dismiss_delay

        # Add severity-specific CSS class
        self.add_class("error-toast")
        self.add_class(severity.value)

    def compose(self):
        """Compose the toast content."""
        yield Static(self.message, classes="toast-message")

    def on_mount(self):
        """Handle mount event - start auto-dismiss timer if enabled."""
        if self.auto_dismiss:
            self.set_timer(self.dismiss_delay, self.dismiss)

    def dismiss(self):
        """Dismiss the toast."""
        self.remove()
