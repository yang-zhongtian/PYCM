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

from PyQt5.QtCore import QObject, QBuffer, QIODevice, Qt
from PyQt5.QtGui import QImage, QPainter, QCursor
import socket
import struct
from threading import Thread
from mss import mss
import zlib
import logging
from Module.Packages import RemoteSpyFlag


class RemoteSpy(QObject):
    socket_ip = None
    socket_port = None
    socket_obj = None
    working = False
    screen_send_thread = None

    def __init__(self, socket_port):
        super(RemoteSpy, self).__init__()
        self.socket_port = socket_port
        self.init_socket_obj()

    def init_socket_obj(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def set_socket_ip(self, socket_ip):
        self.socket_ip = socket_ip

    def screen_send(self):
        cursor = QCursor()
        while self.working:
            try:
                with mss() as sct:
                    frame = sct.grab(sct.monitors[1])
                    cursor_pos = cursor.pos()
                    img = QImage(frame.rgb, frame.width, frame.height, QImage.Format_RGB888)
                    painter = QPainter()
                    painter.begin(img)
                    painter.setBrush(Qt.red)
                    painter.drawEllipse(cursor_pos, 5, 5)
                    painter.end()
                    buffer = QBuffer()
                    buffer.open(QIODevice.ReadWrite)
                    img.save(buffer, 'JPEG', quality=80)
                    img_encoded = zlib.compress(buffer.data())
                    buffer.close()
                    header = struct.pack('!2i', RemoteSpyFlag.PackInfo, len(img_encoded))
                    self.socket_obj.send(header)
                    self.socket_obj.sendall(img_encoded)
            except ConnectionResetError:
                break
            except Exception as e:
                logging.warning(f'Screen send thread unexpected error: {e}')

    def stop(self):
        self.working = False
        if self.screen_send_thread is not None:
            self.screen_send_thread.join()
        if self.socket_obj is not None:
            self.socket_obj.close()
            self.socket_obj = None

    def start(self):
        self.socket_obj.connect((self.socket_ip, self.socket_port))
        self.screen_send_thread = Thread(target=self.screen_send, daemon=True)
        self.screen_send_thread.start()
        recv_header_size = struct.calcsize('!i')
        while self.working:
            try:
                socket_data = self.socket_obj.recv(recv_header_size)
                if not socket_data:
                    self.stop()
                    break
                flag = struct.unpack('!i', socket_data)[0]
                if flag == RemoteSpyFlag.RemoteSpyStop:
                    self.socket_obj.send(struct.pack('!2i', RemoteSpyFlag.RemoteSpyStop, 0))
                    self.stop()
                    break
            except ConnectionResetError:
                self.stop()
            except Exception as e:
                logging.warning(f'Error: {e}')
