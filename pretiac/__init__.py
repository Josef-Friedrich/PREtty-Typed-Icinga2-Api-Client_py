# Copyright 2017 fmnisme@gmail.com christian@jonak.org
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# @author: Christian Jonak-Moechel, fmnisme, Tobias von der Krone
# @contact: christian@jonak.org, fmnisme@gmail.com, tobias@vonderkrone.info
# @summary: Python library for the Icinga 2 RESTful API

"""
pretiac is a `Python <http://www.python.org>`_ module to interact with the
`Icinga 2 RESTful API <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/>`_.
"""

import socket
from collections.abc import Sequence
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, TypeAdapter

from pretiac.config import ObjectConfig
from pretiac.log import logger
from pretiac.object_types import ApiUser, Service, ServiceState, TimePeriod, User
from pretiac.raw_client import RawClient
from pretiac.request_handler import Payload, State
from pretiac.status import StatusMessage

__client: Optional[RawClient] = None


def get_client(
    domain: Optional[str] = None,
    port: Optional[int] = None,
    api_user: Optional[str] = None,
    password: Optional[str] = None,
    certificate: Optional[str] = None,
    key: Optional[str] = None,
    ca_certificate: Optional[str] = None,
    config_file: Optional[str | Path] = None,
) -> RawClient:
    global __client
    if not __client:
        __client = RawClient(
            api_endpoint_host=domain,
            api_endpoint_port=port,
            http_basic_username=api_user,
            http_basic_password=password,
            client_certificate=certificate,
            client_private_key=key,
            ca_certificate=ca_certificate,
            config_file=config_file,
        )
    return __client


def _normalize_object_config(
    templates: Optional[Sequence[str] | str] = None,
    attrs: Optional[Payload] = None,
    object_config: Optional[ObjectConfig] = None,
) -> ObjectConfig:
    """
    :param templates: Import existing configuration templates for this
        object type. Note: These templates must either be statically
        configured or provided in config packages.
    :param attrs: Set specific object attributes for this object type.
    :param object_config: Bundle of all configurations required to create an object.
    """
    if attrs is None and object_config is not None and object_config.attrs is not None:
        attrs = object_config.attrs

    if (
        templates is None
        and object_config is not None
        and object_config.templates is not None
    ):
        templates = object_config.templates

    if isinstance(templates, str):
        templates = [templates]

    return ObjectConfig(attrs=attrs, templates=templates)


def create_host(
    name: str,
    templates: Optional[Sequence[str]] = None,
    attrs: Optional[Payload] = None,
    object_config: Optional[ObjectConfig] = None,
    suppress_exception: Optional[bool] = None,
) -> None:
    """
    Create a new host. If no host configuration is specified, the template
    ``generic-host`` is assigned.

    :param name: The name of the host.
    :param templates: Import existing configuration templates for this
        object type. Note: These templates must either be statically
        configured or provided in config packages.
    :param attrs: Set specific object attributes for this object type.
    :param object_config: Bundle of all configurations required to create a host.
    :param suppress_exception: If this parameter is set to ``True``, no exceptions are thrown.
    """
    client = get_client()
    config = _normalize_object_config(
        templates=templates, attrs=attrs, object_config=object_config
    )

    if config.attrs is None and config.templates is None:
        config.templates = ["generic-host"]

    logger.info("Create host %s", name)

    client.objects.create(
        "Host",
        name,
        templates=config.templates,
        attrs=config.attrs,
        suppress_exception=suppress_exception,
    )


def create_service(
    name: str,
    host: str,
    templates: Optional[Sequence[str]] = None,
    attrs: Optional[Payload] = None,
    object_config: Optional[ObjectConfig] = None,
    suppress_exception: Optional[bool] = None,
) -> None:
    """
    Create a new service. If no service configuration is specified, the dummy check
    command is assigned.

    :param name: The name of the service.
    :param host: The name of the host.
    :param templates: Import existing configuration templates for this
        object type. Note: These templates must either be statically
        configured or provided in config packages.
    :param attrs: Set specific object attributes for this object type.
    :param object_config: Bundle of all configurations required to create a service.
    :param suppress_exception: If this parameter is set to ``True``, no exceptions are thrown.
    """
    client = get_client()
    config = _normalize_object_config(
        templates=templates, attrs=attrs, object_config=object_config
    )

    if config.attrs is None and config.templates is None:
        config.attrs = {"check_command": "dummy"}

    logger.info("Create service %s", name)

    client.objects.create(
        "Service",
        f"{host}!{name}",
        templates=config.templates,
        attrs=config.attrs,
        suppress_exception=suppress_exception,
    )


class CheckResult(BaseModel):
    code: int
    status: str


class CheckError(BaseModel):
    error: int
    status: str


def _get_host(host: Optional[str] = None) -> str:
    if host is None:
        host = socket.gethostname()
    return host


def send_service_check_result(
    service: str,
    host: Optional[str] = None,
    exit_status: Optional[State] = ServiceState.OK,
    plugin_output: Optional[str] = None,
    performance_data: Optional[Sequence[str] | str] = None,
    check_command: Optional[Sequence[str] | str] = None,
    check_source: Optional[str] = None,
    execution_start: Optional[float] = None,
    execution_end: Optional[float] = None,
    ttl: Optional[int] = None,
    create: bool = True,
) -> CheckResult | CheckError:
    """
    Send a check result for a service and create the host or the service if necessary.

    :param service: The name of the service.
    :param host: The name of the host.
    :param exit_status: For services: ``0=OK``, ``1=WARNING``, ``2=CRITICAL``,
        ``3=UNKNOWN``, for hosts: ``0=UP``, ``1=DOWN``.
    :param plugin_output: One or more lines of the plugin main output. Does **not**
        contain the performance data.
    :param performance_data: The performance data.
    :param check_command: The first entry should be the check commands path, then
        one entry for each command line option followed by an entry for each of its
        argument. Alternativly a single string can be used.
    :param check_source: Usually the name of the ``command_endpoint``.
    :param execution_start: The timestamp where a script/process started its
        execution.
    :param execution_end: The timestamp where a script/process ended its execution.
        This timestamp is used in features to determine e.g. the metric timestamp.
    :param ttl: Time-to-live duration in seconds for this check result. The next
        expected check result is ``now + ttl`` where freshness checks are executed.
    :param create: Whether non-existent services and hosts should be created.
    """
    client = get_client()
    config = client.config
    host = _get_host(host)

    if exit_status is None:
        exit_status = ServiceState.OK

    if plugin_output is None:
        plugin_output = f"{service}: {exit_status}"

    def _send_service_check_result() -> CheckResult | CheckError:
        name = f"{host}!{service}"
        logger.info(
            "Send service check result: %s exit_status: %s plugin_output: %s",
            name,
            exit_status,
            plugin_output,
        )
        result = client.actions.process_check_result(
            type="Service",
            name=f"{host}!{service}",
            exit_status=exit_status,
            plugin_output=plugin_output,
            performance_data=performance_data,
            check_command=check_command,
            check_source=check_source,
            execution_start=execution_start,
            execution_end=execution_end,
            ttl=ttl,
            suppress_exception=True,
        )
        if "results" in result and len(result["results"]) > 0:
            return CheckResult(**result["results"][0])
        return CheckError(**result)

    result: CheckResult | CheckError = _send_service_check_result()

    if isinstance(result, CheckResult):
        return result

    if not create:
        return result

    create_host(
        name=host, object_config=config.new_host_defaults, suppress_exception=True
    )
    create_service(
        name=service,
        host=host,
        object_config=config.new_host_defaults,
        suppress_exception=True,
    )

    return _send_service_check_result()


def _convert_object(result: Any, type: Any) -> Any:
    adapter = TypeAdapter(type)
    attrs = result["attrs"]
    if "__name" in attrs:
        attrs["name"] = attrs["__name"]
        del attrs["__name"]
    return adapter.validate_python(attrs)


def _get_objects(type: Any) -> Sequence[Any]:
    client = get_client()
    results = client.objects.list(type.__name__)
    objects: list[type] = []
    for result in results:
        objects.append(_convert_object(result, type))
    return objects


def _get_object(type: Any, name: str) -> Any:
    client = get_client()
    return _convert_object(client.objects.get(type.__name__, name), type)


def get_services() -> Sequence[Service]:
    return _get_objects(Service)


def get_time_periods() -> Sequence[TimePeriod]:
    return _get_objects(TimePeriod)


def get_users() -> Sequence[User]:
    return _get_objects(User)


def get_api_user(name: str) -> ApiUser:
    return _get_object(ApiUser, name)


def get_api_users() -> Sequence[ApiUser]:
    return _get_objects(ApiUser)


def get_status() -> Sequence[StatusMessage]:
    client = get_client()
    result = client.status.list()
    adapter = TypeAdapter(list[StatusMessage], config={"arbitrary_types_allowed": True})
    return adapter.validate_python(result["results"])
