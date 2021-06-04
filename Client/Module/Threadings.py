from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from Module.ClassBroadcast import ClassBroadcast
from Module.NetworkDiscover import NetworkDiscover
from Module.ScreenBroadcast import ScreenBroadcast


class ClassBroadcastThread(QThread):
    message_recieved = pyqtSignal(str, str)
    reset_all = pyqtSignal()
    toggle_screen_broadcats = pyqtSignal(bool)

    def __init__(self, config):
        super(ClassBroadcastThread, self).__init__()
        self.current_ip = config.get('Local').get('IP')
        self.socket_ip = config.get('ClassBroadcast').get('IP')
        self.socket_port = config.get('ClassBroadcast').get('Port')
        self.socket_buffer_size = config.get('ClassBroadcast').get('Buffer')
        self.socket = ClassBroadcast(self, self.current_ip, self.socket_ip, self.socket_port, self.socket_buffer_size)

    def run(self):
        self.socket.start()


class NetworkDiscoverThread(QThread):
    server_info = pyqtSignal(str, object)

    def __init__(self, config):
        super(NetworkDiscoverThread, self).__init__()
        self.current_ip = config.get('Local').get('IP')
        self.socket_ip = config.get('NetworkDiscover').get('IP')
        self.socket_port = config.get('NetworkDiscover').get('Port')
        self.config = config
        self.socket = NetworkDiscover(self.current_ip, self.socket_ip, self.socket_port)

    def run(self):
        server_ip = self.socket.wait_for_console()
        self.server_info.emit(server_ip, self.config)


class ScreenBroadcastThread(QThread):
    frame_recieved = pyqtSignal(QPixmap)
    fps_update = pyqtSignal(int)

    def __init__(self, config):
        super(ScreenBroadcastThread, self).__init__()
        self.current_ip = config.get('Local').get('IP')
        self.socket_ip = config.get('ScreenBroadcast').get('IP')
        self.socket_port = config.get('ScreenBroadcast').get('Port')
        self.socket = ScreenBroadcast(self, self.current_ip, self.socket_ip, self.socket_port)

    def run(self):
        self.socket.start()
