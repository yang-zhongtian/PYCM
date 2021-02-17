from PyQt5.QtCore import QObject
from threading import Thread
from queue import Queue, PriorityQueue
import socket
import time
import struct
import numpy as np
import cv2
from PIL import Image


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


class PeekablePriorityQueue(PriorityQueue):
    def peek(self):
        try:
            with self.mutex:
                return self.queue[0]
        except IndexError:
            return None

    def pop(self):
        self.get()


class ScreenBroadcast(QObject):
    def __init__(self, parent, current_ip, socket_ip, socket_port, socket_buffer_size, reciever_sleep=0.001,
                 max_queue_size=50):
        super(ScreenBroadcast, self).__init__()
        self.parent = parent
        self.current_ip = current_ip
        self.socket_ip = socket_ip
        self.socket_port = socket_port
        self.socket_buffer_size = socket_buffer_size
        self.position_size = struct.calcsize('!Q5i')  # 时间戳 idx 两个坐标
        self.payload_size = socket_buffer_size - struct.calcsize('!Q6i')
        self.reciever_sleep = reciever_sleep
        self.pieces_queue_limit = max_queue_size - 20
        self.screen_width = None
        self.screen_height = None
        self.pieces_queue = PeekablePriorityQueue(maxsize=max_queue_size)
        self.frames_queue = Queue()
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
                    print(e)
            else:
                time.sleep(self.reciever_sleep)

    def __rebuild_thread(self):
        frame = np.zeros(self.screen_width * self.screen_height * 3, dtype=np.uint8).reshape(
            (self.screen_height, self.screen_width, 3))
        pieces_used_flag = np.zeros(6, dtype=bool)
        current_stamp = 0
        stamp_limit = 0
        failure_count = 0
        last_time = None
        fps = 0
        while self.working:
            if self.pieces_queue.qsize() > self.pieces_queue_limit:
                self.pieces_queue = PeekablePriorityQueue()
                if self.pieces_queue.mutex:
                    self.pieces_queue.queue.clear()
            try:
                if failure_count >= 6:
                    self.pieces_queue.pop()
                    stamp_limit = current_stamp
                    current_stamp = 0
                    failure_count = 0
                    pieces_used_flag.fill(0)
                top = self.pieces_queue.peek()
                if top is not None:
                    stamp = top.stamp
                    if ((current_stamp == 0) or (stamp == current_stamp)) and (stamp > stamp_limit):
                        pack = self.pieces_queue.get()
                        x1, y1, x2, y2 = pack.position
                        data = pack.data
                        frame[x1:x2, y1:y2] = data
                        pieces_used_flag[pack.index] = True
                        current_stamp = pack.stamp
                        failure_count = 0
                    elif stamp < current_stamp:
                        self.pieces_queue.pop()
                    else:
                        failure_count += 1
            except Exception as e:
                print(e)
            if pieces_used_flag.all():
                self.frames_queue.put(frame)
                failure_count = 0
                stamp_limit = current_stamp
                current_stamp = 0
                pieces_used_flag.fill(0)
                current_time = time.time()
                if last_time is None:
                    fps += 1
                    last_time = current_time
                elif (current_time - last_time) < 1:
                    fps += 1
                else:
                    self.parent.fps_update.emit(fps)
                    fps = 0
                    last_time = current_time

    def start(self):
        for _ in range(4):
            Thread(target=self.__recieve_thread, daemon=True).start()
        Thread(target=self.__rebuild_thread, daemon=True).start()
        while self.working:
            frame = self.frames_queue.get()
            qpixmap = Image.fromarray(frame).toqpixmap()
            self.parent.frame_recieved.emit(qpixmap)
