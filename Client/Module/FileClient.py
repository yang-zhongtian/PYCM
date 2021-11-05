import socket
import struct
import zlib
import os
import base64
import pickle
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

    def download(self, files):
        encoded_path = pickle.dumps(files)
        target_head = struct.pack('!2i', FileClientFlag.DownloadFile, len(encoded_path))
        self.socket_obj.send(target_head)
        target_path = struct.pack(f'!{len(encoded_path)}s', encoded_path)
        self.socket_obj.send(target_path)
