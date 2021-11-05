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
    working_path = 'D:/tes'

    def __init__(self, parent, socket_port):
        self.parent = parent
        self.socket_port = socket_port
        self.__init_socket_obj()

    def __init_socket_obj(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_obj.bind(('', self.socket_port))
        self.socket_obj.listen(100)
        self.socket_inputs.append(self.socket_obj)
        self.dir_filter = QDir.AllEntries | QDir.NoDotAndDotDot | QDir.NoSymLinks

    def walk_dir(self, path):
        path = QDir(path)
        files = []
        for file in path.entryInfoList(self.dir_filter):
            if file.isDir():
                files.extend(self.walk_dir(file.absoluteFilePath()))
            elif file.isFile():
                files.append(file.absoluteFilePath())
        return files

    def start(self):
        recv_header_size = struct.calcsize('!2i')
        while self.working:
            readable, writable, exceptionable = select.select(self.socket_inputs, [], [])
            for sock in readable:
                if sock == self.socket_obj:
                    socket_conn, socket_addr = sock.accept()
                    self.socket_inputs.append(socket_conn)
                else:
                    try:
                        socket_data = sock.recv(recv_header_size)
                    except ConnectionResetError:
                        self.socket_inputs.remove(sock)
                        sock.close()
                        continue
                    if socket_data:
                        socket_flag, path_len = struct.unpack('!2i', socket_data)
                        path = struct.unpack(f'!{path_len}s', sock.recv(path_len))[0]
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
                            sock.send(struct.pack('!2i', FileServerFlag.ListDir, len(list_data)))
                            sock.sendall(list_data)
                        elif socket_flag == FileServerFlag.DownloadFile:
                            path = pickle.loads(path)
                            files = []
                            for file in path:
                                file = QFileInfo(real_path.absoluteFilePath(file.lstrip('/')))
                                if file.isFile():
                                    files.append([file, file.absoluteFilePath()])
                                elif file.isDir():
                                    files.extend(self.walk_dir(file.absoluteFilePath()))
                            print(files)
                    else:
                        self.socket_inputs.remove(sock)
                        sock.close()

    def close(self):
        self.socket_obj.close()
