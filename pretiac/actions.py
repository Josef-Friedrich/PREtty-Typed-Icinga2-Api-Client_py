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

from __future__ import print_function

import logging
from dataclasses import dataclass
from typing import Optional

from pretiac.base import (
    Base,
    Payload,
    State,
    normalize_state,
)
from pretiac.exceptions import PretiacException
from pretiac.object_types import (
    FilterVars,
    HostOrService,
)

LOG = logging.getLogger(__name__)


@dataclass
class Result:
    code: int

    status: str


@dataclass
class ResultContainer:
    results: list[Result]


class Actions(Base):
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
        performance_data: Optional[list[str] | str] = None,
        check_command: Optional[list[str] | str] = None,
        check_source: Optional[str] = None,
        execution_start: Optional[int] = None,
        execution_end: Optional[int] = None,
        ttl: Optional[int] = None,
        filter: Optional[str] = None,
        filter_vars: FilterVars = None,
        suppress_exception: Optional[bool] = None,
    ):
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

            process_check_result('Service',
                                'myhost.domain!ping4',
                                'exit_status': 2,
                                'plugin_output': 'PING CRITICAL - Packet loss = 100%',
                                'performance_data': [
                                    'rta=5000.000000ms;3000.000000;5000.000000;0.000000',
                                    'pl=100%;80;100;0'],
                                'check_source': 'python client'})


        :see: https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#process-check-result
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
    ):
        """
        Reschedule a check for hosts and services.

        example 1:

        .. code-block:: python

            reschedule_check('Service'
                            'service.name=="ping4")

        example 2:

        .. code-block:: python

            reschedule_check("Host", 'host.name=="localhost"', "1577833200")

        :param object_type: Host or Service
        :param filters: filters matched object(s)
        :type filters: string
        :param filter_vars: variables used in the for filters expression
        :param next_check: timestamp to run the check
        :type next_check: int
        :param force: ignore period restrictions and disabled checks
        :type force: bool
        :returns: the response as json
        :rtype: dictionary
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
        :rtype: dictionary
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
        :rtype: dictionary
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
        :rtype: dictionary
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
    ):
        """
        Remove the acknowledgement for services or hosts.

        example 1:
        .. code-block:: python

            remove_acknowledgement(object_type='Service',
                                'service.state==2')

        :param object_type: Host or Service
        :type object_type: string
        :param filters: filters matched object(s)
        :type filters: string
        :param filter_vars: variables used in the filters expression

        :returns: the response as json
        :rtype: dictionary
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
    ):
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
        :type comment: string
        :param filter_vars: variables used in the filters expression

        :returns: the response as json
        :rtype: dictionary
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
    ):
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
        :rtype: dictionary
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
    ):
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
        :rtype: dictionary
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
    ):
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
        :rtype: dictionary
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

    def shutdown_process(self):
        """
        Shuts down Icinga2. May or may not return.

        example 1:

        .. code-block:: python

            shutdown_process()
        """

        url = "{}/{}".format(self.base_url_path, "shutdown-process")

        return self._request("POST", url)

    def restart_process(self):
        """
        Restarts Icinga2. May or may not return.

        example 1:

        .. code-block:: python

            restart_process()
        """

        url = "{}/{}".format(self.base_url_path, "restart-process")

        return self._request("POST", url)

    def generate_ticket(self, host_common_name: str):
        """
        Generates a PKI ticket for CSR auto-signing.
        This can be used in combination with satellite/client
        setups requesting this ticket number.

        example 1:

        .. code-block:: python

            generate_ticket("my-server-name")

        :param host_common_name: the host's common name for which the ticket should be generated.
        """

        if not host_common_name:
            raise PretiacException("host_common_name is empty or none")

        url = "{}/{}".format(self.base_url_path, "generate-ticket")

        payload = {"cn": host_common_name}

        return self._request("POST", url, payload)
