"""
Execute checks using subprocess and send it via the API to the monitoring server.
"""

import shlex
import subprocess
import time
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Union

import yaml
from pydantic import TypeAdapter

from pretiac import set_default_client
from pretiac.client import CheckError, CheckResult
from pretiac.log import logger
from pretiac.object_types import ServiceState, get_service_state


class CheckExecution:
    check_command: Sequence[str]

    execution_start: float

    execution_end: float

    exit_status: ServiceState

    plugin_output: str

    performance_data: Optional[str] = None

    def __init__(self, check_command: Union[Sequence[str], str]) -> None:
        if isinstance(check_command, str):
            check_command = shlex.split(check_command)
        self.check_command = check_command
        try:
            self.execution_start = time.time()
            self.execution_end = self.execution_start
            process = subprocess.run(
                self.check_command, capture_output=True, encoding="utf-8"
            )
            self.execution_end = time.time()
            self.exit_status = get_service_state(process.returncode)
            output = process.stdout.strip()
            segments = output.split("|")
            self.plugin_output = segments[0].strip()
            if len(segments) > 1:
                self.performance_data = segments[1].strip()

            logger.debug(
                "CheckExecution: check_command: %s", " ".join(self.check_command)
            )
        except Exception as e:
            self.exit_status = ServiceState.CRITICAL
            self.plugin_output = f"{e.__class__.__name__}: {e.args}"


@dataclass
class ServiceCheck:
    service: str
    """The name of the service."""

    check_command: str

    host: Optional[str] = None
    """The name of the host."""

    display_name: Optional[str] = None
    """A short description of the service, if it needs to be created."""

    def check(self) -> CheckResult | CheckError:
        """Check and send the check result to the monitoring endpoint using the API."""
        check = CheckExecution(self.check_command)
        return set_default_client().send_service_check_result(
            service=self.service,
            host=self.host,
            exit_status=check.exit_status,
            execution_start=check.execution_start,
            execution_end=check.execution_end,
            check_command=check.check_command,
            plugin_output=check.plugin_output,
            performance_data=check.performance_data,
            display_name=self.display_name,
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
