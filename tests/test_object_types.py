from pretiac.object_types import (
    _convert_pascal_to_snake_case,  # type: ignore
    get_object_types_names,
    normalize_to_plural_snake_object_type_name,
    object_type_names_snake,
)


def test_convert_pascal_to_snake_case() -> None:
    assert (
        _convert_pascal_to_snake_case("LongPascalCaseName") == "long_pascal_case_name"
    )


def test_get_object_types_names() -> None:
    assert get_object_types_names() == [
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
        "Comment",
        "Downtime",
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


def test_object_type_names_snake() -> None:
    assert object_type_names_snake == [
        "api_user",
        "check_command",
        "check_command_arguments",
        "dependency",
        "endpoint",
        "event_command",
        "host",
        "host_group",
        "notification",
        "notification_command",
        "scheduled_downtime",
        "service",
        "service_group",
        "time_period",
        "user",
        "user_group",
        "zone",
        "comment",
        "downtime",
        "api_listener",
        "checker_component",
        "compat_logger",
        "elasticsearch_writer",
        "external_command_listener",
        "file_logger",
        "gelf_writer",
        "graphite_writer",
        "icinga_application",
        "icinga_db",
        "ido_my_sql_connection",
        "ido_pgsql_connection",
        "influxdb_writer",
        "influxdb2_writer",
        "journald_logger",
        "live_status_listener",
        "notification_component",
        "open_tsdb_writer",
        "perfdata_writer",
        "syslog_logger",
        "windows_event_log_logger",
    ]


class TestNormalizeToPluralSnakeObjectTypeName:
    def assert_name(self, name: str, expected: str) -> None:
        assert normalize_to_plural_snake_object_type_name(name) == expected

    def test_pascal_case(self) -> None:
        self.assert_name("WindowsEventLogLogger", "windows_event_log_loggers")

    def test_already_normalized(self) -> None:
        self.assert_name("windows_event_log_loggers", "windows_event_log_loggers")

    def test_singular(self) -> None:
        self.assert_name("windows_event_log_logger", "windows_event_log_loggers")
