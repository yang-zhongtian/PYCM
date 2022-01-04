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

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QImage, QPixmap
from Module.Packages import ScreenBroadcastFlag
import socket
import struct
import zlib
from threading import Thread, Lock
from queue import Queue
import logging


class ScreenBroadcast(QObject):
    def __init__(self, parent, current_ip, socket_ip, socket_port, socket_buffer):
        super(ScreenBroadcast, self).__init__()
        self.parent = parent
        self.current_ip = current_ip
        self.socket_ip = socket_ip
        self.socket_port = socket_port
        self.socket_buffer = socket_buffer
        self.frames_queue = Queue()
        self.working = False
        self.__init_socket_obj()

    def __init_socket_obj(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket_obj.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.socket_buffer)
        self.socket_obj.bind(('', self.socket_port))
        self.socket_obj.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_ADD_MEMBERSHIP,
            socket.inet_aton(self.socket_ip) + socket.inet_aton(self.current_ip)
        )

    def __receive_thread(self):
        header_size = struct.calcsize('!4i')
        payload_size = self.socket_buffer - struct.calcsize('!2i')
        frame_data = b''
        pack_drop_flag = False
        pack_drop_buffer = b''
        while self.working:
            try:
                if not pack_drop_flag:
                    socket_data, _ = self.socket_obj.recvfrom(header_size)
                else:
                    socket_data = pack_drop_buffer
                    pack_drop_flag = False
                    pack_drop_buffer = b''
                data_flag, data_index, data_length, data_rounds = struct.unpack('!4i', socket_data)
                if data_flag == ScreenBroadcastFlag.PackInfo:
                    while len(frame_data) < data_length:
                        socket_data, _ = self.socket_obj.recvfrom(self.socket_buffer)
                        data_flag, pack_length, pack = struct.unpack(f'!2i{payload_size}s', socket_data)
                        pack = pack[:pack_length]
                        if data_flag == ScreenBroadcastFlag.PackData:
                            frame_data += pack
                        elif data_flag == ScreenBroadcastFlag.PackInfo:
                            pack_drop_flag = True
                            pack_drop_buffer = socket_data
                            break
                    if pack_drop_flag:
                        continue
                    elif len(frame_data) == data_length:
                        frame = zlib.decompress(frame_data)
                        self.frames_queue.put(frame)
                        frame_data = b''
                    elif len(frame_data) > data_length:
                        frame_data = b''
            except (OSError, struct.error):
                continue
            except Exception as e:
                logging.warning(f'Failed to handle frame: {e}')

    def start(self):
        Thread(target=self.__receive_thread, daemon=True).start()
        while self.working:
            frame_raw = self.frames_queue.get()
            frame_qimage = QImage.fromData(frame_raw)
            self.parent.frame_received.emit(QPixmap.fromImage(frame_qimage))
