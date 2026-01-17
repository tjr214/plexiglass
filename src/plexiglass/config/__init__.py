"""
Configuration module for PlexiGlass.

This module handles loading and parsing YAML configuration files,
environment variable substitution, and server configuration management.
"""

from plexiglass.config.exceptions import ConfigurationError
from plexiglass.config.loader import ConfigLoader

__all__ = ["ConfigLoader", "ConfigurationError"]
