from PyQt5.QtCore import QSettings


class Config(object):
    def __init__(self):
        self.settings = QSettings('HCC', 'PYCMConsole')
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
                    'FFMpegPath': 'ffmpeg',
                    'FFMpegQuality': 6
                },
                'RemoteSpy': {
                    'Port': 4093
                }
            },
            'Login': {
                'Username': 'admin',
                'Password': 'e10adc3949ba59abbe56e057f20f883e'
            },
            'Client': {
                'FileUploadPath': '',
                'ClientLabel': {
                    'XX-XX-XX-XX-XX-XX': 'ExampleClient'
                },
                'AvailableRemoteCommands': {
                    '关机(Window)': 'shutdown -s -t 0',
                    '关机(OSX)': "osascript -e 'tell app \"System Events\" to shut down'",
                    '关机(Linux)': 'sudo poweroff',
                    '打开计算器(Windows)': 'calc'
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

    def init_all(self):
        if not self.first_run():
            return False
        self.__default_tree.clear()
        self.__generate_default_tree(self.__default_config)
        for key, value in self.__default_tree:
            self.save(key, value)
        self.settings.sync()
