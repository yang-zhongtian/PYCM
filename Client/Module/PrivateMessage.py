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

from PyQt5.QtCore import pyqtSignal, QObject, QBuffer, QIODevice, Qt
from PyQt5.QtGui import QImage
import socket
import struct
from threading import Thread
from mss import mss
import zlib
from math import ceil
import time
from Module.Packages import NetworkDiscoverFlag, PrivateMessageFlag


class PrivateMessage(QObject):
    current_ip = None
    socket_ip = None
    socket_port = None
    socket_buffer_size = None
    socket_obj = None
    file_send_progress = pyqtSignal(float)

    def __init__(self, config):
        super(PrivateMessage, self).__init__()
        self.current_ip = config.get_item('Network/Local/IP')
        self.current_mac = config.get_item('Network/Local/MAC')
        self.socket_port = config.get_item('Network/PrivateMessage/Port')
        self.socket_buffer_size = config.get_item('Network/PrivateMessage/Buffer')
        self.__init_socket_obj()

    def __init_socket_obj(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.socket_buffer_size)

    def set_socket_ip(self, socket_ip):
        self.socket_ip = socket_ip

    def send_data(self, flag, data):
        payload_size = self.socket_buffer_size - struct.calcsize('!2i')
        socket_data = struct.pack(f'!2i{payload_size}s', flag, len(data), data)
        self.socket_obj.sendto(socket_data, (self.socket_ip, self.socket_port))

    def online_notify(self):
        self.send_data(PrivateMessageFlag.ClientLogin, str(self.current_mac).encode())

    def offline_notify(self):
        self.send_data(PrivateMessageFlag.ClientLogout, str(self.current_mac).encode())

    def notify_console(self):
        self.send_data(PrivateMessageFlag.ClientNotify, b'')

    def screen_spy_send(self):
        with mss() as sct:
            sct_img = sct.grab(sct.monitors[1])
            img = QImage(sct_img.rgb, sct_img.width, sct_img.height, QImage.Format_RGB888)
            img = img.scaled(360, 203, Qt.KeepAspectRatio)
            buffer = QBuffer()
            buffer.open(QIODevice.ReadWrite)
            img.save(buffer, 'JPEG', quality=75)
            img_compressed = zlib.compress(buffer.data())
            buffer.close()
            self.send_data(PrivateMessageFlag.ClientScreen, img_compressed)

    def send_file(self, file_buffer):
        chuck_size = self.socket_buffer_size - struct.calcsize('!5i')  # 包标志，包载荷长度，当前块编号，当前块实际载荷长度，总包数
        chuck_count = ceil(len(file_buffer) / chuck_size)
        for index in range(chuck_count):
            if index < chuck_count - 1:
                file_payload = file_buffer[index * chuck_size: (index + 1) * chuck_size]
            else:
                file_payload = file_buffer[index * chuck_size:]
            chuck_pack = struct.pack(f'!3i{chuck_size}s', index, len(file_payload), chuck_count, file_payload)
            self.send_data(PrivateMessageFlag.ClientFileData, chuck_pack)
            self.file_send_progress.emit((index + 1) / chuck_count)
            time.sleep(0.01)
        cksum_pack = struct.pack('!l', zlib.crc32(file_buffer))
        self.send_data(PrivateMessageFlag.ClientFileInfo, cksum_pack)
