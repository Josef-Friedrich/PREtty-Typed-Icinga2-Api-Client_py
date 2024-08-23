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

from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from pretiac.base import State
from pretiac.client import Client

__client: Optional[Client] = None


def get_client(
    domain: Optional[str] = None,
    port: Optional[int] = None,
    api_user: Optional[str] = None,
    password: Optional[str] = None,
    certificate: Optional[str] = None,
    key: Optional[str] = None,
    ca_certificate: Optional[str] = None,
    config_file: Optional[str | Path] = None,
) -> Client:
    global __client
    if not __client:
        __client = Client(
            domain=domain,
            port=port,
            api_user=api_user,
            password=password,
            certificate=certificate,
            key=key,
            ca_certificate=ca_certificate,
            config_file=config_file,
        )
    return __client


class CheckResult(BaseModel):
    code: int
    status: str


class CheckError(BaseModel):
    error: int
    status: str


def send_service_check_result(
    host: str,
    service: str,
    exit_status: State,
    plugin_output: str,
    performance_data: Optional[list[str] | str] = None,
    check_command: Optional[list[str] | str] = None,
    check_source: Optional[str] = None,
    execution_start: Optional[int] = None,
    execution_end: Optional[int] = None,
    ttl: Optional[int] = None,
    suppress_exception: Optional[bool] = None,
) -> CheckResult | CheckError:
    """
    Send a check result for a service.

    :param host: The name of the host.
    :param service: The name of the service.
    :param exit_status: For services: ``0=OK``, ``1=WARNING``, ``2=CRITICAL``,
        ``3=UNKNOWN``, for hosts: ``0=UP``, ``1=DOWN``.
    :param plugin_output: One or more lines of the plugin main output. Does **not**
        contain the performance data.
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
    :param suppress_exception: If this parameter is set to ``True``, no exceptions
        are thrown.

    """
    client = get_client()
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
        suppress_exception=suppress_exception,
    )

    if "results" in result and len(result["results"]) > 0:
        return CheckResult(**result["results"][0])

    return CheckError(**result)


def send_service_check_result_safe(
    host: str, service: str, exit_status: State, plugin_output: str
):
    client = get_client()
    config = client.config

    result = client.actions.process_check_result(
        type="Service",
        name=f"{host}!{service}",
        exit_status=exit_status,
        plugin_output=plugin_output,
        suppress_exception=True,
    )

    if "error" in result:
        if config.service_defaults is not None:
            client.objects.create(
                "Service",
                service,
                templates=config.service_defaults.templates,
                attrs=config.service_defaults.attrs,
                suppress_exception=True,
            )

        if config.host_defaults is not None:
            client.objects.create(
                "Host",
                host,
                templates=config.host_defaults.templates,
                attrs=config.host_defaults.attrs,
                suppress_exception=True,
            )

        client.objects.create("Host", host, suppress_exception=True)
