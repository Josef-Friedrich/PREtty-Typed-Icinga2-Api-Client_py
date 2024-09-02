from pretiac.check_executor import _read_check_collection  # type: ignore
from tests.conftest import get_resources_path


def test_read_collection():
    collection = _read_check_collection(get_resources_path("checks.yml"))
    assert collection.host == "RandomHost"
    assert collection.checks[0].service == "procs"
    assert collection.checks[0].check_command == "check_procs -w 500 -c 600"
