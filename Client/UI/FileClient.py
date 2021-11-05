from PyQt5.QtWidgets import QDialog, QListWidget, QListWidgetItem, QStyle
from PyQt5.QtCore import QCoreApplication, QUrl, Qt, QMimeData
from PyQt5.QtGui import QDrag
import os
from .FileClientUI import Ui_FileClient
from Module.FileClient import FileClient


class FileClientDialog(QDialog):
    _translate = QCoreApplication.translate

    def __init__(self, parent=None):
        super(FileClientDialog, self).__init__(parent)
        self.ui = Ui_FileClient()
        self.parent = parent
        self.ui.setupUi(self)
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
                widget.setData(Qt.DisplayRole, 'dir')
            elif item['type'] == 0:
                icon = self.style().standardIcon(QStyle.SP_FileIcon)
                widget.setData(Qt.DisplayRole, 'file')
            else:
                icon = self.style().standardIcon(QStyle.SP_CustomBase)
            widget.setIcon(icon)
            widget.setData(Qt.UserRole, os.path.join(path, item['name']))
            self.ui.file_area.addItem(widget)

    def update_selection(self):
        if len(self.ui.file_area.selectedIndexes()) > 0:
            self.ui.download_button.setEnabled(True)
        else:
            self.ui.download_button.setEnabled(False)

    def download(self):
        # UI display no dir
        items = self.ui.file_area.selectedItems()
        files = []
        for item in items:
            if item.data(Qt.DisplayRole) == 'file':
                files.append(item.data(Qt.UserRole))
        self.file_client.download(files)

    def closeEvent(self, e):
        self.file_client.socket_obj.close()
