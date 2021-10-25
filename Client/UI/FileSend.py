from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, \
    QFileIconProvider, QApplication, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QFileInfo, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
import os
import zipfile
from io import BytesIO
from functools import partial
from .FileSendUI import Ui_FileSendForm


class FileCompressThread(QThread):
    file_buffer = pyqtSignal(bytes)
    file_finished = pyqtSignal(int)
    file_list = None

    def __init__(self, file_list):
        super(FileCompressThread, self).__init__()
        self.file_list = file_list

    def run(self):
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zfile:
            for index, file_path in enumerate(self.file_list):
                file_name = os.path.basename(file_path)
                zfile.write(file_path, file_name)
                self.file_finished.emit(index)
        self.file_buffer.emit(buffer.getvalue())


class FileSendThread(QThread):
    private_message_object = None
    buffer = None
    file_send_progress = pyqtSignal(float)

    def __init__(self, private_message_object, buffer):
        super(FileSendThread, self).__init__()
        self.private_message_object = private_message_object
        self.private_message_object.file_send_progress.connect(lambda x: self.file_send_progress.emit(x))
        self.buffer = buffer

    def run(self):
        self.private_message_object.send_file(self.buffer)


class DraggableQListWidget(QTableWidget):

    def __init__(self):
        super(DraggableQListWidget, self).__init__()
        self.setAcceptDrops(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(['File Name', 'File Size', 'Status'])
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.setColumnWidth(1, 120)
        self.setColumnWidth(2, 120)

    @staticmethod
    def parse_file_size(file_size):
        def str_of_size(integer, remainder, level):
            if integer >= 1024:
                remainder = integer % 1024
                integer //= 1024
                level += 1
                return str_of_size(integer, remainder, level)
            else:
                return integer, remainder, level

        units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        integer, remainder, level = str_of_size(file_size, 0, 0)
        if level + 1 > len(units):
            level = -1
        return '{}.{:>03d} {}'.format(integer, remainder, units[level])

    def batch_add_files(self, files):
        for file_info in files:
            if not file_info.isFile():
                continue
            current_row = self.rowCount()
            icon = QIcon(QFileIconProvider().icon(file_info))
            file_name_and_icon = QTableWidgetItem(file_info.absoluteFilePath())
            file_name_and_icon.setIcon(icon)
            self.setRowCount(current_row + 1)
            self.setItem(current_row, 0, file_name_and_icon)
            self.setItem(current_row, 1, QTableWidgetItem(self.parse_file_size(file_info.size())))
            self.setItem(current_row, 2, QTableWidgetItem('Ready'))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
            files = [QFileInfo(url.toLocalFile()) for url in event.mimeData().urls()]
            self.batch_add_files(files)
        else:
            event.ignore()


class FileSendForm(QDialog):
    is_sending = False
    is_finished = False
    __compress_thread = None
    __file_send_thread = None
    parent = None

    def __init__(self, parent=None):
        super(FileSendForm, self).__init__()
        self.parent = parent
        self.ui = Ui_FileSendForm()
        self.ui.setupUi(self)
        self.__repaint_ui()

    def __repaint_ui(self):
        self.ui.file_list = DraggableQListWidget()
        self.ui.file_list_container.addWidget(self.ui.file_list)

    def show_add_file_dialog(self):
        files, _ = QFileDialog.getOpenFileNames(self, 'Select Files', os.path.expanduser('~'), 'All Files (*)')
        if files:
            self.ui.file_list.batch_add_files(list(map(QFileInfo, files)))

    def delete_selected_files(self):
        selected_rows = list({item.row() for item in self.ui.file_list.selectedItems()})
        selected_rows.sort(reverse=True)
        for row in selected_rows:
            self.ui.file_list.removeRow(row)

    def send_all(self):
        file_list = [self.ui.file_list.item(row, 0).text() for row in range(self.ui.file_list.rowCount())]
        self.__compress_thread = FileCompressThread(file_list)
        self.__compress_thread.file_finished.connect(partial(self.update_status, 'Compressed'))
        self.__compress_thread.file_buffer.connect(self.submit_compressed_file)
        self.is_sending = True
        self.ui.file_send_progress_label.setText('Compressing')
        self.__compress_thread.start()

    def submit_compressed_file(self, file_buffer):
        self.is_sending = False
        self.__file_send_thread = FileSendThread(self.parent.private_message_object, file_buffer)
        self.__file_send_thread.file_send_progress.connect(self.update_send_status)
        self.__file_send_thread.start()

    def update_status(self, label, index):
        self.ui.file_list.item(index, 2).setText(label)
        current_row_count = self.ui.file_list.rowCount()
        if index + 1 < current_row_count:
            self.update_send_status((index + 1) / current_row_count)
        else:
            self.ui.file_send_progress_label.setText('Submitting')
            self.update_send_status(0)

    def update_send_status(self, progress):
        progress = int(progress * 100)
        self.ui.file_send_progress_bar.setValue(progress)
        if progress >= 100 and not self.is_finished:
            self.is_finished = True
            QMessageBox.information(self, 'Info', 'Submit Success!')
            self.close()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def closeEvent(self, event):
        if self.is_sending:
            event.ignore()
        else:
            self.ui.file_list.clearContents()
            self.ui.file_list.setRowCount(0)
            self.ui.file_send_progress_bar.setValue(0)
            self.hide()
            event.ignore()
