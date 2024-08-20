from typing import Any, List, Union

from _typeshed import Incomplete as Incomplete

from pretiac.base import Base, Json, ObjectType

LOG: Incomplete

class Objects(Base):
    base_url_path: str
    def get(
        self,
        object_type: ObjectType,
        name: str,
        attrs: Union[Incomplete, None] = ...,
        joins: Union[Incomplete, None] = ...,
    ) -> Json: ...
    def list(
        self,
        object_type: ObjectType,
        name: str | None = ...,
        attrs: List[str] | None = ...,
        filters: str | None = ...,
        filter_vars: Union[Incomplete, None] = ...,
        joins: bool | List[str] | None = ...,
    ) -> Json: ...
    def create(
        self,
        object_type: ObjectType,
        name: str,
        templates: Union[Incomplete, None] = ...,
        attrs: Union[Incomplete, None] = ...,
    ) -> Json: ...
    def update(self, object_type: ObjectType, name: str, attrs) -> Json: ...
    def delete(
        self,
        object_type: ObjectType,
        name: Union[Incomplete, None] = ...,
        filters: Union[Incomplete, None] = ...,
        filter_vars: Union[Incomplete, None] = ...,
        cascade: bool = ...,
    ) -> Json: ...

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
