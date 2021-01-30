from PyQt5.QtWidgets import QWidget, QApplication
import sys
import os

from LoadConfig import NetworkConfig

from UI.Login import LoginForm
from UI.Dashboard import DashboardForm

from Threadings import NetworkDiscoverThread, PrivateMessageThread

base_dir = os.path.dirname(os.path.abspath(__file__))
config = NetworkConfig(base_dir)
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
    config = config

    def __init__(self):
        super(DashboardWindow, self).__init__()
        self.net_discover_thread = NetworkDiscoverThread(config)
        self.private_message_thread = PrivateMessageThread(config)
        self.init_connections()


login_window = LoginWindow()
dashboard_window = DashboardWindow()

if __name__ == '__main__':
    login_window.show()
    sys.exit(app.exec_())
