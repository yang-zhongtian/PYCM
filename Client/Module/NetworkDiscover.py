import socket
import struct
from Module.Packages import NetworkDiscoverFlag


class NetworkDiscover(object):
    current_ip = None
    socket_ip = None
    socket_port = None
    socket_client = None

    def __init__(self, current_ip, socket_ip, socket_port):
        self.current_ip = current_ip
        self.socket_ip = socket_ip
        self.socket_port = socket_port
        self.__init_socket_client()

    def __init_socket_client(self):
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_client.bind(('', self.socket_port))
        self.socket_client.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_ADD_MEMBERSHIP,
            socket.inet_aton(self.socket_ip) + socket.inet_aton(self.current_ip)
        )

    def wait_for_console(self):
        try:
            while True:
                try:
                    socket_data, socket_addr = self.socket_client.recvfrom(1024)
                    if struct.unpack('!i', socket_data)[0] == NetworkDiscoverFlag.ConsoleFlag:
                        return socket_addr[0]
                except Exception as e:
                    pass
        except KeyboardInterrupt:
            self.socket_server.close()
            return None


if __name__ == '__main__':
    A = NetworkDiscover('192.168.1.6', '224.50.50.50', 4088)
    print(A.wait_for_console())
