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
Icinga 2 API client

The Icinga 2 API allows you to manage configuration objects and resources in a simple,
programmatic way using HTTP requests.
"""

from __future__ import print_function

from importlib.metadata import version as get_version
from pathlib import Path
from typing import Optional

from pretiac.actions import Actions
from pretiac.config import Config, load_config
from pretiac.events import Events
from pretiac.exceptions import PretiacException
from pretiac.objects import Objects
from pretiac.status import Status
from pretiac.templates import Templates


class Client:
    """
    Icinga 2 Client class

    You can use the client with either username/password combination or using certificates.

    Example using username and password:

    .. code-block:: python

        from pretiac.client import Client

        client = Client("localhost", 5665, "username", "password")

    Example using certificates:

    .. code-block:: python

        client = Client(
            "localhost",
            5665,
            certificate="/etc/ssl/certs/myhostname.crt",
            key="/etc/ssl/keys/myhostname.key",
        )

    If your public and private are in the same file, just use the `certificate` parameter.


    To verify the server certificate specify a ca file as `ca_file` parameter.

    Example:

    .. code-block:: python

        from pretiac.client import Client

        client = Client(
            "https://icinga2:5665",
            certificate="/etc/ssl/certs/myhostname.crt",
            key="/etc/ssl/keys/myhostname.key",
            ca_file="/etc/ssl/certs/my_ca.crt",
        )

    """

    config: Config

    url: str

    version: str

    actions: Actions

    events: Events

    objects: Objects

    status: Status

    templates: Templates

    def __init__(
        self,
        domain: Optional[str] = None,
        port: Optional[int] = None,
        api_user: Optional[str] = None,
        password: Optional[str] = None,
        certificate: Optional[str] = None,
        key: Optional[str] = None,
        ca_certificate: Optional[str] = None,
        config_file: Optional[str | Path] = None,
        suppress_exception: Optional[bool] = None,
    ) -> None:
        """
        initialize object

        :param suppress_exception: If this parameter is set to ``True``, no exceptions are thrown.
        """
        config: Config = load_config(config_file)
        self.config = config

        if domain is not None:
            config.domain = domain

        if config.domain is None:
            raise PretiacException("no domain")

        if port is not None:
            config.port = port

        if config.port is None:
            config.port = 5665

        self.url = f"https://{config.domain}:{config.port}"

        if api_user is not None:
            config.api_user = api_user

        if password is not None:
            config.password = password

        if certificate is not None:
            config.certificate = certificate

        if key is not None:
            config.key = key

        if ca_certificate is not None:
            config.ca_certificate = ca_certificate

        if suppress_exception is not None:
            config.suppress_exception = suppress_exception

        self.version = get_version("pretiac")

        self.actions = Actions(self)
        self.events = Events(self)
        self.objects = Objects(self)
        self.status = Status(self)
        self.templates = Templates(self)

        if (
            not self.config.api_user
            and not self.config.password
            and not self.config.certificate
        ):
            raise PretiacException("Neither username/password nor certificate defined.")
