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

from PyQt5.QtWidgets import QFileIconProvider
from PyQt5.QtCore import QDir, QFile, QFileInfo
import socket
import struct
import select
import pickle
import base64
import zlib
import os
import logging
from Module.Packages import FileClientFlag, FileServerFlag


class FileServer(object):
    socket_port = None
    socket_obj = None
    socket_inputs = []
    working = False
    working_path = '.'

    def __init__(self, parent, socket_port):
        self.parent = parent
        self.socket_port = socket_port

    def __init_socket_obj(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_obj.bind(('', self.socket_port))
        self.socket_obj.listen(100)
        self.socket_inputs.append(self.socket_obj)
        self.dir_filter = QDir.AllEntries | QDir.NoDotAndDotDot | QDir.NoSymLinks

    def start(self):
        self.__init_socket_obj()
        recv_header_size = struct.calcsize('!2iL')
        while self.working:
            readable, writable, exceptionable = select.select(self.socket_inputs, [], [])
            for sock in readable:
                if sock == self.socket_obj:
                    try:
                        socket_conn, socket_addr = sock.accept()
                        self.socket_inputs.append(socket_conn)
                    except OSError:
                        continue
                else:
                    try:
                        socket_data = sock.recv(recv_header_size)
                    except ConnectionResetError:
                        self.socket_inputs.remove(sock)
                        sock.close()
                        continue
                    except OSError:
                        continue
                    if socket_data:
                        self.handle_socket(sock, socket_data)
                    else:
                        self.socket_inputs.remove(sock)
                        sock.close()

    def handle_socket(self, sock, socket_data):
        socket_flag, path_len, cksum = struct.unpack('!2iL', socket_data)
        path = struct.unpack(f'!{path_len}s', sock.recv(path_len))[0]
        if zlib.crc32(path) != cksum:
            return
        real_path = QDir(self.working_path)
        if socket_flag == FileClientFlag.ListDir:
            path = base64.b64decode(path).decode('utf-8').lstrip('/')
            real_path.cd(path)
            list_dir = []
            for file in real_path.entryList(self.dir_filter):
                info = QFileInfo(real_path.filePath(file))
                if info.isFile():
                    file_type = 0
                elif info.isDir():
                    file_type = 1
                else:
                    file_type = -1
                list_dir.append({'name': info.fileName(), 'type': file_type})
            list_data = pickle.dumps(list_dir)
            cksum = zlib.crc32(list_data)
            sock.send(struct.pack('!2iL', FileServerFlag.ListDir, len(list_data), cksum))
            sock.sendall(list_data)
        elif socket_flag == FileClientFlag.DownloadFile:
            path = pickle.loads(path)
            files = []
            for file_path in path:
                file = QFileInfo(real_path.absoluteFilePath(file_path.lstrip('/')))
                if file.isFile():
                    files.append([file_path, file.absoluteFilePath(), file.size()])
            sock.send(struct.pack('!2i', FileServerFlag.FileDownloadStart, len(files)))
            for file_label, file_path, file_size in files:
                sock.send(struct.pack('!i200si', FileServerFlag.FileInfo,
                                      file_label.encode(), file_size))
                file_handle = open(file_path, 'rb')
                while True:
                    file_chuck = file_handle.read(4096)
                    if not file_chuck:
                        break
                    sock.send(struct.pack('!i4096s', FileServerFlag.FileData, file_chuck))
            sock.send(struct.pack('!2i', FileServerFlag.FileDownloadEnd, len(files)))

    def close(self):
        if self.socket_obj is not None:
            self.socket_obj.close()
            self.socket_inputs.clear()
            self.socket_obj = None
