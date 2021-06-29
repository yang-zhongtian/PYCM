# -*- coding: utf-8 -*-
from PyQtPatch import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from Theme import Theme
import sys
import os
import logging

from Module.LoadConfig import Config

from UI.Login import LoginForm
from UI.Dashboard import DashboardForm
from UI.NetworkDeviceSelect import NetworkDeviceSelectForm

from Module.Threadings import NetworkDiscoverThread, PrivateMessageThread, ScreenBroadcastThread
from Module.ClassBroadcast import ClassBroadcast

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_DisableWindowContextHelpButton)
app = QApplication(sys.argv)
app.setStyleSheet(Theme.load_stylesheet())

config = Config()

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s [%(levelname)s] %(module)s.%(funcName)s | %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %a'
                    )


class DashboardWindow(DashboardForm):
    config = config
    net_discover_thread = None
    class_broadcast_object = None
    private_message_thread = None
    screen_broadcast_thread = None
    send_message_group_dialog = None
    network_devices_select_dialog = None

    def __init__(self):
        super(DashboardWindow, self).__init__()
        login_result = LoginForm(self).exec_()
        if not login_result:
            sys.exit(0)
        network_devices_select_dialog = NetworkDeviceSelectForm(self)
        network_devices_select_dialog.exec_()
        network_device = network_devices_select_dialog.get_selected_device()
        self.init_network_device(network_device)
        self.init_threads()
        self.show()
        self.start_all_threadings()

    def init_threads(self):
        self.net_discover_thread = NetworkDiscoverThread(self.config)
        self.class_broadcast_object = ClassBroadcast(self.config)
        self.private_message_thread = PrivateMessageThread(self.config, self)
        self.screen_broadcast_thread = ScreenBroadcastThread(self.config)
        self.init_connections()


dashboard_window = DashboardWindow()

if __name__ == '__main__':
    sys.exit(app.exec_())
