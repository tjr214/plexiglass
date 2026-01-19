"""
Base demo class for PlexiGlass gallery demos.

All gallery demos inherit from BaseDemo and implement the execute() method.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class BaseDemo(ABC):
    """
    Base class for all PlexiGlass gallery demonstrations.

    Each demo must define:
    - name: Display name of the demo
    - description: Short description of what the demo does
    - category: Category name (e.g., "Server & Connection")
    - operation_type: "READ" or "WRITE"

    Each demo must implement:
    - execute(server, params): Execute the demo and return results
    """

    # Required class attributes (must be defined by subclasses)
    name: str
    description: str
    category: str
    operation_type: str

    @abstractmethod
    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        """
        Execute the demo operation.

        Args:
            server: PlexServer instance (or None for offline demos)
            params: Parameters for the demo

        Returns:
            Dictionary containing demo results
        """

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        """
        Get the code example for this demo.

        Args:
            params: Optional parameters to customize the example

        Returns:
            Python code string showing how to use this feature
        """
        return "# Override get_code_example() to provide code snippet"

    def get_parameters(self) -> list[dict[str, Any]]:
        """
        Get the list of parameters this demo accepts.

        Returns:
            List of parameter definitions, each with:
            - name: Parameter name
            - type: Parameter type (str, int, bool, etc.)
            - required: Whether the parameter is required
            - default: Default value (optional)
            - description: Parameter description (optional)
        """
        return []

    def get_metadata(self) -> dict[str, Any]:
        """
        Get consolidated metadata for this demo.

        Returns:
            Dictionary with name, description, category, and operation_type
        """
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "operation_type": self.operation_type,
        }

    def validate_params(self, params: dict[str, Any]) -> tuple[bool, str | None]:
        """
        Validate that required parameters are provided.

        Args:
            params: Parameters to validate

        Returns:
            Tuple of (is_valid, error_message)
            - is_valid: True if valid, False otherwise
            - error_message: None if valid, error string otherwise
        """
        param_defs = self.get_parameters()
        for param_def in param_defs:
            if param_def.get("required", False):
                param_name = param_def["name"]
                if param_name not in params:
                    return False, f"Required parameter '{param_name}' is missing"
        return True, None
