from PyQt5.QtCore import QObject
import socket
import struct
import base64
from Module.Packages import ClassBroadcastFlag


class ClassBroadcast(QObject):
    current_ip = None
    socket_ip = None
    socket_port = None
    socket_buffer_size = None
    socket_obj = None

    def __init__(self, current_ip, socket_ip, socket_port, socket_buffer_size):
        super(ClassBroadcast, self).__init__()
        self.current_ip = current_ip
        self.socket_ip = socket_ip
        self.socket_port = socket_port
        self.socket_buffer_size = socket_buffer_size
        self.__init_socket_obj()

    def __init_socket_obj(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket_obj.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        self.socket_obj.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_ADD_MEMBERSHIP,
            socket.inet_aton(self.socket_ip) + socket.inet_aton(self.current_ip)
        )

    def send_data(self, flag, data):
        payload_size = self.socket_buffer_size - struct.calcsize('!2i')
        socket_data = struct.pack(f'!2i{payload_size}s', flag, len(data), data)
        self.socket_obj.sendto(socket_data, (self.socket_ip, self.socket_port))

    def send_public_text(self, text):
        text = base64.b64encode(str(text).encode('utf-8'))
        self.send_data(ClassBroadcastFlag.PublicMessage, text)

    def send_private_text(self, address, text):
        targets = b'\x00'.join([socket.inet_aton(ip) for ip in address])
        text = base64.b64encode(str(text).encode('utf-8'))
        payload_data = struct.pack(f'!i{len(targets)}s{len(text)}s', len(targets), targets, text)
        self.send_data(ClassBroadcastFlag.PrivateMessage, payload_data)

    def send_public_command(self, command):
        command = base64.b64encode(str(command).encode('utf-8'))
        self.send_data(ClassBroadcastFlag.PublicCommand, command)

    def send_private_command(self, address, command):
        targets = b'\x00'.join([socket.inet_aton(ip) for ip in address])
        command = base64.b64encode(str(command).encode('utf-8'))
        payload_data = struct.pack(f'!i{len(targets)}s{len(command)}s', len(targets), targets, command)
        self.send_data(ClassBroadcastFlag.PrivateCommand, payload_data)

    def console_quit_notify(self):
        self.send_data(ClassBroadcastFlag.ConsoleQuit, b'')

    def screen_broadcast_nodity(self, working):
        if working:
            self.send_data(ClassBroadcastFlag.StartScreenBroadcast, b'')
        else:
            self.send_data(ClassBroadcastFlag.StopScreenBroadcast, b'')
