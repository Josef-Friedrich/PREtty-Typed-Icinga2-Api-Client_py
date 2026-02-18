from logging import (
    DEBUG,
    INFO,
    Formatter,
    StreamHandler,
    basicConfig,
    getLogger,
)
from logging import (
    Logger as DefaultLogger,
)


class Logger:
    """A wrapper around the Python logging module with 3 debug logging levels.

    1. ``-d``: info
    2. ``-dd``: debug
    3. ``-ddd``: verbose

    :see `check_systemd.py L289-L351 <https://github.com/Josef-Friedrich/check_systemd/blob/a63450608240e3d0432a2a6ad7501f79e5e0dce9/check_systemd.py#L289-L351>`__:
    """

    __logger: DefaultLogger

    __BLUE = "\x1b[0;34m"
    __PURPLE = "\x1b[0;35m"
    __CYAN = "\x1b[0;36m"
    __RESET = "\x1b[0m"

    __INFO: int = INFO
    __DEBUG: int = DEBUG
    __VERBOSE = 5

    def __init__(self) -> None:
        handler = StreamHandler()
        handler.setFormatter(Formatter("%(message)s"))
        basicConfig(handlers=[handler])
        self.__logger = getLogger(__name__)

    def set_level(self, level: int) -> None:
        # NOTSET=0
        # custom level: VERBOSE=5
        # DEBUG=10
        # INFO=20
        # WARN=30
        # ERROR=40
        # CRITICAL=50
        if level == 1:
            self.__logger.setLevel(INFO)
        elif level == 2:
            self.__logger.setLevel(DEBUG)
        elif level > 2:
            self.__logger.setLevel(5)

    def __log(self, level: int, color: str, msg: str, *args: object) -> None:
        a: list[str] = []
        for arg in args:
            a.append(color + str(arg) + self.__RESET)
        self.__logger.log(level, msg, *a)

    def info(self, msg: str, *args: object) -> None:
        """Log on debug level ``1``: ``-d``.

        :param msg: A message format string. Note that this means that you can
            use keywords in the format string, together with a single
            dictionary argument. No ``%`` formatting operation is performed on
            ``msg`` when no args are supplied.
        :param args: The arguments which are merged into ``msg`` using the
            string formatting operator.
        """
        self.__log(self.__INFO, self.__BLUE, msg, *args)

    def debug(self, msg: str, *args: object) -> None:
        """Log on debug level ``2``: ``-dd``.

        :param msg: A message format string. Note that this means that you can
            use keywords in the format string, together with a single
            dictionary argument. No ``%`` formatting operation is performed on
            ``msg`` when no args are supplied.
        :param args: The arguments which are merged into ``msg`` using the
            string formatting operator.
        """
        self.__log(self.__DEBUG, self.__PURPLE, msg, *args)

    def verbose(self, msg: str, *args: object) -> None:
        """Log on debug level ``3``: ``-ddd``

        :param msg: A message format string. Note that this means that you can
            use keywords in the format string, together with a single
            dictionary argument. No ``%`` formatting operation is performed on
            ``msg`` when no args are supplied.
        :param args: The arguments which are merged into ``msg`` using the
            string formatting operator.
        """
        self.__log(self.__VERBOSE, self.__CYAN, msg, *args)

    def show_levels(self) -> None:
        msg = "log level %s (%s): %s"
        self.info(msg, 1, "info", "-d")
        self.debug(msg, 2, "debug", "-dd")
        self.verbose(msg, 3, "verbose", "-ddd")


logger = Logger()
