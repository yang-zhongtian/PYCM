from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QListWidgetItem, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
import ujson
import time
from functools import partial
from .DashboardUI import Ui_DashboardForm


class DashboardForm(QMainWindow):
    def __init__(self, parent=None):
        super(DashboardForm, self).__init__(parent)
        self.ui = Ui_DashboardForm()
        self.threadings = {'net_discover_thread': 'network_discover_status',
                           'private_message_thread': 'private_message_status'}
        self.clients = {}
        self.ui.setupUi(self)

    def init_connections(self):
        self.private_message_thread.client_login_logout.connect(self.__logger)
        self.private_message_thread.client_desktop_recieved.connect(self.__update_client_desktop)
        self.private_message_thread.client_file_recieved.connect(partial(self.__logger, 'file_recieved'))

    def __mark_status(self, name, status):
        obj = getattr(self.ui, name)
        if status == 'online':
            obj.setStyleSheet('color: green')
        elif status == 'offline':
            obj.setStyleSheet('color: red')
        elif status == 'unknown':
            obj.setStyleSheet('color: black')

    def __logger(self, type_, data):
        if type_ == 'online':
            self.__log_append(f'{data}已上线')
            self.__add_client_desktop(data)
        elif type_ == 'offline':
            self.__log_append(f'{data}已离线')
            self.__remove_client_desktop(data)
        elif type_ == 'file_recieved':
            self.__log_append(f'已收到来自 {data} 的文件')

    def __log_append(self, message):
        self.ui.log_area.append(f'[{time.strftime("%H:%M", time.localtime(time.time()))}] {message}')

    def __add_client_desktop(self, client_ip):
        if client_ip in self.clients.keys():
            return
        desktop = QListWidgetItem(client_ip)
        desktop.setIcon(QIcon(':/logo/UI/Resources/client_blank.png'))
        desktop.setTextAlignment(Qt.AlignHCenter)
        desktop.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
        self.clients[client_ip] = desktop
        self.ui.desktop_layout.addItem(self.clients[client_ip])

    def __remove_client_desktop(self, client_ip):
        if client_ip in self.clients.keys():
            index = self.ui.desktop_layout.row(self.clients[client_ip])
            self.ui.desktop_layout.removeItemWidget(self.ui.desktop_layout.takeItem(index))
            self.clients.pop(client_ip)

    def __update_client_desktop(self, client_ip, client_desktop):
        if client_ip in self.clients.keys():
            self.clients[client_ip].setIcon(QIcon(client_desktop))

    def clear_client_selection(self):
        self.ui.desktop_layout.clearSelection()

    def client_scroll_in(self):
        size = self.ui.desktop_layout.iconSize()
        self.ui.desktop_layout.setIconSize(QSize(size.width() + 32, size.height() + 18))

    def client_scroll_out(self):
        size = self.ui.desktop_layout.iconSize()
        self.ui.desktop_layout.setIconSize(QSize(size.width() - 32, size.height() - 18))

    def start_all_threadings(self):
        for thread_name in self.threadings.keys():
            thread = getattr(self, thread_name)
            thread_status_name = self.threadings.get(thread_name)
            thread.started.connect(partial(self.__mark_status, thread_status_name, 'online'))
            thread.finished.connect(partial(self.__mark_status, thread_status_name, 'offline'))
            thread.start()
