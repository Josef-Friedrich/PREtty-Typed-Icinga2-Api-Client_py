from pytest import ExitCode, Pytester


def test_help(pytester: Pytester) -> None:
    result = pytester.run("pretiac", "--help")
    assert result.ret == ExitCode.OK
    result.stdout.fnmatch_lines("Usage: pretiac*")


def test_option_debug(pytester: Pytester) -> None:
    result = pytester.run("pretiac", "-ddd", "check")
    assert result.ret == ExitCode.INTERRUPTED

    # log level 1 (info): -d
    # log level 2 (debug): -dd
    # log level 3 (verbose): -ddd
    result.stderr.fnmatch_lines(
        "log level \x1b[0;34m1\x1b[0m (\x1b[0;34minfo\x1b[0m): \x1b[0;34m-d\x1b[0m"
    )
    result.stderr.fnmatch_lines(
        "log level \x1b[0;35m2\x1b[0m (\x1b[0;35mdebug\x1b[0m): \x1b[0;35m-dd\x1b[0m"
    )
    result.stderr.fnmatch_lines(
        "log level \x1b[0;36m3\x1b[0m (\x1b[0;36mverbose\x1b[0m): \x1b[0;36m-ddd\x1b[0m"
    )
