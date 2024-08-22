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

import logging
from typing import Optional

import pretiac
from pretiac.actions import Actions
from pretiac.events import Events
from pretiac.exceptions import PretiacException
from pretiac.objects import Objects
from pretiac.status import Status

LOG = logging.getLogger(__name__)


class Client:
    """
    Icinga 2 Client class
    """

    domain: str

    port: int

    url: str

    api_user: Optional[str]

    password: Optional[str]

    timeout: Optional[int]

    certificate: Optional[str]

    key: Optional[str]

    ca_certificate: Optional[str]

    objects: Objects

    actions: Actions

    events: Events

    status: Status

    version: str

    def __init__(
        self,
        domain: str,
        port: int = 5665,
        api_user: Optional[str] = None,
        password: Optional[str] = None,
        certificate: Optional[str] = None,
        key: Optional[str] = None,
        ca_certificate: Optional[str] = None,
    ) -> None:
        """
        initialize object
        """
        self.domain = domain
        self.port = port
        self.url = f"https://{domain}:{port}"
        self.api_user = api_user
        self.password = password
        self.certificate = certificate
        self.key = key
        self.ca_certificate = ca_certificate
        self.objects = Objects(self)
        self.actions = Actions(self)
        self.events = Events(self)
        self.status = Status(self)
        self.version = pretiac.__version__

        if not self.api_user and not self.password and not self.certificate:
            raise PretiacException("Neither username/password nor certificate defined.")
