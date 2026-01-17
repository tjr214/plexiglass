"""
Configuration loader for PlexiGlass.

This module provides the ConfigLoader class which:
- Loads YAML configuration files
- Substitutes environment variables
- Validates configuration structure
- Provides access to server and settings configurations
"""

import os
import re
from pathlib import Path
from typing import Any

import yaml

from plexiglass.config.exceptions import ConfigurationError


class ConfigLoader:
    """
    Loads and manages PlexiGlass configuration from YAML files.

    Supports:
    - Environment variable substitution (${VAR_NAME})
    - Configuration validation
    - Server and settings access methods
    - Default server selection

    Example:
        >>> loader = ConfigLoader(Path("config/servers.yaml"))
        >>> config = loader.load()
        >>> default_server = loader.get_default_server()
    """

    # Pattern to match environment variable references: ${VAR_NAME}
    ENV_VAR_PATTERN = re.compile(r"\$\{([^}]+)\}")

    # Required fields for server entries
    REQUIRED_SERVER_FIELDS = {"name", "url", "token"}

    def __init__(self, config_path: Path) -> None:
        """
        Initialize the ConfigLoader with a path to the configuration file.

        Args:
            config_path: Path to the YAML configuration file
        """
        self.config_path = config_path
        self._config: dict[str, Any] | None = None
        self._servers: list[dict[str, Any]] = []

    def load(self) -> dict[str, Any]:
        """
        Load and parse the configuration file.

        Returns:
            The complete configuration dictionary

        Raises:
            FileNotFoundError: If the configuration file doesn't exist
            ConfigurationError: If the configuration is invalid
        """
        # Check file existence
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        # Load YAML content
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                raw_config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Invalid YAML syntax in configuration file: {e}") from e

        if not isinstance(raw_config, dict):
            raise ConfigurationError("Configuration file must contain a YAML dictionary")

        # Validate and process servers
        if "servers" not in raw_config:
            raise ConfigurationError("Configuration must contain a 'servers' section")

        servers = raw_config.get("servers", [])
        if not servers or not isinstance(servers, list):
            raise ConfigurationError(
                "Configuration must contain at least one server in 'servers' list"
            )

        # Process each server: validate and substitute environment variables
        self._servers = []
        for idx, server in enumerate(servers):
            if not isinstance(server, dict):
                raise ConfigurationError(f"Server entry {idx} must be a dictionary")

            # Validate required fields
            missing_fields = self.REQUIRED_SERVER_FIELDS - set(server.keys())
            if missing_fields:
                raise ConfigurationError(
                    f"Server '{server.get('name', f'entry {idx}')}' is missing required "
                    f"fields: {', '.join(missing_fields)}"
                )

            # Substitute environment variables in the entire server config
            processed_server = self._substitute_env_vars(server)
            self._servers.append(processed_server)

        # Update config with processed servers
        raw_config["servers"] = self._servers

        # Store the complete processed configuration
        self._config = raw_config

        return self._config

    def _substitute_env_vars(self, data: Any) -> Any:
        """
        Recursively substitute environment variables in configuration data.

        Replaces ${VAR_NAME} with the value of os.environ['VAR_NAME'].

        Args:
            data: Configuration data (can be dict, list, str, or other types)

        Returns:
            Data with environment variables substituted

        Raises:
            ConfigurationError: If a referenced environment variable doesn't exist
        """
        if isinstance(data, dict):
            return {key: self._substitute_env_vars(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._substitute_env_vars(item) for item in data]
        elif isinstance(data, str):
            # Find all environment variable references
            matches = self.ENV_VAR_PATTERN.findall(data)
            result = data
            for var_name in matches:
                if var_name not in os.environ:
                    raise ConfigurationError(
                        f"Environment variable '{var_name}' referenced in configuration "
                        f"but not found in environment"
                    )
                # Replace ${VAR_NAME} with actual value
                result = result.replace(f"${{{var_name}}}", os.environ[var_name])
            return result
        else:
            return data

    def get_default_server(self) -> dict[str, Any] | None:
        """
        Get the default server configuration.

        Returns the first server with default: true, or the first server if none
        are marked as default.

        Returns:
            Default server configuration dictionary, or None if no servers exist
        """
        if not self._servers:
            return None

        # Find first server with default: true
        for server in self._servers:
            if server.get("default", False):
                return server

        # If no default specified, return first server
        return self._servers[0]

    def get_server_by_name(self, name: str) -> dict[str, Any] | None:
        """
        Retrieve a server configuration by name (case-insensitive).

        Args:
            name: Server name to search for

        Returns:
            Server configuration dictionary, or None if not found
        """
        name_lower = name.lower()
        for server in self._servers:
            if server.get("name", "").lower() == name_lower:
                return server
        return None

    def get_servers(self) -> list[dict[str, Any]]:
        """
        Get all server configurations.

        Returns:
            List of all server configuration dictionaries
        """
        return self._servers.copy()

    def get_settings(self) -> dict[str, Any]:
        """
        Get application settings from configuration.

        Returns:
            Settings dictionary with defaults for missing values
        """
        if not self._config:
            return self._get_default_settings()

        settings = self._config.get("settings", {})

        # Merge with defaults
        default_settings = self._get_default_settings()
        return self._merge_settings(default_settings, settings)

    @staticmethod
    def _get_default_settings() -> dict[str, Any]:
        """
        Get default application settings.

        Returns:
            Default settings dictionary
        """
        return {
            "ui": {
                "theme": "dark",
                "refresh_interval": 5,
                "animations": True,
            },
            "gallery": {
                "show_code_examples": True,
                "enable_write_operations": True,
                "confirm_before_write": True,
                "max_results": 50,
            },
            "performance": {
                "cache_ttl": 60,
                "max_undo_stack": 50,
                "connection_timeout": 30,
                "max_concurrent_requests": 5,
            },
            "logging": {
                "level": "INFO",
                "file": "plexiglass.log",
                "max_size_mb": 10,
                "backup_count": 3,
            },
        }

    @staticmethod
    def _merge_settings(defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
        """
        Merge override settings with defaults.

        Args:
            defaults: Default settings dictionary
            overrides: Override settings from configuration

        Returns:
            Merged settings dictionary
        """
        result = defaults.copy()

        for key, value in overrides.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                # Recursively merge nested dictionaries
                result[key] = ConfigLoader._merge_settings(result[key], value)
            else:
                # Override the value
                result[key] = value

        return result
