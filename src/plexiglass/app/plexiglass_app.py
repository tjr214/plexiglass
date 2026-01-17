"""
PlexiGlass - Main Textual Application.

This is a placeholder for the main PlexiGlass TUI application.
It will be implemented following TDD principles in Sprint 1.
"""

from textual.app import App


class PlexiGlassApp(App):
    """
    PlexiGlass - Multi-server Plex dashboard and python-plexapi feature gallery.

    This is the main Textual application class. Currently a minimal stub
    that will be expanded during implementation sprints.
    """

    # App metadata
    TITLE = "PlexiGlass"
    SUB_TITLE = "Plex Media Server Dashboard & API Gallery"

    # CSS will be loaded from external files later
    CSS = """
    Screen {
        background: $surface;
        color: $text;
    }
    
    #welcome {
        content-align: center middle;
        color: $accent;
    }
    """

    def compose(self):
        """Create child widgets for the app."""
        from textual.widgets import Static

        # Placeholder welcome message
        yield Static(
            "🎨 Welcome to PlexiGlass! 🎨\n\n"
            "This is a placeholder app.\n"
            "The full application will be implemented in upcoming sprints.\n\n"
            "Press 'q' to quit.",
            id="welcome",
        )

    def on_mount(self) -> None:
        """Called when app starts."""
        # These are class variables, already set
        pass

    # Keybindings
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]
