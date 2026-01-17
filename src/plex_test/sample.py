"""Sample module demonstrating TDD structure."""


def hello_plex(name: str = "Plex") -> str:
    """
    Return a greeting for Plex.

    Args:
        name: Name to greet (default: "Plex")

    Returns:
        A greeting string
    """
    return f"Hello, {name}!"
