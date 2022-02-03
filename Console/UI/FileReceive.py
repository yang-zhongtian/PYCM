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

from PyQt5.QtWidgets import QDialog, QHeaderView, QTableWidgetItem, QLabel, QFileDialog
from PyQt5.QtCore import Qt, QUrl, QCoreApplication
from PyQt5.QtGui import QDesktopServices
import os
from .FileReceiveUI import Ui_FileReceiveDialog


class FileReceiveForm(QDialog):
    _translate = QCoreApplication.translate

    def __init__(self, parent=None):
        super(FileReceiveForm, self).__init__(parent)
        self.ui = Ui_FileReceiveDialog()
        self.parent = parent
        self.ui.setupUi(self)
        self.ui.received_files.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.ui.received_files.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.ui.received_files.setColumnWidth(1, 140)
        self.set_receive_folder()

    def set_receive_folder(self):
        directory = self.parent.config.get_item('Client/FileUploadPath')
        self.ui.receive_folder.setText(directory)

    def add_received_file(self, file_name, from_label):
        current_row = self.ui.received_files.rowCount()
        file_path = os.path.join(self.ui.receive_folder.text(), file_name)
        file = QTableWidgetItem(file_name)
        file.setTextAlignment(Qt.AlignCenter)
        file.setData(Qt.UserRole, file_path)
        label = QTableWidgetItem(from_label)
        label.setTextAlignment(Qt.AlignCenter)
        self.ui.received_files.setRowCount(current_row + 1)
        self.ui.received_files.setItem(current_row, 0, file)
        self.ui.received_files.setItem(current_row, 1, label)

    def change_receive_folder(self):
        directory = QFileDialog.getExistingDirectory(self, self._translate('FileReceiveDialog', 'Select Receive Folder'),
                                                     os.path.expanduser('~'))
        if not directory:
            return
        self.parent.config.save('Client/FileUploadPath', directory)
        self.set_receive_folder()

    def open_receive_folder(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.ui.receive_folder.text()))

    def open_selected_file(self, item: QTableWidgetItem):
        item_row = item.row()
        file_item = self.ui.received_files.item(item_row, 0)
        if not file_item:
            return
        file_path = file_item.data(Qt.UserRole)
        QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
