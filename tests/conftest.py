from __future__ import annotations

import os
from pathlib import Path

import pytest

from pretiac.client import Client
from pretiac.raw_client import RawClient


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
def raw_client() -> RawClient:
    return RawClient(
        api_endpoint_host="localhost",
        api_endpoint_port=5665,
        http_basic_username="apiuser",
        http_basic_password="password",
    )


@pytest.fixture
def client(raw_client: RawClient) -> Client:
    return Client(raw_client)
