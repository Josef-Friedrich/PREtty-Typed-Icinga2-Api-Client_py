from tests.conftest import get_resources_path

from pretiac.check_executor import _read_check_collection  # type: ignore


def test_read_collection():
    collection = _read_check_collection(get_resources_path("checks.yml"))
    assert collection.host == "RandomHost"
    assert collection.checks[0].service == "memory"
    assert collection.checks[0].check_command == "check_linux_memory -f -w 2 -c 0"
