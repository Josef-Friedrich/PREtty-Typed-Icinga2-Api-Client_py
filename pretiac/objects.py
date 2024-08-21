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
from collections.abc import Sequence
from typing import Any, Optional, Union

from pretiac.base import Base, FilterVars, ObjectType, Payload
from pretiac.exceptions import PretiacException

LOG = logging.getLogger(__name__)


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

    def get(
        self,
        object_type: ObjectType,
        name: str,
        attrs: Optional[Sequence[str]] = None,
        joins: Optional[Union[bool, Sequence[str]]] = None,
    ) -> Any:
        """
        get object by type or name

        :param object_type: type of the object
        :param name: list object with this name
        :param attrs: only return these attributes
        :param joins: show joined object

        example 1:
        get('Host', 'webserver01.domain')

        example 2:
        get('Service', 'webserver01.domain!ping4')

        example 3:
        get('Host', 'webserver01.domain', attrs=["address", "state"])

        example 4:
        get('Service', 'webserver01.domain!ping4', joins=True)
        """

        return self.list(object_type, name, attrs, joins=joins)[0]

    def list(
        self,
        object_type: ObjectType,
        name: Optional[str] = None,
        attrs: Optional[Sequence[str]] = None,
        filters: Optional[str] = None,
        filter_vars: FilterVars = None,
        joins: Optional[Union[bool, Sequence[str]]] = None,
    ) -> Any:
        """
        get object by type or name

        :param object_type: type of the object
        :type object_type: string
        :param name: list object with this name
        :type name: string
        :param attrs: only return these attributes
        :type attrs: list
        :param filters: filters matched object(s)
        :type filters: string
        :param filter_vars: variables used in the filters expression
        :type filter_vars: dict
        :param joins: show joined object
        :type joins: list

        example 1:
        list('Host')

        example 2:
        list('Service', 'webserver01.domain!ping4')

        example 3:
        list('Host', attrs='["address", "state"])

        example 4:
        list('Host', filters='match("webserver*", host.name)')

        example 5:
        list('Service', joins=['host.name'])

        example 6:
        list('Service', joins=True)
        """

        object_type_url_path = self._convert_object_type(object_type)
        url_path = "{}/{}".format(self.base_url_path, object_type_url_path)
        if name:
            url_path += "/{}".format(name)

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

        return self._request("GET", url_path, payload)["results"]

    def create(
        self,
        object_type: ObjectType,
        name: str,
        templates: Optional[Sequence[str]] = None,
        attrs: Optional[Sequence[str]] = None,
    ) -> Any:
        """
        create an object

        :param object_type: type of the object
        :param name: the name of the object
        :param templates: templates used
        :param attrs: object's attributes

        example 1:
        create('Host', 'localhost', ['generic-host'], {'address': '127.0.0.1'})

        example 2:
        create('Service',
               'testhost3!dummy',
               {'check_command': 'dummy'},
               ['generic-service'])
        """

        object_type_url_path = self._convert_object_type(object_type)

        payload: Payload = {}
        if attrs:
            payload["attrs"] = attrs
        if templates:
            payload["templates"] = templates

        url_path = "{}/{}/{}".format(self.base_url_path, object_type_url_path, name)

        return self._request("PUT", url_path, payload)

    def update(self, object_type: ObjectType, name: str, attrs: dict[str, Any]) -> Any:
        """
        update an object

        :param object_type: type of the object
        :type object_type: string
        :param name: the name of the object
        :type name: string
        :param attrs: object's attributes to change
        :type attrs: dictionary

        example 1:
        update('Host', 'localhost', {'address': '127.0.1.1'})

        example 2:
        update('Service', 'testhost3!dummy', {'check_interval': '10m'})
        """
        object_type_url_path = self._convert_object_type(object_type)
        url_path = "{}/{}/{}".format(self.base_url_path, object_type_url_path, name)

        return self._request("POST", url_path, attrs)

    def delete(
        self,
        object_type: ObjectType,
        name: Optional[str] = None,
        filters: Optional[str] = None,
        filter_vars: FilterVars = None,
        cascade: bool = True,
    ) -> Any:
        """
        delete an object

        :param object_type: type of the object
        :type object_type: string
        :param name: the name of the object
        :type name: string
        :param filters: filters matched object(s)
        :type filters: string
        :param filter_vars: variables used in the filters expression
        :type filter_vars: dict
        :param cascade: deleted dependent objects
        :type joins: bool

        example 1:
        delete('Host', 'localhost')

        example 2:
        delete('Service', filters='match("vhost*", service.name)')
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
            url += "/{}".format(name)

        return self._request("DELETE", url, payload)
