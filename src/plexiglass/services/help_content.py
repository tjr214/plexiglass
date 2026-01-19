"""
Help Content Service - Comprehensive help topics and keyboard shortcuts.

Provides searchable help content for all PlexiGlass features.
"""

from typing import Optional


class HelpContent:
    """
    Help content provider with search and context-sensitive help.

    Features:
    - Comprehensive help topics
    - Searchable content
    - Keyboard shortcuts reference
    - Context-sensitive help
    """

    def __init__(self):
        """Initialize HelpContent with all topics."""
        self._topics = self._initialize_topics()
        self._shortcuts = self._initialize_shortcuts()

    def _initialize_topics(self) -> list[dict]:
        """Initialize all help topics."""
        return [
            {
                "id": "overview",
                "title": "PlexiGlass Overview",
                "category": "Getting Started",
                "content": """
PlexiGlass is a dual-purpose Textual TUI application:

1. **Multi-Server Plex Dashboard**: Monitor and manage multiple Plex Media Servers
2. **python-plexapi Feature Gallery**: Interactive demonstration of 200+ API features

Key Features:
- Beautiful, colorful terminal interface
- Multi-server management
- 15 gallery categories with 35+ demos
- Safe write operations with undo
- Real-time server monitoring
""",
            },
            {
                "id": "dashboard",
                "title": "Dashboard Mode",
                "category": "Core Features",
                "content": """
The Dashboard provides a real-time overview of all your Plex servers.

Features:
- Server status cards showing connection state
- Active sessions with now-playing information
- Library statistics (total libraries, items)
- Quick actions menu for common tasks
- Command prompt (press ':' to open)
- Auto-refresh every 5 seconds

Navigation:
- Press 'd' to switch to Dashboard
- Press ':' to open command prompt
- Use Tab/Shift+Tab to navigate between cards
""",
            },
            {
                "id": "gallery",
                "title": "Gallery Mode",
                "category": "Core Features",
                "content": """
Gallery Mode is an interactive demonstration platform for python-plexapi.

Features:
- 15 categories covering all API features
- 35+ interactive demos with live results
- Code examples for each demo
- Safe write operations with built-in undo
- Parameter inputs for customization

Navigation:
- Press 'g' to switch to Gallery
- Use arrow keys to navigate categories
- Press Enter to run selected demo
- Press 'u' to undo write operations
""",
            },
            {
                "id": "keyboard-shortcuts",
                "title": "Keyboard Shortcuts",
                "category": "Reference",
                "content": """
Complete keyboard shortcuts reference:

Global:
- 'd' - Switch to Dashboard
- 'g' - Switch to Gallery  
- 'h' or 'F1' - Show Help
- ':' - Open command prompt
- 'q' - Quit application
- 'Ctrl+C' - Copy results/output

Dashboard:
- 'r' - Refresh servers
- 'c' - Connect to server
- 'e' - Edit configuration

Gallery:
- Enter - Run selected demo
- 'u' - Undo last write operation
- '/' - Search demos
- Escape - Clear search/close dialogs
""",
            },
            {
                "id": "configuration",
                "title": "Configuration",
                "category": "Setup",
                "content": """
PlexiGlass uses a YAML configuration file for server settings.

Default location: ~/.config/plexiglass/servers.yaml

Example configuration:
```yaml
servers:
  - name: "Home Server"
    url: "http://192.168.1.100:32400"
    token: "your-plex-token"
    default: true
    
  - name: "Remote Server"
    url: "https://plex.example.com"
    token: "your-remote-token"
```

Getting Your Plex Token:
1. Visit https://www.plex.tv/claim
2. Sign in to your Plex account
3. Copy the X-Plex-Token from your account settings
""",
            },
            {
                "id": "error-handling",
                "title": "Error Handling",
                "category": "Features",
                "content": """
PlexiGlass provides robust error handling:

Features:
- User-friendly error messages
- Automatic retry for transient failures
- Error severity indicators (Critical, Warning, Info)
- Toast notifications for minor errors
- Modal dialogs for critical errors
- Error history tracking

Error Types:
- Connection Errors: Server unreachable, network issues
- Configuration Errors: Invalid settings, missing files
- Service Errors: API failures, timeout errors
""",
            },
            {
                "id": "undo-system",
                "title": "Undo System",
                "category": "Features",
                "content": """
Safe testing with built-in undo for write operations.

How it works:
1. Before any write operation, state is captured
2. Operation executes
3. Press 'u' to undo and restore previous state

Supported Operations:
- Metadata updates
- Collection changes
- Playlist modifications
- User permission changes

Note: Undo stack maintains last 50 operations.
""",
            },
        ]

    def _initialize_shortcuts(self) -> list[dict]:
        """Initialize keyboard shortcuts."""
        return [
            {"key": "d", "description": "Switch to Dashboard", "category": "Navigation"},
            {"key": "g", "description": "Switch to Gallery", "category": "Navigation"},
            {"key": "h", "description": "Show Help", "category": "Navigation"},
            {"key": "F1", "description": "Show Help", "category": "Navigation"},
            {"key": ":", "description": "Open Command Prompt", "category": "Navigation"},
            {"key": "q", "description": "Quit Application", "category": "Application"},
            {"key": "Ctrl+C", "description": "Copy Output", "category": "Application"},
            {"key": "r", "description": "Refresh (Dashboard)", "category": "Dashboard"},
            {"key": "c", "description": "Connect to Server", "category": "Dashboard"},
            {"key": "e", "description": "Edit Configuration", "category": "Dashboard"},
            {"key": "Enter", "description": "Run Demo (Gallery)", "category": "Gallery"},
            {"key": "u", "description": "Undo Operation", "category": "Gallery"},
            {"key": "/", "description": "Search Demos", "category": "Gallery"},
            {"key": "Escape", "description": "Close Dialog/Clear Search", "category": "General"},
            {"key": "Tab", "description": "Next Widget", "category": "General"},
            {"key": "Shift+Tab", "description": "Previous Widget", "category": "General"},
        ]

    def get_all_topics(self) -> list[dict]:
        """
        Get all help topics.

        Returns:
            List of all help topics
        """
        return self._topics

    def get_topic(self, topic_id: str) -> Optional[dict]:
        """
        Get specific topic by ID.

        Args:
            topic_id: Topic identifier

        Returns:
            Topic dict or None if not found
        """
        for topic in self._topics:
            if topic["id"] == topic_id:
                return topic
        return None

    def search(self, query: str) -> list[dict]:
        """
        Search help content.

        Args:
            query: Search query (case-insensitive)

        Returns:
            List of matching topics
        """
        if not query:
            return self._topics

        query_lower = query.lower()
        results = []

        for topic in self._topics:
            # Search in title, category, and content
            if (
                query_lower in topic["title"].lower()
                or query_lower in topic["category"].lower()
                or query_lower in topic["content"].lower()
            ):
                results.append(topic)

        return results

    def get_keyboard_shortcuts(self) -> list[dict]:
        """
        Get keyboard shortcuts reference.

        Returns:
            List of keyboard shortcuts
        """
        return self._shortcuts

    def get_context_help(self, context: str) -> Optional[dict]:
        """
        Get context-sensitive help.

        Args:
            context: Context identifier (dashboard, gallery, etc.)

        Returns:
            Relevant help topic or None
        """
        return self.get_topic(context)
