from PyQt5.QtCore import QObject
import socket
import time
import struct
import base64
from Packages import ClassBroadcastFlag


class ClassBroadcast(QObject):
    parent = None
    current_ip = None
    socket_ip = None
    socket_port = None
    socket_buffer_size = None
    socket_obj = None

    def __init__(self, parent, current_ip, socket_ip, socket_port, socket_buffer_size):
        super(ClassBroadcast, self).__init__(parent)
        self.parent = parent
        self.current_ip = current_ip
        self.socket_ip = socket_ip
        self.socket_port = socket_port
        self.socket_buffer_size = socket_buffer_size
        self.__init_socket_obj()

    def __init_socket_obj(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket_obj.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_obj.bind(('', self.socket_port))
        self.socket_obj.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_ADD_MEMBERSHIP,
            socket.inet_aton(self.socket_ip) + socket.inet_aton(self.current_ip)
        )

    def start(self):
        payload_size = self.socket_buffer_size - struct.calcsize('!2i')
        while True:
            try:
                socket_data, socket_addr = self.socket_obj.recvfrom(self.socket_buffer_size)
                unpacked_flag, unpacked_length, unpacked_data = struct.unpack(f'!2i{payload_size}s', socket_data)
                unpacked_data = unpacked_data[:unpacked_length]
                if unpacked_flag == ClassBroadcastFlag.PublicMessage:
                    unpacked_data = base64.b64decode(unpacked_data).decode('utf-8')
                    self.parent.message_recieved.emit('public', str(unpacked_data))
                elif unpacked_flag == ClassBroadcastFlag.PrivateMessage:
                    integer_length = struct.calcsize('!i')
                    targets_length = struct.unpack('!i', unpacked_data[:integer_length])[0]
                    targets = unpacked_data[integer_length:integer_length + targets_length].split(b'\x00')
                    targets = [socket.inet_ntoa(item) for item in targets]
                    if self.current_ip in targets:
                        message = unpacked_data[integer_length + targets_length:]
                        message = base64.b64decode(message).decode('utf-8')
                        self.parent.message_recieved.emit('private', str(message))
                elif unpacked_flag == ClassBroadcastFlag.StartScreenBroadcast:
                    self.parent.toggle_screen_broadcats.emit(True)
                elif unpacked_flag == ClassBroadcastFlag.StopScreenBroadcast:
                    self.parent.toggle_screen_broadcats.emit(False)
                elif unpacked_flag == ClassBroadcastFlag.ConsoleQuit:
                    self.parent.reset_all.emit()
                    return None

            except KeyboardInterrupt:
                self.socket_obj.close()
                return None
            except Exception as e:
                print(e)
