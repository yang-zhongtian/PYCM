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

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from Module.NetworkDiscover import NetworkDiscover
from Module.PrivateMessage import PrivateMessage
from Module.ScreenBroadcast import ScreenBroadcast
from Module.RemoteSpy import RemoteSpy
from Module.FileServer import FileServer


class NetworkDiscoverThread(QThread):
    def __init__(self, config):
        super(NetworkDiscoverThread, self).__init__()
        self.current_ip = config.get_item('Network/Local/IP')
        self.socket_ip = config.get_item('Network/NetworkDiscover/IP')
        self.socket_port = config.get_item('Network/NetworkDiscover/Port')
        self.discover_interval = config.get_item('Network/NetworkDiscover/Interval', 5)
        self.socket = NetworkDiscover(self.current_ip, self.socket_ip, self.socket_port, self.discover_interval)

    def run(self):
        self.socket.start()


class PrivateMessageThread(QThread):
    client_login_logout = pyqtSignal(str, str, str)
    client_desktop_recieved = pyqtSignal(str, object)
    client_notify_recieved = pyqtSignal(str)
    client_file_recieved = pyqtSignal(str, str)

    def __init__(self, config: object, parent: object = None):
        super(PrivateMessageThread, self).__init__()
        self.socket_ip = config.get_item('Network/Local/IP')
        self.socket_port = config.get_item('Network/PrivateMessage/Port')
        self.socket_buffer_size = config.get_item('Network/PrivateMessage/Buffer')
        self.config = config
        self.socket = PrivateMessage(self, parent, self.socket_ip, self.socket_port, self.socket_buffer_size)

    def run(self):
        self.socket.start()


class ScreenBroadcastThread(QThread):
    def __init__(self, config: object):
        super(ScreenBroadcastThread, self).__init__()
        self.current_ip = config.get_item('Network/Local/IP')
        self.socket_ip = config.get_item('Network/ScreenBroadcast/IP')
        self.socket_port = config.get_item('Network/ScreenBroadcast/Port')
        self.socket_buffer = config.get_item('Network/ScreenBroadcast/Buffer')
        self.quality = config.get_item('Network/ScreenBroadcast/Quality', 60)
        self.socket = ScreenBroadcast(self, self.current_ip, self.socket_ip, self.socket_port, self.socket_buffer,
                                      self.quality)

    def safe_stop(self):
        self.socket.working = False

    def run(self):
        self.socket.working = True
        self.socket.start()


class RemoteSpyThread(QThread):
    frame_recieved = pyqtSignal(QPixmap)

    def __init__(self, config: object):
        super(RemoteSpyThread, self).__init__()
        self.socket_port = config.get_item('Network/RemoteSpy/Port')
        self.socket = RemoteSpy(self, self.socket_port)

    def safe_stop(self):
        self.socket.stop()

    def run(self):
        self.socket.start()


class FileServerThread(QThread):
    def __init__(self, config: object):
        super(FileServerThread, self).__init__()
        self.socket_port = config.get_item('Network/FileServer/Port')
        self.socket = FileServer(self, self.socket_port)

    def safe_stop(self):
        self.socket.working = False
        self.socket.close()

    def set_working_dir(self, path):
        self.socket.working_path = path

    def run(self):
        self.socket.working = True
        self.socket.start()
