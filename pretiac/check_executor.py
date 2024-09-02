"""
Execute checks using subprocess and send it via the API to the monitoring server.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import yaml
from pydantic import TypeAdapter


@dataclass
class Check:
    service: str
    check_command: str
    host: Optional[str] = None

    def check(self):
        pass


@dataclass
class CheckCollection:
    checks: Sequence[Check]
    host: Optional[str] = None


def _read_yaml(file_path: str | Path) -> Any:
    if isinstance(file_path, str):
        file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} does not exist.")
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data


def _read_check_collection(file_path: str | Path) -> CheckCollection:
    adapter = TypeAdapter(CheckCollection)
    return adapter.validate_python(_read_yaml(file_path))


def check(file_path: str | Path) -> None:
    collection: CheckCollection = _read_check_collection(file_path)

    for check in collection.checks:
        check.check()
