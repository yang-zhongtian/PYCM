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

from PyQt5.QtWidgets import QDialog, QListWidget, QListWidgetItem, QStyle, QFileDialog, QMessageBox
from PyQt5.QtCore import QCoreApplication, QUrl, Qt, QMimeData, QDir, pyqtSignal, QThread
from PyQt5.QtGui import QDrag
import os
from .FileClientUI import Ui_FileClient
from Module.FileClient import FileClient


class FileDownloadThread(QThread):
    file_count_signal = pyqtSignal(int)
    file_recieved = pyqtSignal(str, bytes)
    file_transfer_progress = pyqtSignal(float)
    base_path = None
    files = None
    file_count = 0
    file_finished = 0
    sock_clent = None

    def __init__(self, sock_clent, base_path, files):
        super(FileDownloadThread, self).__init__()
        self.sock_clent = sock_clent
        self.base_path = base_path
        self.files = files
        self.file_count_signal.connect(self.update_file_count)
        self.file_recieved.connect(self.file_recieved_handler)

    def run(self):
        self.sock_clent.download(self.file_count_signal, self.file_recieved, self.files)

    def update_file_count(self, count):
        self.file_count = count

    def file_recieved_handler(self, file_path, file_data):
        save_path = os.path.join(self.base_path, file_path.lstrip('/'))
        save_dir = os.path.dirname(save_path)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        with open(save_path, 'wb') as file:
            file.write(file_data)
        self.file_finished += 1
        self.file_transfer_progress.emit(self.file_finished / self.file_count)


class FileClientDialog(QDialog):
    _translate = QCoreApplication.translate
    file_download_thread = None

    def __init__(self, parent=None):
        super(FileClientDialog, self).__init__(parent)
        self.ui = Ui_FileClient()
        self.parent = parent
        self.ui.setupUi(self)
        self.ui.download_progress.setHidden(True)
        self.file_client = FileClient(self, self.parent.server_ip,
                                      self.parent.config.get_item('Network/FileServer/Port'))
        self.file_client.connect()
        self.list_dir('/')

    def list_dir(self, path):
        result = self.file_client.list_dir(path)
        self.ui.file_area.clear()
        for item in result:
            widget = QListWidgetItem(item['name'])
            if item['type'] == 1:
                icon = self.style().standardIcon(QStyle.SP_DirIcon)
                widget.setData(Qt.UserRole, ['dir', os.path.join(path, item['name'])])
            elif item['type'] == 0:
                icon = self.style().standardIcon(QStyle.SP_FileIcon)
                widget.setData(Qt.UserRole, ['file', os.path.join(path, item['name'])])
            else:
                icon = self.style().standardIcon(QStyle.SP_CustomBase)
            widget.setIcon(icon)
            self.ui.file_area.addItem(widget)
        self.ui.location.setText(path)

    def update_selection(self):
        if len(self.ui.file_area.selectedIndexes()) > 0:
            self.ui.download_button.setEnabled(True)
        else:
            self.ui.download_button.setEnabled(False)

    def download(self):
        # UI display no dir
        items = self.ui.file_area.selectedItems()
        files = []
        save_path = QFileDialog.getExistingDirectory(self, self._translate('FileClientDialog', 'Select Path To Save'),
                                                     str(QDir.homePath()))
        if not save_path:
            QMessageBox.critical(self, self._translate('FileClientDialog', 'Warning'),
                                 self._translate('FileClientDialog', 'Please select path to save!'))
            return
        for item in items:
            if item.data(Qt.UserRole)[0] == 'file':
                files.append(item.data(Qt.UserRole)[1])
        self.file_download_thread = FileDownloadThread(self.file_client, save_path, files)
        self.file_download_thread.file_transfer_progress.connect(self.update_download_progress)
        self.file_download_thread.start()

    def update_download_progress(self, progress):
        self.ui.download_progress.setHidden(False)
        self.ui.download_progress.setValue(int(progress * 100))
        if progress >= 1:
            QMessageBox.information(self, self._translate('FileClientDialog', 'Info'),
                                    self._translate('FileClientDialog', 'File download finished'))
            self.ui.download_progress.setValue(0)
            self.ui.download_progress.setHidden(True)

    def closeEvent(self, e):
        self.file_client.socket_obj.close()
