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
        self.default_device = parent.network_config.get('Local').get('Device')
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
        return obj_data
