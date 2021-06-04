# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QApplication
from Theme import Theme
import sys
import os

from Module.LoadConfig import NetworkConfig

from UI.Main import MainForm

from Module.Threadings import NetworkDiscoverThread, ClassBroadcastThread, ScreenBroadcastThread
from Module.PrivateMessage import PrivateMessage

base_dir = os.path.dirname(os.path.abspath(__file__))
config = NetworkConfig(base_dir)
app = QApplication(sys.argv)
app.setStyleSheet(Theme.load_stylesheet())
app.setFont(Theme.load_font())


class MainWindow(MainForm):
    base_dir = base_dir
    config = config

    def __init__(self):
        super(MainWindow, self).__init__(self)
        self.net_discover_thread = None
        self.class_broadcast_thread = None
        self.screen_broadcast_thread = None
        self.private_message_object = None
        network_device = self.load_network_device()
        if not network_device:
            print('Local network device not found')
            sys.exit(0)
        self.config.set('Local', network_device)
        self.init_threadings()

    def init_threadings(self):
        self.net_discover_thread = NetworkDiscoverThread(self.config)
        self.class_broadcast_thread = ClassBroadcastThread(self.config)
        self.screen_broadcast_thread = ScreenBroadcastThread(self.config)
        self.private_message_object = PrivateMessage
        self.init_connections()
        self.net_discover_thread.start()

    def reset_all_threadings(self):
        self.screen_spy_timer.stop()
        self.class_broadcast_thread.quit()
        self.class_broadcast_thread.wait()
        self.net_discover_thread = NetworkDiscoverThread(self.config)
        self.class_broadcast_thread = ClassBroadcastThread(self.config)
        self.private_message_object = PrivateMessage
        self.init_connections()
        self.ui.title_label.setText('PYCM Client - Offline')
        self.ui.notify_button.setEnabled(False)
        self.ui.send_file_button.setEnabled(False)
        self.ui.private_message_button.setEnabled(False)
        self.server_ip = None
        self.net_discover_thread.start()


main_window = MainWindow()

if __name__ == '__main__':
    main_window.show()
    sys.exit(app.exec_())
