from pretiac.check_executor import (
    SubprocessCheck,
    _read_check_collection,  # type: ignore
)
from pretiac.object_types import ServiceState
from tests.conftest import get_resources_path


def test_read_collection():
    collection = _read_check_collection(get_resources_path("checks.yml"))
    assert collection.host == "RandomHost"
    assert collection.checks[0].service == "procs"
    assert collection.checks[0].check_command == "check_procs -w 500 -c 600"


class TestSubprocessCheck:
    def test_input_string(self) -> None:
        check = SubprocessCheck("/usr/lib/nagios/plugins/check_users -w 100 -c 200")
        assert check.exit_status == ServiceState.OK
        assert check.check_command == [
            "/usr/lib/nagios/plugins/check_users",
            "-w",
            "100",
            "-c",
            "200",
        ]

    def test_input_list(self) -> None:
        check = SubprocessCheck(
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
        check = SubprocessCheck(
            "/usr/lib/nagios/plugins/check_http -H xxxxx.qwsed334rer"
        )
        assert check.exit_status == ServiceState.CRITICAL
        assert (
            check.plugin_output
            == "Name or service not known\nHTTP CRITICAL - Unable to open TCP socket"
        )

    def test_non_existent_check_command(self) -> None:
        check = SubprocessCheck("/xxxxx")
        assert check.exit_status == ServiceState.CRITICAL
        assert check.check_command == [
            "/xxxxx",
        ]
        assert (
            check.plugin_output == "FileNotFoundError: (2, 'No such file or directory')"
        )
