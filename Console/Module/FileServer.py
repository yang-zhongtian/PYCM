# -*- coding: utf-8 -*-
"""
    This file is part of PYCM project
    Copyright (C)2021 Richard Yang <zhongtian.yang@qq.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from Module.FTPLib.authorizers import DummyAuthorizer
from Module.FTPLib.handlers import FTPHandler
from Module.FTPLib.servers import FTPServer
import logging


class FileServer(object):
    working = False
    working_path = '.'
    current_ip = None
    ftp_port = None
    ftp_password = None
    authorizer = None
    handler = None
    server = None

    def __init__(self, parent, current_ip, ftp_port):
        self.parent = parent
        self.current_ip = current_ip
        self.ftp_port = ftp_port

    def __init_ftp_server(self):
        self.authorizer = DummyAuthorizer()
        print(self.ftp_password)
        self.authorizer.add_user('pycm', self.ftp_password, self.working_path, perm='elr')
        self.handler = FTPHandler
        self.handler.authorizer = self.authorizer
        self.handler.encoding = 'gbk'
        self.server = FTPServer((self.current_ip, self.ftp_port), self.handler)

    def start(self):
        self.__init_ftp_server()
        self.server.serve_forever()

    def close(self):
        if self.server is not None:
            self.server.close_all()
        self.authorizer = None
        self.handler = None
        self.server = None
