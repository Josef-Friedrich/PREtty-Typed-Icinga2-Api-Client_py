from __future__ import annotations

import os
from pathlib import Path

import pytest

from pretiac.client import Client
from pretiac.config import Config, load_config
from pretiac.raw_client import RawClient

pytest_plugins = [
    "pytester",
]


def get_resources_path(relpath: str | Path) -> Path:
    """
    :param relpath: Path relative to ``resources``.
    """
    return (Path(__file__).parent / ".." / "resources" / relpath).resolve()


config_file_path: Path = get_resources_path("config.yml")


def set_env_var() -> None:
    os.environ["PRETIAC_CONFIG_FILE"] = str(config_file_path)


set_env_var()


@pytest.fixture
def config_file() -> Path:
    return config_file_path


@pytest.fixture
def config() -> Config:
    return load_config(
        api_endpoint_host="localhost",
        api_endpoint_port=5665,
        http_basic_username="apiuser",
        http_basic_password="password",
    )


@pytest.fixture
def raw_client(config: Config) -> RawClient:
    return RawClient(config)


@pytest.fixture
def client(raw_client: RawClient) -> Client:
    return Client(
        api_endpoint_host="localhost",
        api_endpoint_port=5665,
        http_basic_username="apiuser",
        http_basic_password="password",
    )
