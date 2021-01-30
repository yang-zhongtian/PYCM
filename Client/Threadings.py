from PyQt5.QtCore import QThread, pyqtSignal
from NetworkDiscover import NetworkDiscover


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
