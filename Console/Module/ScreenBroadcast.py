from PyQt5.QtCore import QObject, QBuffer, QIODevice, Qt
from PyQt5.QtGui import QImage
from Module.Packages import ScreenBroadcastFlag
import socket
import struct
from mss import mss
import zlib
import logging


class ScreenBroadcast(QObject):
    def __init__(self, parent, current_ip, socket_ip, socket_port, socket_buffer, quality=60):
        super(ScreenBroadcast, self).__init__()
        self.parent = parent
        self.current_ip = current_ip
        self.socket_ip = socket_ip
        self.socket_port = socket_port
        self.socket_buffer = socket_buffer
        self.quality = quality
        self.socket_obj = None
        self.working = False
        self.init_socket_obj()

    def init_socket_obj(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket_obj.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        self.socket_obj.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_ADD_MEMBERSHIP,
            socket.inet_aton(self.socket_ip) + socket.inet_aton(self.current_ip)
        )

    def start(self):
        pack_index = 0
        payload_size = self.socket_buffer - struct.calcsize('!2i')
        target = (self.socket_ip, self.socket_port)
        while self.working:
            try:
                with mss() as sct:
                    frame = sct.grab(sct.monitors[1])
                    img = QImage(frame.rgb, frame.width, frame.height, QImage.Format_RGB888)
                    buffer = QBuffer()
                    buffer.open(QIODevice.ReadWrite)
                    img.save(buffer, 'JPEG', quality=self.quality)
                    img_encoded = zlib.compress(buffer.data())
                    buffer.close()
                    rounds = len(img_encoded) // payload_size
                    looped_size = rounds * payload_size
                    logging.debug(f'Screen broadcast index: {pack_index}, rounds: {rounds}')
                    header = struct.pack('!4i', ScreenBroadcastFlag.PackInfo, pack_index, len(img_encoded), rounds)
                    self.socket_obj.sendto(header, target)
                    for i in range(rounds):
                        pack = img_encoded[i * payload_size: (i + 1) * payload_size]
                        data = struct.pack(f'!2i{payload_size}s', ScreenBroadcastFlag.PackData, len(pack), pack)
                        self.socket_obj.sendto(data, target)
                    if looped_size < len(img_encoded):
                        pack = img_encoded[looped_size:]
                        data = struct.pack(f'!2i{payload_size}s', ScreenBroadcastFlag.PackData, len(pack), pack)
                        self.socket_obj.sendto(data, target)
                    pack_index = (pack_index + 1) % 1000
            except Exception as e:
                logging.warning(f'Screen send thread unexpected error: {e}')
