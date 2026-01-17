"""
Custom exceptions for configuration handling.
"""


class ConfigurationError(Exception):
    """
    Raised when there is an error in the configuration file or its processing.

    This includes:
    - Invalid YAML syntax
    - Missing required fields
    - Invalid environment variable references
    - Empty servers list
    - Other configuration validation errors
    """

    pass
