"""
All available config object types.

Listed in the same order as in this `Markdown document <https://github.com/Icinga/icinga2/blob/master/doc/09-object-types.md>`__.
"""

import re
from collections.abc import Sequence
from enum import Enum
from typing import (
    Annotated,
    Any,
    Literal,
    Optional,
    TypeAlias,
    Union,
    get_args,
)

from pydantic import BeforeValidator
from pydantic.dataclasses import dataclass


def _empty_str_to_none(v: str | None) -> str | None:
    if v is None:
        return None
    if v == "":
        return None
    return v


# https://github.com/pydantic/pydantic/discussions/2687#discussioncomment-9893991
OptionalStr: TypeAlias = Annotated[Optional[str], BeforeValidator(_empty_str_to_none)]
"""
An empty string is set to None by the Pydantic validator.
"""


MonitoringObjectName = Literal[
    "ApiUser",
    "CheckCommand",
    # "CheckCommandArguments", used in CheckCommand
    "Dependency",
    "Endpoint",
    "EventCommand",
    "Host",
    "HostGroup",
    "Notification",
    "NotificationCommand",
    "ScheduledDowntime",
    "Service",
    "ServiceGroup",
    "TimePeriod",
    "User",
    "UserGroup",
    "Zone",
]
"""
see `doc/09-object-types.md object-types-monitoring <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md#object-types-monitoring>`__
"""


RuntimeObjectName = Literal["Comment", "Downtime"]
"""
see [doc/09-object-types.md runtime-objects-](https://github.com/Icinga/icinga2/b
"""

FeatureObjectName = Literal[
    "ApiListener",
    "CheckerComponent",
    "CompatLogger",
    "ElasticsearchWriter",
    "ExternalCommandListener",
    "FileLogger",
    "GelfWriter",
    "GraphiteWriter",
    "IcingaApplication",
    "IcingaDB",
    "IdoMySqlConnection",
    "IdoPgsqlConnection",
    "InfluxdbWriter",
    "Influxdb2Writer",
    "JournaldLogger",
    "LiveStatusListener",
    "NotificationComponent",
    "OpenTsdbWriter",
    "PerfdataWriter",
    "SyslogLogger",
    "WindowsEventLogLogger",
]
"""
see `doc/09-object-types.md features- <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md#features->`__
"""


ObjectTypeName = Union[MonitoringObjectName, RuntimeObjectName, FeatureObjectName]


def _convert_pascal_to_snake_case(name: str) -> str:
    """
    Insert underscores before capital letters and convert to lowercase
    """
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def get_object_types_names() -> list[str]:
    return (
        list(get_args(MonitoringObjectName))
        + list(get_args(RuntimeObjectName))
        + list(get_args(FeatureObjectName))
    )


object_type_names: list[str] = get_object_types_names()

object_type_names_snake = list(
    map(lambda name: _convert_pascal_to_snake_case(name), object_type_names)
)


def normalize_to_plural_snake_object_type_name(object_type_name: str) -> str:
    """
    for example: ``ApiUser`` to ``api_users``

    :returns: A pluralized object type name in the snake case.
    """
    snake = _convert_pascal_to_snake_case(object_type_name)
    if snake in object_type_names_snake:
        return f"{snake}s"
    return snake


def pluralize_to_lower_object_type_name(object_type_name: ObjectTypeName) -> str:
    """
    for example: ``ApiUser`` to ``apiusers``
    """
    return f"{object_type_name.lower()}s"


HostOrService = Literal["Host", "Service"]

HostServiceComment = Union[Literal["Comment"], HostOrService]

HostServiceDowntime = Union[Literal["Downtime"], HostOrService]


Payload = dict[str, Any]

FilterVars = Optional[Payload]

RequestMethod = Literal["GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"]
"""
https://github.com/psf/requests/blob/a3ce6f007597f14029e6b6f54676c34196aa050e/src/requests/api.py#L17

https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
"""


########################################################################################
# Delegated interfaces and types
########################################################################################


@dataclass
class SourceLocation:
    first_column: int
    first_line: int
    last_column: int
    last_line: int

    path: str
    """
    ``/etc/icinga2-custom/conf.d/api-users.conf``
    """


class HAMode(Enum):
    """:see: `lib/base/configobject.ti L12-L16 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L12-L16>`__"""

    HARunOnce = 0
    HARunEverywhere = 1


class StateType(Enum):
    """
    see: `lib/icinga/checkresult.ti L38-L43 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/checkresult.ti#L38-L43>`__
    """

    StateTypeSoft = 0
    StateTypeHard = 1


@dataclass
class Dictionary:
    pass


Timestamp = float
"""
for example `1699475880.364077`

:see: `lib/base/value.hpp L15 <https://github.com/Icinga/icinga2/blob/4c6b93d61775ff98fc671b05ad4de2b62945ba6a/lib/base/value.hpp#L15>`__
"""


Value = int | float | str | bool | Any
"""
A type that can hold an arbitrary value.

`lib/base/value.hpp L31-L145 <https://github.com/Icinga/icinga2/blob/4c6b93d61775ff98fc671b05ad4de2b62945ba6a/lib/base/value.hpp#L31-L145>`_
"""


class ServiceState(Enum):
    """

    0=OK, 1=WARNING, 2=CRITICAL, 3=UNKNOWN

    https://github.com/Icinga/icinga2/blob/a8adfeda60232260e3eee6d68fa5f4787bb6a245/lib/icinga/checkresult.ti#L22-L33
    """

    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3

    def __str__(self) -> str:
        return f"{self.value} ({self.name})"


class HostState(Enum):
    """
     0=UP, 1=DOWN.

    https://github.com/Icinga/icinga2/blob/a8adfeda60232260e3eee6d68fa5f4787bb6a245/lib/icinga/checkresult.ti#L11-L20
    """

    UP = 0
    DOWN = 1

    def __str__(self) -> str:
        return f"{self.value} ({self.name})"


State = HostState | ServiceState | Literal[0, 1, 2, 3] | int


def get_service_state(state: Union[State, Any]) -> ServiceState:
    if isinstance(state, ServiceState):
        return state
    if isinstance(state, int) and 0 <= state <= 3:
        return ServiceState(state)
    return ServiceState.CRITICAL


@dataclass
class CheckResult:
    pass


########################################################################################
# Interface from which the object types inherit
########################################################################################


@dataclass(config={"extra": "forbid"})
class ConfigObject:
    """
    :see: `lib/base/configobject.ti L57-L92 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L57-L92>`__
    """

    name: Optional[str] = None
    """:see: `lib/base/configobject.ti L59-L68 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L59-L68>`__"""

    type: Optional[str] = None

    zone: OptionalStr = None
    """:see: `lib/base/configobject.ti L69 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L69>`__"""

    package: Optional[str] = None
    """for example ``_etc``

    :see: `lib/base/configobject.ti L70 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L70>`__"""

    templates: Optional[Sequence[str]] = None
    """:see: `lib/base/configobject.ti L71 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L71>`__"""

    source_location: Optional[SourceLocation] = None
    """
    :see: `lib/base/configobject.ti L72-L74 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L72-L74>`__
    """

    active: Optional[bool] = None
    """:see: `lib/base/configobject.ti L75 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L75>`__"""

    paused: Optional[bool] = None
    """:see: `lib/base/configobject.ti L76-L78 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L76-L78>`__"""

    ha_mode: Optional[HAMode] = None
    """:see: `lib/base/configobject.ti L83 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L83>`__"""

    original_attributes: Optional[dict[str, Any]] = None
    """:see: `lib/base/configobject.ti L87 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L87>`__"""

    version: Optional[float] = None
    """:see: `lib/base/configobject.ti L88-L90 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L88-L90>`__"""


@dataclass(config={"extra": "forbid"})
class CustomVarObject(ConfigObject):
    """
    :see: `lib/icinga/customvarobject.ti L10 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/customvarobject.ti#L10>`__
    """

    vars: Optional[dict[str, Any]] = None
    """
    :see: `lib/icinga/customvarobject.ti L12 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/customvarobject.ti#L12>`__
    """


@dataclass(config={"extra": "forbid"})
class Checkable(CustomVarObject):
    """
    :see: `lib/icinga/checkable.ti <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/checkable.ti>`__
    """

    check_command: Optional[str] = None
    """
    The name of the check command.

    :see: `doc/09-object-types.md L717 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L717>`__
    """

    max_check_attempts: Optional[int] = None
    """
    The float of times a service is re-checked before changing into a hard state. Defaults to 3.

    :see: `doc/09-object-types.md L718 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L718>`__
    """

    check_period: Optional[str] = None
    """
    The name of a time period which determines when this service should be checked. Not set by default (effectively 24x7).

    :see: `doc/09-object-types.md L719 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L719>`__

    """

    check_timeout: Optional[Value] = None
    """
    Check command timeout in seconds. Overrides the CheckCommand's `timeout` attribute.

    :see: `doc/09-object-types.md L720 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L720>`__
    """

    check_interval: Optional[float] = None
    """
    The check interval (in seconds). This interval is used for checks when the service is in a `HARD` state. Defaults to `5m`.

    :see: `doc/09-object-types.md L721 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L721>`__
    """

    retry_interval: Optional[float] = None
    """
    This interval is used for checks when the service is in a `SOFT` state. Defaults to `1m`. Note: This does not affect the scheduling `after a passive check result <08-advanced-topics.md#check-result-freshness>`__.
    """

    event_command: Optional[str] = None

    volatile: Optional[bool] = None

    enable_active_checks: Optional[bool] = None

    enable_passive_checks: Optional[bool] = None

    enable_event_handler: Optional[bool] = None

    enable_notifications: Optional[bool] = None

    enable_flapping: Optional[bool] = None

    enable_perfdata: Optional[bool] = None

    flapping_ignore_states: Optional[Sequence[str]] = None

    flapping_threshold: Optional[float] = None
    """
    deprecated
    """
    flapping_threshold_low: Optional[float] = None

    flapping_threshold_high: Optional[float] = None

    notes: OptionalStr = None
    """ Optional. Notes for the checkable."""

    notes_url: OptionalStr = None
    """Optional. URL for notes for the checkable (for example, in notification commands)."""

    action_url: OptionalStr = None
    """Optional. URL for actions for the checkable (for example, an external graphing tool)."""

    icon_image: OptionalStr = None
    """Optional. Icon image for the checkable. Used by external interfaces only."""

    icon_image_alt: OptionalStr = None
    """Optional. Icon image description for the checkable. Used by external interface only."""

    next_check: Optional[Timestamp] = None

    check_attempt: Optional[int] = None

    state_type: Optional[StateType] = None

    last_state_type: Optional[StateType] = None

    last_reachable: Optional[bool] = None

    last_check_result: Optional[CheckResult] = None

    last_state_change: Optional[Timestamp] = None

    last_hard_state_change: Optional[Timestamp] = None

    last_state_unreachable: Optional[Timestamp] = None

    previous_state_change: Optional[Timestamp] = None

    severity: Optional[int] = None

    problem: Optional[bool] = None

    handled: Optional[bool] = None

    next_update: Optional[Timestamp] = None

    force_next_check: Optional[bool] = None

    acknowledgement: Optional[int] = None

    acknowledgement_expiry: Optional[Timestamp] = None

    acknowledgement_last_change: Optional[Timestamp] = None

    force_next_notification: Optional[bool] = None

    last_check: Optional[Timestamp] = None

    downtime_depth: Optional[int] = None

    flapping_current: Optional[float] = None

    flapping_last_change: Optional[Timestamp] = None

    flapping: Optional[bool] = None

    command_endpoint: Optional[str] = None

    executions: Optional[Dictionary] = None


########################################################################################
# The individual object types
########################################################################################

########################################################################################
# Monitoring Objects
########################################################################################


@dataclass(config={"extra": "forbid"})
class ApiUser(ConfigObject):
    """
    ApiUser objects are used for authentication against the `Icinga 2 API <12-icinga2-api.md#icinga2-api-authentication>`__.


    .. code-block::

        object ApiUser "root" {
            password = "mysecretapipassword"
            permissions = [ "*" ]
        }

    .. tags:: Object type, Monitoring object type

    https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#apiuser
    :see: `lib/remote/apiuser.ti <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/remote/apiuser.ti>`__
    :see: `doc/09-object-types.md L41-L63 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L41-L63>`__
    """

    password: Optional[str] = None
    """
    Password string. Note: This attribute is hidden in API responses.

    :see: `lib/remote/apiuser.ti L14 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/remote/apiuser.ti#L14>`__
    """

    client_cn: Optional[str] = None
    """
    Client Common Name (CN).

    .. tags:: config

    :see: `lib/remote/apiuser.ti L16 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/remote/apiuser.ti#L16>`__
    """

    permissions: Optional[Sequence[str]] = None
    """
    Array of permissions. Either as string or dictionary with the keys `permission` and `filter`. The latter must be specified as function.

    .. tags:: config

    :see: `lib/remote/apiuser.ti L17 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/remote/apiuser.ti#L17>`__
    :see: `lib/remote/apiuser.ti L21-L28 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/remote/apiuser.ti#L21-L28>`__
    """


@dataclass(config={"extra": "forbid"})
class Function:
    """
    https://github.com/Icinga/icinga2/blob/c0b047b1aab6de3c5e51fdeb63d3bf4236f7fa6d/lib/base/function.ti#L10-L16
    """

    type: str
    name: str
    side_effect_free: bool
    deprecated: bool
    arguments: Sequence[str]


@dataclass(config={"extra": "forbid"})
class CheckCommandArguments:
    """
    Command arguments can be defined as key-value-pairs in the `arguments`
    dictionary. Best practice is to assign a dictionary as value which
    provides additional details such as the `description` next to the `value`.

    Example

    .. code-block::

        arguments = {
            "--parameter" = {
                description = "..."
                value = "..."
            }
        }

    .. tags:: Object type, Monitoring object type

    :see: `doc/09-object-types.md L117-L150 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L117-L150>`__
    :see: `lib/icinga/command.ti L30-L46 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/command.ti#L30-L46>`__
    :see: `lib/icinga/command.ti L33-L45 <https://github.com/Icinga/icinga2/blob/c0b047b1aab6de3c5e51fdeb63d3bf4236f7fa6d/lib/icinga/command.ti#L33-L45>`__
    """

    key: Optional[str] = None
    value: Optional[str | Function | Any] = None
    description: Optional[str] = None
    required: Optional[bool] = None
    skip_key: Optional[bool] = None
    repeat_key: Optional[bool] = None
    set_if: Optional[str | Function] = None
    order: Optional[float] = None
    separator: Optional[str] = None


@dataclass(config={"extra": "forbid"})
class CheckCommand(CustomVarObject):
    """
    A check command definition. Additional default command custom variables can be
    defined here.

    Example

    .. code-block::

        object CheckCommand "http" {
            command = [ PluginDir + "/check_http" ]

            arguments = {
                "-H" = "$http_vhost$"
                "-I" = "$http_address$"
                "-u" = "$http_uri$"
                "-p" = "$http_port$"
                "-S" = {
                    set_if = "$http_ssl$"
                }
                "--sni" = {
                    set_if = "$http_sni$"
                }
                "-a" = {
                    value = "$http_auth_pair$"
                    description = "Username:password on sites with basic authentication"
                }
                "--no-body" = {
                    set_if = "$http_ignore_body$"
                }
                "-r" = "$http_expect_body_regex$"
                "-w" = "$http_warn_time$"
                "-c" = "$http_critical_time$"
                "-e" = "$http_expect$"
            }

            vars.http_address = "$address$"
            vars.http_ssl = false
            vars.http_sni = false
        }

    https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#checkcommand
    :see: `doc/09-object-types.md L65-L114 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L65-L114>`__
    :see: `lib/icinga/command.ti <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/command.ti>`__

    .. tags:: Object type, Monitoring object type
    """

    timeout: Optional[int] = None
    """
    **Optional.** The command timeout in seconds.  Defaults to `1m`.

    https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/command.ti#L15-L17
    """

    execute: Optional[Union[str, Function]] = None
    """
    https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/command.ti#L19
    """

    command: Optional[Union[Sequence[str], Payload]] = None
    """
    **Required.** The command. This can either be an array of individual
    command arguments. Alternatively a string can be specified in which case
    the shell interpreter (usually /bin/sh) takes care of parsing the command.
    When using the "arguments" attribute this must be an array. Can be specified
    as function for advanced implementations.

    https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/command.ti#L25-L28
    """

    arguments: Optional[
        Union[dict[str, Union[CheckCommandArguments, str, Sequence[str], Payload]], str]
    ] = None
    """
    **Optional.** A dictionary of command arguments.

    https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/command.ti#L30-L46
    """

    env: Optional[Any] = None
    """
    **Optional.** A dictionary of macros which should be exported as environment variables prior to executing the command.

    https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/command.ti#L48-L51
    """

    vars: dict[str, Any] | None = None
    """**Optional.** A dictionary containing custom variables that are specific to this command."""


@dataclass(config={"extra": "forbid"})
class Dependency:
    """
    Dependency objects are used to specify dependencies between hosts and services. Dependencies
    can be defined as Host-to-Host, Service-to-Service, Service-to-Host, or Host-to-Service
    relations.

    Service-to-Service Example:

    .. code-block::

        object Dependency "webserver-internet" {
            parent_host_name = "internet"
            parent_service_name = "ping4"

            child_host_name = "webserver"
            child_service_name = "ping4"

            states = [ OK, Warning ]

            disable_checks = true
        }

    Host-to-Host Example:

    .. code-block::

        object Dependency "webserver-internet" {
            parent_host_name = "internet"

            child_host_name = "webserver"

            states = [ Up ]

            disable_checks = true
        }

    https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#dependency
    :see: `doc/09-object-types.md L153-L258 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L153-L258>`__

    .. tags:: Object type, Monitoring object type
    """

    parent_host_name: Optional[str] = None
    """Required. The parent host."""

    parent_service_name: Optional[str] = None
    """Optional. The parent service. If omitted, this dependency object is
    treated as host dependency."""

    child_host_name: Optional[str] = None
    """Required. The child host."""

    child_service_name: Optional[str] = None
    """Optional. The child service. If omitted, this dependency object is
    treated as host dependency."""

    redundancy_group: Optional[str] = None
    """Optional. Puts the dependency into a group of mutually redundant
    ones."""

    disable_checks: Optional[bool] = None

    """Optional. Whether to disable checks (i.e., don’t schedule active checks
    and drop passive results) when this dependency fails. Defaults to false."""

    disable_notifications: Optional[bool] = None
    """Optional. Whether to disable notifications when this dependency fails.
    Defaults to true."""

    ignore_soft_states: Optional[bool] = None
    """Optional. Whether to ignore soft states for the reachability calculation.
    Defaults to true."""

    period: Optional[str] = None
    """Optional. Time period object during which this dependency is enabled."""

    states: Optional[Sequence[str]] = None
    """Optional. A list of state filters when this dependency should be OK.
    Defaults to [ OK, Warning ] for services and [ Up ] for hosts."""


@dataclass(config={"extra": "forbid"})
class Endpoint:
    """
    Endpoint objects are used to specify connection information for remote
    Icinga 2 instances.

    Example

    .. code-block::

        object Endpoint "icinga2-agent1.localdomain" {
            host = "192.168.56.111"
            port = 5665
            log_duration = 1d
        }

    Example (disable replay log):

    .. code-block::

        object Endpoint "icinga2-agent1.localdomain" {
            host = "192.168.5.111"
            port = 5665
            log_duration = 0
        }

    https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#endpoint
    :see: `doc/09-object-types.md L260-L293 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L260-L293>`__

    .. tags:: Object type, Monitoring object type
    """


@dataclass(config={"extra": "forbid"})
class EventCommand:
    """
    An event command definition.

    .. code-block::

        object EventCommand "restart-httpd-event" {
            command = "/opt/bin/restart-httpd.sh"
        }


    https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#eventcommand
    :see: `doc/09-object-types.md L295-L320 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L295-L320>`__

    .. tags:: Object type, Monitoring object type
    """


@dataclass(config={"extra": "forbid"})
class Host(Checkable):
    """
    A host.

    .. code-block::

        object Host "icinga2-agent1.localdomain" {
            display_name = "Linux Client 1"
            address = "192.168.56.111"
            address6 = "2a00:1450:4001:815::2003"

            groups = [ "linux-servers" ]

            check_command = "hostalive"
        }

    :see: `Icinga2 documentation: Host <https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#host>`__
    :see: `doc/09-object-types.md L323-L413 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L323-L413>`__
    :see: `lib/icinga/host.ti <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/host.ti>`__

    .. tags:: Object type, Monitoring object type
    """

    groups: Optional[Sequence[str]] = None
    """

     A list of host groups this host belongs to.

     :see: `lib/icinga/host.ti L18-L20 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/host.ti#L18-L20>`__
    """

    display_name: Optional[str] = None
    """
    A short description of the host (e.g. displayed by external interfaces instead of the name if set).

    :see: `lib/icinga/host.ti L22-L30 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/host.ti#L22-L30>`__
    """

    address: Optional[str] = None
    """
    The host's IPv4 address. Available as command runtime macro ``$address$`` if set.

    :see: `lib/icinga/host.ti L32 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/host.ti#L32>`__
    """

    address6: Optional[str] = None
    """
    The host's IPv6 address. Available as command runtime macro ``$address6$`` if set.

    :see: `lib/icinga/host.ti L33 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/host.ti#L33>`__
    """

    state: Optional[HostState] = None
    """

    The current state (0 = UP, 1 = DOWN).

    :see: `lib/icinga/host.ti L35-L37 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/host.ti#L35-L37>`__
    """

    last_state: Optional[HostState] = None
    """
    The previous state (0 = UP, 1 = DOWN).

    :see: `lib/icinga/host.ti L38-L40 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/host.ti#L38-L40>`__
    """

    last_hard_state: Optional[HostState] = None
    """
    The last hard state (0 = UP, 1 = DOWN).

    :see: `lib/icinga/host.ti L41-L43 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/host.ti#L41-L43>`__
    """

    last_state_up: Optional[Timestamp] = None
    """
    When the last UP state occurred (as a UNIX timestamp).

    :see: `lib/icinga/host.ti L44 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/host.ti#L44>`__
    """

    last_state_down: Optional[Timestamp] = None
    """
    When the last DOWN state occurred (as a UNIX timestamp).

    :see: `lib/icinga/host.ti L45 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/host.ti#L45>`__
    """


@dataclass(config={"extra": "forbid"})
class HostGroup:
    """
    A group of hosts.

    .. code-block::

        object HostGroup "linux-servers" {
            display_name = "Linux Servers"

            assign where host.vars.os == "Linux"
        }

    https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#hostgroup
    :see: `doc/09-object-types.md L417-L440 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L417-L440>`__

    .. tags:: Object type, Monitoring object type
    """


@dataclass(config={"extra": "forbid"})
class Notification:
    """
    Notification objects are used to specify how users should be notified in case
    of host and service state changes and other events.

    Example:

    .. code-block::

        object Notification "localhost-ping-notification" {
            host_name = "localhost"
            service_name = "ping4"

            command = "mail-notification"

            users = [ "user1", "user2" ] // reference to User objects

            types = [ Problem, Recovery ]
            states = [ Critical, Warning, OK ]
        }

    https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#notification
    :see: `doc/09-object-types.md L444-L527 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L444-L527>`__

    .. tags:: Object type, Monitoring object type
    """


@dataclass(config={"extra": "forbid"})
class NotificationCommand:
    """
    A notification command definition.

    .. code-block::

        object NotificationCommand "mail-service-notification" {
            command = [ ConfigDir + "/scripts/mail-service-notification.sh" ]

            arguments += {
                "-4" = {
                    required = true
                    value = "$notification_address$"
                }
                "-6" = "$notification_address6$"
                "-b" = "$notification_author$"
                "-c" = "$notification_comment$"
                "-d" = {
                    required = true
                    value = "$notification_date$"
                }
                "-e" = {
                    required = true
                    value = "$notification_servicename$"
                }
                "-f" = {
                    value = "$notification_from$"
                    description = "Set from address. Requires GNU mailutils (Debian/Ubuntu) or mailx (RHEL/SUSE)"
                }
                "-i" = "$notification_icingaweb2url$"
                "-l" = {
                    required = true
                    value = "$notification_hostname$"
                }
                "-n" = {
                    required = true
                    value = "$notification_hostdisplayname$"
                }
                "-o" = {
                    required = true
                    value = "$notification_serviceoutput$"
                }
                "-r" = {
                    required = true
                    value = "$notification_useremail$"
                }
                "-s" = {
                    required = true
                    value = "$notification_servicestate$"
                }
                "-t" = {
                    required = true
                    value = "$notification_type$"
                }
                "-u" = {
                    required = true
                    value = "$notification_servicedisplayname$"
                }
                "-v" = "$notification_logtosyslog$"
            }

            vars += {
                notification_address = "$address$"
                notification_address6 = "$address6$"
                notification_author = "$notification.author$"
                notification_comment = "$notification.comment$"
                notification_type = "$notification.type$"
                notification_date = "$icinga.long_date_time$"
                notification_hostname = "$host.name$"
                notification_hostdisplayname = "$host.display_name$"
                notification_servicename = "$service.name$"
                notification_serviceoutput = "$service.output$"
                notification_servicestate = "$service.state$"
                notification_useremail = "$user.email$"
                notification_servicedisplayname = "$service.display_name$"
            }
        }

    https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#notificationcommand
    :see: `doc/09-object-types.md L530-L622 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L530-L622>`__

    .. tags:: Object type, Monitoring object type
    """


@dataclass(config={"extra": "forbid"})
class ScheduledDowntime:
    """
    ScheduledDowntime objects can be used to set up recurring downtimes for hosts/services.

    Example:

    .. code-block::


        object ScheduledDowntime "some-downtime" {
            host_name = "localhost"
            service_name = "ping4"

            author = "icingaadmin"
            comment = "Some comment"

            fixed = false
            duration = 30m

            ranges = {
                "sunday" = "02:00-03:00"
            }
        }

    https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#scheduleddowntime
    :see: `doc/09-object-types.md L624-L674 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L624-L674>`__

    .. tags:: Object type, Monitoring object type
    """


@dataclass(config={"extra": "forbid"})
class Service(Checkable):
    """
    Service objects describe network services and how they should be checked
    by Icinga 2.

    Best Practice

    Rather than creating a ``Service`` object for a specific host it is usually easier
    to just create a ``Service`` template and use the ``apply`` keyword to assign the
    service to a float of hosts.
    Check the `apply <03-monitoring-basics.md#using-apply>`__ chapter for details.

    Example:

    .. code-block::


        object Service "uptime" {
            host_name = "localhost"

            display_name = "localhost Uptime"

            check_command = "snmp"

            vars.snmp_community = "public"
            vars.snmp_oid = "DISMAN-EVENT-MIB::sysUpTimeInstance"

            check_interval = 60s
            retry_interval = 15s

            groups = [ "all-services", "snmp" ]
        }

    .. tags:: Object type, Monitoring object type

    https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#service
    :see: `lib/icinga/service.ti <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/service.ti>`__
    :see: `doc/09-object-types.md L677-L781 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L677-L781>`__
    """

    groups: Optional[Sequence[str]] = None
    """
    The service groups this service belongs to.
    """

    display_name: Optional[str] = None
    """
    A short description of the service.

    :see: `doc/09-object-types.md L712 <https://github.com/Icinga/icinga2/blob/0951230ce1be27c9957ef8801be258524524dc01/doc/09-object-types.md?plain=1#L712>`__
    :see: `lib/icinga/service.ti L34-L42 <https://github.com/Icinga/icinga2/blob/0951230ce1be27c9957ef8801be258524524dc01/lib/icinga/service.ti#L34-L42>`__
    """

    host_name: Optional[str] = None
    """
    The host this service belongs to. There must be a `Host` object with that name.
    """

    host: Optional[Host] = None

    state: Optional[ServiceState] = None
    """
    The current state (0 = OK, 1 = WARNING, 2 = CRITICAL, 3 = UNKNOWN).
    """

    last_state: Optional[ServiceState] = None
    """
    The previous state (0 = OK, 1 = WARNING, 2 = CRITICAL, 3 = UNKNOWN).
    """

    last_hard_state: Optional[ServiceState] = None
    """
    The last hard state (0 = OK, 1 = WARNING, 2 = CRITICAL, 3 = UNKNOWN).
    """

    last_state_ok: Optional[Timestamp] = None
    """
    When the last OK state occurred (as a UNIX timestamp).
    """

    last_state_warning: Optional[Timestamp] = None
    """
    When the last WARNING state occurred (as a UNIX timestamp).
    """

    last_state_critical: Optional[Timestamp] = None
    """
    When the last CRITICAL state occurred (as a UNIX timestamp).
    """

    last_state_unknown: Optional[Timestamp] = None
    """
    When the last UNKNOWN state occurred (as a UNIX timestamp).
    """


@dataclass(config={"extra": "forbid"})
class ServiceGroup:
    """
    A group of services.

    Example:

    .. code-block::

        object ServiceGroup "snmp" {
            display_name = "SNMP services"
        }

    https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#servicegroup
    :see: `doc/09-object-types.md L784-L805 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L784-L805>`__

    .. tags:: Object type, Monitoring object type
    """


@dataclass(config={"extra": "forbid"})
class TimePeriodSegment:
    """
    :see: `lib/icinga/timeperiod.cpp L84-L87 <https://github.com/Icinga/icinga2/blob/c0b047b1aab6de3c5e51fdeb63d3bf4236f7fa6d/lib/icinga/timeperiod.cpp#L84-L87>`__
    """

    begin: int

    end: int


@dataclass(config={"extra": "forbid"})
class TimePeriod(CustomVarObject):
    """
    Time periods can be used to specify when hosts/services should be checked or to limit
    when notifications should be sent out.

    Examples:

    .. code-block::

        object TimePeriod "nonworkhours" {
            display_name = "Icinga 2 TimePeriod for non working hours"

            ranges = {
                monday = "00:00-8:00,17:00-24:00"
                tuesday = "00:00-8:00,17:00-24:00"
                wednesday = "00:00-8:00,17:00-24:00"
                thursday = "00:00-8:00,17:00-24:00"
                friday = "00:00-8:00,16:00-24:00"
                saturday = "00:00-24:00"
                sunday = "00:00-24:00"
            }
        }

    .. code-block::

        object TimePeriod "exampledays" {
            display_name = "Icinga 2 TimePeriod for random example days"

            ranges = {
                //We still believe in Santa, no peeking!
                //Applies every 25th of December every year
                "december 25" = "00:00-24:00"

                //Any point in time can be specified,
                //but you still have to use a range
                "2038-01-19" = "03:13-03:15"

                //Evey 3rd day from the second monday of February
                //to 8th of November
                "monday 2 february - november 8 / 3" = "00:00-24:00"
            }
        }

    Additional examples can be found `here <08-advanced-topics.md#timeperiods>`__.

    .. tags:: Object type, Monitoring object type

    https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#timeperiod
    :see: `doc/09-object-types.md L809-L869 <https://github.com/Icinga/icinga2/blob/4c6b93d61775ff98fc671b05ad4de2b62945ba6a/doc/09-object-types.md?plain=1#L807-L867>`__
    :see: `lib/icinga/timeperiod.ti L11-L39 <https://github.com/Icinga/icinga2/blob/894d6aa290e83797d001fcc2887611b23707dbf9/lib/icinga/timeperiod.ti#L11-L39>`__
    """

    display_name: Optional[str] = None
    """
    A short description of the time period.

    :see: `lib/icinga/timeperiod.ti L13-L21 <https://github.com/Icinga/icinga2/blob/894d6aa290e83797d001fcc2887611b23707dbf9/lib/icinga/timeperiod.ti#L13-L21>`__
    """

    ranges: Optional[dict[str, str]] = None
    """
    A dictionary containing information which days and durations apply to this timeperiod.

    :see: `lib/icinga/timeperiod.ti L22 <https://github.com/Icinga/icinga2/blob/894d6aa290e83797d001fcc2887611b23707dbf9/lib/icinga/timeperiod.ti#L22>`__
    """

    update: Optional[Payload] = None
    """
    :see: `lib/icinga/timeperiod.ti L23 <https://github.com/Icinga/icinga2/blob/894d6aa290e83797d001fcc2887611b23707dbf9/lib/icinga/timeperiod.ti#L23>`__
    """

    prefer_includes: Optional[bool] = None
    """
    Whether to prefer timeperiods ``includes`` or ``excludes``. Default to true.

    :see: `lib/icinga/timeperiod.ti L24-L26 <https://github.com/Icinga/icinga2/blob/894d6aa290e83797d001fcc2887611b23707dbf9/lib/icinga/timeperiod.ti#L24-L26>`__
    """

    excludes: Optional[Sequence[str]] = None
    """
    An array of timeperiods, which should exclude from your timerange.

    :see: `lib/icinga/timeperiod.ti L27-L29 <https://github.com/Icinga/icinga2/blob/894d6aa290e83797d001fcc2887611b23707dbf9/lib/icinga/timeperiod.ti#L27-L29>`__
    """

    includes: Optional[Sequence[str]] = None
    """
    An array of timeperiods, which should include into your timerange.

    :see: `lib/icinga/timeperiod.ti L30-L32 <https://github.com/Icinga/icinga2/blob/894d6aa290e83797d001fcc2887611b23707dbf9/lib/icinga/timeperiod.ti#L30-L32>`__
    """

    valid_begin: Optional[Timestamp] = None
    """
    :see: `lib/icinga/timeperiod.ti L33 <https://github.com/Icinga/icinga2/blob/894d6aa290e83797d001fcc2887611b23707dbf9/lib/icinga/timeperiod.ti#L33>`__
    """

    valid_end: Optional[Timestamp] = None
    """
    :see: `lib/icinga/timeperiod.ti L34 <https://github.com/Icinga/icinga2/blob/894d6aa290e83797d001fcc2887611b23707dbf9/lib/icinga/timeperiod.ti#L34>`__
    """

    segments: Optional[Sequence[TimePeriodSegment]] = None
    """
    :see: `lib/icinga/timeperiod.ti L35 <https://github.com/Icinga/icinga2/blob/894d6aa290e83797d001fcc2887611b23707dbf9/lib/icinga/timeperiod.ti#L35>`__
    """

    is_inside: Optional[bool] = None
    """
    :see: `lib/icinga/timeperiod.ti L36-L38 <https://github.com/Icinga/icinga2/blob/894d6aa290e83797d001fcc2887611b23707dbf9/lib/icinga/timeperiod.ti#L36-L38>`__
    """


@dataclass(config={"extra": "forbid"})
class User(CustomVarObject):
    """A user.

    Example:

    .. code-block::

        object User "icingaadmin" {
            display_name = "Icinga 2 Admin"
            groups = [ "icingaadmins" ]
            email = "icinga@localhost"
            pager = "icingaadmin@localhost.localdomain"

            period = "24x7"

            states = [ OK, Warning, Critical, Unknown ]
            types = [ Problem, Recovery ]

            vars.additional_notes = "This is the Icinga 2 Admin account."
        }


    Available notification state filters:

    .. code-block::

        OK
        Warning
        Critical
        Unknown
        Up
        Down


    Available notification type filters:

    .. code-block::

        DowntimeStart
        DowntimeEnd
        DowntimeRemoved
        Custom
        Acknowledgement
        Problem
        Recovery
        FlappingStart
        FlappingEnd

    .. tags:: Object type, Monitoring object type

    https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#user
    :see: `lib/icinga/user.ti <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/user.ti>`__
    :see: `doc/09-object-types.md L872-L937 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L872-L937>`__
    """

    display_name: Optional[str] = None
    """
    A short description of the user.

    :see: `lib/icinga/user.ti L14-L22 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/user.ti#L14-L22>`__
    :see: `doc/09-object-types.md L923 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L923>`__

    """

    groups: Optional[Sequence[str]] = None
    """
    An array of group names.

    :see: `lib/icinga/user.ti L23-L25 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/user.ti#L23-L25>`__
    :see: `doc/09-object-types.md L927 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L927>`__

    """

    period: Optional[str] = None
    """
    The name of a time period which determines when a notification for this user should be triggered. Not set by default (effectively 24x7).

    :see: `lib/icinga/user.ti L26-L30 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/user.ti#L26-L30>`__
    :see: `doc/09-object-types.md L929 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L929>`__

    """

    types: Optional[Sequence[str]] = None
    """
    A set of type filters when a notification for this user should be triggered. By default everything is matched.

    :see: `lib/icinga/user.ti L32 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/user.ti#L32>`__
    :see: `doc/09-object-types.md L930 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L930>`__

    """

    states: Optional[Sequence[str]] = None
    """
    A set of state filters when a notification for this should be triggered. By default everything is matched.

    :see: `lib/icinga/user.ti L34 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/user.ti#L34>`__
    :see: `doc/09-object-types.md L931 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L931>`__

    """

    email: Optional[str] = None
    """
    An email string for this user. Useful for notification commands.

    :see: `lib/icinga/user.ti L37 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/user.ti#L37>`__
    :see: `doc/09-object-types.md L924 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L924>`__

    """

    pager: Optional[str] = None
    """
    A pager str for this user. Useful for notification commands.

    :see: `lib/icinga/user.ti L38 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/user.ti#L38>`__
    :see: `doc/09-object-types.md L925 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L925>`__

    """

    enable_notifications: Optional[bool] = None
    """
    Whether notifications are enabled for this user. Defaults to true.

    :see: `lib/icinga/user.ti L40-L42 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/user.ti#L40-L42>`__
    :see: `doc/09-object-types.md L928 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L928>`__

    """

    last_notification: Optional[float] = None
    """
    When the last notification was sent for this user (as a UNIX timestamp).

    :see: `lib/icinga/user.ti L44 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/user.ti#L44>`__
    :see: `doc/09-object-types.md L937 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L937>`__

    """


@dataclass(config={"extra": "forbid"})
class UserGroup(CustomVarObject):
    """
    A user group.

    Example:

    .. code-block::

        object UserGroup "icingaadmins" {
            display_name = "Icinga 2 Admin Group"
        }

    .. tags:: Object type, Monitoring object type

    https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#usergroup
    :see: `doc/09-object-types.md L939-L960 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L939-L960>`__
    https://github.com/Icinga/icinga2/blob/c0b047b1aab6de3c5e51fdeb63d3bf4236f7fa6d/lib/icinga/usergroup.ti#L10-L23
    """

    display_name: OptionalStr = None
    """Optional. A short description of the user group."""

    groups: Optional[Sequence[str]] = None
    """Optional. An array of nested group names."""


@dataclass(config={"extra": "forbid"})
class Zone(ConfigObject):
    """
    Zone objects are used to specify which Icinga 2 instances are located in a zone.

    Example:

    .. code-block::

        object Zone "master" {
            endpoints = [ "icinga2-master1.localdomain", "icinga2-master2.localdomain" ]
        }

        object Zone "satellite" {
            endpoints = [ "icinga2-satellite1.localdomain" ]
            parent = "master"
        }

    .. tags:: Object type, Monitoring object type

    https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#zone
    :see: `doc/09-object-types.md L963-L989 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L963-L989>`__
    https://github.com/Icinga/icinga2/blob/c0b047b1aab6de3c5e51fdeb63d3bf4236f7fa6d/lib/remote/zone.ti#L10-L23
    """

    endpoints: Optional[Sequence[str]] = None
    """Optional. Array of endpoint names located in this zone."""

    parent: OptionalStr = None
    """Optional. The name of the parent zone. (Do not specify a global zone)"""

    all_parents: Optional[Sequence[str]] = None

    is_global: Optional[bool] = None
    """Optional. Whether configuration files for this zone should be synced to all endpoints. Defaults to false."""


########################################################################################
# Runtime Objects
########################################################################################


@dataclass(config={"extra": "forbid"})
class Comment:
    """
    .. tags:: Object type, Runtime object type
    """


@dataclass(config={"extra": "forbid"})
class Downtime:
    """
    .. tags:: Object type, Runtime object type
    """


########################################################################################
# Features
########################################################################################


@dataclass(config={"extra": "forbid"})
class ApiListener:
    """
    .. tags:: Object type, Feature object type
    """


@dataclass(config={"extra": "forbid"})
class CheckerComponent:
    """
    .. tags:: Object type, Feature object type
    """


@dataclass(config={"extra": "forbid"})
class CompatLogger:
    """
    .. tags:: Object type, Feature object type
    """


@dataclass(config={"extra": "forbid"})
class ElasticsearchWriter:
    """
    .. tags:: Object type, Feature object type
    """


@dataclass(config={"extra": "forbid"})
class ExternalCommandListener:
    """
    .. tags:: Object type, Feature object type
    """


@dataclass(config={"extra": "forbid"})
class FileLogger:
    """
    .. tags:: Object type, Feature object type
    """


@dataclass(config={"extra": "forbid"})
class GelfWriter:
    """
    .. tags:: Object type, Feature object type
    """


@dataclass(config={"extra": "forbid"})
class GraphiteWriter:
    """
    .. tags:: Object type, Feature object type
    """


@dataclass(config={"extra": "forbid"})
class IcingaApplication:
    """
    .. tags:: Object type, Feature object type
    """


@dataclass(config={"extra": "forbid"})
class IcingaDB:
    """
    .. tags:: Object type, Feature object type
    """


@dataclass(config={"extra": "forbid"})
class IdoMySqlConnection:
    """
    .. tags:: Object type, Feature object type
    """


@dataclass(config={"extra": "forbid"})
class IdoPgsqlConnection:
    """
    .. tags:: Object type, Feature object type
    """


@dataclass(config={"extra": "forbid"})
class InfluxdbWriter:
    """
    .. tags:: Object type, Feature object type
    """


@dataclass(config={"extra": "forbid"})
class Influxdb2Writer:
    """
    .. tags:: Object type, Feature object type
    """


@dataclass(config={"extra": "forbid"})
class JournaldLogger:
    """
    .. tags:: Object type, Feature object type
    """


@dataclass(config={"extra": "forbid"})
class LiveStatusListener:
    """
    .. tags:: Object type, Feature object type
    """


@dataclass(config={"extra": "forbid"})
class NotificationComponent:
    """
    .. tags:: Object type, Feature object type
    """


@dataclass(config={"extra": "forbid"})
class OpenTsdbWriter:
    """
    .. tags:: Object type, Feature object type
    """


@dataclass(config={"extra": "forbid"})
class PerfdataWriter:
    """
    .. tags:: Object type, Feature object type
    """


@dataclass(config={"extra": "forbid"})
class SyslogLogger:
    """
    .. tags:: Object type, Feature object type
    """


@dataclass(config={"extra": "forbid"})
class WindowsEventLogLogger:
    """
    .. tags:: Object type, Feature object type
    """
