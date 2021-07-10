from PyQt5.QtCore import QObject
import socket
import struct
from threading import Thread
from mss import mss
from PIL import Image
import zlib
from io import BytesIO
import time
import logging
from Module.Packages import RemoteSpyFlag


class RemoteSpy(QObject):
    socket_ip = None
    socket_port = None
    socket_obj = None
    working = False
    screen_send_thread = None

    def __init__(self, socket_port):
        super(RemoteSpy, self).__init__()
        self.socket_port = socket_port
        self.init_socket_obj()

    def init_socket_obj(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def set_socket_ip(self, socket_ip):
        self.socket_ip = socket_ip

    def screen_send(self):
        while self.working:
            try:
                with mss() as sct:
                    frame = sct.grab(sct.monitors[1])
                    img = Image.frombytes('RGB', frame.size, frame.bgra, 'raw', 'BGRX')
                    img_encoded = BytesIO()
                    img.save(img_encoded, 'JPEG')
                    img_encoded = zlib.compress(img_encoded.getvalue())
                    header = struct.pack('!2i', RemoteSpyFlag.PackInfo, len(img_encoded))
                    self.socket_obj.send(header)
                    self.socket_obj.sendall(img_encoded)
            except ConnectionResetError:
                break
            except Exception as e:
                logging.warning(f'Screen send thread unexpected error: {e}')

    def stop(self):
        self.working = False
        self.screen_send_thread.join()
        if self.socket_obj is not None:
            self.socket_obj.close()
            self.socket_obj = None

    def start(self):
        self.socket_obj.connect((self.socket_ip, self.socket_port))
        self.screen_send_thread = Thread(target=self.screen_send, daemon=True)
        self.screen_send_thread.start()
        recv_header_size = struct.calcsize('!i')
        while self.working:
            try:
                socket_data = self.socket_obj.recv(recv_header_size)
                if not socket_data:
                    self.stop()
                    break
                flag = struct.unpack('!i', socket_data)
                if flag == RemoteSpyFlag.RemoteSpyStop:
                    self.socket_obj.send(struct.pack('2!', RemoteSpyFlag.RemoteSpyStop, b''))
                    self.stop()
                    break
            except ConnectionResetError:
                self.stop()
            except Exception as e:
                logging.warning(f'Error: {e}')
