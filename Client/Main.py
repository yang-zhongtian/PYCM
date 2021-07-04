# -*- coding: utf-8 -*-
from PyQtPatch import *
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt
from Theme import Theme
import sys
import os
import logging

from Module.LoadConfig import Config

from UI.Main import MainForm

from Module.Threadings import NetworkDiscoverThread, ClassBroadcastThread, ScreenBroadcastThread, RemoteControlThread
from Module.PrivateMessage import PrivateMessage

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_DisableWindowContextHelpButton)
app = QApplication(sys.argv)
app.setStyleSheet(Theme.load_stylesheet())
app.setQuitOnLastWindowClosed(False)

config = Config()

logging.basicConfig(level=logging.CRITICAL,
                    format='%(asctime)s %(name)s [%(levelname)s] %(module)s.%(funcName)s | %(message)s',
                    datefmt='%Y-%m-%d  %H:%M:%S %a'
                    )


class MainWindow(MainForm):
    config = config
    net_discover_thread = None
    class_broadcast_thread = None
    screen_broadcast_thread = None
    remote_control_thread = None
    private_message_object = None

    def __init__(self):
        super(MainWindow, self).__init__(self)
        network_device = self.load_network_device()
        if not network_device:
            logging.critical('Local network device not found')
            sys.exit(0)
        self.init_network_device(network_device)
        self.init_threadings()

    def init_threadings(self):
        self.net_discover_thread = NetworkDiscoverThread(self.config)
        self.class_broadcast_thread = ClassBroadcastThread(self.config)
        self.screen_broadcast_thread = ScreenBroadcastThread(self.config)
        self.remote_control_thread = RemoteControlThread(self.config)
        self.private_message_object = PrivateMessage(self.config)
        self.init_connections()
        self.net_discover_thread.start()

    def reset_all_threadings(self):
        self.screen_spy_timer.stop()
        self.class_broadcast_thread.quit()
        self.remote_control_thread.quit()
        self.class_broadcast_thread.wait()
        self.remote_control_thread.wait()
        self.net_discover_thread = NetworkDiscoverThread(self.config)
        self.class_broadcast_thread = ClassBroadcastThread(self.config)
        self.remote_control_thread = RemoteControlThread(self.config)
        self.private_message_object = PrivateMessage(self.config)
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
