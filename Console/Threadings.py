from PyQt5.QtCore import QThread, pyqtSignal
import os
from NetworkDiscover import NetworkDiscover
from PrivateMessage import PrivateMessage
from ScreenBroadcast import ScreenBroadcast
from Packages import PrivateMessageFlag


class NetworkDiscoverThread(QThread):
    def __init__(self, network_config):
        super(NetworkDiscoverThread, self).__init__()
        self.current_ip = network_config.get('Local').get('IP')
        self.socket_ip = network_config.get('NetworkDiscover').get('IP')
        self.socket_port = network_config.get('NetworkDiscover').get('Port')
        self.discover_interval = network_config.get('NetworkDiscover').get('Interval', 5)
        self.socket = NetworkDiscover(self.current_ip, self.socket_ip, self.socket_port, self.discover_interval)

    def run(self):
        self.socket.start()


class PrivateMessageThread(QThread):
    client_login_logout = pyqtSignal(str, str, str)
    client_desktop_recieved = pyqtSignal(str, object)
    client_notify_recieved = pyqtSignal(str)
    client_file_recieved = pyqtSignal(str)

    def __init__(self, network_config, client_config, parent=None):
        super(PrivateMessageThread, self).__init__()
        self.socket_ip = network_config.get('Local').get('IP')
        self.socket_port = network_config.get('PrivateMessage').get('Port')
        self.socket_buffer_size = network_config.get('PrivateMessage').get('Buffer')
        self.file_upload_path = client_config.get('FileUploadPath')
        self.root_parent = parent
        self.socket = PrivateMessage(self, self.root_parent, self.socket_ip, self.socket_port, self.socket_buffer_size)

    def get_client_label_by_ip(self, ip):
        label = self.client_config.get('ClientLabel').get(self.mac_binding.get(ip))
        if not label:
            return ip
        return label

    def run(self):
        self.socket.start()


class ScreenBroadcastThread(QThread):
    def __init__(self, network_config):
        super(ScreenBroadcastThread, self).__init__()
        self.current_ip = network_config.get('Local').get('IP')
        self.socket_ip = network_config.get('ScreenBroadcast').get('IP')
        self.socket_port = network_config.get('ScreenBroadcast').get('Port')
        self.ffmpeg_path = network_config.get('ScreenBroadcast').get('FFMpegPath')
        self.ffmpeg_quality = network_config.get('ScreenBroadcast').get('FFMpegQuality', 6)
        self.socket = ScreenBroadcast(self, self.current_ip, self.socket_ip, self.socket_port, self.ffmpeg_path,
                                      self.ffmpeg_quality)

    def safe_stop(self):
        self.socket.working = False
        self.wait()

    def run(self):
        self.socket.working = True
        self.socket.start()
