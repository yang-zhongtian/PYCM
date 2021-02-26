from PyQt5.QtCore import QObject
from threading import Thread
from queue import Queue
import socket
import time
import struct
import numpy as np
import cv2
from mss import mss
from ScreenPacker import ScreenPacker


class ScreenBroadcast(QObject):
    def __init__(self, parent, current_ip, socket_ip, socket_port, packer_sleep=0.02, frame_sleep=0.2,
                 socket_buffer_size=40960):
        super(ScreenBroadcast, self).__init__()
        self.parent = parent
        self.current_ip = current_ip
        self.socket_ip = socket_ip
        self.socket_port = socket_port
        self.socket_buffer_size = socket_buffer_size
        self.packer_sleep = packer_sleep
        self.frame_sleep = frame_sleep
        self.packer = None
        self.screen_width = None
        self.screen_height = None
        self.pieces = Queue(maxsize=128)
        self.row_per_piece = None
        self.col_per_piece = None
        self.pieces_arrangement = (2, 3)
        self.pieces_range = []
        self.working = True
        self.__init_socket_object()
        self.__init_packer()

    def __init_socket_object(self):
        self.socket_object = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket_object.setsockopt(
            socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        self.socket_object.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_ADD_MEMBERSHIP,
            socket.inet_aton(self.socket_ip) + socket.inet_aton(self.current_ip)
        )

    def __init_packer(self):
        with mss() as sct:
            screen_size = sct.grab(sct.monitors[1]).size
        self.packer = ScreenPacker(screen_size.width, screen_size.height, buffer_size=self.socket_buffer_size)
        self.screen_width = screen_size.width
        self.screen_height = screen_size.height
        self.row_per_piece = int(self.screen_height / self.pieces_arrangement[0])
        self.col_per_piece = int(self.screen_width / self.pieces_arrangement[1])
        for row_index in range(self.pieces_arrangement[0]):
            x1 = row_index * self.row_per_piece
            if row_index < self.pieces_arrangement[0] - 1:
                x2 = (row_index + 1) * self.row_per_piece
            else:
                x2 = self.screen_height
            for col_index in range(self.pieces_arrangement[1]):
                y1 = col_index * self.col_per_piece
                if col_index < self.pieces_arrangement[1] - 1:
                    y2 = (col_index + 1) * self.col_per_piece
                else:
                    y2 = self.screen_width
                self.pieces_range.append((x1, y1, x2, y2))

    def update_frame(self):
        monitor = {'top': 0, 'left': 0, 'width': self.screen_width, 'height': self.screen_height}
        with mss() as sct:
            while self.working:
                time.sleep(self.frame_sleep)
                frame_stamp = int(time.time() * 1000)
                frame_array = np.array(sct.grab(monitor))
                frame_array = np.flip(frame_array[:, :, :3], 2)
                for index, piece_range in enumerate(self.pieces_range):
                    self.packer.pack_data(piece_range, frame_stamp, index, frame_array, self.pieces)

    def start(self):
        Thread(target=self.update_frame, daemon=True).start()
        while self.working:
            time.sleep(self.packer_sleep)
            frame_pack = self.pieces.get()
            if self.pieces.qsize() > 118:
                self.pieces = Queue()
                if self.pieces.mutex:
                    self.pieces.queue.clear()
            self.socket_object.sendto(frame_pack, (self.socket_ip, self.socket_port))


if __name__ == '__main__':
    A = ScreenBroadcast(None, '192.168.3.2', '225.2.2.21', 4092)
    # A.start()
