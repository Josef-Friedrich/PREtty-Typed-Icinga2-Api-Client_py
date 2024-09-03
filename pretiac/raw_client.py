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

from importlib.metadata import version as get_version

from pretiac.actions import Actions
from pretiac.config import Config
from pretiac.events import Events
from pretiac.objects import Objects
from pretiac.status import Status
from pretiac.templates import Templates


class RawClient:
    """
    This raw client is a thin wrapper around the Icinga2 REST API.

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

    def __init__(self, config: Config) -> None:
        """
        initialize object

        :param suppress_exception: If this parameter is set to ``True``, no exceptions are thrown.
        """
        self.config = config

        self.url = (
            f"https://{self.config.api_endpoint_host}:{self.config.api_endpoint_port}"
        )

        self.version = get_version("pretiac")

        self.actions = Actions(self)
        self.events = Events(self)
        self.objects = Objects(self)
        self.status = Status(self)
        self.templates = Templates(self)
