"""
Loading Indicator Widget - Animated spinner for loading states.

Provides visual feedback during async operations.
"""

from textual.widget import Widget
from textual.widgets import Static
from textual.reactive import reactive


class LoadingIndicator(Widget):
    """
    Animated loading indicator widget.

    Features:
    - Animated spinner
    - Customizable message
    - Start/stop animation control
    - Auto-starts by default
    """

    DEFAULT_CSS = """
    LoadingIndicator {
        width: auto;
        height: auto;
        padding: 1 2;
        background: $panel;
        border: tall $accent;
    }
    
    LoadingIndicator .spinner {
        color: $accent;
        text-style: bold;
    }
    
    LoadingIndicator .message {
        color: $text;
        margin-left: 2;
    }
    """

    # Reactive properties
    message = reactive("Loading...")
    is_animating = reactive(True)

    # Spinner frames for animation
    SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def __init__(self, message: str = "Loading...", **kwargs):
        """
        Initialize LoadingIndicator.

        Args:
            message: Loading message to display
        """
        super().__init__(**kwargs)
        self.message = message
        self.is_animating = True
        self._frame_index = 0
        self._timer = None

        # Add CSS class
        self.add_class("loading-indicator")

    def compose(self):
        """Compose the loading indicator."""
        yield Static(f"{self.SPINNER_FRAMES[0]} {self.message}", classes="spinner-text")

    def on_mount(self):
        """Start animation when mounted."""
        if self.is_animating:
            self._start_animation()

    def _start_animation(self):
        """Start the spinner animation."""
        if self._timer is None:
            self._timer = self.set_interval(0.1, self._update_spinner)

    def _update_spinner(self):
        """Update spinner frame."""
        if not self.is_animating:
            return

        self._frame_index = (self._frame_index + 1) % len(self.SPINNER_FRAMES)
        spinner_text = self.query_one(".spinner-text", Static)
        spinner_text.update(f"{self.SPINNER_FRAMES[self._frame_index]} {self.message}")

    def start(self):
        """Start the animation."""
        self.is_animating = True
        self._start_animation()

    def stop(self):
        """Stop the animation."""
        self.is_animating = False
        if self._timer is not None:
            self._timer.stop()
            self._timer = None

    def update_message(self, message: str):
        """
        Update the loading message.

        Args:
            message: New message to display
        """
        self.message = message
        try:
            spinner_text = self.query_one(".spinner-text", Static)
            spinner_text.update(f"{self.SPINNER_FRAMES[self._frame_index]} {self.message}")
        except Exception:
            pass  # Widget not mounted yet
