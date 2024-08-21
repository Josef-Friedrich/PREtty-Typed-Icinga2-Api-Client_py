# -*- coding: utf-8 -*-
"""
Copyright 2017 fmnisme@gmail.com, Copyright 2020 christian@jonak.org

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Icinga 2 API client base
"""

import logging
from logging import Logger
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Generator,
    List,
    Literal,
    Optional,
    Type,
    Union,
)
from urllib.parse import urljoin

import requests

from pretiac.exceptions import PretiacException, PretiacRequestException

if TYPE_CHECKING:
    from pretiac.client import Client

LOG: Logger = logging.getLogger(__name__)


Json = Union[Dict[str, "Json"], List["Json"], int, str, float, bool, Type[None]]

HostOrService = Literal["Host", "Service"]

HostServiceComment = Union[Literal["Comment"], HostOrService]

HostServiceDowntime = Union[Literal["Downtime"], HostOrService]

ObjectType = Literal[
    "ApiListener",
    "ApiUser",
    "CheckCommand",
    "Arguments",
    "CheckerComponent",
    "CheckResultReader",
    "Comment",
    "CompatLogger",
    "Dependency",
    "Downtime",
    "Endpoint",
    "EventCommand",
    "ExternalCommandListener",
    "FileLogger",
    "GelfWriter",
    "GraphiteWriter",
    "Host",
    "HostGroup",
    "IcingaApplication",
    "IdoMySqlConnection",
    "IdoPgSqlConnection",
    "LiveStatusListener",
    "Notification",
    "NotificationCommand",
    "NotificationComponent",
    "OpenTsdbWriter",
    "PerfdataWriter",
    "ScheduledDowntime",
    "Service",
    "ServiceGroup",
    "StatusDataWriter",
    "SyslogLogger",
    "TimePeriod",
    "User",
    "UserGroup",
    "Zone",
]

Payload = dict[str, Any]

FilterVars = Optional[Payload]

RequestMethod = Literal["GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"]
"""
https://github.com/psf/requests/blob/a3ce6f007597f14029e6b6f54676c34196aa050e/src/requests/api.py#L17

https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
"""


class Base:
    """
    Icinga 2 API Base class
    """

    manager: "Client"

    base_url_path: Optional[str] = None

    def __init__(self, manager: "Client") -> None:
        """
        initialize object
        """

        self.manager = manager
        self.stream_cache = ""

    @property
    def base_url(self) -> str:
        if not self.base_url_path:
            raise PretiacException("Specify self.base_url_path")
        return self.base_url_path

    def _create_session(self, method: RequestMethod = "POST") -> requests.Session:
        """
        create a session object
        """

        session = requests.Session()
        # prefer certificate authentification
        if self.manager.certificate and self.manager.key:
            # certificate and key are in different files
            session.cert = (self.manager.certificate, self.manager.key)
        elif self.manager.certificate:
            # certificate and key are in the same file
            session.cert = self.manager.certificate
        elif self.manager.username and self.manager.password:
            # use username and password
            session.auth = (self.manager.username, self.manager.password)
        session.headers = {
            "User-Agent": "Python-pretiac/{0}".format(self.manager.version),
            "X-HTTP-Method-Override": method.upper(),
            "Accept": "application/json",
        }

        return session

    def _request(
        self,
        method: RequestMethod,
        url_path: str,
        payload: Optional[dict[str, Any]] = None,
        stream: bool = False,
    ) -> Any:
        """
        make the request and return the body

        :param method: the HTTP method
        :type method: string
        :param url_path: the requested url path
        :type url_path: string
        :param payload: the payload to send
        :type payload: dictionary
        :returns: the response as json
        :rtype: dictionary
        """

        request_url = urljoin(self.manager.url, url_path)
        LOG.debug("Request URL: %s", request_url)

        # create session
        session = self._create_session(method)

        # create arguments for the request
        request_args: Payload = {"url": request_url}
        if payload:
            request_args["json"] = payload
        if self.manager.ca_certificate:
            request_args["verify"] = self.manager.ca_certificate
        else:
            request_args["verify"] = False
        if stream:
            request_args["stream"] = True

        # do the request
        response: requests.Response = session.post(**request_args)

        if not stream:
            session.close()
        # # for debugging
        # from pprint import pprint
        # pprint(request_url)
        # pprint(payload)
        # pprint(response)

        if not 200 <= response.status_code <= 299:
            raise PretiacRequestException(
                'Request "{}" failed with status {}: {}'.format(
                    response.url,
                    response.status_code,
                    response.text,
                ),
                response.json(),
            )

        if stream:
            return response
        else:
            return response.json()

    @staticmethod
    def _get_message_from_stream(
        stream: requests.Response,
    ) -> Generator[str | Any, Any, None]:
        """
        make the request and return the body

        :param stream: the stream
        :type method: request
        :returns: the message
        :rtype: dictionary
        """

        # TODO: test iter_lines()
        message = b""
        for char in stream.iter_content():
            if char == b"\n":
                yield message.decode("unicode_escape")
                message = b""
            else:
                message += char
