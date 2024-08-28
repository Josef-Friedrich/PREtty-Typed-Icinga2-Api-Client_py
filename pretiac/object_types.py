"""
Listed in the order as in this `Markdown document <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md>`__
"""

from collections.abc import Sequence
from enum import Enum, auto
from typing import (
    Any,
    Literal,
    Optional,
    Union,
)

MonitoringObjectName = Literal[
    "ApiUser",
    "CheckCommand",
    "CheckCommandArguments",
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


Payload = dict[str, Any]

FilterVars = Optional[Payload]

RequestMethod = Literal["GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"]
"""
https://github.com/psf/requests/blob/a3ce6f007597f14029e6b6f54676c34196aa050e/src/requests/api.py#L17

https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
"""


# /***************************************************************************
#  * Delegated interfaces and types
#  **************************************************************************/


class SourceLocation:
    first_column: int
    first_line: int
    last_column: int
    last_line: int

    path: int
    """
    ``/etc/icinga2-custom/conf.d/api-users.conf``
    """


class HAMode(Enum):
    """:see: `lib/base/configobject.ti L12-L16 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L12-L16>`__"""

    HARunOnce = auto()
    HARunEverywhere = auto()


# /**
#  * :see: `lib/icinga/checkresult.ti L38-L43 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/checkresult.ti#L38-L43>`__
#  */
# export enum StateType {
#   StateTypeSoft = 0,
#   StateTypeHard = 1
# }

# export interface Dictionary {}

# /**
#  * for example `1699475880.364077`
#  */
# export type TimeStamp = number

# export type Timestamp = number

# export interface Value {}

# /**
#  * 0=OK, 1=WARNING, 2=CRITICAL, 3=UNKNOWN
#  */
# export type State = 0 | 1 | 2 | 3

# /**
#  * 0=OK, 1=WARNING, 2=CRITICAL, 3=UNKNOWN
#  *
#  * :see: `lib/icinga/checkresult.ti L25-L31 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/checkresult.ti#L25-L31>`__
#  */
# export enum ServiceState {
#   ServiceOK = 0,
#   ServiceWarning = 1,
#   ServiceCritical = 2,
#   ServiceUnknown = 3
# }

# /**
#  * 0=UP, 1=DOWN.
#  */
# export enum HostState {
#   HostUp = 0,
#   HostDown = 1
# }

# export interface CheckResult {}

# /***************************************************************************
#  * Interface from which the object types inherit
#  **************************************************************************/


class ConfigObject:
    """
    :see: `lib/base/configobject.ti L57-L92 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L57-L92>`__
    """

    __name: str
    """:see: `lib/base/configobject.ti L59-L68 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L59-L68>`__"""

    zone: str
    """:see: `lib/base/configobject.ti L69 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L69>`__"""

    package: str
    """for example ``_etc``

    :see: `lib/base/configobject.ti L70 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L70>`__"""

    templates: Sequence[str]
    """:see: `lib/base/configobject.ti L71 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L71>`__"""

    source_location: SourceLocation
    """
    :see: `lib/base/configobject.ti L72-L74 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L72-L74>`__
    """

    active: bool
    """:see: `lib/base/configobject.ti L75 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L75>`__"""

    paused: bool
    """:see: `lib/base/configobject.ti L76-L78 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L76-L78>`__"""

    ha_mode: HAMode
    """:see: `lib/base/configobject.ti L83 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L83>`__"""

    original_attributes: dict[str, Any]
    """:see: `lib/base/configobject.ti L87 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L87>`__"""

    version: float
    """:see: `lib/base/configobject.ti L88-L90 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/base/configobject.ti#L88-L90>`__"""


class CustomVarObject(ConfigObject):
    """
    :see: `lib/icinga/customvarobject.ti L10 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/customvarobject.ti#L10>`__
    """

    vars: dict[str, Any]
    """
    :see: `lib/icinga/customvarobject.ti L12 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/customvarobject.ti#L12>`__
    """


# /**
#  * :see: `lib/icinga/checkable.ti <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/checkable.ti>`__
#  */
# interface Checkable extends CustomVarObject {
#   /**
#    * The name of the check command.
#    *
#    * @group navigation
#    *
#    * :see: `doc/09-object-types.md L717 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L717>`__
#    */
#   check_command: string

#   /**
#    * The number of times a service is re-checked before changing into a hard state. Defaults to 3.
#    *
#    * :see: `doc/09-object-types.md L718 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L718>`__
#    */
#   max_check_attempts: bigint

#   /**
#    * The name of a time period which determines when this service should be checked. Not set by default (effectively 24x7).
#    *
#    * @group navigation
#    *
#    * :see: `doc/09-object-types.md L719 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L719>`__
#    */
#   check_period: string

#   /**
#    * Check command timeout in seconds. Overrides the CheckCommand's `timeout` attribute.
#    *
#    * :see: `doc/09-object-types.md L720 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L720>`__
#    */
#   check_timeout: Value

#   /**
#    * The check interval (in seconds). This interval is used for checks when the service is in a `HARD` state. Defaults to `5m`.
#    *
#    * :see: `doc/09-object-types.md L721 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L721>`__
#    */
#   check_interval: number

#   /**
#    * This interval is used for checks when the service is in a `SOFT` state. Defaults to `1m`. Note: This does not affect the scheduling `after a passive check result <08-advanced-topics.md#check-result-freshness>`__.
#    */
#   retry_interval: number

#   /**
#    * @group navigation
#    */
#   event_command: string

#   volatile: bool

#   enable_active_checks: bool

#   enable_passive_checks: bool

#   enable_event_handler: bool

#   enable_notifications: bool

#   enable_flapping: bool

#   enable_perfdata: bool

#   flapping_ignore_states: string[]

#   /**
#    * @deprecated
#    */
#   flapping_threshold: number

#   flapping_threshold_low: number

#   flapping_threshold_high: number

#   notes: string

#   notes_url: string

#   action_url: string

#   icon_image: string

#   icon_image_alt: string

#   next_check: Timestamp

#   check_attempt: bigint

#   state_type: StateType

#   last_state_type: StateType

#   last_reachable: bool

#   last_check_result: CheckResult

#   last_state_change: Timestamp

#   last_hard_state_change: Timestamp

#   last_state_unreachable: Timestamp

#   previous_state_change: Timestamp

#   severity: bigint

#   problem: bool

#   handled: bool

#   next_update: Timestamp

#   force_next_check: bool

#   acknowledgement: bigint

#   acknowledgement_expiry: Timestamp

#   acknowledgement_last_change: Timestamp

#   force_next_notification: bool

#   last_check: Timestamp

#   downtime_depth: bigint

#   flapping_current: number

#   flapping_last_change: Timestamp

#   flapping: bool

#   /**
#    * @group navigation
#    */
#   command_endpoint: string

#   executions: Dictionary
# }

# export interface CheckableWithRelations
#   extends Omit<
#     Checkable,
#     'check_command' | 'check_period' | 'event_command' | 'command_endpoint'
#   > {
#   check_command?: CheckCommand
#   check_period?: TimePeriod
#   event_command?: EventCommand
#   command_endpoint?: Endpoint
# }

# /***************************************************************************
#  * The individual object types
#  **************************************************************************/

# /***************************************************************************
#  * Monitoring Objects
#  **************************************************************************/

# /**
#  * ApiUser objects are used for authentication against the `Icinga 2 API <12-icinga2-api.md#icinga2-api-authentication>`__.
#  *
#  * @example
#  *
#  * ```
#  * object ApiUser "root" {
#  *   password = "mysecretapipassword"
#  *   permissions = [ "*" ]
#  * }
#  * ```
#  *
#  * @category Object type
#  * @category Monitoring object type
#  *
#  * :see: `lib/remote/apiuser.ti <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/remote/apiuser.ti>`__
#  * :see: `doc/09-object-types.md L41-L63 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L41-L63>`__
#  */
# export interface ApiUser extends ConfigObject {
#   /**
#    * Password string. Note: This attribute is hidden in API responses.
#    *
#    * @group config
#    * :see: `lib/remote/apiuser.ti L14 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/remote/apiuser.ti#L14>`__
#    */
#   password?: string

#   /**
#    * Client Common Name (CN).
#    *
#    * @group config
#    * :see: `lib/remote/apiuser.ti L16 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/remote/apiuser.ti#L16>`__
#    */
#   client_cn?: string

#   /**
#    * Array of permissions. Either as string or dictionary with the keys `permission` and `filter`. The latter must be specified as function.
#    *
#    * @group config
#    * :see: `lib/remote/apiuser.ti L17 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/remote/apiuser.ti#L17>`__
#    * :see: `lib/remote/apiuser.ti L21-L28 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/remote/apiuser.ti#L21-L28>`__
#    */
#   permissions: string[]
# }

# /**
#  * A check command definition. Additional default command custom variables can be
#  * defined here.
#  *
#  * @example
#  *
#  * ```
#  * object CheckCommand "http" {
#  *   command = [ PluginDir + "/check_http" ]
#  *
#  *   arguments = {
#  *     "-H" = "$http_vhost$"
#  *     "-I" = "$http_address$"
#  *     "-u" = "$http_uri$"
#  *     "-p" = "$http_port$"
#  *     "-S" = {
#  *       set_if = "$http_ssl$"
#  *     }
#  *     "--sni" = {
#  *       set_if = "$http_sni$"
#  *     }
#  *     "-a" = {
#  *       value = "$http_auth_pair$"
#  *       description = "Username:password on sites with basic authentication"
#  *     }
#  *     "--no-body" = {
#  *       set_if = "$http_ignore_body$"
#  *     }
#  *     "-r" = "$http_expect_body_regex$"
#  *     "-w" = "$http_warn_time$"
#  *     "-c" = "$http_critical_time$"
#  *     "-e" = "$http_expect$"
#  *   }
#  *
#  *   vars.http_address = "$address$"
#  *   vars.http_ssl = false
#  *   vars.http_sni = false
#  * }
#  * ```
#  *
#  * @category Object type
#  * @category Monitoring object type
#  *
#  * :see: `doc/09-object-types.md L65-L114 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L65-L114>`__
#  * :see: `lib/icinga/command.ti <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/command.ti>`__
#  */
# export interface CheckCommand {}

# /**
#  *
#  * Command arguments can be defined as key-value-pairs in the `arguments`
#  * dictionary. Best practice is to assign a dictionary as value which
#  * provides additional details such as the `description` next to the `value`.
#  *
#  * @example
#  *
#  * ```
#  *   arguments = {
#  *     "--parameter" = {
#  *       description = "..."
#  *       value = "..."
#  *     }
#  *   }
#  * ```
#  *
#  * @category Object type
#  * @category Monitoring object type
#  *
#  * :see: `doc/09-object-types.md L117-L150 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L117-L150>`__
#  * :see: `lib/icinga/command.ti L30-L46 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/command.ti#L30-L46>`__
#  */
# export interface CheckCommandArguments {}

# /**
#  * Dependency objects are used to specify dependencies between hosts and services. Dependencies
#  * can be defined as Host-to-Host, Service-to-Service, Service-to-Host, or Host-to-Service
#  * relations.
#  *
#  * > **Best Practice**
#  * >
#  * > Rather than creating a `Dependency` object for a specific host or service it is usually easier
#  * > to just create a `Dependency` template and use the `apply` keyword to assign the
#  * > dependency to a number of hosts or services. Use the `to` keyword to set the specific target
#  * > type for `Host` or `Service`.
#  * > Check the `dependencies <03-monitoring-basics.md#dependencies>`__ chapter for detailed examples.
#  *
#  * @example Service-to-Service
#  *
#  * ```
#  * object Dependency "webserver-internet" {
#  *   parent_host_name = "internet"
#  *   parent_service_name = "ping4"
#  *
#  *   child_host_name = "webserver"
#  *   child_service_name = "ping4"
#  *
#  *   states = [ OK, Warning ]
#  *
#  *   disable_checks = true
#  * }
#  * ```
#  *
#  * @example Host-to-Host
#  *
#  * ```
#  * object Dependency "webserver-internet" {
#  *   parent_host_name = "internet"
#  *
#  *   child_host_name = "webserver"
#  *
#  *   states = [ Up ]
#  *
#  *   disable_checks = true
#  * }
#  * ```
#  *
#  * @category Object type
#  * @category Monitoring object type
#  *
#  * :see: `doc/09-object-types.md L153-L258 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L153-L258>`__
#  */
# export interface Dependency {}

# /**
#  * Endpoint objects are used to specify connection information for remote
#  * Icinga 2 instances. More details can be found in the `distributed monitoring chapter <06-distributed-monitoring.md#distributed-monitoring>`__.
#  *
#  * @example
#  *
#  * ```
#  * object Endpoint "icinga2-agent1.localdomain" {
#  *   host = "192.168.56.111"
#  *   port = 5665
#  *   log_duration = 1d
#  * }
#  * ```
#  *
#  * @example (disable replay log):
#  *
#  * ```
#  * object Endpoint "icinga2-agent1.localdomain" {
#  *   host = "192.168.5.111"
#  *   port = 5665
#  *   log_duration = 0
#  * }
#  * ```
#  *
#  * @category Object type
#  * @category Monitoring object type
#  *
#  * :see: `doc/09-object-types.md L260-L293 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L260-L293>`__
#  */
# export interface Endpoint {}

# /**
#  * An event command definition.
#  *
#  * @example
#  *
#  * ```
#  * object EventCommand "restart-httpd-event" {
#  *   command = "/opt/bin/restart-httpd.sh"
#  * }
#  * ```
#  *
#  * @category Object type
#  * @category Monitoring object type
#  *
#  * :see: `doc/09-object-types.md L295-L320 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L295-L320>`__
#  */
# export interface EventCommand {}

# /**
#  * A host.
#  *
#  * @example
#  *
#  * ```
#  * object Host "icinga2-agent1.localdomain" {
#  *   display_name = "Linux Client 1"
#  *   address = "192.168.56.111"
#  *   address6 = "2a00:1450:4001:815::2003"
#  *
#  *   groups = [ "linux-servers" ]
#  *
#  *   check_command = "hostalive"
#  * }
#  * ```
#  *
#  * @category Object type
#  * @category Monitoring object type
#  *
#  * :see: `doc/09-object-types.md L323-L413 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L323-L413>`__
#  * :see: `lib/icinga/host.ti <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/host.ti>`__
#  */
# export interface Host extends Checkable {
#   /**
#    * A list of host groups this host belongs to.
#    *
#    * :see: `lib/icinga/host.ti L18-L20 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/host.ti#L18-L20>`__
#    */
#   groups: string[]

#   /**
#    * A short description of the host (e.g. displayed by external interfaces instead of the name if set).
#    *
#    * :see: `lib/icinga/host.ti L22-L30 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/host.ti#L22-L30>`__
#    */
#   display_name: string

#   /**
#    * The host's IPv4 address. Available as command runtime macro `$address$` if set.
#    *
#    * :see: `lib/icinga/host.ti L32 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/host.ti#L32>`__
#    */
#   address: string

#   /**
#    * The host's IPv6 address. Available as command runtime macro `$address6$` if set.
#    *
#    * :see: `lib/icinga/host.ti L33 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/host.ti#L33>`__
#    */
#   address6: string

#   /**
#    * The current state (0 = UP, 1 = DOWN).
#    *
#    * :see: `lib/icinga/host.ti L35-L37 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/host.ti#L35-L37>`__
#    */
#   state: HostState

#   /**
#    * The previous state (0 = UP, 1 = DOWN).
#    *
#    * :see: `lib/icinga/host.ti L38-L40 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/host.ti#L38-L40>`__
#    */
#   last_state: HostState

#   /**
#    * The last hard state (0 = UP, 1 = DOWN).
#    *
#    * :see: `lib/icinga/host.ti L41-L43 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/host.ti#L41-L43>`__
#    */
#   last_hard_state: HostState

#   /**
#    * When the last UP state occurred (as a UNIX timestamp).
#    *
#    * :see: `lib/icinga/host.ti L44 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/host.ti#L44>`__
#    */
#   last_state_up: Timestamp

#   /**
#    * When the last DOWN state occurred (as a UNIX timestamp).
#    *
#    * :see: `lib/icinga/host.ti L45 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/host.ti#L45>`__
#    */
#   last_state_down: Timestamp
# }

# /**
#  * A group of hosts.
#  *
#  * > **Best Practice**
#  * >
#  * > Assign host group members using the `group assign <17-language-reference.md#group-assign>`__ rules.
#  *
#  * @example
#  *
#  * ```
#  * object HostGroup "linux-servers" {
#  *   display_name = "Linux Servers"
#  *
#  *   assign where host.vars.os == "Linux"
#  * }
#  * ```
#  *
#  * @category Object type
#  * @category Monitoring object type
#  *
#  * :see: `doc/09-object-types.md L417-L440 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L417-L440>`__
#  */
# export interface HostGroup {}

# /**
#  * Notification objects are used to specify how users should be notified in case
#  * of host and service state changes and other events.
#  *
#  * > **Best Practice**
#  * >
#  * > Rather than creating a `Notification` object for a specific host or service it is
#  * > usually easier to just create a `Notification` template and use the `apply` keyword
#  * > to assign the notification to a number of hosts or services. Use the `to` keyword
#  * > to set the specific target type for `Host` or `Service`.
#  * > Check the `notifications <03-monitoring-basics.md#alert-notifications>`__ chapter for detailed examples.
#  *
#  * Example:
#  *
#  * ```
#  * object Notification "localhost-ping-notification" {
#  *   host_name = "localhost"
#  *   service_name = "ping4"
#  *
#  *   command = "mail-notification"
#  *
#  *   users = [ "user1", "user2" ] // reference to User objects
#  *
#  *   types = [ Problem, Recovery ]
#  *   states = [ Critical, Warning, OK ]
#  * }
#  * ```
#  *
#  * @category Object type
#  * @category Monitoring object type
#  *
#  * :see: `doc/09-object-types.md L444-L527 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L444-L527>`__
#  */
# export interface Notification {}

# /**
#  * A notification command definition.
#  *
#  * @example
#  *
#  * ```
#  * object NotificationCommand "mail-service-notification" {
#  *   command = [ ConfigDir + "/scripts/mail-service-notification.sh" ]
#  *
#  *   arguments += {
#  *     "-4" = {
#  *       required = true
#  *       value = "$notification_address$"
#  *     }
#  *     "-6" = "$notification_address6$"
#  *     "-b" = "$notification_author$"
#  *     "-c" = "$notification_comment$"
#  *     "-d" = {
#  *       required = true
#  *       value = "$notification_date$"
#  *     }
#  *     "-e" = {
#  *       required = true
#  *       value = "$notification_servicename$"
#  *     }
#  *     "-f" = {
#  *       value = "$notification_from$"
#  *       description = "Set from address. Requires GNU mailutils (Debian/Ubuntu) or mailx (RHEL/SUSE)"
#  *     }
#  *     "-i" = "$notification_icingaweb2url$"
#  *     "-l" = {
#  *       required = true
#  *       value = "$notification_hostname$"
#  *     }
#  *     "-n" = {
#  *       required = true
#  *       value = "$notification_hostdisplayname$"
#  *     }
#  *     "-o" = {
#  *       required = true
#  *       value = "$notification_serviceoutput$"
#  *     }
#  *     "-r" = {
#  *       required = true
#  *       value = "$notification_useremail$"
#  *     }
#  *     "-s" = {
#  *       required = true
#  *       value = "$notification_servicestate$"
#  *     }
#  *     "-t" = {
#  *       required = true
#  *       value = "$notification_type$"
#  *     }
#  *     "-u" = {
#  *       required = true
#  *       value = "$notification_servicedisplayname$"
#  *     }
#  *     "-v" = "$notification_logtosyslog$"
#  *   }
#  *
#  *   vars += {
#  *     notification_address = "$address$"
#  *     notification_address6 = "$address6$"
#  *     notification_author = "$notification.author$"
#  *     notification_comment = "$notification.comment$"
#  *     notification_type = "$notification.type$"
#  *     notification_date = "$icinga.long_date_time$"
#  *     notification_hostname = "$host.name$"
#  *     notification_hostdisplayname = "$host.display_name$"
#  *     notification_servicename = "$service.name$"
#  *     notification_serviceoutput = "$service.output$"
#  *     notification_servicestate = "$service.state$"
#  *     notification_useremail = "$user.email$"
#  *     notification_servicedisplayname = "$service.display_name$"
#  *   }
#  * }
#  * ```
#  *
#  * @category Object type
#  * @category Monitoring object type
#  *
#  * :see: `doc/09-object-types.md L530-L622 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L530-L622>`__
#  */
# export interface NotificationCommand {}

# /**
#  * ScheduledDowntime objects can be used to set up recurring downtimes for hosts/services.
#  *
#  * > **Best Practice**
#  * >
#  * > Rather than creating a `ScheduledDowntime` object for a specific host or service it is usually easier
#  * > to just create a `ScheduledDowntime` template and use the `apply` keyword to assign the
#  * > scheduled downtime to a number of hosts or services. Use the `to` keyword to set the specific target
#  * > type for `Host` or `Service`.
#  * > Check the `recurring downtimes <08-advanced-topics.md#recurring-downtimes>`__ example for details.
#  *
#  * Example:
#  *
#  * ```
#  * object ScheduledDowntime "some-downtime" {
#  *   host_name = "localhost"
#  *   service_name = "ping4"
#  *
#  *   author = "icingaadmin"
#  *   comment = "Some comment"
#  *
#  *   fixed = false
#  *   duration = 30m
#  *
#  *   ranges = {
#  *     "sunday" = "02:00-03:00"
#  *   }
#  * }
#  * ```
#  *
#  * @category Object type
#  * @category Monitoring object type
#  *
#  * :see: `doc/09-object-types.md L624-L674 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L624-L674>`__
#  */
# export interface ScheduledDowntime {}

# /**
#  * Service objects describe network services and how they should be checked
#  * by Icinga 2.
#  *
#  * > **Best Practice**
#  * >
#  * > Rather than creating a `Service` object for a specific host it is usually easier
#  * > to just create a `Service` template and use the `apply` keyword to assign the
#  * > service to a number of hosts.
#  * > Check the `apply <03-monitoring-basics.md#using-apply>`__ chapter for details.
#  *
#  * Example:
#  *
#  * ```
#  * object Service "uptime" {
#  *   host_name = "localhost"
#  *
#  *   display_name = "localhost Uptime"
#  *
#  *   check_command = "snmp"
#  *
#  *   vars.snmp_community = "public"
#  *   vars.snmp_oid = "DISMAN-EVENT-MIB::sysUpTimeInstance"
#  *
#  *   check_interval = 60s
#  *   retry_interval = 15s
#  *
#  *   groups = [ "all-services", "snmp" ]
#  * }
#  * ```
#  *
#  * @category Object type
#  * @category Monitoring object type
#  *
#  * :see: `lib/icinga/service.ti <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/service.ti>`__
#  * :see: `doc/09-object-types.md L677-L781 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L677-L781>`__
#  */
# export interface Service extends Checkable {
#   /**
#    * The service groups this service belongs to.
#    */
#   groups: string

#   /**
#    * A short description of the service.
#    */
#   display_name: string

#   /**
#    * The host this service belongs to. There must be a `Host` object with that name.
#    */
#   host_name: string

#   /**
#    * @group navigation
#    */
#   host?: Host

#   /**
#    * The current state (0 = OK, 1 = WARNING, 2 = CRITICAL, 3 = UNKNOWN).
#    */
#   state: ServiceState

#   /**
#    * The previous state (0 = OK, 1 = WARNING, 2 = CRITICAL, 3 = UNKNOWN).
#    */
#   last_state: ServiceState

#   /**
#    * The last hard state (0 = OK, 1 = WARNING, 2 = CRITICAL, 3 = UNKNOWN).
#    */
#   last_hard_state: ServiceState

#   /**
#    * When the last OK state occurred (as a UNIX timestamp).
#    */
#   last_state_ok: TimeStamp

#   /**
#    * When the last WARNING state occurred (as a UNIX timestamp).
#    */
#   last_state_warning: TimeStamp

#   /**
#    * When the last CRITICAL state occurred (as a UNIX timestamp).
#    */
#   last_state_critical: TimeStamp

#   /**
#    * When the last UNKNOWN state occurred (as a UNIX timestamp).
#    */
#   last_state_unknown: TimeStamp
# }

# /**
#  * A group of services.
#  *
#  * > **Best Practice**
#  * >
#  * > Assign service group members using the `group assign <17-language-reference.md#group-assign>`__ rules.
#  *
#  * Example:
#  *
#  * ```
#  * object ServiceGroup "snmp" {
#  *   display_name = "SNMP services"
#  * }
#  * ```
#  *
#  * @category Object type
#  * @category Monitoring object type
#  *
#  * :see: `doc/09-object-types.md L784-L805 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L784-L805>`__
#  */
# export interface ServiceGroup {}

# /**
#  * Time periods can be used to specify when hosts/services should be checked or to limit
#  * when notifications should be sent out.
#  *
#  * Examples:
#  *
#  * ```
#  * object TimePeriod "nonworkhours" {
#  *   display_name = "Icinga 2 TimePeriod for non working hours"
#  *
#  *   ranges = {
#  *     monday = "00:00-8:00,17:00-24:00"
#  *     tuesday = "00:00-8:00,17:00-24:00"
#  *     wednesday = "00:00-8:00,17:00-24:00"
#  *     thursday = "00:00-8:00,17:00-24:00"
#  *     friday = "00:00-8:00,16:00-24:00"
#  *     saturday = "00:00-24:00"
#  *     sunday = "00:00-24:00"
#  *   }
#  * }
#  *
#  * object TimePeriod "exampledays" {
#  *     display_name = "Icinga 2 TimePeriod for random example days"
#  *
#  *     ranges = {
#  *         //We still believe in Santa, no peeking!
#  *         //Applies every 25th of December every year
#  *         "december 25" = "00:00-24:00"
#  *
#  *         //Any point in time can be specified,
#  *         //but you still have to use a range
#  *         "2038-01-19" = "03:13-03:15"
#  *
#  *         //Evey 3rd day from the second monday of February
#  *         //to 8th of November
#  *         "monday 2 february - november 8 / 3" = "00:00-24:00"
#  *     }
#  * }
#  * ```
#  *
#  * Additional examples can be found `here <08-advanced-topics.md#timeperiods>`__.
#  *
#  * @category Object type
#  * @category Monitoring object type
#  *
#  * :see: `doc/09-object-types.md L809-L869 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L809-L869>`__
#  */
# export interface TimePeriod {}

# /**
#  * A user.
#  *
#  * Example:
#  *
#  * ```
#  * object User "icingaadmin" {
#  *   display_name = "Icinga 2 Admin"
#  *   groups = [ "icingaadmins" ]
#  *   email = "icinga@localhost"
#  *   pager = "icingaadmin@localhost.localdomain"
#  *
#  *   period = "24x7"
#  *
#  *   states = [ OK, Warning, Critical, Unknown ]
#  *   types = [ Problem, Recovery ]
#  *
#  *   vars.additional_notes = "This is the Icinga 2 Admin account."
#  * }
#  * ```
#  *
#  * Available notification state filters:
#  *
#  * ```
#  * OK
#  * Warning
#  * Critical
#  * Unknown
#  * Up
#  * Down
#  * ```
#  *
#  * Available notification type filters:
#  *
#  * ```
#  * DowntimeStart
#  * DowntimeEnd
#  * DowntimeRemoved
#  * Custom
#  * Acknowledgement
#  * Problem
#  * Recovery
#  * FlappingStart
#  * FlappingEnd
#  * ```
#  *
#  * @category Object type
#  * @category Monitoring object type
#  *
#  * :see: `lib/icinga/user.ti <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/user.ti>`__
#  * :see: `doc/09-object-types.md L872-L937 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L872-L937>`__
#  */
# export interface User extends CustomVarObject {
#   /**
#    * A short description of the user.
#    *
#    * :see: `lib/icinga/user.ti L14-L22 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/user.ti#L14-L22>`__
#    * :see: `doc/09-object-types.md L923 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L923>`__
#    */
#   display_name: string

#   /**
#    * An array of group names.
#    *
#    * :see: `lib/icinga/user.ti L23-L25 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/user.ti#L23-L25>`__
#    * :see: `doc/09-object-types.md L927 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L927>`__
#    */
#   groups: string[]

#   /**
#    * The name of a time period which determines when a notification for this user should be triggered. Not set by default (effectively 24x7).
#    *
#    * :see: `lib/icinga/user.ti L26-L30 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/user.ti#L26-L30>`__
#    * :see: `doc/09-object-types.md L929 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L929>`__
#    */
#   period: string

#   /**
#    * A set of type filters when a notification for this user should be triggered. By default everything is matched.
#    *
#    * :see: `lib/icinga/user.ti L32 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/user.ti#L32>`__
#    * :see: `doc/09-object-types.md L930 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L930>`__
#    */
#   types: string[]

#   /**
#    * A set of state filters when a notification for this should be triggered. By default everything is matched.
#    *
#    * :see: `lib/icinga/user.ti L34 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/user.ti#L34>`__
#    * :see: `doc/09-object-types.md L931 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L931>`__
#    */
#   states: string[]

#   /**
#    * An email string for this user. Useful for notification commands.
#    *
#    * :see: `lib/icinga/user.ti L37 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/user.ti#L37>`__
#    * :see: `doc/09-object-types.md L924 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L924>`__
#    */
#   email: string

#   /**
#    * A pager string for this user. Useful for notification commands.
#    *
#    * :see: `lib/icinga/user.ti L38 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/user.ti#L38>`__
#    * :see: `doc/09-object-types.md L925 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L925>`__
#    */
#   pager: string

#   /**
#    * Whether notifications are enabled for this user. Defaults to true.
#    *
#    * :see: `lib/icinga/user.ti L40-L42 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/user.ti#L40-L42>`__
#    * :see: `doc/09-object-types.md L928 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L928>`__
#    */
#   enable_notifications: bool

#   /**
#    * When the last notification was sent for this user (as a UNIX timestamp).
#    *
#    * :see: `lib/icinga/user.ti L44 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/lib/icinga/user.ti#L44>`__
#    * :see: `doc/09-object-types.md L937 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L937>`__
#    */
#   last_notification: number
# }

# /**
#  * A user group.
#  *
#  * > **Best Practice**
#  * >
#  * > Assign user group members using the `group assign <17-language-reference.md#group-assign>`__ rules.
#  *
#  * Example:
#  *
#  * ```
#  * object UserGroup "icingaadmins" {
#  *     display_name = "Icinga 2 Admin Group"
#  * }
#  * ```
#  *
#  * @category Object type
#  * @category Monitoring object type
#  *
#  * :see: `doc/09-object-types.md L939-L960 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L939-L960>`__
#  */
# export interface UserGroup {}

# /**
#  * Zone objects are used to specify which Icinga 2 instances are located in a zone.
#  * Please read the `distributed monitoring chapter <06-distributed-monitoring.md#distributed-monitoring>`__ for additional details.
#  * Example:
#  *
#  * ```
#  * object Zone "master" {
#  *   endpoints = [ "icinga2-master1.localdomain", "icinga2-master2.localdomain" ]
#  *
#  * }
#  *
#  * object Zone "satellite" {
#  *   endpoints = [ "icinga2-satellite1.localdomain" ]
#  *   parent = "master"
#  * }
#  * ```
#  *
#  * @category Object type
#  * @category Monitoring object type
#  *
#  * :see: `doc/09-object-types.md L963-L989 <https://github.com/Icinga/icinga2/blob/2c9117b4f71e00b2072e7dbe6c4ea4e48c882a87/doc/09-object-types.md?plain=1#L963-L989>`__
#  */
# export interface Zone {}

# /***************************************************************************
#  * Runtime Objects
#  **************************************************************************/

# /**
#  * @category Object type
#  * @category Runtime object type
#  */
# export interface Comment {}

# /**
#  * @category Object type
#  * @category Runtime object type
#  */
# export interface Downtime {}

# /***************************************************************************
#  * Features
#  **************************************************************************/

# /**
#  * @category Object type
#  * @category Feature object type
#  */
# export interface ApiListener {}

# /**
#  * @category Object type
#  * @category Feature object type
#  */
# export interface CheckerComponent {}

# /**
#  * @category Object type
#  * @category Feature object type
#  */
# export interface CompatLogger {}

# /**
#  * @category Object type
#  * @category Feature object type
#  */
# export interface ElasticsearchWriter {}

# /**
#  * @category Object type
#  * @category Feature object type
#  */
# export interface ExternalCommandListener {}

# /**
#  * @category Object type
#  * @category Feature object type
#  */
# export interface FileLogger {}

# /**
#  * @category Object type
#  * @category Feature object type
#  */
# export interface GelfWriter {}

# /**
#  * @category Object type
#  * @category Feature object type
#  */
# export interface GraphiteWriter {}

# /**
#  * @category Object type
#  * @category Feature object type
#  */
# export interface IcingaApplication {}

# /**
#  * @category Object type
#  * @category Feature object type
#  */
# export interface IcingaDB {}

# /**
#  * @category Object type
#  * @category Feature object type
#  */
# export interface IdoMySqlConnection {}

# /**
#  * @category Object type
#  * @category Feature object type
#  */
# export interface IdoPgsqlConnection {}

# /**
#  * @category Object type
#  * @category Feature object type
#  */
# export interface InfluxdbWriter {}

# /**
#  * @category Object type
#  * @category Feature object type
#  */
# export interface Influxdb2Writer {}

# /**
#  * @category Object type
#  * @category Feature object type
#  */
# export interface JournaldLogger {}

# /**
#  * @category Object type
#  * @category Feature object type
#  */
# export interface LiveStatusListener {}

# /**
#  * @category Object type
#  * @category Feature object type
#  */
# export interface NotificationComponent {}

# /**
#  * @category Object type
#  * @category Feature object type
#  */
# export interface OpenTsdbWriter {}

# /**
#  * @category Object type
#  * @category Feature object type
#  */
# export interface PerfdataWriter {}

# /**
#  * @category Object type
#  * @category Feature object type
#  */
# export interface SyslogLogger {}

# /**
#  * @category Object type
#  * @category Feature object type
#  */
# export interface WindowsEventLogLogger {}

# export type ObjectType =
#   // Monitoring
#   | ApiUser
#   | CheckCommand
#   | CheckCommandArguments
#   | Dependency
#   | Endpoint
#   | EventCommand
#   | Host
#   | HostGroup
#   | Notification
#   | NotificationCommand
#   | ScheduledDowntime
#   | Service
#   | ServiceGroup
#   | User
#   | UserGroup
#   | Zone
#   // Runtime
#   | Comment
#   | Downtime
#   // Feature
#   | ApiListener
#   | CheckerComponent
#   | CompatLogger
#   | ElasticsearchWriter
#   | ExternalCommandListener
#   | FileLogger
#   | GelfWriter
#   | GraphiteWriter
#   | IcingaApplication
#   | IcingaDB
#   | IdoMySqlConnection
#   | IdoPgsqlConnection
#   | InfluxdbWriter
#   | Influxdb2Writer
#   | JournaldLogger
#   | LiveStatusListener
#   | NotificationComponent
#   | OpenTsdbWriter
#   | PerfdataWriter
#   | SyslogLogger
#   | WindowsEventLogLogger

# export type ObjectByName<T> = T extends 'ApiUser'
#   ? ApiUser
#   : T extends 'CheckCommand'
#   ? CheckCommand
#   : T extends 'CheckCommandArguments'
#   ? CheckCommandArguments
#   : T extends 'Dependency'
#   ? Dependency
#   : T extends 'Endpoint'
#   ? Endpoint
#   : T extends 'EventCommand'
#   ? EventCommand
#   : T extends 'Host'
#   ? Host
#   : T extends 'HostGroup'
#   ? HostGroup
#   : T extends 'Notification'
#   ? Notification
#   : T extends 'NotificationCommand'
#   ? NotificationCommand
#   : T extends 'ScheduledDowntime'
#   ? ScheduledDowntime
#   : T extends 'Service'
#   ? Service
#   : T extends 'ServiceGroup'
#   ? ServiceGroup
#   : T extends 'TimePeriod'
#   ? TimePeriod
#   : T extends 'User'
#   ? User
#   : T extends 'UserGroup'
#   ? UserGroup
#   : T extends 'Zone'
#   ? Zone
#   : // Runtime
#   T extends 'Comment'
#   ? Comment
#   : T extends 'Downtime'
#   ? Downtime
#   : // Feature
#   T extends 'ApiListener'
#   ? ApiListener
#   : T extends 'CheckerComponent'
#   ? CheckerComponent
#   : T extends 'CompatLogger'
#   ? CompatLogger
#   : T extends 'ElasticsearchWriter'
#   ? ElasticsearchWriter
#   : T extends 'ExternalCommandListener'
#   ? ExternalCommandListener
#   : T extends 'FileLogger'
#   ? FileLogger
#   : T extends 'GelfWriter'
#   ? GelfWriter
#   : T extends 'GraphiteWriter'
#   ? GraphiteWriter
#   : T extends 'IcingaApplication'
#   ? IcingaApplication
#   : T extends 'IcingaDB'
#   ? IcingaDB
#   : T extends 'IdoMySqlConnection'
#   ? IdoMySqlConnection
#   : T extends 'IdoPgsqlConnection'
#   ? IdoPgsqlConnection
#   : T extends 'InfluxdbWriter'
#   ? InfluxdbWriter
#   : T extends 'Influxdb2Writer'
#   ? Influxdb2Writer
#   : T extends 'JournaldLogger'
#   ? JournaldLogger
#   : T extends 'LiveStatusListener'
#   ? LiveStatusListener
#   : T extends 'NotificationComponent'
#   ? NotificationComponent
#   : T extends 'OpenTsdbWriter'
#   ? OpenTsdbWriter
#   : T extends 'PerfdataWriter'
#   ? PerfdataWriter
#   : T extends 'SyslogLogger'
#   ? SyslogLogger
#   : T extends 'WindowsEventLogLogger'
#   ? WindowsEventLogLogger
#   : never
