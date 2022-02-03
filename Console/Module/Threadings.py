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

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from Module.LoadConfig import Config
from Module.NetworkDiscover import NetworkDiscover
from Module.PrivateMessage import PrivateMessage
from Module.ScreenBroadcast import ScreenBroadcast
from Module.RemoteSpy import RemoteSpy
from Module.FileServer import FileServer


class NetworkDiscoverThread(QThread):
    def __init__(self, config: Config, parent=None):
        super(NetworkDiscoverThread, self).__init__(parent)
        self.current_ip = config.get_item('Network/Local/IP')
        self.socket_ip = config.get_item('Network/NetworkDiscover/IP')
        self.socket_port = config.get_item('Network/NetworkDiscover/Port')
        self.discover_interval = config.get_item('Network/NetworkDiscover/Interval', 5)
        self.socket = NetworkDiscover(self.current_ip, self.socket_ip, self.socket_port, self.discover_interval, self)

    def get_threadings_status(self):
        parent = self.parent()
        ftp_password = parent.file_server_thread.get_password()
        if ftp_password is None:
            ftp_password = ''
        result = {'screen_broadcast': parent.threadings['screen_broadcast_thread'],
                  'file_server': parent.threadings['file_server_thread'],
                  'file_server_password': ftp_password}
        return result

    def safe_stop(self):
        self.terminate()

    def run(self):
        self.socket.start()


class PrivateMessageThread(QThread):
    client_login_logout = pyqtSignal(str, str, str)
    client_desktop_received = pyqtSignal(str, object)
    client_notify_received = pyqtSignal(str)
    client_file_received = pyqtSignal(str, str)
    client_message_received = pyqtSignal(str, str)

    def __init__(self, config: Config, parent=None):
        super(PrivateMessageThread, self).__init__(parent)
        self.socket_ip = config.get_item('Network/Local/IP')
        self.socket_port = config.get_item('Network/PrivateMessage/Port')
        self.socket_buffer_size = config.get_item('Network/PrivateMessage/Buffer')
        self.config = config
        self.socket = PrivateMessage(self, self.socket_ip, self.socket_port, self.socket_buffer_size)

    def get_client_label_by_ip(self, label):
        return self.parent().get_client_label_by_ip(label)

    def safe_stop(self):
        self.terminate()

    def run(self):
        self.socket.start()


class ScreenBroadcastThread(QThread):
    def __init__(self, config: Config, parent=None):
        super(ScreenBroadcastThread, self).__init__(parent)
        self.current_ip = config.get_item('Network/Local/IP')
        self.socket_ip = config.get_item('Network/ScreenBroadcast/IP')
        self.socket_port = config.get_item('Network/ScreenBroadcast/Port')
        self.socket_buffer = config.get_item('Network/ScreenBroadcast/Buffer')
        self.quality = config.get_item('Network/ScreenBroadcast/Quality', 60)
        self.socket = ScreenBroadcast(self, self.current_ip, self.socket_ip, self.socket_port, self.socket_buffer,
                                      self.quality)

    def safe_stop(self):
        self.socket.working = False
        self.wait()

    def run(self):
        self.socket.working = True
        self.socket.start()


class RemoteSpyThread(QThread):
    frame_received = pyqtSignal(QPixmap)

    def __init__(self, config: Config, parent=None):
        super(RemoteSpyThread, self).__init__(parent)
        self.socket_port = config.get_item('Network/RemoteSpy/Port')
        self.socket = RemoteSpy(self, self.socket_port)

    def safe_stop(self):
        self.socket.working = False
        self.socket.stop()
        self.wait()

    def run(self):
        self.socket.working = True
        self.socket.start()


class FileServerThread(QThread):
    def __init__(self, config: Config, parent=None):
        super(FileServerThread, self).__init__(parent)
        self.current_ip = config.get_item('Network/Local/IP')
        self.socket_port = config.get_item('Network/FileServer/Port')
        self.socket = FileServer(self, self.current_ip, self.socket_port)

    def safe_stop(self):
        self.socket.stop()
        self.wait()

    def set_password(self, password):
        self.socket.ftp_password = password

    def get_password(self):
        return self.socket.ftp_password

    def set_working_dir(self, path):
        self.socket.working_path = path

    def run(self):
        self.socket.start()
