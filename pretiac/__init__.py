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
pretiac is a `Python <http://www.python.org>`_ module to interact with the
`Icinga 2 RESTful API <https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/>`_.
"""

from pathlib import Path
from typing import Optional

from pretiac.client import Client

__client: Optional[Client] = None


def get_client(
    domain: Optional[str] = None,
    port: Optional[int] = None,
    api_user: Optional[str] = None,
    password: Optional[str] = None,
    certificate: Optional[str] = None,
    key: Optional[str] = None,
    ca_certificate: Optional[str] = None,
    config_file: Optional[str | Path] = None,
) -> Client:
    global __client
    if not __client:
        __client = Client(
            domain=domain,
            port=port,
            api_user=api_user,
            password=password,
            certificate=certificate,
            key=key,
            ca_certificate=ca_certificate,
            config_file=config_file,
        )
    return __client
