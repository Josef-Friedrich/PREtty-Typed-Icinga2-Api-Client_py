from enum import Enum
from typing import (
    Any,
    Literal,
    Optional,
    Union,
)

HostOrService = Literal["Host", "Service"]

HostServiceComment = Union[Literal["Comment"], HostOrService]

HostServiceDowntime = Union[Literal["Downtime"], HostOrService]


class HostState(Enum):
    """
    https://github.com/Icinga/icinga2/blob/a8adfeda60232260e3eee6d68fa5f4787bb6a245/lib/icinga/checkresult.ti#L11-L20
    """

    UP = 0
    DOWN = 1


class ServiceState(Enum):
    """
    https://github.com/Icinga/icinga2/blob/a8adfeda60232260e3eee6d68fa5f4787bb6a245/lib/icinga/checkresult.ti#L22-L33
    """

    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3


State = HostState | ServiceState | Literal[0, 1, 2, 3] | int


ObjectType = Literal[
    "ApiListener",
    "ApiUser",
    "CheckCommand",
    "Arguments",
    "CheckerComponent",
    "CheckResultReader",
    "Comment",
    "CompatLogger",
    "Dependency",
    "Downtime",
    "Endpoint",
    "EventCommand",
    "ExternalCommandListener",
    "FileLogger",
    "GelfWriter",
    "GraphiteWriter",
    "Host",
    "HostGroup",
    "IcingaApplication",
    "IdoMySqlConnection",
    "IdoPgSqlConnection",
    "LiveStatusListener",
    "Notification",
    "NotificationCommand",
    "NotificationComponent",
    "OpenTsdbWriter",
    "PerfdataWriter",
    "ScheduledDowntime",
    "Service",
    "ServiceGroup",
    "StatusDataWriter",
    "SyslogLogger",
    "TimePeriod",
    "User",
    "UserGroup",
    "Zone",
]

Payload = dict[str, Any]

FilterVars = Optional[Payload]

RequestMethod = Literal["GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"]
"""
https://github.com/psf/requests/blob/a3ce6f007597f14029e6b6f54676c34196aa050e/src/requests/api.py#L17

https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
"""
