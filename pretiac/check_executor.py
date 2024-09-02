"""
Execute checks using subprocess and send it via the API to the monitoring server.
"""

import shlex
import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Union

import yaml
from pydantic import TypeAdapter

from pretiac import send_service_check_result
from pretiac.log import logger
from pretiac.object_types import ServiceState, get_service_state


class SubprocessCheck:
    check_command: Sequence[str]

    exit_status: ServiceState

    plugin_output: str

    performance_data: Optional[str]

    def __init__(self, check_command: Union[Sequence[str], str]) -> None:
        if isinstance(check_command, str):
            check_command = shlex.split(check_command)
        self.check_command = check_command
        try:
            process = subprocess.run(
                self.check_command, capture_output=True, encoding="utf-8"
            )
            self.exit_status = get_service_state(process.returncode)
            self.plugin_output = process.stdout.strip()
        except Exception as e:
            self.exit_status = ServiceState.CRITICAL
            self.plugin_output = f"{e.__class__.__name__}: {e.args}"


@dataclass
class ServiceCheck:
    service: str
    check_command: str
    host: Optional[str] = None

    def check(self):
        process = subprocess.run(
            self.check_command, capture_output=True, encoding="utf-8"
        )

        send_service_check_result(
            service=self.service, host=self.host, exit_status=process.returncode
        )


@dataclass
class CheckCollection:
    checks: Sequence[ServiceCheck]
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


def check(file_path: str | Path | None) -> None:
    logger.info("Read check collection file: %s", file_path)
    if file_path is None:
        file_path = "/etc/pretiac/checks.yml"
    collection: CheckCollection = _read_check_collection(file_path)

    for check in collection.checks:
        check.check()
