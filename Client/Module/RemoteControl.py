from PyQt5.QtCore import QObject
import socket
import struct
from threading import Thread
from mss import mss
from PIL import Image
import zlib
from io import BytesIO
import time
import numpy as np
import logging
from pynput import mouse, keyboard
from Module.Packages import RemoteControlFlag
from Module.QtKeyMap import Code2Pynput


class RemoteControl(QObject):
    socket_ip = None
    socket_port = None
    socket_obj = None
    working = False

    def __init__(self, socket_port):
        super(RemoteControl, self).__init__()
        self.socket_port = socket_port
        self.init_socket_obj()

    def init_socket_obj(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def set_socket_ip(self, socket_ip):
        self.socket_ip = socket_ip

    def screen_send_thread(self):
        old_frame = None
        while self.working:
            try:
                with mss() as sct:
                    frame = np.array(sct.grab(sct.monitors[1]))
                    if old_frame is None:
                        new_frame = frame
                    else:
                        new_frame = np.bitwise_xor(old_frame, frame)
                    if (new_frame != 0).any():
                        frame_bytes_raw = new_frame.tobytes()
                        frame_bytes_compressed = zlib.compress(frame_bytes_raw)
                        frame_shape = frame.shape
                        header = struct.pack('!5i', RemoteControlFlag.PackInfo, len(frame_bytes_compressed),
                                             *frame_shape)
                        self.socket_obj.send(header)
                        self.socket_obj.sendall(frame_bytes_compressed)
                    old_frame = frame
                    time.sleep(0.005)
            except Exception as e:
                print(str(e))
        self.socket_obj.close()

    def start(self):
        self.socket_obj.connect((self.socket_ip, self.socket_port))
        screen_send_thread = Thread(target=self.screen_send_thread, daemon=True)
        screen_send_thread.start()
        recv_header_size = struct.calcsize('!5i')  # Flag, Operation, Key, X, Y; for client
        mouse_controller = mouse.Controller()
        mouse_mapping = {0: mouse.Button.left, 1: mouse.Button.right, 2: mouse.Button.middle}
        keyboard_controller = keyboard.Controller()
        while self.working:
            try:
                socket_data = self.socket_obj.recv(recv_header_size)
                if not socket_data:
                    self.working = False
                    screen_send_thread.join()
                    break
                flag, operation, key, x, y = struct.unpack('!5i', socket_data)
                if flag == RemoteControlFlag.ControlCommmand:
                    if operation == 0:
                        mouse_controller.position = (x, y)
                    elif operation == 1:
                        button = mouse_mapping[key]
                        if x == 0:
                            mouse_controller.press(button)
                        elif x == 1:
                            mouse_controller.release(button)
                    elif operation == 2:
                        keyboard_key = Code2Pynput[key]
                        if x == 0:
                            keyboard_controller.press(keyboard_key)
                        elif x == 1:
                            keyboard_controller.release(keyboard_key)
                    elif operation == 3:
                        mouse_controller.scroll(x, y)
                elif flag == RemoteControlFlag.RemoteControlStop:
                    self.working = False
                    screen_send_thread.join()
            except ConnectionResetError:
                self.working = False
                screen_send_thread.join()
                self.socket_obj.close()
            except Exception as e:
                logging.warning(f'Error: {e}')
