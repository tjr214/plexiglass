"""
Progress Bar Widget - Visual progress indicator for long operations.

Displays progress with percentage and optional label.
"""

from textual.widget import Widget
from textual.widgets import Static, ProgressBar as TextualProgressBar
from textual.reactive import reactive
from textual.containers import Vertical


class ProgressBar(Widget):
    """
    Progress bar widget with label and percentage display.

    Features:
    - Visual progress bar
    - Percentage display
    - Optional label
    - Progress clamping (0-100%)
    - Completion detection
    """

    DEFAULT_CSS = """
    ProgressBar {
        width: 100%;
        height: auto;
        padding: 1 2;
        background: $panel;
        border: tall $primary;
    }
    
    ProgressBar .progress-label {
        color: $text;
        text-style: bold;
        margin-bottom: 1;
    }
    
    ProgressBar .progress-percentage {
        color: $accent;
        text-style: bold;
        text-align: right;
    }
    
    ProgressBar TextualProgressBar {
        height: 1;
    }
    """

    # Reactive properties
    progress = reactive(0)
    total = reactive(100)
    label = reactive("")
    show_percentage = reactive(True)

    def __init__(
        self,
        progress: int = 0,
        total: int = 100,
        label: str = "",
        show_percentage: bool = True,
        **kwargs,
    ):
        """
        Initialize ProgressBar.

        Args:
            progress: Current progress value
            total: Total/maximum value
            label: Optional label text
            show_percentage: Whether to show percentage
        """
        super().__init__(**kwargs)
        self.progress = max(0, min(progress, total))  # Clamp
        self.total = total
        self.label = label
        self.show_percentage = show_percentage

        # Add CSS class
        self.add_class("progress-bar")

    @property
    def percentage(self) -> float:
        """
        Calculate current percentage.

        Returns:
            Percentage value (0-100)
        """
        if self.total == 0:
            return 0.0
        return (self.progress / self.total) * 100.0

    @property
    def is_complete(self) -> bool:
        """
        Check if progress is complete.

        Returns:
            True if progress equals total
        """
        return self.progress >= self.total

    def compose(self):
        """Compose the progress bar."""
        with Vertical():
            if self.label:
                yield Static(self.label, classes="progress-label")

            yield TextualProgressBar(
                total=self.total, show_eta=False, show_percentage=self.show_percentage
            )

    def update(self, progress: int):
        """
        Update progress value.

        Args:
            progress: New progress value (will be clamped to 0-total)
        """
        self.progress = max(0, min(progress, self.total))

        # Update the Textual ProgressBar widget
        try:
            bar = self.query_one(TextualProgressBar)
            bar.update(progress=self.progress)
        except Exception:
            pass  # Widget not mounted yet

    def increment(self, amount: int = 1):
        """
        Increment progress by amount.

        Args:
            amount: Amount to increment
        """
        self.update(self.progress + amount)

    def reset(self):
        """Reset progress to 0."""
        self.update(0)

    def update_label(self, label: str):
        """
        Update the progress label.

        Args:
            label: New label text
        """
        self.label = label
        try:
            label_widget = self.query_one(".progress-label", Static)
            label_widget.update(label)
        except Exception:
            pass  # Widget doesn't exist
