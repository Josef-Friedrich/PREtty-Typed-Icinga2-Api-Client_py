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
Icinga 2 API client

The Icinga 2 API allows you to manage configuration objects and resources in a simple,
programmatic way using HTTP requests.
"""

import urllib
import urllib.parse
from collections.abc import Sequence
from importlib.metadata import version as get_version
from typing import Any, Generator, Literal, Optional, Union

from pydantic.dataclasses import dataclass

from pretiac.config import Config
from pretiac.exceptions import PretiacException
from pretiac.object_types import (
    CheckResult,
    FilterVars,
    HostOrService,
    ObjectTypeName,
    Payload,
    Value,
    pluralize_to_lower_object_type_name,
)
from pretiac.request_handler import (
    RequestHandler,
    State,
    normalize_state,
)


def assemble_payload(**kwargs: Any) -> Payload:
    # https://stackoverflow.com/a/2544761
    return {k: v for k, v in kwargs.items() if v is not None}


@dataclass
class Result:
    code: int

    status: str


@dataclass
class ResultContainer:
    results: list[Result]


EventStreamType = Literal[
    "CheckResult",  # Check results for hosts and services.
    "StateChange",  # Host/service state changes.
    "Notification",  # Notification events including notified users for hosts and services.
    "AcknowledgementSet",  # Acknowledgement set on hosts and services.
    "AcknowledgementCleared",  # Acknowledgement cleared on hosts and services.
    "CommentAdded",  # Comment added for hosts and services.
    "CommentRemoved",  # Comment removed for hosts and services.
    "DowntimeAdded",  # Downtime added for hosts and services.
    "DowntimeRemoved",  # Downtime removed for hosts and services.
    "DowntimeStarted",  # Downtime started for hosts and services.
    "DowntimeTriggered",  # Downtime triggered for hosts and services.
    "ObjectCreated",  # Object created for all Icinga 2 objects.
    "ObjectDeleted",  # Object deleted for all Icinga 2 objects.
    "ObjectModified",  # Object modified for all Icinga 2 objects.
]
"""
:see: `doc/12-icinga2-api/#event-stream-types <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#event-stream-types>`__
:see: `lib/icinga/apievents.hpp L16-L47 <https://github.com/Icinga/icinga2/blob/c0b047b1aab6de3c5e51fdeb63d3bf4236f7fa6d/lib/icinga/apievents.hpp#L16-L47>`__
:see: `lib/remote/eventshandler.cpp L22-L38 <https://github.com/Icinga/icinga2/blob/c0b047b1aab6de3c5e51fdeb63d3bf4236f7fa6d/lib/remote/eventshandler.cpp#L22-L38>`__"""


def _normalize_name(name: str) -> str:
    """To be able to send names with spaces or special characters to the REST API."""
    return urllib.parse.quote(name, safe="")


class Attrs:
    """https://github.com/Icinga/icinga2/blob/master/lib/icinga/checkable.ti"""

    __name: str
    acknowledgement: int
    acknowledgement_expiry: int
    acknowledgement_last_change: int
    action_url: str
    active: bool
    check_attempt: int
    check_command: str
    check_interval: int
    check_period: str
    check_timeout: None
    command_endpoint: str
    display_name: str
    downtime_depth: int
    enable_active_checks: bool
    enable_event_handler: bool
    enable_flapping: bool
    enable_notifications: bool
    enable_passive_checks: bool
    enable_perfdata: bool
    event_command: str
    executions: None
    flapping: bool
    flapping_current: int
    flapping_ignore_states: None
    flapping_last_change: int
    flapping_threshold: int
    flapping_threshold_high: int
    flapping_threshold_low: int
    force_next_check: bool
    force_next_notification: bool
    groups: list[str]
    ha_mode: int
    handled: bool
    host_name: str
    icon_image: str
    icon_image_alt: str
    last_check: float


class Object:
    attrs: dict[str, Any]
    joins: dict[str, Any]


class Service(Object):
    """https://github.com/Icinga/icinga2/blob/master/lib/icinga/service.ti"""

    type = "Service"
    name: str
    meta: dict[str, Any]


class Host:
    name: str
    state: int
    last_check_result: CheckResult


# Order as in https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/


class ObjectsUrlEndpoint(RequestHandler):
    """
    Connects to the URL endpoint ``objects`` of the Icinga2 API.

    Provides methods to manage configuration objects:

    - creating objects
    - querying objects
    - modifying objects
    - deleting objects
    """

    path_prefix = "objects"

    def list(
        self,
        object_type: ObjectTypeName,
        name: Optional[str] = None,
        attrs: Optional[Sequence[str]] = None,
        filters: Optional[str] = None,
        filter_vars: FilterVars = None,
        joins: Optional[Union[bool, Sequence[str]]] = None,
        suppress_exception: Optional[bool] = None,
    ) -> Any:
        """
        get object by type or name

        :param object_type: The type of the object, for example ``Service``,
            ``Host`` or ``User``.
        :param name: The full object name, for example ``example.localdomain``
            or ``example.localdomain!http``.
        :param attrs: only return these attributes
        :param filters: filters matched object(s)
        :param filter_vars: variables used in the filters expression
        :param joins: show joined object
        :param suppress_exception: If this parameter is set to ``True``, no exceptions are thrown.

        Get all hosts:

        .. code-block:: python

            raw_client.objects.list("Host")

        List the service ``ping4`` of host ``webserver01.domain!ping4``:

        .. code-block:: python

            raw_client.objects.list("Service", "webserver01.domain!ping4")

        Get all hosts but limit attributes to `address` and `state`:

        .. code-block:: python

            raw_client.objects.list("Host", attrs=["address", "state"])

        Get all hosts which have ``webserver`` in their host name:

        .. code-block:: python

            raw_client.objects.list("Host", filters='match("webserver*", host.name)')

        Get all services and the joined host name:

        .. code-block:: python

            raw_client.objects.list("Service", joins=["host.name"])

        Get all services and all supported joins:

        .. code-block:: python

            raw_client.objects.list("Service", joins=True)

        Get all services which names start with ``vHost`` and are assigned to hosts named ``webserver*`` using ``filter_vars``:

        .. code-block:: python

            hostname_pattern = "webserver*"
            service_pattern = "vHost*"
            raw_client.objects.list(
                "Service",
                filters="match(hpattern, host.name) && match(spattern, service.name)",
                filter_vars={"hpattern": hostname_pattern, "spattern": service_pattern},
            )

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#querying-objects <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#querying-objects>`__
        """

        url_path = pluralize_to_lower_object_type_name(object_type)
        if url_path == "dependencys":
            url_path = "dependencies"
        if name:
            url_path += f"/{_normalize_name(name)}"

        payload: Payload = {}
        if attrs:
            payload["attrs"] = attrs
        if filters:
            payload["filter"] = filters
        if filter_vars:
            payload["filter_vars"] = filter_vars
        if isinstance(joins, bool) and joins:
            payload["all_joins"] = "1"
        elif joins:
            payload["joins"] = joins

        result = self._request(
            "GET", url_path, payload, suppress_exception=suppress_exception
        )
        if "results" in result:
            return result["results"]
        return result

    def get(
        self,
        object_type: ObjectTypeName,
        name: str,
        attrs: Optional[Sequence[str]] = None,
        joins: Optional[Union[bool, Sequence[str]]] = None,
        suppress_exception: Optional[bool] = None,
    ) -> Any:
        """
        Get a single object (``Host``, ``Service``, ...).

        :param object_type: The type of the object, for example ``Service``,
            ``Host`` or ``User``.
        :param name: The full object name, for example ``example.localdomain``
            or ``example.localdomain!http``.
        :param attrs:  Get only the specified objects attributes.
        :param joins: Also get the joined object, e.g. for a `Service` the `Host` object.

        :param suppress_exception: If this parameter is set to ``True``, no exceptions are thrown.

        Get host ``webserver01.domain``:

        .. code-block:: python

            raw_client.objects.get("Host", "webserver01.domain")

        Get service ``ping4`` of host ``webserver01.domain``:

        .. code-block:: python

            raw_client.objects.get("Service", "webserver01.domain!ping4")

        Get host ``webserver01.domain`` but the attributes ``address`` and ``state``:

        .. code-block:: python

            raw_client.objects.get("Host", "webserver01.domain", attrs=["address", "state"])

        Get service ``ping4`` of host ``webserver01.domain`` and the host attributes:

        .. code-block:: python

            raw_client.objects.get("Service", "webserver01.domain!ping4", joins=True)

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#querying-objects <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#querying-objects>`__
        """
        result = self.list(
            object_type, name, attrs, joins=joins, suppress_exception=suppress_exception
        )
        if "error" not in result:
            return result[0]

    def create(
        self,
        object_type: ObjectTypeName,
        name: str,
        templates: Optional[Sequence[str]] = None,
        attrs: Optional[Payload] = None,
        suppress_exception: Optional[bool] = None,
    ) -> Any:
        """
        Create an object using ``templates`` and specify attributes (``attrs``).

        :param object_type: The type of the object, for example ``Service``,
            ``Host`` or ``User``.
        :param name: The full object name, for example ``example.localdomain``
            or ``example.localdomain!http``.
        :param templates: Import existing configuration templates for this
            object type. Note: These templates must either be statically
            configured or provided in config packages.
        :param attrs: Set specific object attributes for this object type.
        :param suppress_exception: If this parameter is set to ``True``, no exceptions are thrown.

        Create a host:

        .. code-block:: python

            raw_client.objects.create(
                "Host", "localhost", ["generic-host"], {"address": "127.0.0.1"}
            )

        Create a service for Host ``localhost``:

        .. code-block:: python

            raw_client.objects.create(
                "Service",
                "testhost3!dummy",
                {"check_command": "dummy"},
                ["generic-service"],
            )

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#creating-config-objects <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#creating-config-objects>`__
        """

        payload: Payload = {}
        if attrs:
            payload["attrs"] = attrs
        if templates:
            payload["templates"] = templates

        return self._request(
            "PUT",
            f"{pluralize_to_lower_object_type_name(object_type)}/{_normalize_name(name)}",
            payload,
            suppress_exception=suppress_exception,
        )

    def update(
        self,
        object_type: ObjectTypeName,
        name: str,
        attrs: dict[str, Any],
        suppress_exception: Optional[bool] = None,
    ) -> Any:
        """
        Update an object with the specified attributes.

        :param object_type: The type of the object, for example ``Service``,
            ``Host`` or ``User``.
        :param name: the name of the object
        :param attrs: object's attributes to change
        :param suppress_exception: If this parameter is set to ``True``, no exceptions are thrown.

        Change the ip address of a host:

        .. code-block:: python

            raw_client.objects.update("Host", "localhost", {"address": "127.0.1.1"})

        Update a service and change the check interval:

        .. code-block:: python

            raw_client.objects.update(
                "Service", "testhost3!dummy", {"check_interval": "10m"}
            )

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#modifying-objects <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#modifying-objects>`__
        """
        return self._request(
            "POST",
            f"{pluralize_to_lower_object_type_name(object_type)}/{name}",
            attrs,
            suppress_exception=suppress_exception,
        )

    def delete(
        self,
        object_type: ObjectTypeName,
        name: Optional[str] = None,
        filters: Optional[str] = None,
        filter_vars: FilterVars = None,
        cascade: bool = True,
        suppress_exception: Optional[bool] = None,
    ) -> Any:
        """Delete an object.

        :param object_type: The type of the object, for example ``Service``,
            ``Host`` or ``User``.
        :param name: The full object name, for example ``example.localdomain``
            or ``example.localdomain!http``.
        :param filters: filters matched object(s)
        :param filter_vars: variables used in the filters expression
        :param cascade: Delete objects depending on the deleted objects (e.g. services on a host).
        :param suppress_exception: If this parameter is set to ``True``, no exceptions are thrown.

        Delete the ``localhost``:

        .. code-block:: python

            raw_client.objects.delete("Host", "localhost")

        Delete all services matching ``vhost*``:

        .. code-block:: python

            raw_client.objects.delete("Service", filters='match("vhost*", service.name)')

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#deleting-objects <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#deleting-objects>`__
        """

        object_type_url_path = pluralize_to_lower_object_type_name(object_type)

        payload: Payload = {}
        if filters:
            payload["filter"] = filters
        if filter_vars:
            payload["filter_vars"] = filter_vars
        if cascade:
            payload["cascade"] = 1

        url = object_type_url_path
        if name:
            url += f"/{_normalize_name(name)}"

        return self._request(
            "DELETE", url, payload, suppress_exception=suppress_exception
        )


StatusType = Literal[
    "ApiListener",
    "CIB",
    "CheckerComponent",
    "ElasticsearchWriter",
    "FileLogger",
    "GelfWriter",
    "GraphiteWriter",
    "IcingaApplication",
    "IdoMysqlConnection",
    "IdoPgsqlConnection",
    "Influxdb2Writer",
    "InfluxdbWriter",
    "JournaldLogger",
    "NotificationComponent",
    "OpenTsdbWriter",
    "PerfdataWriter",
    "SyslogLogger",
]


class ActionsUrlEndpoint(RequestHandler):
    """
    Connects to the URL endpoint ``actions`` of the Icinga2 API.
    """

    path_prefix = "actions"

    def process_check_result(
        self,
        type: HostOrService,
        name: str,
        exit_status: State,
        plugin_output: str,
        performance_data: Optional[Sequence[str] | str] = None,
        check_command: Optional[Sequence[str] | str] = None,
        check_source: Optional[str] = None,
        execution_start: Optional[float] = None,
        execution_end: Optional[float] = None,
        ttl: Optional[int] = None,
        filter: Optional[str] = None,
        filter_vars: FilterVars = None,
        suppress_exception: Optional[bool] = None,
    ) -> Any:
        """Process a check result for a host or a service.

        Send a ``POST`` request to the URL endpoint ``actions/process-check-result``.

        :param type: ``Host`` or ``Service``.
        :param name: The name of the object.
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
        :param filter: filters matched object(s)
        :param filter_vars: variables used in the filters expression
        :param suppress_exception: If this parameter is set to ``True``, no exceptions
            are thrown.

        :returns: the response as json

        .. code-block:: python

            raw_client.process_check_result(
                "Service",
                "myhost.domain!ping4",
                exit_status=2,
                plugin_output="PING CRITICAL - Packet loss = 100%",
                performance_data=[
                    "rta=5000.000000ms;3000.000000;5000.000000;0.000000",
                    "pl=100%;80;100;0",
                ],
                check_source="python client",
            )

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#process-check-result <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#process-check-result>`__
        """
        if not name and not filter:
            raise PretiacException("name and filters is empty or none")

        if name and (filter or filter_vars):
            raise PretiacException("name and filters are mutually exclusive")

        if type not in ["Host", "Service"]:
            raise PretiacException('type needs to be "Host" or "Service".')

        payload: Payload = {
            "type": type,
            "exit_status": normalize_state(exit_status),
            "plugin_output": plugin_output,
        }

        if name:
            payload[type.lower()] = name
        if performance_data:
            payload["performance_data"] = performance_data
        if check_command:
            payload["check_command"] = check_command
        if check_source:
            payload["check_source"] = check_source
        if execution_start:
            payload["execution_start"] = execution_start
        if execution_end:
            payload["execution_end"] = execution_end
        if ttl:
            payload["ttl"] = ttl
        if filter:
            payload["filter"] = filter
        if filter_vars:
            payload["filter_vars"] = filter_vars

        return self._request(
            "POST",
            "process-check-result",
            payload,
            suppress_exception=suppress_exception,
        )

    def reschedule_check(
        self,
        object_type: HostOrService,
        filters: str,
        filter_vars: FilterVars = None,
        next_check: Optional[int] = None,
        force_check: Optional[bool] = True,
    ) -> Any:
        """
        Reschedule a check for hosts and services.

        example 1:

        .. code-block:: python

            raw_client.reschedule_check("Service", 'service.name=="ping4"')

        example 2:

        .. code-block:: python

            raw_client.reschedule_check("Host", 'host.name=="localhost"', 1577833200)

        :param object_type: Host or Service
        :param filters: filters matched object(s)
        :param filter_vars: variables used in the for filters expression
        :param next_check: timestamp to run the check
        :param force: ignore period restrictions and disabled checks

        :returns: the response as json

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#reschedule-check <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#reschedule-check>`__
        """

        payload: Payload = {
            "type": object_type,
            "filter": filters,
            "force_check": force_check,
        }
        if next_check:
            payload["next_check"] = next_check
        if filter_vars:
            payload["filter_vars"] = filter_vars

        return self._request("POST", "reschedule-check", payload)

    def send_custom_notification(
        self,
        object_type: HostOrService,
        filters: str,
        author: str,
        comment: str,
        filter_vars: FilterVars = None,
        force: Optional[int] = False,
    ) -> Any:
        """
        Send a custom notification for hosts and services.

        example 1:

        .. code-block:: python

            send_custom_notification(
                "Host", "host.name==localhost", "icingaadmin", "test comment"
            )

        :param object_type: Host or Service
        :param filters: filters matched object
        :param author: name of the author
        :param comment: comment text
        :param force: ignore downtimes and notification settings
        :param filter_vars: variables used in the filters expression

        :returns: the response as json

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#send-custom-notification <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#send-custom-notification>`__
        """
        payload: Payload = {
            "type": object_type,
            "filter": filters,
            "author": author,
            "comment": comment,
            "force": force,
        }
        if filter_vars:
            payload["filter_vars"] = filter_vars

        return self._request("POST", "send-custom-notification", payload)

    def delay_notification(
        self,
        object_type: HostOrService,
        filters: str,
        timestamp: int,
        filter_vars: FilterVars = None,
    ) -> Any:
        """
        Delay notifications for a host or a service.

        example 1:

        .. code-block:: python

            delay_notification("Service", "1446389894")

            delay_notification("Host", 'host.name=="localhost"', "1446389894")

        :param object_type: Host or Service
        :param filters: filters matched object(s)
        :param timestamp: timestamp to delay the notifications to
        :param filter_vars: variables used in the filters expression

        :returns: the response as json

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#delay-notification <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#delay-notification>`__
        """
        payload: Payload = {
            "type": object_type,
            "filter": filters,
            "timestamp": timestamp,
        }
        if filter_vars:
            payload["filter_vars"] = filter_vars

        return self._request("POST", "delay-notification", payload)

    def acknowledge_problem(
        self,
        object_type: HostOrService,
        filters: str,
        author: str,
        comment: str,
        filter_vars: FilterVars = None,
        expiry: Optional[int] = None,
        sticky: Optional[bool] = None,
        notify: Optional[bool] = None,
        persistent: Optional[bool] = None,
    ) -> Any:
        """
        Acknowledge a Service or Host problem.

        :param object_type: Host or Service
        :param filters: filters matched object(s)
        :param author: name of the author
        :param comment: comment text
        :param filter_vars: variables used in the filters expression
        :param expiry: acknowledgement expiry timestamp
        :param sticky: stay till full problem recovery
        :param notify: send notification
        :param persistent: the comment will remain after the acknowledgement recovers or expires

        :returns: the response as json

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#acknowledge-problem <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#acknowledge-problem>`__
        """
        payload: Payload = {
            "type": object_type,
            "filter": filters,
            "author": author,
            "comment": comment,
        }
        if filter_vars:
            payload["filter_vars"] = filter_vars
        if expiry:
            payload["expiry"] = expiry
        if sticky:
            payload["sticky"] = sticky
        if notify:
            payload["notify"] = notify
        if persistent:
            payload["persistent"] = persistent

        return self._request("POST", "acknowledge-problem", payload)

    def remove_acknowledgement(
        self, object_type: HostOrService, filters: str, filter_vars: FilterVars = None
    ) -> Any:
        """
        Remove the acknowledgement for services or hosts.

        example 1:

        .. code-block:: python

            raw_client.actions.remove_acknowledgement(
                object_type="Service", filters="service.state==2"
            )

        :param object_type: Host or Service
        :param filters: filters matched object(s)
        :param filter_vars: variables used in the filters expression

        :returns: the response as json

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#remove-acknowledgement <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#remove-acknowledgement>`__
        """
        payload: Payload = {"type": object_type, "filter": filters}
        if filter_vars:
            payload["filter_vars"] = filter_vars

        return self._request("POST", "remove-acknowledgement", payload)

    def add_comment(
        self,
        object_type: HostOrService,
        filter: str,
        author: str,
        comment: str,
        filter_vars: FilterVars = None,
    ) -> Any:
        """
        Add a ``comment`` from an ``author`` to services or hosts.

        example 1:

        .. code-block:: python

            raw_client.actions.add_comment(
                "Service",
                'service.name=="ping4"',
                "icingaadmin",
                "Troubleticket #123456789 opened.",
            )

        :param object_type: The valid types for this action are Host and Service.
        :param filter: filters matched object(s)
        :param author: name of the author
        :param comment: comment text
        :param filter_vars: variables used in the filters expression

        :returns: the response as json

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#add-comment <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#add-comment>`__
        """
        return self._request(
            "POST",
            "add-comment",
            assemble_payload(
                type=object_type,
                filter=filter,
                author=author,
                comment=comment,
                filter_vars=filter_vars,
            ),
        )

    def remove_comment(
        self,
        object_type: HostOrService,
        name: Optional[str] = None,
        filters: Optional[str] = None,
        filter_vars: FilterVars = None,
    ) -> Any:
        """
        Remove a comment using its name or filters.

        example 1:

        .. code-block:: python

            remove_comment("Comment" "localhost!localhost-1458202056-25")

        example 2:

        .. code-block:: python

            remove_comment('Service'
                        filters='service.name=="ping4"')

        :param object_type: Host, Service or Comment
        :param name: name of the Comment
        :param filters: filters matched object(s)
        :param filter_vars: variables used in the filters expression

        :returns: the response as json

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#remove-comment <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#remove-comment>`__
        """
        if not name and not filters:
            raise PretiacException("name and filters is empty or none")

        payload: Payload = {"type": object_type}
        if name:
            payload[object_type.lower()] = name
        if filters:
            payload["filter"] = filters
        if filter_vars:
            payload["filter_vars"] = filter_vars

        return self._request("POST", "remove-comment", payload)

    def schedule_downtime(
        self,
        object_type: HostOrService,
        filters: str,
        author: str,
        comment: str,
        start_time: int,
        end_time: int,
        duration: int,
        filter_vars: FilterVars = None,
        fixed: Optional[bool] = None,
        all_services: Optional[bool] = None,
        trigger_name: Optional[str] = None,
        child_options: Optional[str] = None,
    ) -> Any:
        """
        Schedule a downtime for hosts and services.

        example 1:

        .. code-block:: python

            schedule_downtime(
                'object_type': 'Service',
                'filters': r'service.name=="ping4"',
                'author': 'icingaadmin',
                'comment': 'IPv4 network maintenance',
                'start_time': 1446388806,
                'end_time': 1446389806,
                'duration': 1000
            )

        example 2:

        .. code-block:: python

            schedule_downtime(
                'object_type': 'Host',
                'filters': r'match("*", host.name)',
                'author': 'icingaadmin',
                'comment': 'IPv4 network maintenance',
                'start_time': 1446388806,
                'end_time': 1446389806,
                'duration': 1000
            )

        :param object_type: Host or Service
        :param filters: filters matched object(s)
        :param author: name of the author
        :param comment: comment text
        :param start_time: timestamp marking the beginning
        :param end_time: timestamp marking the end
        :param duration: duration of the downtime in seconds
        :param filter_vars: variables used in the filters expression
        :param fixed: fixed or flexible downtime
        :param all_services: sets downtime for all services for the matched host objects
        :param trigger_name: trigger for the downtime
        :param child_options: schedule child downtimes.

        :returns: the response as json

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#schedule-downtime <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#schedule-downtime>`__
        """
        payload: Payload = {
            "type": object_type,
            "filter": filters,
            "author": author,
            "comment": comment,
            "start_time": start_time,
            "end_time": end_time,
            "duration": duration,
        }
        if filter_vars:
            payload["filter_vars"] = filter_vars
        if fixed:
            payload["fixed"] = fixed
        if all_services:
            payload["all_services"] = all_services
        if trigger_name:
            payload["trigger_name"] = trigger_name
        if child_options:
            payload["child_options"] = child_options

        return self._request("POST", "schedule-downtime", payload)

    def remove_downtime(
        self,
        object_type: HostOrService,
        name: Optional[str] = None,
        filters: Optional[str] = None,
        filter_vars: FilterVars = None,
    ) -> Any:
        """
        Remove the downtime using its name or filters.

        example 1:

        .. code-block:: python

            remove_downtime("Downtime", "localhost!ping4!localhost-1458148978-14")

        example 2:

        .. code-block:: python

            remove_downtime("Service", filters='service.name=="ping4"')

        :param object_type: Host, Service or Downtime
        :param name: name of the downtime
        :param filters: filters matched object(s)
        :param filter_vars: variables used in the filters expression

        :returns: the response as json

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#remove-downtime <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#remove-downtime>`__
        """

        if not name and not filters:
            raise PretiacException("name and filters is empty or none")

        payload: Payload = {"type": object_type}
        if name:
            payload[object_type.lower()] = name
        if filters:
            payload["filter"] = filters
        if filter_vars:
            payload["filter_vars"] = filter_vars

        return self._request("POST", "remove-downtime", payload)

    def shutdown_process(self) -> Any:
        """
        Shuts down Icinga2. May or may not return.

        example 1:

        .. code-block:: python

            shutdown_process()

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#shutdown-process <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#shutdown-process>`__
        """
        return self._request("POST", "shutdown-process")

    def restart_process(self) -> Any:
        """
        Restarts Icinga2. May or may not return.

        example 1:

        .. code-block:: python

            restart_process()

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#restart-process <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#restart-process>`__
        """
        return self._request("POST", "restart-process")

    def generate_ticket(self, cn: str) -> Any:
        """
        Generates a PKI ticket for `CSR auto-signing <https://icinga.com/docs/icinga-2/latest/doc/06-distributed-monitoring/#distributed-monitoring-setup-csr-auto-signing>`__.
        This can be used in combination with satellite/client
        setups requesting this ticket number.

        Example:

        .. code-block:: python

            raw_client.actions.generate_ticket("my-server-name")

        :param cn: Required. The host’s common name for which the ticket should be generated.

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#generate-ticket <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#generate-ticket>`__
        """
        return self._request("POST", "generate-ticket", assemble_payload(cn=cn))


class EventsUrlEndpoint(RequestHandler):
    """
    Connects to the URL endpoint ``events`` of the Icinga2 API.
    """

    path_prefix = "events"

    def subscribe(
        self,
        types: Sequence[EventStreamType],
        queue: str,
        filter: Optional[str] = None,
        filter_vars: FilterVars = None,
    ) -> Generator[str | Any, Any, None]:
        """
        Subscribe to an event stream.

        Event streams can be used to receive check results, downtimes,
        comments, acknowledgements, etc. as a “live stream” from Icinga.

        You can for example forward these types into your own backend. Process
        the metrics and correlate them with notifications and state changes
        e.g. in Elasticsearch with the help of Icingabeat. Another use case
        are aligned events and creating/resolving tickets automatically in
        your ticket system.

        You can subscribe to event streams by sending a POST request to the
        URL endpoint /v1/events. The following parameters need to be
        specified (either as URL parameters or in a JSON-encoded message body):

        example 1:

        .. code-block:: python

            types = ["CheckResult"]
            queue = "monitor"
            filters = "event.check_result.exit_status==2"
            for event in subscribe(types, queue, filters):
                print event

        :param types: **Required.** Event type(s). Multiple types as
            URL parameters are supported.
        :param queue: **Required.** Unique queue name. Multiple HTTP clients
            can use the same queue as long as they use the same event types
            and filter.
        :param filter: Filter for specific event attributes using
            filter expressions.
        :param filter_vars: variables used in the filters expression

        :returns: the events

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#event-streams <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#event-streams>`__
        """
        stream = self._request(
            "POST",
            None,
            assemble_payload(
                types=types, queue=queue, filter=filter, filter_vars=filter_vars
            ),
            stream=True,
        )
        for event in self._get_message_from_stream(stream):
            yield event


class StatusUrlEndpoint(RequestHandler):
    """
    Connects to the URL endpoint ``status`` of the Icinga2 API.

    :see: `lib/remote/statushandler.cpp <https://github.com/Icinga/icinga2/blob/master/lib/remote/statushandler.cpp>`__:
    """

    path_prefix = "status"

    def list(self, status_type: Optional[StatusType | str] = None) -> Any:
        """
        Retrieve status information and statistics for Icinga 2.

        List complete status::

        .. code-block:: python

            client.status.list()

        List the status of the core application:

        .. code-block:: python

            client.status.list("IcingaApplication")

        :param status_type: Limit the output by specifying a status type, e.g. ``IcingaApplication``.

        :returns: status information

        :see: `doc/12-icinga2-api/#status-and-statistics <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#status-and-statistics>`__
        """

        url: str = ""
        if status_type:
            url = status_type

        return self._request("GET", url)


@dataclass
class PerfdataValue:
    """
    `lib/base/perfdatavalue.ti L8-L18 <https://github.com/Icinga/icinga2/blob/4c6b93d61775ff98fc671b05ad4de2b62945ba6a/lib/base/perfdatavalue.ti#L8-L18>`_
    `lib/base/perfdatavalue.hpp L17-L36 <https://github.com/Icinga/icinga2/blob/4c6b93d61775ff98fc671b05ad4de2b62945ba6a/lib/base/perfdatavalue.hpp#L17-L36>`__
    """

    label: str
    value: float
    counter: bool
    unit: str
    crit: Optional[Value] = None
    warn: Optional[Value] = None
    min: Optional[Value] = None
    max: Optional[Value] = None


@dataclass
class StatusMessage:
    """
    :see: `lib/remote/statushandler.cpp L53-L57 <https://github.com/Icinga/icinga2/blob/4c6b93d61775ff98fc671b05ad4de2b62945ba6a/lib/remote/statushandler.cpp#L53-L57>`_
    """

    name: str

    status: dict[str, Any]

    perfdata: Optional[Sequence[PerfdataValue]]


class ConfigUrlEndpoint(RequestHandler):
    """
    Connects to the URL endpoint ``config`` of the Icinga2 API.
    """

    path_prefix = "config"

    def create_package(
        self,
        package_name: str,
        suppress_exception: Optional[bool] = None,
    ) -> Any:
        """
        Create a new empty configuration package.

        :param package_name: Package names with the ``_`` prefix are reserved for
            internal packages and must not be used. You can recognize
            ``_api``, ``_etc`` and ``_cluster`` when querying specific objects
            and packages.
        :param suppress_exception: If this parameter is set to ``True``, no
            exceptions are thrown.

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#create-a-config-package <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#create-a-config-package>`__
        """
        return self._request(
            "POST",
            f"packages/{_normalize_name(package_name)}",
            suppress_exception=suppress_exception,
        )

    def create_stage(
        self,
        package_name: str,
        files: dict[str, str],
        reload: Optional[bool] = None,
        activate: Optional[bool] = None,
        suppress_exception: Optional[bool] = None,
    ) -> Any:
        """
        Configuration files in packages are managed in stages. Stages provide
        a way to maintain multiple configuration versions for a package.
        Once a new stage is deployed, the content is validated and set as
        active stage on success.

        On failure, the older stage remains active, and the caller can fetch
        the startup.log from this stage deployment attempt to see what exactly
        failed. You can see that in the Director’s deployment log.

        :param package_name: Package names with the ``_`` prefix are reserved
            for internal packages and must not be used. You can recognize
            ``_api``, ``_etc`` and ``_cluster`` when querying specific objects
            and packages.
        :param files: Dictionary of file targets and their content.
        :param reload: Tell icinga2 to reload after stage config validation
            (defaults to ``true``).
        :param activate: Tell icinga2 to activate the stage if it validates
            (defaults to ``true``).
            If activate is set to false, reload must
            also be false.
        :param suppress_exception: If this parameter is set to ``True``, no
            exceptions are thrown.

        Example for a local configuration in the ``conf.d`` directory:

        .. code-block::

            raw_client.configuration.create_stage(
                package_name="example-cmdb",
                files={
                    "conf.d/test-host.conf": 'object Host "test-host" { address = "127.0.0.1", check_command = "hostalive" }'
                },
            )

        Example for a host configuration inside the ``satellite`` zone in the ``zones.d`` directory:

        .. code-block::

            raw_client.configuration.create_stage(
                package_name="example-cmdb",
                files={
                    "zones.d/satellite/host2.conf": 'object Host "satellite-host" { address = "192.168.1.100", check_command = "hostalive"',
                },
            )

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#create-a-stage-upload-configuration <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#create-a-stage-upload-configuration>`__
        """
        return self._request(
            "POST",
            f"stages/{_normalize_name(package_name)}",
            assemble_payload(files=files, reload=reload, activate=activate),
            suppress_exception=suppress_exception,
        )

    def list_packages(
        self,
        suppress_exception: Optional[bool] = None,
    ) -> Any:
        """
        List packages and their stages.

        :param suppress_exception: If this parameter is set to ``True``, no
            exceptions are thrown.

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#list-configuration-packages-and-their-stages <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#list-configuration-packages-and-their-stages>`__
        """
        return self._request(
            "GET",
            "packages",
            suppress_exception=suppress_exception,
        )

    def list_stage_files(
        self,
        package_name: str,
        stage_name: str,
        suppress_exception: Optional[bool] = None,
    ) -> Any:
        """
        List packages and their stages.

        :param package_name: Package names with the ``_`` prefix are reserved for
            internal packages and must not be used. You can recognize
            ``_api``, ``_etc`` and ``_cluster`` when querying specific objects
            and packages.
        :param stage_name: The stage name, for example
            ``7e7861c8-8008-4e8d-9910-2a0bb26921bd``.
        :param suppress_exception: If this parameter is set to ``True``, no
            exceptions are thrown.

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#list-configuration-package-stage-files <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#list-configuration-package-stage-files>`__
        """
        return self._request(
            "GET",
            f"stages/{_normalize_name(package_name)}/{stage_name}",
            suppress_exception=suppress_exception,
        )

    def fetch_stage_file(
        self,
        package_name: str,
        stage_name: str,
        relpath: str,
        suppress_exception: Optional[bool] = None,
    ) -> str:
        """
        Fetch the content of a specific configuration file

        :param package_name: Package names with the ``_`` prefix are reserved for
            internal packages and must not be used. You can recognize
            ``_api``, ``_etc`` and ``_cluster`` when querying specific objects
            and packages.
        :param stage_name: The stage name, for example
            ``7e7861c8-8008-4e8d-9910-2a0bb26921bd``.
        :param relpath:  The relative path of the requested configuration file.
        :param suppress_exception: If this parameter is set to ``True``, no
            exceptions are thrown.

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#fetch-configuration-package-stage-files <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#fetch-configuration-package-stage-files>`__
        """
        return self._request(
            "GET",
            f"files/{_normalize_name(package_name)}/{stage_name}/{relpath}",
            suppress_exception=suppress_exception,
            plain=True,
        )

    def get_package_stage_errors(
        self,
        package_name: str,
        stage_name: str,
        suppress_exception: Optional[bool] = None,
    ) -> str:
        """
        Check for validation errors.

        :param package_name: Package names with the ``_`` prefix are reserved for
            internal packages and must not be used. You can recognize
            ``_api``, ``_etc`` and ``_cluster`` when querying specific objects
            and packages.
        :param stage_name: The stage name, for example
            ``7e7861c8-8008-4e8d-9910-2a0bb26921bd``.
        :param suppress_exception: If this parameter is set to ``True``, no
            exceptions are thrown.

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#configuration-package-stage-errors <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#configuration-package-stage-errors>`__
        """
        return self._request(
            "GET",
            f"files/{_normalize_name(package_name)}/{stage_name}/startup.log",
            plain=True,
            suppress_exception=suppress_exception,
        )

    def delete_stage(
        self,
        package_name: str,
        stage_name: str,
        suppress_exception: Optional[bool] = None,
    ) -> Any:
        """
        Send a delete request in order to purge a configuration stage.

        :param name: Package names with the ``_`` prefix are reserved for
            internal packages and must not be used. You can recognize
            ``_api``, ``_etc`` and ``_cluster`` when querying specific objects
            and packages.
        :param stage_name: The stage name, for example
            ``7e7861c8-8008-4e8d-9910-2a0bb26921bd``.
        :param suppress_exception: If this parameter is set to ``True``, no
            exceptions are thrown.

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#deleting-configuration-package-stage <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#deleting-configuration-package-stage>`__
        """
        return self._request(
            "DELETE",
            f"stages/{_normalize_name(package_name)}/{stage_name}",
            suppress_exception=suppress_exception,
        )

    def delete_package(
        self,
        package_name: str,
        suppress_exception: Optional[bool] = None,
    ) -> Any:
        """
        Delete the configuration package entirely.

        :param name: Package names with the ``_`` prefix are reserved for
            internal packages and must not be used. You can recognize
            ``_api``, ``_etc`` and ``_cluster`` when querying specific objects
            and packages.
        :param suppress_exception: If this parameter is set to ``True``, no
            exceptions are thrown.

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#deleting-configuration-package <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#deleting-configuration-package>`__
        """
        return self._request(
            "DELETE",
            f"packages/{_normalize_name(package_name)}",
            suppress_exception=suppress_exception,
        )


class TypesUrlEndpoint(RequestHandler):
    path_prefix = "types"

    def list(self, object_type: Optional[ObjectTypeName] = None) -> Any:
        """Retrieve the configuration object types.

        :param object_type: The type of the object, for example ``Service``,
            ``Host`` or ``User``.

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#types <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#types>`__
        """
        return self._request("GET", object_type)


class TemplatesUrlEndpoint(RequestHandler):
    """
    Connects to the URL endpoint ``templates`` of the Icinga2 API.
    """

    path_prefix = "templates"

    def list(self, object_type: ObjectTypeName, filter: Optional[str] = None) -> Any:
        """Request information about configuration templates.

        :param object_type: The type of the object, for example ``Service``,
            ``Host`` or ``User``.
        :param filter: The template object can be accessed in the filter using the
            ``tmpl`` variable. In the example ``"match(\"g*\", tmpl.name)"``
            the match function is used to check a wildcard string pattern against
            ``tmpl.name``.

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#querying-templates <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#querying-templates>`__
        """
        payload: Payload = {}
        if filter:
            payload["filter"] = filter
        return self._request(
            "GET",
            pluralize_to_lower_object_type_name(object_type),
            payload,
        )


class VariablesUrlEndpoint(RequestHandler):
    path_prefix = "variables"

    def list(self) -> Any:
        """Request information about global variables

        :see: `Icinga2 API documentation: doc/12-icinga2-api/#querying-variables <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#querying-variables>`__
        """
        return self._request("GET", None)


class ConsoleUrlEndpoint(RequestHandler):
    path_prefix = "console"


class RawClient:
    """
    This raw client is a thin wrapper around the Icinga2 REST API.

    You can use the client with either username/password combination or using certificates.

    Example using username and password:

    .. code-block:: python

        from pretiac.client import Client

        client = Client("localhost", 5665, "username", "password")

    Example using certificates:

    .. code-block:: python

        client = Client(
            "localhost",
            5665,
            certificate="/etc/ssl/certs/myhostname.crt",
            key="/etc/ssl/keys/myhostname.key",
        )

    If your public and private are in the same file, just use the `certificate` parameter.

    To verify the server certificate specify a ca file as `ca_file` parameter.

    Example:

    .. code-block:: python

        from pretiac.client import Client

        client = Client(
            "https://icinga2:5665",
            certificate="/etc/ssl/certs/myhostname.crt",
            key="/etc/ssl/keys/myhostname.key",
            ca_file="/etc/ssl/certs/my_ca.crt",
        )

    """

    __config: Config

    url: str

    version: str

    # Order as in https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/

    objects: ObjectsUrlEndpoint
    """Connects to the URL endpoint ``objects`` of the Icinga2 API."""

    actions: ActionsUrlEndpoint
    """Connects to the URL endpoint ``actions`` of the Icinga2 API."""

    events: EventsUrlEndpoint
    """Connects to the URL endpoint ``events`` of the Icinga2 API."""

    status: StatusUrlEndpoint
    """Connects to the URL endpoint ``status`` of the Icinga2 API."""

    config: ConfigUrlEndpoint
    """Connects to the URL endpoint ``config`` of the Icinga2 API."""

    types: TypesUrlEndpoint
    """Connects to the URL endpoint ``types`` of the Icinga2 API."""

    templates: TemplatesUrlEndpoint
    """Connects to the URL endpoint ``templates`` of the Icinga2 API."""

    variables: VariablesUrlEndpoint
    """Connects to the URL endpoint ``types`` of the Icinga2 API."""

    console: ConsoleUrlEndpoint
    """Connects to the URL endpoint ``types`` of the Icinga2 API."""

    def __init__(self, config: Config) -> None:
        """
        initialize object

        :param suppress_exception: If this parameter is set to ``True``, no exceptions are thrown.
        """
        self.__config = config

        self.url = f"https://{self.__config.api_endpoint_host}:{self.__config.api_endpoint_port}"

        self.version = get_version("pretiac")

        self.actions = ActionsUrlEndpoint(self)
        self.config = ConfigUrlEndpoint(self)
        self.events = EventsUrlEndpoint(self)
        self.objects = ObjectsUrlEndpoint(self)
        self.status = StatusUrlEndpoint(self)
        self.templates = TemplatesUrlEndpoint(self)
        self.types = TypesUrlEndpoint(self)
        self.variables = VariablesUrlEndpoint(self)

    def get_client_config(self) -> Config:
        return self.__config
