import python_boilerplate


class TestPythonProjectBoilerplate:
    def test_version(self) -> None:
        assert python_boilerplate.__version__ == "0.1.0"

    def test_print(self) -> None:
        print("use pytest --capture=sys-tee to capture the printed test")
