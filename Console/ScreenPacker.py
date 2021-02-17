from threading import Thread
import socket
import time
import struct
import cv2
import numpy
from matplotlib import pyplot as plt


class ScreenPacker(object):
    def __init__(self, screen_width, screen_height, buffer_size=40960):
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.buffer_size = buffer_size
        self.piece_header_size = struct.calcsize('!Q6i')  # 时间戳 idx x1 y1 x2 y2 载荷长度
        self.piece_payload_size = buffer_size - self.piece_header_size

    def pack_data(self, position, stamp, index, frame_raw, pieces):
        if len(frame_raw) <= 0:
            return None
        Thread(target=self.compress, args=(position, stamp, index, frame_raw, pieces), daemon=True).start()

    def compress(self, position, stamp, index, frame_raw, pieces):
        if len(frame_raw) <= 0:
            return False
        if pieces.full():
            return False
        try:
            x1, y1, x2, y2 = position
            result, piece_encoded = cv2.imencode('.jpg', frame_raw[x1:x2, y1:y2], self.encode_param)
            if result:
                piece_bytes = piece_encoded.tobytes()
                piece_length = len(piece_bytes)
                packed_data = struct.pack(f'!Q6i{self.piece_payload_size}s', stamp, index, x1, y1, x2, y2,
                                          piece_length, piece_bytes)
                pieces.put(packed_data)
                return True
        except Exception as e:
            print(e)
        return False
