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


def set_default_client(
    config_file: Optional[str | Path] = None,
    api_endpoint_host: Optional[str] = None,
    api_endpoint_port: Optional[int] = None,
    http_basic_username: Optional[str] = None,
    http_basic_password: Optional[str] = None,
    client_private_key: Optional[str] = None,
    client_certificate: Optional[str] = None,
    ca_certificate: Optional[str] = None,
    suppress_exception: Optional[bool] = None,
) -> Client:
    """
    Set and configure the default client.

    :param config_file: The path of the configuration file to load.
    :param api_endpoint_host: The domain or the IP address of the API
        endpoint, e. g. ``icinga.example.com``, ``localhost`` or ``127.0.0.1``.
    :param api_endpoint_port: The TCP port of the API endpoint, for example
        ``5665``.
    :param http_basic_username: The name of the API user used in the HTTP basic
        authentification, e. g. ``apiuser``.
    :param http_basic_password: The password of the API user used in the HTTP
        basic authentification, e. g. ``password``.
    :param client_private_key: The file path of the client’s **private RSA
        key**, for example ``/etc/pretiac/api-client.key.pem``.
    :param client_certificate: The file path of the client’s **certificate**,
        for example ``/etc/pretiac/api-client.cert.pem``.
    :param ca_certificate: The file path of the Icinga **CA (Certification
        Authority)**, for example ``/var/lib/icinga2/certs/ca.crt``.
    :param suppress_exception: If set to ``True``, no exceptions are thrown.
    """
    global __client
    __client = Client(
        config_file=config_file,
        api_endpoint_host=api_endpoint_host,
        api_endpoint_port=api_endpoint_port,
        http_basic_username=http_basic_username,
        http_basic_password=http_basic_password,
        client_private_key=client_private_key,
        client_certificate=client_certificate,
        ca_certificate=ca_certificate,
        suppress_exception=suppress_exception,
    )
    return __client


def get_default_client() -> Client:
    """
    Get the default client.
    """
    global __client
    if not __client:
        __client = Client()
    return __client
