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

from PyQt5.QtWidgets import QDialog, QListWidgetItem
from PyQt5.QtCore import Qt
from .RemoteCommandGroupUI import Ui_RemoteCommandGroupDialog


class RemoteCommandGroupForm(QDialog):
    def __init__(self, parent=None):
        super(RemoteCommandGroupForm, self).__init__(parent)
        self.ui = Ui_RemoteCommandGroupDialog()
        self.parent = parent
        self.available_commands = parent.config.get_all('Client/AvailableRemoteCommands')
        self.ui.setupUi(self)
        self.init()

    def init(self):
        for label, command in self.available_commands.items():
            new_item = QListWidgetItem(label)
            new_item.setData(Qt.UserRole, command)
            self.ui.command_select.addItem(new_item)
