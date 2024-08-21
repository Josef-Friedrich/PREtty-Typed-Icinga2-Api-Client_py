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
Icinga 2 API client config file
"""

import configparser as configparser
import os
from typing import Optional

from pretiac.exceptions import PretiacConfigFileException


class ClientConfigFile(object):
    """
    Icinga 2 API config file
    """

    file_name: Optional[str]

    section: str

    url: Optional[str]

    username: Optional[str]

    password: Optional[str]

    timeout: Optional[int]

    certificate: Optional[str]

    key: Optional[str]

    ca_certificate: Optional[str]

    def __init__(self, file_name: Optional[str]) -> None:
        """
        initialization
        """

        self.file_name = file_name
        self.section = "api"
        self.url = None
        self.username = None
        self.password = None
        self.certificate = None
        self.key = None
        self.ca_certificate = None
        self.timeout = None
        if self.file_name:
            self.check_access()

    def check_access(self):
        """
        check access to the config file

        :returns: True
        :rtype: bool
        """

        if not self.file_name:
            return False

        if not os.path.exists(self.file_name):
            raise PretiacConfigFileException(
                'Config file "{0}" doesn\'t exist.'.format(self.file_name)
            )

        if not os.access(self.file_name, os.R_OK):
            raise PretiacConfigFileException(
                'No read access for config file "{0}".\n'.format(self.file_name)
            )

        return True

    def parse(self) -> None:
        """
        parse the config file
        """

        if not self.file_name:
            raise PretiacConfigFileException("Config file isn't specifieds.")

        cfg = configparser.ConfigParser()
        cfg.read(self.file_name)

        if not cfg.has_section(self.section):
            raise PretiacConfigFileException(
                'Config file is missing "{0}" section.'.format(self.section)
            )

        # [api]/url
        try:
            self.url = str(cfg.get(self.section, "url")).strip()
        except configparser.NoOptionError:
            pass

        # [api]/username
        try:
            self.username = str(cfg.get(self.section, "username")).strip()
        except configparser.NoOptionError:
            pass

        # [api]/password
        # do we really want to store the password here
        # or use the keyring
        try:
            self.password = str(cfg.get(self.section, "password")).strip()
        except configparser.NoOptionError:
            pass

        # [api]/certificate
        try:
            self.certificate = str(cfg.get(self.section, "certificate")).strip()
        except configparser.NoOptionError:
            pass

        # [api]/client_key
        try:
            self.key = str(cfg.get(self.section, "key")).strip()
        except configparser.NoOptionError:
            pass

        # [api]/ca_certificate
        try:
            self.ca_certificate = str(cfg.get(self.section, "ca_certificate")).strip()
        except configparser.NoOptionError:
            pass

        # [api]/timeout
        try:
            self.timeout = int(str(cfg.get(self.section, "timeout")).strip())
        except configparser.NoOptionError:
            pass
