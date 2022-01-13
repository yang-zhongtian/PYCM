# -*- coding: utf-8 -*-
"""
    This file is part of PYCM project
    Copyright (C) 2021 Richard Yang  <zhongtian.yang@qq.com>

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

import socket
import time
import struct
import logging
from Module.Packages import NetworkDiscoverFlag


class NetworkDiscover(object):
    current_ip = None
    socket_ip = None
    socket_port = None
    socket_obj = None
    discover_interval = None

    def __init__(self, current_ip, socket_ip, socket_port, discover_interval=5):
        self.current_ip = current_ip
        self.socket_ip = socket_ip
        self.socket_port = socket_port
        self.discover_interval = discover_interval
        self.__init_socket_obj()

    def __init_socket_obj(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket_obj.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        self.socket_obj.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_ADD_MEMBERSHIP,
            socket.inet_aton(self.socket_ip) + socket.inet_aton(self.current_ip)
        )

    def start(self):
        socket_packet = struct.pack('!i', NetworkDiscoverFlag.ConsoleFlag)
        while True:
            try:
                self.socket_obj.sendto(socket_packet, (self.socket_ip, self.socket_port))
                time.sleep(self.discover_interval)
            except Exception as e:
                logging.warning(f'Failed to send net discover pack: {e}')
