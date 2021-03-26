from PyQt5.QtCore import QObject
from threading import Thread, Lock
from queue import Queue
import socket
import time
import struct
import numpy as np
import cv2
from PIL import Image
from copy import deepcopy
import traceback


class PiecePack(object):
    def __init__(self, stamp, index, position, data):
        self.stamp = stamp
        self.index = index
        self.position = position
        self.data = data

    def __lt__(self, other):
        return (self.stamp < other.stamp) and (self.index < other.index)

    def __str__(self):
        return f'<PiecePack stamp={self.stamp} index={self.index}>'


class ScreenBroadcast(QObject):
    def __init__(self, parent, current_ip, socket_ip, socket_port, socket_buffer_size, reciever_sleep=0,
                 max_queue_size=50, piece_buffer_size=3, pieces_amount=6):
        super(ScreenBroadcast, self).__init__()
        self.parent = parent
        self.current_ip = current_ip
        self.socket_ip = socket_ip
        self.socket_port = socket_port
        self.socket_buffer_size = socket_buffer_size
        self.position_size = struct.calcsize('!Q5i')  # 时间戳 idx 两个坐标
        self.payload_size = socket_buffer_size - struct.calcsize('!Q6i')
        self.reciever_sleep = reciever_sleep
        self.max_queue_size = max_queue_size
        self.screen_width = None
        self.screen_height = None
        self.pieces_queue = Queue(maxsize=max_queue_size)
        self.piece_buffer_size = piece_buffer_size * 10
        self.pieces_amount = pieces_amount
        self.frames_queue = Queue()
        self.frames_list = None
        self.pieces_used = [np.zeros(self.pieces_amount, dtype=bool) for _ in range(self.piece_buffer_size)]
        self.pieces_time = np.zeros(self.piece_buffer_size, dtype=np.uint64)
        self.fps = 0
        self.fps_lock = Lock()
        self.working = True

    def __init_socket_object(self):
        socket_object = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        socket_object.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_object.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        socket_object.bind(('', self.socket_port))
        socket_object.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_ADD_MEMBERSHIP,
            socket.inet_aton(self.socket_ip) + socket.inet_aton(self.current_ip)
        )
        return socket_object

    def set_screen_size(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.frames_list = [np.zeros(self.screen_width * self.screen_height * 3, dtype=np.uint8).reshape(
            (self.screen_height, self.screen_width, 3)) for _ in range(self.piece_buffer_size)]

    def __recieve_thread(self):
        socket_object = self.__init_socket_object()
        while self.working:
            if not self.pieces_queue.full():
                try:
                    socket_data, socket_addr = socket_object.recvfrom(self.socket_buffer_size)
                    stamp, index, x1, y1, x2, y2 = struct.unpack('!Q5i', socket_data[:self.position_size])
                    piece_len, piece_bytes = struct.unpack(f'!i{self.payload_size}s', socket_data[self.position_size:])
                    piece_bytes = piece_bytes[:piece_len]
                    piece_data = np.frombuffer(piece_bytes, dtype=np.uint8)
                    piece_data = cv2.imdecode(piece_data, cv2.IMREAD_COLOR)
                    self.pieces_queue.put(PiecePack(stamp, index, (x1, y1, x2, y2), piece_data))
                except Exception as e:
                    print(repr(e))
                    print(traceback.format_exc())
            else:
                time.sleep(self.reciever_sleep)

    def __rebuild_thread(self):
        while self.working:
            if self.pieces_queue.qsize() > self.max_queue_size:
                self.pieces_queue = Queue()
                if self.pieces_queue.mutex:
                    self.pieces_queue.queue.clear()
            try:
                piece = self.pieces_queue.get()
                time_stamp = piece.stamp
                index = piece.index
                x1, y1, x2, y2 = piece.position
                data = piece.data
                piece_list_index = time_stamp % self.piece_buffer_size
                piece_time_stamp = self.pieces_time[piece_list_index]
                piece_used = self.pieces_used[piece_list_index]
                frame = self.frames_list[piece_list_index]
                if piece_time_stamp > time_stamp:
                    continue
                elif piece_time_stamp < time_stamp:
                    piece_used.fill(0)
                    self.pieces_time[piece_list_index] = time_stamp
                if piece_used[index]:
                    continue
                frame[x1:x2, y1:y2] = data
                piece_used[index] = True
                if np.all(piece_used):
                    new_frame = deepcopy(frame)
                    self.frames_queue.put(new_frame)
                    frame.fill(0)
                    with self.fps_lock:
                        self.fps += 1

            except Exception as e:
                print(repr(e))
                print(traceback.format_exc())

    def __fps_statistics(self):
        while self.working:
            with self.fps_lock:
                fps = self.fps
                self.fps = 0
            self.parent.fps_update.emit(fps)
            time.sleep(1)

    def start(self):
        for _ in range(4):
            Thread(target=self.__recieve_thread, daemon=True).start()
        Thread(target=self.__rebuild_thread, daemon=True).start()
        Thread(target=self.__fps_statistics, daemon=True).start()
        while self.working:
            frame = self.frames_queue.get()
            qpixmap = Image.fromarray(frame).toqpixmap()
            self.parent.frame_recieved.emit(qpixmap)
