from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt5.QtCore import Qt, QFileInfo
from .FileSendUI import Ui_FileSendForm


class DraggableQListWidget(QTableWidget):

    def __init__(self):
        super(DraggableQListWidget, self).__init__()
        self.setAcceptDrops(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(['文件名', '文件类型', '文件大小', '发送状态'])
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

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
            current_row = self.rowCount()
            self.setRowCount(current_row + 1)
            self.setItem(current_row, 0, QTableWidgetItem(file_info.absoluteFilePath()))
            self.setItem(current_row, 1, QTableWidgetItem('文件' if file_info.isFile() else '目录'))
            self.setItem(current_row, 2, QTableWidgetItem(self.parse_file_size(file_info.size()) if file_info.isFile()
                                                          else '-'))
            self.setItem(current_row, 3, QTableWidgetItem('就绪'))

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


class FileSendForm(QWidget):
    is_sending = False

    def __init__(self, parent=None):
        super(FileSendForm, self).__init__(parent)
        self.ui = Ui_FileSendForm()
        self.ui.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.__repaint_ui()

    def __repaint_ui(self):
        self.ui.file_list.deleteLater()
        self.ui.file_list = DraggableQListWidget()
        self.ui.file_list_container.addWidget(self.ui.file_list)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def closeEvent(self, event):
        if self.is_sending:
            event.ignore()
        else:
            event.accept()
