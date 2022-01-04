# -*- coding: utf-8 -*-
"""
    This file is part of PYCM project
    Copyright (C)2021 Richard Yang <zhongtian.yang@qq.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from Utils import LoadTranslation
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt5.QtCore import Qt, QCoreApplication, QTranslator
import sys
import os
import logging

from Module.LoadConfig import Config

from Resources import Resources
from Module import Theme

from UI.Main import MainForm

from Module.Threadings import NetworkDiscoverThread, ClassBroadcastThread, ScreenBroadcastThread, RemoteSpyThread
from Module.PrivateMessage import PrivateMessage

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_DisableWindowContextHelpButton)
app = QApplication(sys.argv)
app.setStyleSheet(Theme.load_stylesheet())
app.setQuitOnLastWindowClosed(False)

translator = QTranslator(app)
qt_translator = QTranslator(app)
language = LoadTranslation.load_translation()
if language is not None:
    translator.load(LoadTranslation.load_path(language))
    qt_translator.load(LoadTranslation.load_path('qtbase_' + language))
    app.installTranslator(translator)
    app.installTranslator(qt_translator)

config = Config()

debug_flag_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'DEBUG'))
logging.basicConfig(level=logging.DEBUG if os.path.isfile(debug_flag_path) else logging.CRITICAL,
                    format='%(asctime)s %(name)s [%(levelname)s] %(module)s.%(funcName)s | %(message)s',
                    datefmt='%Y-%m-%d  %H:%M:%S %a'
                    )


class MainWindow(MainForm):
    config = config
    net_discover_thread = None
    class_broadcast_thread = None
    screen_broadcast_thread = None
    remote_spy_thread = None
    private_message_object = None
    _translate = QCoreApplication.translate

    def __init__(self):
        super(MainWindow, self).__init__(self)
        network_device = self.load_network_device()
        if not network_device:
            QMessageBox.critical(self, self._translate('MainForm', 'Error'),
                                 self._translate('MainForm', 'Network device error, please select another device!'))
            device = config.force_get_network_device(only_name=False)
            config.save('Network/Local/Device', device['NAME'])
            self.init_network_device(device)
        else:
            self.init_network_device(network_device)
        self.init_threadings()

    def init_threadings(self):
        self.net_discover_thread = NetworkDiscoverThread(self.config)
        self.class_broadcast_thread = ClassBroadcastThread(self.config)
        self.screen_broadcast_thread = ScreenBroadcastThread(self.config)
        self.remote_spy_thread = RemoteSpyThread(self.config)
        self.private_message_object = PrivateMessage(self.config)
        self.init_connections()
        self.net_discover_thread.start()

    def reset_all_threadings(self):
        self.screen_spy_timer.stop()
        self.class_broadcast_thread.quit()
        self.remote_spy_thread.safe_stop()
        self.class_broadcast_thread.wait()
        self.remote_spy_thread.wait()
        self.net_discover_thread = NetworkDiscoverThread(self.config)
        self.class_broadcast_thread = ClassBroadcastThread(self.config)
        self.remote_spy_thread = RemoteSpyThread(self.config)
        self.private_message_object = PrivateMessage(self.config)
        self.init_connections()
        self.ui.title_label.setText(self._translate('MainForm', 'PYCM Client - Offline'))
        self.update_tray_tooltip()
        self.ui.notify_button.setEnabled(False)
        self.ui.file_button.setEnabled(False)
        self.ui.private_message_button.setEnabled(False)
        self.server_ip = None
        self.net_discover_thread.start()


main_window = MainWindow()

if __name__ == '__main__':
    main_window.show()
    sys.exit(app.exec_())
