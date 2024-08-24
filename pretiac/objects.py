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
Icinga 2 API objects
"""

from __future__ import print_function

import logging
import urllib
import urllib.parse
from collections.abc import Sequence
from typing import Any, Optional, Union

from pretiac.base import Base
from pretiac.exceptions import PretiacException
from pretiac.object_types import FilterVars, ObjectType, Payload

LOG = logging.getLogger(__name__)


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


class Objects(Base):
    """
    Icinga 2 API objects class
    """

    base_url_path = "v1/objects"

    @staticmethod
    def _convert_object_type(object_type: Optional[ObjectType] = None) -> str:
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
        object_type: ObjectType,
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

            client.objects.list("Host")

        List the service ``ping4`` of host ``webserver01.domain!ping4``:

        .. code-block:: python

            client.objects.list("Service", "webserver01.domain!ping4")

        Get all hosts but limit attributes to `address` and `state`:

        .. code-block:: python

            client.objects.list("Host", attrs=["address", "state"])

        Get all hosts which have ``webserver`` in their host name:

        .. code-block:: python

            client.objects.list("Host", filters='match("webserver*", host.name)')

        Get all services and the joined host name:

        .. code-block:: python

            client.objects.list("Service", joins=["host.name"])

        Get all services and all supported joins:

        .. code-block:: python

            client.objects.list("Service", joins=True)

        Get all services which names start with ``vHost`` and are assigned to hosts named ``webserver*`` using ``filter_vars``:

        .. code-block:: python

            hostname_pattern = "webserver*"
            service_pattern = "vHost*"
            client.objects.list(
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
        object_type: ObjectType,
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

            client.objects.get("Host", "webserver01.domain")

        Get service ``ping4`` of host ``webserver01.domain``:

        .. code-block:: python

            client.objects.get("Service", "webserver01.domain!ping4")

        Get host ``webserver01.domain`` but the attributes ``address`` and ``state``:

        .. code-block:: python

            client.objects.get("Host", "webserver01.domain", attrs=["address", "state"])

        Get service ``ping4`` of host ``webserver01.domain`` and the host attributes:

        .. code-block:: python

            client.objects.get("Service", "webserver01.domain!ping4", joins=True)
        """

        return self.list(
            object_type, name, attrs, joins=joins, suppress_exception=suppress_exception
        )[0]

    def create(
        self,
        object_type: ObjectType,
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

            client.objects.create(
                "Host", "localhost", ["generic-host"], {"address": "127.0.0.1"}
            )

        Create a service for Host ``localhost``:

        .. code-block:: python

            client.objects.create(
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
        object_type: ObjectType,
        name: str,
        attrs: dict[str, Any],
        suppress_exception: Optional[bool] = None,
    ) -> Any:
        """
        Update an object with the specified attributes.

        :param object_type: The type of the object, for example ``Service``,
            ``Host`` or ``User``.
        :param name: the name of the object
        :type name: string
        :param attrs: object's attributes to change
        :type attrs: dictionary
        :param suppress_exception: If this parameter is set to ``True``, no exceptions are thrown.

        Change the ip address of a host:

        .. code-block:: python

            client.objects.update("Host", "localhost", {"address": "127.0.1.1"})

        Update a service and change the check interval:

        .. code-block:: python

            client.objects.update("Service", "testhost3!dummy", {"check_interval": "10m"})

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
        object_type: ObjectType,
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

            delete("Host", "localhost")

        Delete all services matching ``vhost*``:

        .. code-block:: python

            delete("Service", filters='match("vhost*", service.name)')

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
