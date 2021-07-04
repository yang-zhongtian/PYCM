import socket
import struct
from PIL import Image
from io import BytesIO
from queue import Queue
from threading import Thread
import zlib
import logging
import numpy as np
from Module.Packages import RemoteControlFlag
import traceback


class Command(object):
    """
        包体定义
            operation   |   0->鼠标移动事件   |   1->鼠标点击                |   2->键盘输入事件    |   3->滚动
            key         |   0 [NULL]        |   0->左键 1->右键 2->中键     |  按键映射值         |   0 [NULL]
            x           |   posX            |   0->按下 1->弹起            |  0->按下 1->弹起    |   DeltaX
            y           |   posY            |   0 [NULL]                  |  0 [NULL]         |   DeltaY
    """

    operation = None
    key = None
    x = None
    y = None

    def __init__(self, operation, key, x, y):
        self.operation = operation
        self.key = key
        self.x = x
        self.y = y

    def serialize(self):
        return self.operation, self.key, self.x, self.y


class RemoteControl(object):
    socket_port = None
    socket_obj = None
    socket_conn = None
    command_queue = None
    old_frame = None

    def __init__(self, parent, socket_port):
        self.parent = parent
        self.socket_port = socket_port
        self.command_queue = Queue()
        self.__init_socket_obj()

    def __init_socket_obj(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_obj.bind(('', self.socket_port))
        self.socket_obj.listen(1)

    def recieve_thread(self):
        recv_header_size = struct.calcsize('!5i')
        while True:
            try:
                self.socket_conn, socket_addr = self.socket_obj.accept()
                while True:
                    socket_data = self.socket_conn.recv(recv_header_size)
                    if not socket_data:
                        break
                    unpacked_flag, unpacked_data, shape_0, shape_1, shape2 = struct.unpack('!5i', socket_data)
                    if unpacked_flag == RemoteControlFlag.RemoteControlStop:
                        break
                    elif unpacked_flag == RemoteControlFlag.PackInfo:
                        payload_size = unpacked_data
                        shape = (shape_0, shape_1, shape2)
                        frame = b''
                        while len(frame) < payload_size:
                            payload_part = self.socket_conn.recv(payload_size)
                            frame += payload_part
                        frame = zlib.decompress(frame)
                        frame = np.frombuffer(frame, dtype=np.uint8)
                        frame = frame.reshape(shape)
                        if self.old_frame is not None:
                            frame = np.bitwise_xor(frame, self.old_frame)
                        img = Image.fromarray(frame[..., :3][..., ::-1])
                        self.parent.frame_recieved.emit(img.toqpixmap())
                        self.old_frame = frame
                self.socket_conn.close()
                self.socket_conn = None
            except Exception as e:
                logging.warning(f'Failed to decode socket data: {e}')

    def stop(self):
        if not self.socket_conn:
            return
        socket_data = struct.pack('!5i', RemoteControlFlag.RemoteControlStop, 0, 0, 0, 0)
        self.socket_conn.send(socket_data)

    def start(self):
        Thread(target=self.recieve_thread, daemon=True).start()
        while True:
            try:
                command = self.command_queue.get()
                if self.socket_conn is not None:
                    socket_data = struct.pack('!5i', RemoteControlFlag.ControlCommmand, *command.serialize())
                    self.socket_conn.send(socket_data)
            except Exception as e:
                logging.warning(f'Error: {e}')
