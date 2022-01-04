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
from PyQt5.QtNetwork import QNetworkInterface, QAbstractSocket
import socket
from .NetworkDeviceSelectUI import Ui_NetworkDeviceSelectDialog


class NetworkDeviceSelectForm(QDialog):
    def __init__(self):
        super(NetworkDeviceSelectForm, self).__init__()
        self.devices = []
        self.ui = Ui_NetworkDeviceSelectDialog()
        self.setFixedSize(413, 120)
        self.setWindowModality(Qt.ApplicationModal)
        self.ui.setupUi(self)
        self.load_network_devices()

    def sync_network_devices(self):
        self.ui.network_device_list.clear()
        for idx, device in enumerate(self.devices):
            device_name, device_info = device
            self.ui.network_device_list.addItem(device_name, device_info)

    @staticmethod
    def get_devices():
        devices_list = QNetworkInterface.allInterfaces()
        devices = []
        for device in devices_list:
            for address in device.addressEntries():
                ip = address.ip()
                if ip.protocol() == QAbstractSocket.IPv4Protocol:
                    devices.append((device.humanReadableName(),
                                    {'IP': ip.toString(),
                                     'MAC': device.hardwareAddress(),
                                     'NAME': device.name()}))
                    break
        return devices

    def load_network_devices(self):
        devices_list = QNetworkInterface.allInterfaces()
        self.devices = self.get_devices()
        self.sync_network_devices()

    def get_selected_device(self, only_name=True):
        obj_data = self.ui.network_device_list.currentData()
        if only_name:
            return obj_data['NAME']
        else:
            return obj_data
