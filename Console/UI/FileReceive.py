from PyQt5.QtWidgets import QDialog, QHeaderView, QTableWidgetItem, QLabel, QFileDialog
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
import os
from .FileReceiveUI import Ui_FileReceiveDialog


class FileReceiveForm(QDialog):
    def __init__(self, parent=None):
        super(FileReceiveForm, self).__init__(parent)
        self.ui = Ui_FileReceiveDialog()
        self.parent = parent
        self.ui.setupUi(self)
        self.ui.received_files.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.ui.received_files.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.ui.received_files.setColumnWidth(1, 120)
        self.ui.received_files.setColumnWidth(2, 120)
        self.set_receive_folder()

    def set_receive_folder(self):
        directory = self.parent.config.get_item('Client/FileUploadPath')
        self.ui.receive_folder.setText(directory)

    def add_received_file(self, file_name, from_label, file_path):
        current_row = self.ui.received_files.rowCount()
        file = QTableWidgetItem(file_name)
        file.setTextAlignment(Qt.AlignCenter)
        label = QTableWidgetItem(from_label)
        label.setTextAlignment(Qt.AlignCenter)
        open_file = QLabel(self.ui.received_files)
        open_file.setText(f"<a href='file:///{file_path}'>Open</a>")
        open_file.setOpenExternalLinks(True)
        open_file.setAlignment(Qt.AlignCenter)
        self.ui.received_files.setRowCount(current_row + 1)
        self.ui.received_files.setItem(current_row, 0, file)
        self.ui.received_files.setItem(current_row, 1, label)
        self.ui.received_files.setCellWidget(current_row, 2, open_file)

    def change_receive_folder(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select Receive Folder', os.path.expanduser('~'))
        if not directory:
            return
        self.parent.config.save('Client/FileUploadPath', directory)
        self.set_receive_folder()

    def open_receive_folder(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.ui.receive_folder.text()))
