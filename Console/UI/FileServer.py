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

from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import QCoreApplication
import os
from .FileServerUI import Ui_FileServerForm


class FileServerForm(QDialog):
    _translate = QCoreApplication.translate
    working = False

    def __init__(self, parent=None):
        super(FileServerForm, self).__init__(parent)
        self.ui = Ui_FileServerForm()
        self.parent = parent
        self.ui.setupUi(self)

    def change_working_folder(self):
        directory = QFileDialog.getExistingDirectory(self, self._translate('FileServerForm', 'Select Working Folder'),
                                                     os.path.expanduser('~'))
        if not directory:
            return
        self.parent.file_server_thread.set_working_dir(directory)
        self.ui.working_folder.setText(directory)

    def toggle_server(self):
        if not self.working:
            self.parent.file_server_thread.start()
            self.parent.class_broadcast_object.file_server_status_notify(True)
            self.working = True
        else:
            self.parent.class_broadcast_object.file_server_status_notify(False)
            self.parent.file_server_thread.safe_stop()
            self.working = False
        self.update_status()

    def update_status(self):
        if self.working:
            self.ui.server_info.setText(self._translate('FileServerForm', 'Server Status: Working'))
            self.ui.toggle_working.setText(self._translate('FileServerForm', 'Stop'))
        else:
            self.ui.server_info.setText(self._translate('FileServerForm', 'Server Status: Stopped'))
            self.ui.toggle_working.setText(self._translate('FileServerForm', 'Start'))
