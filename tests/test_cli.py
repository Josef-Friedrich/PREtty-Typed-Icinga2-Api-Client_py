from pytest import ExitCode, Pytester


def test_cli(pytester: Pytester):
    result = pytester.run("pretiac", "--help")
    assert result.ret == ExitCode.OK
