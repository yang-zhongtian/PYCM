# -*- coding: utf-8 -*-
"""
    This file is part of PYCM project
    Copyright (C) 2021 Richard Yang  <zhongtian.yang@qq.com>

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
                    'Buffer': 65500,
                    'Quality': 60
                },
                'RemoteSpy': {
                    'Port': 4093
                },
                'FileServer': {
                    'Port': 4096
                },
            },
            'Login': {
                'Username': 'admin',
                'Password': '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
            },
            'Client': {
                'FileUploadPath': '',
                'ClientLabel': {

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

    def remove(self, path, sync=True):
        self.settings.remove(str(path))
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
