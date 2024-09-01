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
Retrieve status information and statistics for Icinga 2.

:see: `doc/12-icinga2-api/#status-and-statistics <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#status-and-statistics>`__
"""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Literal, Optional

from pretiac.base import Base
from pretiac.object_types import Value

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


class Status(Base):
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
