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
from dataclasses import dataclass
from importlib.metadata import version as get_version
from typing import Any, Generator, Literal, Optional, Union

from pretiac.config import Config
from pretiac.exceptions import PretiacException
from pretiac.object_types import (
    FilterVars,
    HostOrService,
    ObjectTypeName,
    Payload,
    Value,
)
from pretiac.request_handler import (
    RequestHandler,
    State,
    normalize_state,
)


@dataclass
class Result:
    code: int

    status: str


@dataclass
class ResultContainer:
    results: list[Result]


class Actions(RequestHandler):
    """
    Icinga 2 API actions class
    """

    base_url_path = "v1/actions"

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

        Send a ``POST`` request to the URL endpoint ``/v1/actions/process-check-result``.

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


        :see: `Icinga2 API-Documentation: doc/12-icinga2-api/#process-check-result <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#process-check-result>`__
        """
        if not name and not filter:
            raise PretiacException("name and filters is empty or none")

        if name and (filter or filter_vars):
            raise PretiacException("name and filters are mutually exclusive")

        if type not in ["Host", "Service"]:
            raise PretiacException('type needs to be "Host" or "Service".')

        url = f"{self.base_url}/process-check-result"

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
            "POST", url, payload, suppress_exception=suppress_exception
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

        https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#reschedule-check
        """

        url = "{}/{}".format(self.base_url_path, "reschedule-check")

        payload: Payload = {
            "type": object_type,
            "filter": filters,
            "force_check": force_check,
        }
        if next_check:
            payload["next_check"] = next_check
        if filter_vars:
            payload["filter_vars"] = filter_vars

        return self._request("POST", url, payload)

    def send_custom_notification(
        self,
        object_type: HostOrService,
        filters: str,
        author: str,
        comment: str,
        filter_vars: FilterVars = None,
        force: Optional[int] = False,
    ):
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

        https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#send-custom-notification
        """

        url = "{}/{}".format(self.base_url_path, "send-custom-notification")

        payload: Payload = {
            "type": object_type,
            "filter": filters,
            "author": author,
            "comment": comment,
            "force": force,
        }
        if filter_vars:
            payload["filter_vars"] = filter_vars

        return self._request("POST", url, payload)

    def delay_notification(
        self,
        object_type: HostOrService,
        filters: str,
        timestamp: int,
        filter_vars: FilterVars = None,
    ):
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

        https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#delay-notification
        """

        url = "{}/{}".format(self.base_url_path, "delay-notification")

        payload: Payload = {
            "type": object_type,
            "filter": filters,
            "timestamp": timestamp,
        }
        if filter_vars:
            payload["filter_vars"] = filter_vars

        return self._request("POST", url, payload)

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
    ):
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

        https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#acknowledge-problem
        """

        url = "{}/{}".format(self.base_url_path, "acknowledge-problem")

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

        return self._request("POST", url, payload)

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

        :see: `Icinga2 API-Documentation <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#remove-acknowledgement>`__
        """

        url = "{}/{}".format(self.base_url_path, "remove-acknowledgement")

        payload: Payload = {"type": object_type, "filter": filters}
        if filter_vars:
            payload["filter_vars"] = filter_vars

        return self._request("POST", url, payload)

    def add_comment(
        self,
        object_type: HostOrService,
        filters: str,
        author: str,
        comment: str,
        filter_vars: FilterVars = None,
    ) -> Any:
        """
        Add a comment from an author to services or hosts.

        example 1:

        .. code-block:: python

            add_comment(
                "Service",
                'service.name=="ping4"',
                "icingaadmin",
                "Incident ticket #12345 opened.",
            )

        :param object_type: Host or Service
        :param filters: filters matched object(s)
        :param author: name of the author
        :param comment: comment text
        :param filter_vars: variables used in the filters expression

        :returns: the response as json

        https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#add-comment
        """

        url = "{}/{}".format(self.base_url_path, "add-comment")

        payload: Payload = {
            "type": object_type,
            "filter": filters,
            "author": author,
            "comment": comment,
        }
        if filter_vars:
            payload["filter_vars"] = filter_vars

        return self._request("POST", url, payload)

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

        https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#remove-comment
        """

        if not name and not filters:
            raise PretiacException("name and filters is empty or none")

        url = "{}/{}".format(self.base_url_path, "remove-comment")

        payload: Payload = {"type": object_type}
        if name:
            payload[object_type.lower()] = name
        if filters:
            payload["filter"] = filters
        if filter_vars:
            payload["filter_vars"] = filter_vars

        return self._request("POST", url, payload)

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

        https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#schedule-downtime
        """

        url = "{}/{}".format(self.base_url_path, "schedule-downtime")

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

        return self._request("POST", url, payload)

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

        https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#remove-downtime
        """

        if not name and not filters:
            raise PretiacException("name and filters is empty or none")

        url = "{}/{}".format(self.base_url_path, "remove-downtime")

        payload: Payload = {"type": object_type}
        if name:
            payload[object_type.lower()] = name
        if filters:
            payload["filter"] = filters
        if filter_vars:
            payload["filter_vars"] = filter_vars

        return self._request("POST", url, payload)

    def shutdown_process(self) -> Any:
        """
        Shuts down Icinga2. May or may not return.

        example 1:

        .. code-block:: python

            shutdown_process()

        https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#shutdown-process
        """

        url = "{}/{}".format(self.base_url_path, "shutdown-process")

        return self._request("POST", url)

    def restart_process(self) -> Any:
        """
        Restarts Icinga2. May or may not return.

        example 1:

        .. code-block:: python

            restart_process()

        https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#restart-process
        """

        url = "{}/{}".format(self.base_url_path, "restart-process")

        return self._request("POST", url)

    def generate_ticket(self, host_common_name: str) -> Any:
        """
        Generates a PKI ticket for CSR auto-signing.
        This can be used in combination with satellite/client
        setups requesting this ticket number.

        example 1:

        .. code-block:: python

            generate_ticket("my-server-name")

        :param host_common_name: the host's common name for which the ticket should be generated.

        https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#generate-ticket
        """

        if not host_common_name:
            raise PretiacException("host_common_name is empty or none")

        url = "{}/{}".format(self.base_url_path, "generate-ticket")

        payload = {"cn": host_common_name}

        return self._request("POST", url, payload)


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


class Events(RequestHandler):
    """
    Icinga 2 API events class
    """

    base_url_path = "v1/events"

    def subscribe(
        self,
        types: Sequence[EventStreamType],
        queue: str,
        filters: Optional[str] = None,
        filter_vars: FilterVars = None,
    ) -> Generator[str | Any, Any, None]:
        """
        subscribe to an event stream

        example 1:

        .. code-block:: python

            types = ["CheckResult"]
            queue = "monitor"
            filters = "event.check_result.exit_status==2"
            for event in subscribe(types, queue, filters):
                print event

        :param types: Event type(s). Multiple types as URL parameters are supported.
        :param queue: Unique queue name. Multiple HTTP clients can use the same queue as long as they use the same event types and filter.
        :param filters: Filter for specific event attributes using filter expressions.
        :param filter_vars: variables used in the filters expression

        :returns: the events
        """
        payload: Payload = {
            "types": types,
            "queue": queue,
        }
        if filters:
            payload["filter"] = filters
        if filter_vars:
            payload["filter_vars"] = filter_vars

        stream = self._request("POST", self.base_url, payload, stream=True)
        for event in self._get_message_from_stream(stream):
            yield event


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


class CheckResult:
    """https://github.com/Icinga/icinga2/blob/master/lib/icinga/checkresult.ti"""

    type = "CheckResult"
    active: bool
    check_source: str
    command: list[str]
    execution_end: float
    execution_start: float
    exit_status: int
    output: str
    performance_data: list[str]
    previous_hard_state: int
    schedule_end: float
    schedule_start: float
    scheduling_source: str
    state: int
    ttl: int
    vars_after: dict[str, Any]
    vars_before: dict[str, Any]


class Host:
    name: str
    state: int
    last_check_result: CheckResult


class Objects(RequestHandler):
    """
    Icinga 2 API objects class
    """

    base_url_path = "v1/objects"

    @staticmethod
    def _convert_object_type(object_type: Optional[ObjectTypeName] = None) -> str:
        """
        check if the object_type is a valid Icinga 2 object type
        """

        type_conv = {
            "ApiListener": "apilisteners",
            "ApiUser": "apiusers",
            "CheckCommand": "checkcommands",
            "Arguments": "argumentss",
            "CheckerComponent": "checkercomponents",
            "CheckResultReader": "checkresultreaders",
            "Comment": "comments",
            "CompatLogger": "compatloggers",
            "Dependency": "dependencies",
            "Downtime": "downtimes",
            "Endpoint": "endpoints",
            "EventCommand": "eventcommands",
            "ExternalCommandListener": "externalcommandlisteners",
            "FileLogger": "fileloggers",
            "GelfWriter": "gelfwriters",
            "GraphiteWriter": "graphitewriters",
            "Host": "hosts",
            "HostGroup": "hostgroups",
            "IcingaApplication": "icingaapplications",
            "IdoMySqlConnection": "idomysqlconnections",
            "IdoPgSqlConnection": "idopgsqlconnections",
            "LiveStatusListener": "livestatuslisteners",
            "Notification": "notifications",
            "NotificationCommand": "notificationcommands",
            "NotificationComponent": "notificationcomponents",
            "OpenTsdbWriter": "opentsdbwriters",
            "PerfdataWriter": "perfdatawriters",
            "ScheduledDowntime": "scheduleddowntimes",
            "Service": "services",
            "ServiceGroup": "servicegroups",
            "StatusDataWriter": "statusdatawriters",
            "SyslogLogger": "syslogloggers",
            "TimePeriod": "timeperiods",
            "User": "users",
            "UserGroup": "usergroups",
            "Zone": "zones",
        }
        if object_type not in type_conv:
            raise PretiacException(
                'Icinga 2 object type "{}" does not exist.'.format(object_type)
            )

        return type_conv[object_type]

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


        :see: `Icinga2 API-Documentation <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#querying-objects>`__
        """

        url_path = "{}/{}".format(
            self.base_url_path, self._convert_object_type(object_type)
        )
        if name:
            url_path += "/{}".format(_normalize_name(name))

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

        :see: `Icinga2 API-Documentation <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#creating-config-objects>`__
        """

        payload: Payload = {}
        if attrs:
            payload["attrs"] = attrs
        if templates:
            payload["templates"] = templates

        return self._request(
            "PUT",
            "{}/{}/{}".format(
                self.base_url,
                self._convert_object_type(object_type),
                _normalize_name(name),
            ),
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

        :see: `Icinga2 API-Documentation <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#modifying-objects>`__
        """
        return self._request(
            "POST",
            "{}/{}/{}".format(
                self.base_url, self._convert_object_type(object_type), name
            ),
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

        :see: `Icinga2 API-Documentation <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#deleting-objects>`_
        """

        object_type_url_path = self._convert_object_type(object_type)

        payload: Payload = {}
        if filters:
            payload["filter"] = filters
        if filter_vars:
            payload["filter_vars"] = filter_vars
        if cascade:
            payload["cascade"] = 1

        url = "{}/{}".format(self.base_url_path, object_type_url_path)
        if name:
            url += "/{}".format(_normalize_name(name))

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


class Status(RequestHandler):
    """
    Icinga 2 API status class

    :see: `lib/remote/statushandler.cpp <https://github.com/Icinga/icinga2/blob/master/lib/remote/statushandler.cpp>`_:
    """

    base_url_path = "v1/status"

    def list(self, status_type: Optional[StatusType | str] = None) -> Any:
        """
        Retrieve status information and statistics for Icinga 2.

        Example 1:

        .. code-block:: python

            client.status.list()

        Example 2:

        .. code-block:: python

            client.status.list("IcingaApplication")

        :param status_type: Limit the output by specifying a status type, e.g. ``IcingaApplication``.

        :returns: status information
        """

        url: str = self.base_url
        if status_type:
            url += f"/{status_type}"

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


class Templates(RequestHandler):
    base_url_path = "v1/templates"

    def list(self, object_type: ObjectTypeName, filter: Optional[str] = None) -> Any:
        """Request information about configuration templates.

        :param object_type: The type of the object, for example ``Service``,
            ``Host`` or ``User``.
        :param filter: The template object can be accessed in the filter using the
            ``tmpl`` variable. In the example ``"match(\"g*\", tmpl.name)"``
            the match function is used to check a wildcard string pattern against
            ``tmpl.name``.
        """
        payload: Payload = {}
        if filter:
            payload["filter"] = filter
        return self._request(
            "GET", f"{self.base_url}/{self._pluralize(object_type)}", payload
        )


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

    config: Config

    url: str

    version: str

    actions: Actions

    events: Events

    objects: Objects

    status: Status

    templates: Templates

    def __init__(self, config: Config) -> None:
        """
        initialize object

        :param suppress_exception: If this parameter is set to ``True``, no exceptions are thrown.
        """
        self.config = config

        self.url = (
            f"https://{self.config.api_endpoint_host}:{self.config.api_endpoint_port}"
        )

        self.version = get_version("pretiac")

        self.actions = Actions(self)
        self.events = Events(self)
        self.objects = Objects(self)
        self.status = Status(self)
        self.templates = Templates(self)
