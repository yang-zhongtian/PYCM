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

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
import psutil
import socket
from .NetworkDeviceSelectUI import Ui_NetworkDeviceSelectDialog


class NetworkDeviceSelectForm(QDialog):
    def __init__(self, parent=None):
        super(NetworkDeviceSelectForm, self).__init__(parent)
        self.devices = []
        self.ui = Ui_NetworkDeviceSelectDialog()
        self.setFixedSize(413, 120)
        self.setWindowModality(Qt.ApplicationModal)
        self.ui.setupUi(self)
        self.default_device = parent.config.get_item('Network/Local/Device')
        self.load_network_devices()

    def sync_network_devices(self):
        self.ui.network_device_list.clear()
        for idx, device in enumerate(self.devices):
            device_name, device_info = device
            self.ui.network_device_list.addItem(device_name, device_info)
            if device_name == self.default_device:
                self.ui.network_device_list.setCurrentIndex(idx)

    def load_network_devices(self):
        network_devices = psutil.net_if_addrs()
        self.devices.clear()
        for device in network_devices.keys():
            af_inet4 = []
            af_link = []
            for item in network_devices[device]:
                if item.family == socket.AF_INET:
                    af_inet4.append(item.address)
                elif item.family == psutil.AF_LINK:
                    af_link.append(item.address)
            if len(af_inet4) == 1 and len(af_link) == 1:
                self.devices.append((device, {'IP': af_inet4[0], 'MAC': af_link[0]}))
        self.sync_network_devices()

    def get_selected_device(self):
        obj_data = self.ui.network_device_list.currentData()
        obj_tag = self.ui.network_device_list.currentText()
        self.parent().config.save('Network/Local/Device', obj_tag)
        return obj_data
