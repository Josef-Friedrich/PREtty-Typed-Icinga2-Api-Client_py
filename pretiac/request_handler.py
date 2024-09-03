# Copyright 2017 fmnisme@gmail.com christian@jonak.org
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# @author: Christian Jonak-Moechel, fmnisme, Tobias von der Krone
# @contact: christian@jonak.org, fmnisme@gmail.com, tobias@vonderkrone.info
# @summary: Python library for the Icinga 2 RESTful API

"""
Provides the base class :class:`RequestHandler` that is inherited by the different
endpoint classes, for example the class ``Events`` handles the ``v1/events`` endpoint,
the class ``Objects`` handles the ``v1/objects`` entpoint and so on...
"""

from typing import (
    TYPE_CHECKING,
    Any,
    Generator,
    Optional,
)
from urllib.parse import urljoin

import requests
import urllib3

from pretiac.config import Config
from pretiac.exceptions import PretiacException, PretiacRequestException
from pretiac.object_types import (
    HostState,
    ObjectTypeName,
    Payload,
    RequestMethod,
    ServiceState,
    State,
)

if TYPE_CHECKING:
    from pretiac.raw_client import RawClient

# https://stackoverflow.com/a/28002687
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def normalize_state(state: State | Any) -> int:
    if isinstance(state, ServiceState) or isinstance(state, HostState):
        return state.value
    if isinstance(state, int) and 0 <= state <= 3:
        return state
    raise PretiacException("invalid")


class RequestHandler:
    """
    Handles the HTTP requests to the Icinga2 API.
    """

    raw_client: "RawClient"

    base_url_path: Optional[str] = None

    def __init__(self, client: "RawClient") -> None:
        """
        initialize object
        """

        self.raw_client = client
        self.stream_cache = ""

    @property
    def base_url(self) -> str:
        if not self.base_url_path:
            raise PretiacException("Specify self.base_url_path")
        return self.base_url_path

    @property
    def config(self) -> Config:
        return self.raw_client.config

    def _create_session(self, method: RequestMethod = "POST") -> requests.Session:
        """
        create a session object
        """

        session = requests.Session()
        # prefer certificate authentification
        if self.config.client_certificate and self.config.client_private_key:
            # The certificate and RSA private key are in different files.
            session.cert = (
                self.config.client_certificate,
                self.config.client_private_key,
            )
        elif self.config.client_certificate:
            # The certificate and RSA private key are in the same file.
            session.cert = self.config.client_certificate
        elif self.config.http_basic_username and self.config.http_basic_password:
            # use username and password
            session.auth = (
                self.config.http_basic_username,
                self.config.http_basic_password,
            )
        session.headers = {
            "User-Agent": "Python-pretiac/{0}".format(self.raw_client.version),
            "X-HTTP-Method-Override": method.upper(),
            "Accept": "application/json",
        }

        return session

    @staticmethod
    def _pluralize(object_type: ObjectTypeName) -> str:
        return f"{object_type.lower()}s"

    def _throw_exception(self, suppress_exception: Optional[bool] = None) -> bool:
        if isinstance(suppress_exception, bool):
            return not suppress_exception
        if isinstance(self.config.suppress_exception, bool):
            return not self.config.suppress_exception
        return True

    def _request(
        self,
        method: RequestMethod,
        url_path: str,
        payload: Optional[dict[str, Any]] = None,
        stream: bool = False,
        suppress_exception: Optional[bool] = None,
    ) -> Any:
        """
        make the request and return the body

        :param method: the HTTP method
        :param url_path: the requested url path
        :param payload: the payload to send
        :param suppress_exception: If this parameter is set to ``True``, no exceptions are thrown.

        :returns: the response as json
        """

        request_url = urljoin(self.raw_client.url, url_path)

        # create session
        session = self._create_session(method)

        # create arguments for the request
        request_args: Payload = {"url": request_url}
        if payload:
            request_args["json"] = payload
        if self.config.ca_certificate:
            request_args["verify"] = self.config.ca_certificate
        else:
            request_args["verify"] = False
        if stream:
            request_args["stream"] = True

        # do the request
        response: requests.Response = session.post(**request_args)

        if not stream:
            session.close()

        if (
            self._throw_exception(suppress_exception)
            and not 200 <= response.status_code <= 299
        ):
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
        Make the request and return the body.

        :param stream: The stream.

        :returns: The message.
        """

        # TODO: test iter_lines()
        message = b""
        for char in stream.iter_content():
            if char == b"\n":
                yield message.decode("unicode_escape")
                message = b""
            else:
                message += char
