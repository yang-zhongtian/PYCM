from PyQt5.QtCore import QThread, pyqtSignal
from NetworkDiscover import NetworkDiscover
from PrivateMessage import PrivateMessage
from Packages import PrivateMessageFlag


class NetworkDiscoverThread(QThread):
    def __init__(self, config):
        super(NetworkDiscoverThread, self).__init__()
        self.socket_ip = config.get('NetworkDiscover').get('IP')
        self.socket_port = config.get('NetworkDiscover').get('Port')
        self.socket = NetworkDiscover(self.socket_ip, self.socket_port,
                                      config.get('NetworkDiscover').get('Interval', 5))

    def run(self):
        self.socket.start()


class PrivateMessageThread(QThread):
    client_login_logout = pyqtSignal(str, str)
    client_desktop_recieved = pyqtSignal(str, object)

    def __init__(self, config):
        super(PrivateMessageThread, self).__init__()
        self.socket_ip = config.get('Local').get('IP')
        self.socket_port = config.get('PrivateMessage').get('Port')
        self.socket_buffer_size = config.get('PrivateMessage').get('Buffer')
        self.socket = PrivateMessage(self, self.socket_ip, self.socket_port, self.socket_buffer_size)

    def run(self):
        self.socket.start()
