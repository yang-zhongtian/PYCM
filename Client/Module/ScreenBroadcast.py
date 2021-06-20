from PyQt5.QtCore import QObject
from PyQt5.QtGui import QImage, QPixmap
import logging
from threading import Thread, Lock
from queue import Queue
import av
import time


class ScreenBroadcast(QObject):
    video_capture = None

    def __init__(self, parent, current_ip, socket_ip, socket_port):
        super(ScreenBroadcast, self).__init__()
        self.parent = parent
        self.current_ip = current_ip
        self.socket_ip = socket_ip
        self.socket_port = socket_port
        self.frames_queue = Queue()
        self.working = False

    def __recieve_thread(self):
        try:
            video_capture = av.open(
                f'udp://{self.current_ip}@{self.socket_ip}:{self.socket_port}', 'r')
        except Exception as e:
            logging.error(f'Failed to open udp stream: {e}')
            return
        while self.working:
            try:
                for frame in video_capture.decode():
                    self.frames_queue.put(frame.to_ndarray(format='rgb24'))
            except Exception as e:
                logging.warning(f'Failed to decode frame: {e}')

    def start(self):
        Thread(target=self.__recieve_thread, daemon=True).start()
        while self.working:
            frame_raw = self.frames_queue.get()
            frame_qimage = QImage(frame_raw.data, frame_raw.shape[1], frame_raw.shape[0], QImage.Format_RGB888)
            self.parent.frame_recieved.emit(QPixmap.fromImage(frame_qimage))
