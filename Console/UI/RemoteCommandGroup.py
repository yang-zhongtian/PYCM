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

from PyQt5.QtWidgets import QDialog, QListWidgetItem, QMessageBox
from PyQt5.QtCore import Qt, QCoreApplication
from .RemoteCommandGroupUI import Ui_RemoteCommandGroupDialog
from .RemoteCommandGroupAdd import RemoteCommandGroupAddForm


class RemoteCommandGroupForm(QDialog):
    _translate = QCoreApplication.translate

    def __init__(self, parent=None):
        super(RemoteCommandGroupForm, self).__init__(parent)
        self.ui = Ui_RemoteCommandGroupDialog()
        self.parent = parent
        self.ui.setupUi(self)
        self.load_commands()

    def load_commands(self):
        available_commands = self.parent.config.get_all('Client/AvailableRemoteCommands')
        self.ui.command_select.clear()
        for label, command in available_commands.items():
            new_item = QListWidgetItem(label)
            new_item.setData(Qt.UserRole, command)
            self.ui.command_select.addItem(new_item)

    def add_command(self):
        add_form = RemoteCommandGroupAddForm(self)
        result = add_form.exec_()
        if result != add_form.Accepted:
            return
        title = add_form.ui.title.text()
        command = add_form.ui.command.toPlainText()
        self.parent.config.save(f'Client/AvailableRemoteCommands/{title}', command)
        self.load_commands()

    def remove_command(self):
        selected = self.ui.command_select.selectedItems()
        if len(selected) == 0:
            QMessageBox.warning(self, self._translate('RemoteCommandGroupDialog', 'Warning'),
                                self._translate('RemoteCommandGroupDialog', 'Please select a command to remove'))
            return
        selected = selected[0].text()
        reply = QMessageBox.question(self, self._translate('RemoteCommandGroupDialog', 'Warning'),
                                     self._translate('RemoteCommandGroupDialog',
                                                     'Are you sure to remove this command: ') + str(selected),
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.parent.config.remove(f'Client/AvailableRemoteCommands/{selected}')
            self.load_commands()
