from PyQt5.QtCore import QObject
from PyQt5.QtGui import QImage, QPixmap
from threading import Thread, Lock
from queue import Queue
import cv2
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
        self.fps = 0
        self.fps_lock = Lock()
        self.working = True

    def __recieve_thread(self):
        try:
            self.video_capture = cv2.VideoCapture(f'udp://{self.socket_ip}@{self.current_ip}:{self.socket_port}',
                                                  cv2.CAP_FFMPEG)
            while self.working:
                status, frame = self.video_capture.read()
                if status:
                    self.frames_queue.put(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    with self.fps_lock:
                        self.fps += 1
        except Exception as e:
            print(e)

    def __fps_statistics(self):
        while self.working:
            with self.fps_lock:
                fps = self.fps
                self.fps = 0
            self.parent.fps_update.emit(fps)
            time.sleep(1)

    def start(self):
        Thread(target=self.__recieve_thread, daemon=True).start()
        Thread(target=self.__fps_statistics, daemon=True).start()
        while self.working:
            frame_raw = self.frames_queue.get()
            frame_qimage = QImage(frame_raw.data, frame_raw.shape[1], frame_raw.shape[0], QImage.Format_RGB888)
            self.parent.frame_recieved.emit(QPixmap.fromImage(frame_qimage))
