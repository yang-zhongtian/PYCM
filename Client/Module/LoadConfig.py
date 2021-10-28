from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QMessageBox
from UI.NetworkDeviceSelect import NetworkDeviceSelectForm


class Config(object):
    def __init__(self):
        self.settings = QSettings('HCC', 'PYCMClient')
        self.__default_config = {
            'FirstRun': True,
            'Network': {
                'Local': {'Device': ''},
                'NetworkDiscover': {
                    'IP': '224.50.50.50',
                    'Port': 4088,
                    'Interval': 5
                },
                'ClassBroadcast': {
                    'IP': '225.2.2.19',
                    'Port': 4089,
                    'Buffer': 65500
                },
                'PrivateMessage': {
                    'Port': 4091,
                    'Buffer': 32768
                },
                'ScreenBroadcast': {
                    'IP': '225.2.2.21',
                    'Port': 4092,
                    'Buffer': 65500
                },
                'RemoteSpy': {
                    'Port': 4093
                }
            }
        }
        self.__default_tree = []
        self.init_all()

    def get_item(self, path, default=None):
        return self.settings.value(str(path), default)

    def get_all(self, path, default=None):
        items = {}
        self.settings.beginGroup(str(path))
        for key in self.settings.allKeys():
            items[key] = self.settings.value(key, default)
        self.settings.endGroup()
        return items

    def save(self, path, value, sync=True):
        self.settings.setValue(str(path), value)
        if sync:
            self.settings.sync()

    def first_run(self):
        return self.get_item('FirstRun') is None

    def __generate_default_tree(self, current, path_list=None):
        if path_list is None:
            path_list = []
        if type(current) != dict:
            self.__default_tree.append(('/'.join(path_list), current))
            return
        for key, value in current.items():
            self.__generate_default_tree(value, path_list + [str(key)])

    def modify_network_device(self):
        network_device_select_form = NetworkDeviceSelectForm()
        return_code = network_device_select_form.exec_()
        if return_code == network_device_select_form.Accepted:
            device_tag = network_device_select_form.get_selected_device()
            self.save('Network/Local/Device', device_tag)
            return True
        return False

    def init_all(self):
        if not self.first_run():
            return False
        network_device_select_form = NetworkDeviceSelectForm()
        while network_device_select_form.exec_() != network_device_select_form.Accepted:
            QMessageBox.critical(None, 'Warning', 'Please select a network device!')
        self.__default_config['Network']['Local']['Device'] = network_device_select_form.get_selected_device()
        self.__default_tree.clear()
        self.__generate_default_tree(self.__default_config)
        for key, value in self.__default_tree:
            self.save(key, value)
        self.settings.sync()
