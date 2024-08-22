from pathlib import Path

from pretiac.config import load_config


def test_load_config(config_file: Path) -> None:
    config = load_config(config_file)
    assert config.domain == "localhost"
    assert config.port == 5665
    assert config.api_user == "apiuser"
    assert config.password == "password"
