#!/usr/bin/env python3
"""
PlexiGlass - Main entry point for CLI invocation.

This module serves as the entry point for the plexiglass command-line tool.
It can be invoked in multiple ways:

1. Direct module execution:
   python -m plexiglass

2. Installed command (after uv tool install):
   plexiglass

3. Development mode:
   uv run plexiglass
"""

import sys
from pathlib import Path


def main() -> int:
    """
    Main entry point for PlexiGlass CLI.

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    try:
        # Import here to avoid circular imports and allow for lazy loading
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        # Create and run the Textual application
        app = PlexiGlassApp()
        app.run()
        return 0

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\n👋 PlexiGlass terminated by user. Goodbye!", file=sys.stderr)
        return 130  # Standard exit code for SIGINT

    except ImportError as e:
        # Handle missing dependencies
        print(f"❌ Error: Missing dependency - {e}", file=sys.stderr)
        print("\nPlease ensure PlexiGlass is properly installed:", file=sys.stderr)
        print("  uv tool install plexiglass", file=sys.stderr)
        return 1

    except Exception as e:
        # Handle unexpected errors
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        print("\nPlease report this issue with the full error message.", file=sys.stderr)
        return 1


def version() -> None:
    """Display version information."""
    from plexiglass import __version__

    print(f"PlexiGlass v{__version__}")


def check_environment() -> bool:
    """
    Check if the environment is properly configured.

    Returns:
        True if environment is valid, False otherwise
    """
    # Check for required config files
    config_paths = [
        Path.home() / ".config" / "plexiglass" / "servers.yaml",
        Path.cwd() / "config" / "servers.yaml",
    ]

    config_exists = any(path.exists() for path in config_paths)

    if not config_exists:
        print("⚠️  Warning: No server configuration found!", file=sys.stderr)
        print("\nExpected configuration at one of:", file=sys.stderr)
        for path in config_paths:
            print(f"  - {path}", file=sys.stderr)
        print("\nCopy config/servers.example.yaml to one of these locations.", file=sys.stderr)
        return False

    return True


def cli() -> int:
    """
    Command-line interface with argument parsing.

    This function will be expanded to support CLI arguments in the future.
    For now, it provides a simple version check and launches the TUI.

    Returns:
        Exit code
    """
    # Simple argument handling (will expand with proper CLI parser later)
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()

        if arg in ["-v", "--version"]:
            version()
            return 0

        elif arg in ["-h", "--help"]:
            print("PlexiGlass - Plex Media Server Dashboard & API Gallery")
            print("\nUsage:")
            print("  plexiglass           Launch the TUI application")
            print("  plexiglass --version Show version information")
            print("  plexiglass --help    Show this help message")
            print("\nDocumentation:")
            print("  https://github.com/yourusername/plexiglass")
            return 0

        elif arg in ["--check", "--check-config"]:
            if check_environment():
                print("✅ Environment configured correctly")
                return 0
            else:
                return 1

        else:
            print(f"❌ Unknown argument: {arg}", file=sys.stderr)
            print("Use --help for usage information", file=sys.stderr)
            return 1

    # No arguments provided, launch the application
    return main()


if __name__ == "__main__":
    # When run as a script or module
    sys.exit(cli())
