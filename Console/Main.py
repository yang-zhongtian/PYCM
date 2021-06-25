# -*- coding: utf-8 -*-
from PyQtPatch import *
from PyQt5.QtWidgets import QApplication
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

config = Config()
config.init_all()
# print(config.get('Client/AvailableRemoteCommands/打开计算器(Windows)'))
# TODO: fix all config pattern, this is just an example
exit(0)

app = QApplication(sys.argv)
app.setStyleSheet(Theme.load_stylesheet())

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)s %(module)s %(funcName)s %(message)s',
                    datefmt='%Y-%m-%d  %H:%M:%S %a'
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
        self.network_config.set('Local', network_device)
        self.init_threads()
        self.show()
        self.start_all_threadings()

    def init_threads(self):
        self.net_discover_thread = NetworkDiscoverThread(self.network_config)
        self.class_broadcast_object = ClassBroadcast(self.network_config.get('Local').get('IP'),
                                                     self.network_config.get('ClassBroadcast').get('IP'),
                                                     self.network_config.get('ClassBroadcast').get('Port'),
                                                     self.network_config.get('ClassBroadcast').get('Buffer'))
        self.private_message_thread = PrivateMessageThread(self.network_config, self.client_config, self)
        self.screen_broadcast_thread = ScreenBroadcastThread(self.network_config)
        self.init_connections()


dashboard_window = DashboardWindow()

if __name__ == '__main__':
    sys.exit(app.exec_())
