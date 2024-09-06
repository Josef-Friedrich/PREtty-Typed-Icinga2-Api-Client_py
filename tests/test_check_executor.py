from pretiac.check_executor import (
    CheckExecution,
    _read_check_collection,  # type: ignore
)
from pretiac.object_types import ServiceState
from tests.conftest import get_resources_path


def test_read_collection():
    collection = _read_check_collection(get_resources_path("checks.yml"))
    assert collection.host == "RandomHost"
    assert collection.checks[0].service == "procs"
    assert collection.checks[0].check_command == "check_procs -w 500 -c 600"


class TestClassCheckExecution:
    class TestAttributes:
        check = CheckExecution("/usr/lib/nagios/plugins/check_users -w 100 -c 200")

        def test_check_command(self) -> None:
            assert self.check.check_command == [
                "/usr/lib/nagios/plugins/check_users",
                "-w",
                "100",
                "-c",
                "200",
            ]

        def test_execution_start(self) -> None:
            assert self.check.execution_start > 0

        def test_execution_end(self) -> None:
            assert self.check.execution_end > 0
            assert self.check.execution_end >= self.check.execution_start

        def test_exit_status(self) -> None:
            assert self.check.exit_status == ServiceState.OK

        def test_plugin_output(self) -> None:
            assert "USERS OK" in self.check.plugin_output

        def test_performance_data(self) -> None:
            assert self.check.performance_data
            assert "users=" in self.check.performance_data

    def test_input_string(self) -> None:
        check = CheckExecution("/usr/lib/nagios/plugins/check_users -w 100 -c 200")
        assert check.exit_status == ServiceState.OK
        assert check.check_command == [
            "/usr/lib/nagios/plugins/check_users",
            "-w",
            "100",
            "-c",
            "200",
        ]

    def test_input_list(self) -> None:
        check = CheckExecution(
            [
                "/usr/lib/nagios/plugins/check_users",
                "-w",
                "100",
                "-c",
                "200",
            ]
        )
        assert check.exit_status == ServiceState.OK
        assert check.check_command == [
            "/usr/lib/nagios/plugins/check_users",
            "-w",
            "100",
            "-c",
            "200",
        ]

    def test_critical(self) -> None:
        check = CheckExecution(
            "/usr/lib/nagios/plugins/check_http -H xxxxx.qwsed334rer"
        )
        assert check.exit_status == ServiceState.CRITICAL
        assert (
            check.plugin_output
            == "Name or service not known\nHTTP CRITICAL - Unable to open TCP socket"
        )

    def test_non_existent_check_command(self) -> None:
        check = CheckExecution("/xxxxx")
        assert check.exit_status == ServiceState.CRITICAL
        assert check.check_command == [
            "/xxxxx",
        ]
        assert check.plugin_output == "Plugin not found: /xxxxx"
