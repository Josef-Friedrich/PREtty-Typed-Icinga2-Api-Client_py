from typing import Literal

from _typeshed import Incomplete

from .base import (Base, HostService, HostServiceComment, HostServiceDowntime,
                   Json)
from .exceptions import Icinga2ApiException as Icinga2ApiException

LOG: Incomplete

ExitStatus = Literal[0, 1, 2, 3]

class Actions(Base):
    base_url_path: str
    def process_check_result(
        self,
        object_type: HostService,
        name: str,
        exit_status: ExitStatus,
        plugin_output: str,
        performance_data: Incomplete | None = ...,
        check_command: Incomplete | None = ...,
        check_source: str | None = ...,
        execution_start: int | None = ...,
        execution_end: int | None = ...,
        ttl: int | None = ...,
        filters: Incomplete | None = ...,
        filter_vars: Incomplete | None = ...,
    ) -> Json: ...
    def reschedule_check(
        self,
        object_type: HostService,
        filters,
        filter_vars: Incomplete | None = ...,
        next_check: Incomplete | None = ...,
        force_check: bool = ...,
    ) -> Json: ...
    def send_custom_notification(
        self,
        object_type: HostService,
        filters,
        author,
        comment,
        filter_vars: Incomplete | None = ...,
        force: bool = ...,
    ) -> Json: ...
    def delay_notification(
        self,
        object_type: HostService,
        filters,
        timestamp,
        filter_vars: Incomplete | None = ...,
    ) -> Json: ...
    def acknowledge_problem(
        self,
        object_type: HostService,
        filters,
        author,
        comment,
        filter_vars: Incomplete | None = ...,
        expiry: Incomplete | None = ...,
        sticky: Incomplete | None = ...,
        notify: Incomplete | None = ...,
        persistent: Incomplete | None = ...,
    ) -> Json: ...
    def remove_acknowledgement(
        self, object_type: ObjectType, filters, filter_vars: Incomplete | None = ...
    ) -> Json: ...
    def add_comment(
        self,
        object_type: HostService,
        filters,
        author,
        comment,
        filter_vars: Incomplete | None = ...,
    ) -> Json: ...
    def remove_comment(
        self,
        object_type: HostServiceComment,
        name: Incomplete | None = ...,
        filters: Incomplete | None = ...,
        filter_vars: Incomplete | None = ...,
    ) -> Json: ...
    def schedule_downtime(
        self,
        object_type: HostService,
        filters,
        author,
        comment,
        start_time,
        end_time,
        duration,
        filter_vars: Incomplete | None = ...,
        fixed: Incomplete | None = ...,
        all_services: Incomplete | None = ...,
        trigger_name: Incomplete | None = ...,
        child_options: Incomplete | None = ...,
    ) -> Json: ...
    def remove_downtime(
        self,
        object_type: HostServiceDowntime,
        name: Incomplete | None = ...,
        filters: Incomplete | None = ...,
        filter_vars: Incomplete | None = ...,
    ) -> Json: ...
    def shutdown_process(self) -> Json: ...
    def restart_process(self) -> Json: ...
    def generate_ticket(self, host_common_name) -> Json: ...
