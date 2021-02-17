from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QDialog, QListWidgetItem, QLabel
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
        self.threadings = {'net_discover_thread': False,
                           'private_message_thread': False}
        self.clients = {}
        self.ui.setupUi(self)
        self.ui.toggle_broadcast.setProperty('class', 'big_button')
        self.ui.remote_spy.setProperty('class', 'big_button')
        self.ui.file_transfer.setProperty('class', 'big_button')
        self.ui.toggle_black_screen.setProperty('class', 'big_button')

    def init_connections(self):
        self.private_message_thread.client_login_logout.connect(self.__logger)
        self.private_message_thread.client_desktop_recieved.connect(self.__update_client_desktop)
        self.private_message_thread.client_file_recieved.connect(partial(self.__logger, 'file_recieved'))

    def __mark_status(self, name, status):
        self.threadings[name] = status

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
            thread.started.connect(partial(self.__mark_status, thread_name, 'online'))
            thread.finished.connect(partial(self.__mark_status, thread_name, 'offline'))
            thread.start()

    def send_message(self):
        self.send_message_group_dialog.ui.send_to_selected.setChecked(True)
        self.send_message_group_dialog.ui.target_select.show()
        self.send_message_group_dialog.ui.send_message_input.clear()
        self.send_message_group_dialog.ui.target_list.clear()
        self.send_message_group_dialog.ui.target_list.addItems(self.clients.keys())
        result = self.send_message_group_dialog.exec_()
        if result:
            message = self.send_message_group_dialog.ui.send_message_input.toPlainText()
            if self.send_message_group_dialog.ui.send_to_all.isChecked():
                self.class_broadcast_object.send_public_text(message)
                self.__log_append(f'广播消息：{message}')
            elif self.send_message_group_dialog.ui.send_to_selected.isChecked():
                targets = list(map(lambda x: x.text(), self.send_message_group_dialog.ui.target_list.selectedItems()))
                self.class_broadcast_object.send_private_text(targets, message)
                self.__log_append(f'私人消息({",".join(targets)})：{message}')

    def toggle_broadcast(self, working):
        if working:
            self.screen_broadcast_thread.start()
            screen_width = self.screen_broadcast_thread.socket.screen_width
            screen_height = self.screen_broadcast_thread.socket.screen_height
            self.class_broadcast_object.screen_broadcast_nodity(True, (screen_width, screen_height))
        else:
            self.screen_broadcast_thread.safe_stop()
            self.class_broadcast_object.screen_broadcast_nodity(False)

    def closeEvent(self, event):
        self.class_broadcast_object.console_quit_notify()
        event.accept()
