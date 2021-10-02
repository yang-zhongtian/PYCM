from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from Module.NetworkDiscover import NetworkDiscover
from Module.PrivateMessage import PrivateMessage
from Module.ScreenBroadcast import ScreenBroadcast
from Module.RemoteSpy import RemoteSpy


class NetworkDiscoverThread(QThread):
    def __init__(self, config):
        super(NetworkDiscoverThread, self).__init__()
        self.current_ip = config.get_item('Network/Local/IP')
        self.socket_ip = config.get_item('Network/NetworkDiscover/IP')
        self.socket_port = config.get_item('Network/NetworkDiscover/Port')
        self.discover_interval = config.get_item('Network/NetworkDiscover/Interval', 5)
        self.socket = NetworkDiscover(self.current_ip, self.socket_ip, self.socket_port, self.discover_interval)

    def run(self):
        self.socket.start()


class PrivateMessageThread(QThread):
    client_login_logout = pyqtSignal(str, str, str)
    client_desktop_recieved = pyqtSignal(str, object)
    client_notify_recieved = pyqtSignal(str)
    client_file_recieved = pyqtSignal(str)

    def __init__(self, config: object, parent: object = None):
        super(PrivateMessageThread, self).__init__()
        self.socket_ip = config.get_item('Network/Local/IP')
        self.socket_port = config.get_item('Network/PrivateMessage/Port')
        self.socket_buffer_size = config.get_item('Network/PrivateMessage/Buffer')
        self.file_upload_path = config.get_item('Client/FileUploadPath')
        self.config = config
        self.socket = PrivateMessage(self, parent, self.socket_ip, self.socket_port, self.socket_buffer_size)

    def run(self):
        self.socket.start()


class ScreenBroadcastThread(QThread):
    def __init__(self, config):
        super(ScreenBroadcastThread, self).__init__()
        self.current_ip = config.get_item('Network/Local/IP')
        self.socket_ip = config.get_item('Network/ScreenBroadcast/IP')
        self.socket_port = config.get_item('Network/ScreenBroadcast/Port')
        self.ffmpeg_quality = config.get_item('Network/ScreenBroadcast/FFMpegQuality', 6)
        self.socket = ScreenBroadcast(self, self.current_ip, self.socket_ip, self.socket_port, self.ffmpeg_quality)

    def safe_stop(self):
        self.socket.working = False
        self.wait()

    def run(self):
        self.socket.working = True
        self.socket.start()


class RemoteSpyThread(QThread):
    frame_recieved = pyqtSignal(QPixmap)

    def __init__(self, config: object):
        super(RemoteSpyThread, self).__init__()
        self.socket_port = config.get_item('Network/RemoteSpy/Port')
        self.socket = RemoteSpy(self, self.socket_port)

    def safe_stop(self):
        self.socket.stop()

    def run(self):
        self.socket.start()
