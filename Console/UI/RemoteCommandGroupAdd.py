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
from .RemoteCommandGroupAddUI import Ui_RemoteCommandGroupAddDialog


class RemoteCommandGroupAddForm(QDialog):
    _translate = QCoreApplication.translate

    def __init__(self, parent=None):
        super(RemoteCommandGroupAddForm, self).__init__(parent)
        self.ui = Ui_RemoteCommandGroupAddDialog()
        self.parent = parent
        self.ui.setupUi(self)

    def accept(self):
        if self.ui.title.text() == '':
            QMessageBox.critical(self, self._translate('RemoteCommandGroupAddDialog', 'Error'),
                                 self._translate('RemoteCommandGroupAddDialog', 'Please set a name for the command'))
        elif self.ui.command.document().lineCount() != 1:
            QMessageBox.critical(self, self._translate('RemoteCommandGroupAddDialog', 'Error'),
                                 self._translate('RemoteCommandGroupAddDialog',
                                                 'Please input only one line of command'))
        elif '/' in self.ui.title.text():
            QMessageBox.critical(self, self._translate('RemoteCommandGroupAddDialog', 'Error'),
                                 self._translate('RemoteCommandGroupAddDialog', "Name cannot contain '/'"))
        else:
            super(RemoteCommandGroupAddForm, self).accept()
