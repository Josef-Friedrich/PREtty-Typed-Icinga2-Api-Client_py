from _typeshed import Incomplete

class Icinga2ApiException(Exception):
    error: Incomplete
    def __init__(self, error) -> None: ...

class Icinga2ApiRequestException(Icinga2ApiException):
    response: Incomplete
    def __init__(self, error, response) -> None: ...

class Icinga2ApiConfigFileException(Exception):
    error: Incomplete
    def __init__(self, error) -> None: ...
