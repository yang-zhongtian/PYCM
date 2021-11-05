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

import socket
import struct
import zlib
import os
import base64
import pickle
import logging
from Module.Packages import FileServerFlag, FileClientFlag


class FileClient(object):
    socket_ip = None
    socket_port = None
    socket_obj = None

    def __init__(self, parent, socket_ip, socket_port):
        self.parent = parent
        self.socket_ip = socket_ip
        self.socket_port = socket_port
        self.__init_socket_obj()

    def __init_socket_obj(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def connect(self):
        self.socket_obj.connect((self.socket_ip, self.socket_port))

    def list_dir(self, path='/'):
        encoded_path = base64.b64encode(str(path).encode('utf-8'))
        target_head = struct.pack('!2i', FileClientFlag.ListDir, len(encoded_path))
        self.socket_obj.send(target_head)
        target_path = struct.pack(f'!{len(encoded_path)}s', encoded_path)
        self.socket_obj.send(target_path)
        data = self.socket_obj.recv(struct.calcsize('!2i'))
        data_flag, data_len = struct.unpack('!2i', data)
        if data_flag != FileServerFlag.ListDir:
            return []
        result = b''
        while len(result) < data_len:
            data = self.socket_obj.recv(1024)
            result += data
        result = pickle.loads(result)
        return result

    def download(self, count_signal, recieve_signal, files):
        encoded_path = pickle.dumps(files)
        target_head = struct.pack('!2i', FileClientFlag.DownloadFile, len(encoded_path))
        self.socket_obj.send(target_head)
        target_path = struct.pack(f'!{len(encoded_path)}s', encoded_path)
        self.socket_obj.send(target_path)
        head = self.socket_obj.recv(struct.calcsize('!2i'))
        flag, file_count = struct.unpack('!2i', head)
        if flag != FileServerFlag.FileDownloadStart:
            return
        count_signal.emit(file_count)
        for idx in range(file_count):
            file_head = self.socket_obj.recv(struct.calcsize('!i200si'))
            flag, file_path, file_size = struct.unpack('!i200si', file_head)
            if flag != FileServerFlag.FileInfo:
                continue
            file_path = file_path.rstrip(b'\x00').decode()
            buffer = b''
            while len(buffer) < file_size:
                file_data = self.socket_obj.recv(struct.calcsize('!i4096s'))
                flag, file_data = struct.unpack('!i4096s', file_data)
                if flag != FileServerFlag.FileData:
                    buffer = None
                    break
                buffer += file_data
            if buffer is not None:
                recieve_signal.emit(file_path, buffer)
        end = self.socket_obj.recv(struct.calcsize('!2i'))
        flag, file_count = struct.unpack('!2i', end)
        if flag != FileServerFlag.FileDownloadEnd:
            logging.warning(f'File download finish flag not found!')
