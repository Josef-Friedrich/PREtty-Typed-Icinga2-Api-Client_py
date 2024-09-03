from pathlib import Path

from pretiac.config import ObjectConfig, load_config_file


def test_load_config(config_file: Path) -> None:
    config = load_config_file(config_file)
    assert config.api_endpoint_host == "localhost"
    assert config.api_endpoint_port == 5665
    assert config.http_basic_username == "apiuser"
    assert config.http_basic_password == "password"
    assert "resources/config.yml" in str(config.config_file)


def test_class_object_config() -> None:
    config = ObjectConfig(templates=["Template"], attrs={"key": "value"})
    assert config.attrs
    assert config.attrs["key"] == "value"

    assert config.templates
    assert config.templates == ["Template"]
