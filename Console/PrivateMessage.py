from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
import socket
import struct
from threading import Thread
from PIL import Image
from PIL.ImageQt import ImageQt
from io import BytesIO
import zlib
from Packages import NetworkDiscoverFlag, PrivateMessageFlag


class PrivateMessage(object):
    socket_ip = None
    socket_port = None
    socket_buffer_size = None
    socket_obj = None

    def __init__(self, parent, socket_ip, socket_port, socket_buffer_size):
        self.parent = parent
        self.socket_ip = socket_ip
        self.socket_port = socket_port
        self.socket_buffer_size = socket_buffer_size
        self.__init_socket_obj()

    def __init_socket_obj(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_obj.bind(('', self.socket_port))

    def start(self):
        payload_size = self.socket_buffer_size - struct.calcsize('!i')
        while True:
            try:
                socket_data, socket_addr = self.socket_obj.recvfrom(self.socket_buffer_size)
                unpacked_flag, unpacked_data = struct.unpack(f'!i{payload_size}s', socket_data)
                unpacked_data = unpacked_data.strip(b'\x00')
                if unpacked_flag == PrivateMessageFlag.ClientLogin:
                    client_ip = socket.inet_ntoa(unpacked_data)
                    self.parent.client_login_logout.emit('online', client_ip)
                elif unpacked_flag == PrivateMessageFlag.ClientLogout:
                    client_ip = socket.inet_ntoa(unpacked_data)
                    self.parent.client_login_logout.emit('offline', client_ip)
                elif unpacked_flag == PrivateMessageFlag.ClientScreen:
                    unpacked_data = zlib.decompress(unpacked_data)
                    image = Image.open(BytesIO(unpacked_data)).toqpixmap()
                    self.parent.client_desktop_recieved.emit(socket_addr[0], image)

            except KeyboardInterrupt:
                self.socket_obj.close()
                return None
            except Exception as e:
                print(e)


if __name__ == '__main__':
    A = PrivateMessage('192.168.1.8', 4089, 32768)
