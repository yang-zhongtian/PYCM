import socket
import time
import struct
import numpy as np
import matplotlib.pyplot as plt
import zlib
from mss import mss
from Public.ScreenScanning import ScreenDiff


class ScreenBroadcast(object):
    socket_ip = None
    socket_port = None
    socket_server = None
    cast_interval = None

    def __init__(self, socket_ip, socket_port, cast_interval=5):
        self.socket_ip = socket_ip
        self.socket_port = socket_port
        self.cast_interval = cast_interval
        self.__init_socket_server()

    def __init_socket_server(self):
        self.socket_server = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket_server.setsockopt(
            socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        self.socket_server.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_ADD_MEMBERSHIP,
            socket.inet_aton(self.socket_ip) + socket.inet_aton('0.0.0.0')
        )

    def start(self):
        # try:
        #     socket_packet = struct.pack('!i', NetworkDiscoverFlag.ConsoleFlag)
        #     while True:
        #         self.socket_server.sendto(
        #             socket_packet, (self.socket_ip, self.socket_port))
        #         time.sleep(self.discover_interval)
        # except KeyboardInterrupt:
        #     self.socket_server.close()
        #     return
        with mss() as sct:
            sct_img = np.array(sct.grab(sct.monitors[1]))
            sct_img = np.flip(sct_img[:, :, :3], 2)
            sct_compressed = zlib.compress(sct_img.tobytes())
            print(len(sct_compressed))


if __name__ == '__main__':
    A = ScreenBroadcast('225.2.2.21', 4092, 1)
    A.start()
