import sys
from logging import Logger
from typing import Dict, List, Literal, Type, Union

from .client import Client
from .exceptions import *

if sys.version_info >= (3, 0): ...
else: ...
LOG: Logger = ...

Json = Union[Dict[str, "Json"], List["Json"], int, str, float, bool, Type[None]]

HostService = Literal["Host", "Service"]

HostServiceComment = Union[Literal["Comment"], HostService]

HostServiceDowntime = Union[Literal["Downtime"], HostService]

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

class Base:

    base_url_path: str = ...

    def __init__(self, manager: Client) -> None: ...
