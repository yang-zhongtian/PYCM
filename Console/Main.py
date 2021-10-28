# -*- coding: utf-8 -*-
from PyQtPatch import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QTranslator
import sys
import os
import logging

from Module.LoadConfig import Config

import Resources_rc
import Theme
from Translation import LoadTranslation

from UI.Login import LoginForm
from UI.Dashboard import DashboardForm
from UI.NetworkDeviceSelect import NetworkDeviceSelectForm

from Module.Threadings import NetworkDiscoverThread, PrivateMessageThread, ScreenBroadcastThread, RemoteSpyThread
from Module.ClassBroadcast import ClassBroadcast

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_DisableWindowContextHelpButton)
app = QApplication(sys.argv)
app.setStyleSheet(Theme.load_stylesheet())
app.setQuitOnLastWindowClosed(False)

config = Config()
translator = QTranslator(app)
qt_translator = QTranslator(app)
language = LoadTranslation.load_translation()
if language is not None:
    translator.load(language, 'Translation')
    qt_translator.load('qtbase_' + language, 'Translation')
    app.installTranslator(translator)
    app.installTranslator(qt_translator)

debug_flag_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'DEBUG'))
is_debug = os.path.isfile(debug_flag_path)
logging.basicConfig(level=logging.DEBUG if is_debug else logging.CRITICAL,
                    format='%(asctime)s %(name)s [%(levelname)s] %(module)s.%(funcName)s | %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %a'
                    )


class DashboardWindow(DashboardForm):
    config = config
    net_discover_thread = None
    class_broadcast_object = None
    private_message_thread = None
    screen_broadcast_thread = None
    remote_spy_thread = None
    send_message_group_dialog = None
    network_devices_select_dialog = None

    def __init__(self):
        super(DashboardWindow, self).__init__()
        login = LoginForm(self)
        if is_debug:
            login.ui.username.setText('admin')
            login.ui.password.setText('123456')
        if login.exec_() != login.Accepted:
            sys.exit(0)
        network_devices_select_dialog = NetworkDeviceSelectForm(self)
        if network_devices_select_dialog.exec_() != network_devices_select_dialog.Accepted:
            sys.exit(0)
        network_device = network_devices_select_dialog.get_selected_device()
        self.init_network_device(network_device)
        self.init_threads()
        self.init_tray()
        self.show()
        self.start_all_threadings()

    def init_threads(self):
        self.net_discover_thread = NetworkDiscoverThread(self.config)
        self.class_broadcast_object = ClassBroadcast(self.config)
        self.private_message_thread = PrivateMessageThread(self.config, self)
        self.screen_broadcast_thread = ScreenBroadcastThread(self.config)
        self.remote_spy_thread = RemoteSpyThread(self.config)
        self.init_connections()


dashboard_window = DashboardWindow()

if __name__ == '__main__':
    sys.exit(app.exec_())
