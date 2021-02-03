from PyQt5.QtWidgets import QWidget, QApplication
import sys
import os

from LoadConfig import NetworkConfig, ClientConfig

from UI.Login import LoginForm
from UI.Dashboard import DashboardForm

from Threadings import NetworkDiscoverThread, PrivateMessageThread

base_dir = os.path.dirname(os.path.abspath(__file__))
network_config = NetworkConfig(base_dir)
client_config = ClientConfig(base_dir)
app = QApplication(sys.argv)


class LoginWindow(LoginForm):
    base_dir = base_dir

    def __init__(self):
        super(LoginWindow, self).__init__()

    def show_dashboard_window(self):
        self.hide()
        dashboard_window.show()
        dashboard_window.start_all_threadings()


class DashboardWindow(DashboardForm):
    base_dir = base_dir
    network_config = network_config
    client_config = client_config

    def __init__(self):
        super(DashboardWindow, self).__init__()
        self.net_discover_thread = NetworkDiscoverThread(network_config)
        self.private_message_thread = PrivateMessageThread(network_config, client_config)
        self.init_connections()


login_window = LoginWindow()
dashboard_window = DashboardWindow()

if __name__ == '__main__':
    login_window.show()
    sys.exit(app.exec_())
