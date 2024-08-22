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
Icinga 2 API events
"""

from __future__ import print_function

import logging
from collections.abc import Sequence
from typing import Any, Generator, Literal, Optional

from pretiac.base import Base, FilterVars, Payload

LOG = logging.getLogger(__name__)


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


class Events(Base):
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
