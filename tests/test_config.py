from pathlib import Path

import pytest

from pretiac.config import ObjectConfig, load_config, load_config_file
from pretiac.exceptions import PretiacException


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


class TestLoadConfig:
    def test_without_arguments(self):
        config = load_config()
        assert config

    def test_exception_both_auth_methods(self):
        with pytest.raises(PretiacException):
            load_config(
                http_basic_password="1234", client_private_key="/tmp/private.key"
            )
