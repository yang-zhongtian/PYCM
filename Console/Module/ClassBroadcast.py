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

    def __init__(self, config):
        super(ClassBroadcast, self).__init__()
        self.current_ip = config.get_item('Network/Local/IP')
        self.socket_ip = config.get_item('Network/ClassBroadcast/IP')
        self.socket_port = config.get_item('Network/ClassBroadcast/Port')
        self.socket_buffer_size = config.get_item('Network/ClassBroadcast/Buffer')
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

    def batch_send(self, flag, clients, payload):
        targets = b'\x00'.join([socket.inet_aton(ip) for ip in clients])
        full_data = struct.pack(f'!i{len(targets)}s{len(payload)}s', len(targets), targets, payload)
        self.send_data(flag, full_data)

    def send_text(self, clients, text):
        text = base64.b64encode(str(text).encode('utf-8'))
        self.batch_send(ClassBroadcastFlag.Message, clients, text)

    def send_command(self, clients, command):
        command = base64.b64encode(str(command).encode('utf-8'))
        self.batch_send(ClassBroadcastFlag.Command, clients, command)

    def remote_spy_start_notify(self, client):
        self.batch_send(ClassBroadcastFlag.RemoteSpyStart, [client], b'1')

    def console_quit_notify(self):
        self.send_data(ClassBroadcastFlag.ConsoleQuit, b'')

    def screen_broadcast_nodity(self, working):
        if working:
            self.send_data(ClassBroadcastFlag.StartScreenBroadcast, b'')
        else:
            self.send_data(ClassBroadcastFlag.StopScreenBroadcast, b'')
