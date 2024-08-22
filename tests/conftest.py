from __future__ import annotations

import os
from pathlib import Path

import pytest

from pretiac.client import Client

config_file_path: Path = (
    Path(__file__).parent / ".." / "resources" / "icinga-api-client.json"
).resolve()

os.environ["ICINGA_API_CLIENT"] = str(config_file_path)


@pytest.fixture
def config_file() -> Path:
    return config_file_path


@pytest.fixture
def client() -> Client:
    return Client(
        domain="localhost", port=5665, api_user="apiuser", password="password"
    )
