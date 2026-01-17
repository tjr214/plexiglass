"""
Tests for Configuration Loader (TDD Red Phase)

This module tests the YAML configuration loading system including:
- Loading server configurations from YAML files
- Parsing environment variable references (${VAR_NAME})
- Validation of required fields
- Default server selection
- Settings parsing
"""

import os
from pathlib import Path
from typing import Any

import pytest


class TestConfigLoader:
    """Test suite for the ConfigLoader class."""

    def test_load_valid_config_file(self, tmp_path: Path, sample_config_yaml: str) -> None:
        """
        RED TEST: Should load a valid YAML configuration file.

        Expected behavior:
        - Parse YAML file successfully
        - Return configuration dictionary
        - No exceptions raised
        """
        # Arrange
        config_file = tmp_path / "servers.yaml"
        config_file.write_text(sample_config_yaml)

        # Act & Assert - Import will fail (module doesn't exist yet)
        from plexiglass.config.loader import ConfigLoader

        loader = ConfigLoader(config_file)
        config = loader.load()

        assert config is not None
        assert "servers" in config
        assert len(config["servers"]) > 0

    def test_environment_variable_substitution(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """
        RED TEST: Should substitute environment variables in token fields.

        Expected behavior:
        - Replace ${VAR_NAME} with os.environ['VAR_NAME']
        - Handle multiple environment variables
        - Leave non-env values unchanged
        """
        # Arrange
        monkeypatch.setenv("PLEX_TOKEN_TEST", "test-token-12345")

        config_content = """
servers:
  - name: "Test Server"
    url: "http://localhost:32400"
    token: "${PLEX_TOKEN_TEST}"
    default: true
"""
        config_file = tmp_path / "servers.yaml"
        config_file.write_text(config_content)

        # Act
        from plexiglass.config.loader import ConfigLoader

        loader = ConfigLoader(config_file)
        config = loader.load()

        # Assert
        assert config["servers"][0]["token"] == "test-token-12345"

    def test_missing_environment_variable_raises_error(self, tmp_path: Path) -> None:
        """
        RED TEST: Should raise error when referenced env var doesn't exist.

        Expected behavior:
        - Detect ${VAR_NAME} pattern
        - Check if VAR_NAME exists in os.environ
        - Raise ConfigurationError with helpful message
        """
        # Arrange
        config_content = """
servers:
  - name: "Test Server"
    url: "http://localhost:32400"
    token: "${NONEXISTENT_TOKEN}"
    default: true
"""
        config_file = tmp_path / "servers.yaml"
        config_file.write_text(config_content)

        # Act & Assert
        from plexiglass.config.loader import ConfigLoader
        from plexiglass.config.exceptions import ConfigurationError

        loader = ConfigLoader(config_file)
        with pytest.raises(ConfigurationError, match="NONEXISTENT_TOKEN"):
            loader.load()

    def test_missing_config_file_raises_error(self, tmp_path: Path) -> None:
        """
        RED TEST: Should raise error when config file doesn't exist.

        Expected behavior:
        - Check file existence before loading
        - Raise FileNotFoundError with helpful message
        """
        # Arrange
        nonexistent_file = tmp_path / "nonexistent.yaml"

        # Act & Assert
        from plexiglass.config.loader import ConfigLoader

        with pytest.raises(FileNotFoundError):
            loader = ConfigLoader(nonexistent_file)
            loader.load()

    def test_invalid_yaml_syntax_raises_error(self, tmp_path: Path) -> None:
        """
        RED TEST: Should raise error for invalid YAML syntax.

        Expected behavior:
        - Attempt to parse YAML
        - Catch YAML parsing errors
        - Raise ConfigurationError with helpful message
        """
        # Arrange
        config_file = tmp_path / "bad.yaml"
        config_file.write_text("servers:\n  - name: 'unclosed string\n    url: test")

        # Act & Assert
        from plexiglass.config.loader import ConfigLoader
        from plexiglass.config.exceptions import ConfigurationError

        loader = ConfigLoader(config_file)
        with pytest.raises(ConfigurationError, match="YAML"):
            loader.load()

    def test_validate_required_server_fields(self, tmp_path: Path) -> None:
        """
        RED TEST: Should validate that servers have required fields.

        Required fields: name, url, token

        Expected behavior:
        - Check each server entry for required fields
        - Raise ConfigurationError if any required field is missing
        """
        # Arrange - missing 'token' field
        config_content = """
servers:
  - name: "Test Server"
    url: "http://localhost:32400"
    default: true
"""
        config_file = tmp_path / "servers.yaml"
        config_file.write_text(config_content)

        # Act & Assert
        from plexiglass.config.loader import ConfigLoader
        from plexiglass.config.exceptions import ConfigurationError

        loader = ConfigLoader(config_file)
        with pytest.raises(ConfigurationError, match="token"):
            loader.load()

    def test_default_server_selection(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """
        RED TEST: Should identify the default server correctly.

        Expected behavior:
        - Find server with default: true
        - If multiple defaults, use first one
        - If no defaults, use first server
        """
        # Arrange
        monkeypatch.setenv("TOKEN1", "token1")
        monkeypatch.setenv("TOKEN2", "token2")

        config_content = """
servers:
  - name: "Server 1"
    url: "http://localhost:32400"
    token: "${TOKEN1}"
    default: false
  - name: "Server 2"
    url: "http://localhost:32401"
    token: "${TOKEN2}"
    default: true
"""
        config_file = tmp_path / "servers.yaml"
        config_file.write_text(config_content)

        # Act
        from plexiglass.config.loader import ConfigLoader

        loader = ConfigLoader(config_file)
        config = loader.load()

        # Assert
        default_server = loader.get_default_server()
        assert default_server is not None
        assert default_server["name"] == "Server 2"

    def test_get_server_by_name(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """
        RED TEST: Should retrieve server configuration by name.

        Expected behavior:
        - Search for server by name (case-insensitive)
        - Return server config dict
        - Return None if not found
        """
        # Arrange
        monkeypatch.setenv("TOKEN1", "token1")

        config_content = """
servers:
  - name: "Home Server"
    url: "http://localhost:32400"
    token: "${TOKEN1}"
    default: true
"""
        config_file = tmp_path / "servers.yaml"
        config_file.write_text(config_content)

        # Act
        from plexiglass.config.loader import ConfigLoader

        loader = ConfigLoader(config_file)
        loader.load()

        # Assert
        server = loader.get_server_by_name("Home Server")
        assert server is not None
        assert server["url"] == "http://localhost:32400"

        # Test case-insensitive
        server2 = loader.get_server_by_name("home server")
        assert server2 is not None

        # Test not found
        server3 = loader.get_server_by_name("Nonexistent")
        assert server3 is None

    def test_load_settings_section(self, tmp_path: Path, sample_config_yaml: str) -> None:
        """
        RED TEST: Should load application settings section.

        Expected behavior:
        - Parse settings section
        - Provide defaults for missing settings
        - Return settings dictionary
        """
        # Arrange
        config_file = tmp_path / "servers.yaml"
        config_file.write_text(sample_config_yaml)

        # Act
        from plexiglass.config.loader import ConfigLoader

        loader = ConfigLoader(config_file)
        config = loader.load()

        # Assert
        assert "settings" in config
        assert "ui" in config["settings"]
        assert "gallery" in config["settings"]
        assert config["settings"]["ui"]["theme"] in ["dark", "light"]

    def test_empty_servers_list_raises_error(self, tmp_path: Path) -> None:
        """
        RED TEST: Should raise error if servers list is empty.

        Expected behavior:
        - Check that servers list has at least one entry
        - Raise ConfigurationError with helpful message
        """
        # Arrange
        config_content = """
servers: []
settings:
  ui:
    theme: dark
"""
        config_file = tmp_path / "servers.yaml"
        config_file.write_text(config_content)

        # Act & Assert
        from plexiglass.config.loader import ConfigLoader
        from plexiglass.config.exceptions import ConfigurationError

        loader = ConfigLoader(config_file)
        with pytest.raises(ConfigurationError, match="at least one server"):
            loader.load()

    def test_get_servers_returns_copy(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """
        Test that get_servers() returns a copy of the servers list.

        Expected behavior:
        - Return list of all servers
        - Return a copy (not original reference)
        """
        # Arrange
        monkeypatch.setenv("TOKEN1", "token1")

        config_content = """
servers:
  - name: "Server 1"
    url: "http://localhost:32400"
    token: "${TOKEN1}"
    default: true
"""
        config_file = tmp_path / "servers.yaml"
        config_file.write_text(config_content)

        # Act
        from plexiglass.config.loader import ConfigLoader

        loader = ConfigLoader(config_file)
        loader.load()

        servers = loader.get_servers()

        # Assert
        assert len(servers) == 1
        assert servers[0]["name"] == "Server 1"

        # Modify returned list shouldn't affect internal state
        servers.append({"name": "Fake Server"})
        assert len(loader.get_servers()) == 1

    def test_get_settings_with_no_config_loaded(self) -> None:
        """
        Test that get_settings() returns defaults when no config loaded.

        Expected behavior:
        - Return default settings
        - No errors raised
        """
        # Arrange
        from pathlib import Path
        from plexiglass.config.loader import ConfigLoader

        loader = ConfigLoader(Path("nonexistent.yaml"))

        # Act
        settings = loader.get_settings()

        # Assert
        assert "ui" in settings
        assert settings["ui"]["theme"] == "dark"
        assert "gallery" in settings
        assert "performance" in settings
        assert "logging" in settings

    def test_get_settings_merges_with_defaults(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """
        Test that custom settings are merged with defaults.

        Expected behavior:
        - Merge custom settings with defaults
        - Custom values override defaults
        - Missing keys use defaults
        """
        # Arrange
        monkeypatch.setenv("TOKEN1", "token1")

        config_content = """
servers:
  - name: "Server 1"
    url: "http://localhost:32400"
    token: "${TOKEN1}"
    default: true

settings:
  ui:
    theme: "light"
    # refresh_interval not specified - should use default
  gallery:
    max_results: 100
"""
        config_file = tmp_path / "servers.yaml"
        config_file.write_text(config_content)

        # Act
        from plexiglass.config.loader import ConfigLoader

        loader = ConfigLoader(config_file)
        loader.load()
        settings = loader.get_settings()

        # Assert
        assert settings["ui"]["theme"] == "light"  # Custom value
        assert settings["ui"]["refresh_interval"] == 5  # Default value
        assert settings["gallery"]["max_results"] == 100  # Custom value
        assert settings["gallery"]["show_code_examples"] is True  # Default value

    def test_default_server_when_none_marked_default(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """
        Test that first server is default when none marked as default.

        Expected behavior:
        - Return first server if no default: true found
        """
        # Arrange
        monkeypatch.setenv("TOKEN1", "token1")
        monkeypatch.setenv("TOKEN2", "token2")

        config_content = """
servers:
  - name: "First Server"
    url: "http://localhost:32400"
    token: "${TOKEN1}"
  - name: "Second Server"
    url: "http://localhost:32401"
    token: "${TOKEN2}"
"""
        config_file = tmp_path / "servers.yaml"
        config_file.write_text(config_content)

        # Act
        from plexiglass.config.loader import ConfigLoader

        loader = ConfigLoader(config_file)
        loader.load()
        default = loader.get_default_server()

        # Assert
        assert default is not None
        assert default["name"] == "First Server"

    def test_get_default_server_returns_none_when_no_servers(self) -> None:
        """
        Test that get_default_server() returns None when no servers loaded.

        Expected behavior:
        - Return None if servers list is empty
        """
        # Arrange
        from pathlib import Path
        from plexiglass.config.loader import ConfigLoader

        loader = ConfigLoader(Path("nonexistent.yaml"))

        # Act
        default = loader.get_default_server()

        # Assert
        assert default is None

    def test_invalid_config_not_dict_raises_error(self, tmp_path: Path) -> None:
        """
        Test that non-dict YAML raises ConfigurationError.

        Expected behavior:
        - Raise ConfigurationError if root YAML is not a dictionary
        """
        # Arrange
        config_content = """
- item1
- item2
"""
        config_file = tmp_path / "servers.yaml"
        config_file.write_text(config_content)

        # Act & Assert
        from plexiglass.config.loader import ConfigLoader
        from plexiglass.config.exceptions import ConfigurationError

        loader = ConfigLoader(config_file)
        with pytest.raises(ConfigurationError, match="must contain a YAML dictionary"):
            loader.load()

    def test_missing_servers_section_raises_error(self, tmp_path: Path) -> None:
        """
        Test that missing 'servers' section raises ConfigurationError.

        Expected behavior:
        - Raise ConfigurationError if 'servers' key is missing
        """
        # Arrange
        config_content = """
settings:
  ui:
    theme: dark
"""
        config_file = tmp_path / "servers.yaml"
        config_file.write_text(config_content)

        # Act & Assert
        from plexiglass.config.loader import ConfigLoader
        from plexiglass.config.exceptions import ConfigurationError

        loader = ConfigLoader(config_file)
        with pytest.raises(ConfigurationError, match="must contain a 'servers' section"):
            loader.load()

    def test_server_entry_not_dict_raises_error(self, tmp_path: Path) -> None:
        """
        Test that non-dict server entries raise ConfigurationError.

        Expected behavior:
        - Raise ConfigurationError if server entry is not a dictionary
        """
        # Arrange
        config_content = """
servers:
  - "not a dict"
"""
        config_file = tmp_path / "servers.yaml"
        config_file.write_text(config_content)

        # Act & Assert
        from plexiglass.config.loader import ConfigLoader
        from plexiglass.config.exceptions import ConfigurationError

        loader = ConfigLoader(config_file)
        with pytest.raises(ConfigurationError, match="must be a dictionary"):
            loader.load()

    def test_env_var_substitution_in_nested_structures(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """
        Test environment variable substitution in nested structures.

        Expected behavior:
        - Substitute variables in nested dicts and lists
        """
        # Arrange
        monkeypatch.setenv("TEST_TOKEN", "my-secret-token")
        monkeypatch.setenv("TEST_TAG", "testing")

        config_content = """
servers:
  - name: "Test Server"
    url: "http://localhost:32400"
    token: "${TEST_TOKEN}"
    default: true
    tags: ["${TEST_TAG}", "development"]
"""
        config_file = tmp_path / "servers.yaml"
        config_file.write_text(config_content)

        # Act
        from plexiglass.config.loader import ConfigLoader

        loader = ConfigLoader(config_file)
        config = loader.load()

        # Assert
        assert config["servers"][0]["token"] == "my-secret-token"
        assert config["servers"][0]["tags"][0] == "testing"
        assert config["servers"][0]["tags"][1] == "development"


# Fixtures


@pytest.fixture
def sample_config_yaml(monkeypatch: pytest.MonkeyPatch) -> str:
    """Provide a valid sample configuration for testing."""
    monkeypatch.setenv("PLEX_TOKEN_HOME", "home-token-12345")
    monkeypatch.setenv("PLEX_TOKEN_TEST", "test-token-67890")

    return """
servers:
  - name: "Home Server"
    description: "Main home Plex server"
    url: "http://192.168.1.100:32400"
    token: "${PLEX_TOKEN_HOME}"
    default: true
    read_only: false
    tags: ["production", "home"]
    
  - name: "Test Server"
    description: "Development and testing server"
    url: "http://localhost:32400"
    token: "${PLEX_TOKEN_TEST}"
    default: false
    read_only: false
    tags: ["development", "testing"]

settings:
  ui:
    theme: "dark"
    refresh_interval: 5
    animations: true
    
  gallery:
    show_code_examples: true
    enable_write_operations: true
    confirm_before_write: true
    max_results: 50
    
  performance:
    cache_ttl: 60
    max_undo_stack: 50
    connection_timeout: 30
    max_concurrent_requests: 5
    
  logging:
    level: "INFO"
    file: "plexiglass.log"
    max_size_mb: 10
    backup_count: 3
"""
