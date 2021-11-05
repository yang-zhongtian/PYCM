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

from PyQt5.QtGui import QImage, QPixmap
import socket
import struct
import zlib
import time
import os
import logging
from Module.Packages import PrivateMessageFlag


class FileMerger(object):
    file_buffer = None

    def __init__(self, config, root_parent=None):
        self.chuck_count = None
        self.file_buffer = {}
        self.config = config
        self.root_parent = root_parent

    def update_chuck(self, ip, index, amount, buffer):
        if ip not in self.file_buffer.keys():
            self.file_buffer[ip] = {'chuck_count': amount, 'buffers': []}
        self.file_buffer[ip]['buffers'].append((index, buffer))

    def write_file(self, ip, cksum):
        if len(self.file_buffer[ip]['buffers']) >= self.file_buffer[ip]['chuck_count']:
            file_buffer_sorted = sorted(self.file_buffer[ip]['buffers'], key=lambda x: x[0])
            file_data = b''.join(map(lambda x: x[1], file_buffer_sorted))
            if zlib.crc32(file_data) == cksum:
                file_timestamp = time.strftime("%Y%m%d-%H.%M.%S", time.localtime(time.time()))
                file_name = f'[{file_timestamp}] {self.root_parent.get_client_label_by_ip(ip)}.zip'
                open(os.path.join(self.config.get_item('Client/FileUploadPath'), file_name), 'wb').write(file_data)
                self.file_buffer.pop(ip)
                return file_name
        self.file_buffer.pop(ip)
        return None


class PrivateMessage(object):
    socket_ip = None
    socket_port = None
    socket_buffer_size = None
    socket_obj = None

    def __init__(self, parent, root_parent, socket_ip, socket_port, socket_buffer_size):
        self.parent = parent
        self.root_parent = root_parent
        self.socket_ip = socket_ip
        self.socket_port = socket_port
        self.socket_buffer_size = socket_buffer_size
        self.__init_socket_obj()

    def __init_socket_obj(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_obj.bind(('', self.socket_port))

    def start(self):
        payload_size = self.socket_buffer_size - struct.calcsize('!2i')
        chuck_size = self.socket_buffer_size - struct.calcsize('!5i')
        file_merger = FileMerger(self.parent.config, self.root_parent)
        while True:
            try:
                socket_data, socket_addr = self.socket_obj.recvfrom(self.socket_buffer_size)
                unpacked_flag, unpacked_length, unpacked_data = struct.unpack(f'!2i{payload_size}s', socket_data)
                unpacked_data = unpacked_data[:unpacked_length]
                if unpacked_flag == PrivateMessageFlag.ClientLogin:
                    client_mac = unpacked_data.decode()
                    self.parent.client_login_logout.emit('online', socket_addr[0], client_mac)
                elif unpacked_flag == PrivateMessageFlag.ClientLogout:
                    client_mac = unpacked_data.decode()
                    self.parent.client_login_logout.emit('offline', socket_addr[0], client_mac)
                elif unpacked_flag == PrivateMessageFlag.ClientScreen:
                    unpacked_data = zlib.decompress(unpacked_data)
                    image = QImage.fromData(unpacked_data)
                    self.parent.client_desktop_recieved.emit(socket_addr[0], QPixmap.fromImage(image))
                elif unpacked_flag == PrivateMessageFlag.ClientNotify:
                    self.parent.client_notify_recieved.emit(socket_addr[0])
                elif unpacked_flag == PrivateMessageFlag.ClientFileData:
                    file_index, file_buffer_length, file_amount, file_buffer = struct.unpack(f'!3i{chuck_size}s',
                                                                                             unpacked_data)
                    file_merger.update_chuck(socket_addr[0], file_index, file_amount, file_buffer[:file_buffer_length])
                elif unpacked_flag == PrivateMessageFlag.ClientFileInfo:
                    file_cksum = struct.unpack('!l', unpacked_data)[0]
                    status = file_merger.write_file(socket_addr[0], file_cksum)
                    if status is not None:
                        self.parent.client_file_recieved.emit(socket_addr[0], status)
            except Exception as e:
                logging.warning(f'Failed to decode socket data: {e}')
