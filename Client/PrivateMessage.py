from PyQt5.QtCore import pyqtSignal, QObject
import socket
import struct
from threading import Thread
from mss import mss
from PIL import Image
import zlib
from io import BytesIO
from math import ceil
import time
from Packages import NetworkDiscoverFlag, PrivateMessageFlag


class PrivateMessage(QObject):
    current_ip = None
    socket_ip = None
    socket_port = None
    socket_buffer_size = None
    socket_obj = None
    file_send_progress = pyqtSignal(float)

    def __init__(self, current_ip, socket_ip, socket_port, socket_buffer_size):
        super(PrivateMessage, self).__init__()
        self.current_ip = current_ip
        self.socket_ip = socket_ip
        self.socket_port = socket_port
        self.socket_buffer_size = socket_buffer_size
        self.__init_socket_obj()

    def __init_socket_obj(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def send_data(self, flag, data):
        payload_size = self.socket_buffer_size - struct.calcsize('!2i')
        socket_data = struct.pack(f'!2i{payload_size}s', flag, len(data), data)
        self.socket_obj.sendto(socket_data, (self.socket_ip, self.socket_port))

    def online_notify(self):
        self.send_data(PrivateMessageFlag.ClientLogin, socket.inet_aton(self.current_ip))

    def offline_notify(self):
        self.send_data(PrivateMessageFlag.ClientLogout, socket.inet_aton(self.current_ip))

    def screen_spy_send(self):
        with mss() as sct:
            sct_img = sct.grab(sct.monitors[1])
            img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
            img = img.resize((img.size[0] // 4, img.size[1] // 4), Image.ANTIALIAS)
            img_bytes = BytesIO()
            img.save(img_bytes, format='JPEG')
            img_compressed = zlib.compress(img_bytes.getvalue())
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
            self.send_data(PrivateMessageFlag.ClientFile, chuck_pack)
            self.file_send_progress.emit((index + 1) / chuck_count)
            time.sleep(0.01)


if __name__ == '__main__':
    A = PrivateMessage('192.168.1.8', '192.168.1.8', 4089, 32768)
