from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QDialog, QListWidgetItem, QLabel, QMessageBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
import ujson
import time
from functools import partial
from .DashboardUI import Ui_DashboardForm
from .SendMessageGroup import SendMessageGroupForm
from .RemoteCommandGroup import RemoteCommandGroupForm


class DashboardForm(QMainWindow):
    def __init__(self, parent=None):
        super(DashboardForm, self).__init__(parent)
        self.ui = Ui_DashboardForm()
        self.threadings = {'net_discover_thread': False,
                           'private_message_thread': False}
        self.clients = {}
        self.mac_binding = {}
        self.ui.setupUi(self)
        self.ui.toggle_broadcast.setProperty('class', 'big_button')
        self.ui.remote_spy.setProperty('class', 'big_button')
        self.ui.remote_command.setProperty('class', 'big_button')
        self.ui.file_transfer.setProperty('class', 'big_button')

    def init_connections(self):
        self.private_message_thread.client_login_logout.connect(self.__logger)
        self.private_message_thread.client_notify_recieved.connect(partial(self.__logger, 'client_notify'))
        self.private_message_thread.client_desktop_recieved.connect(self.__update_client_desktop)
        self.private_message_thread.client_file_recieved.connect(partial(self.__logger, 'file_recieved'))

    def __mark_status(self, name, status):
        self.threadings[name] = status

    def __logger(self, type_, ip, mac=None):
        if type_ == 'online':
            self.mac_binding[ip] = mac
            self.__log_append(f'{self.get_client_label_by_ip(ip)}上线')
            self.__add_client_desktop(ip)
        elif type_ == 'offline':
            self.__log_append(f'{self.get_client_label_by_ip(ip)}离线')
            self.__remove_client_desktop(ip)
        elif type_ == 'file_recieved':
            self.__log_append(f'已收到来自{self.get_client_label_by_ip(ip)}的文件')
        elif type_ == 'client_notify':
            self.__log_append(f'{self.get_client_label_by_ip(ip)}举手')

    def __log_append(self, message):
        self.ui.log_area.append(f'[{time.strftime("%H:%M", time.localtime(time.time()))}] {message}')

    def __add_client_desktop(self, client_ip):
        if client_ip in self.clients.keys():
            return
        desktop = QListWidgetItem(self.get_client_label_by_ip(client_ip))
        desktop.setIcon(QIcon(':/logo/UI/Resources/client_blank.png'))
        desktop.setTextAlignment(Qt.AlignHCenter)
        desktop.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
        self.clients[client_ip] = desktop
        self.ui.desktop_layout.addItem(self.clients[client_ip])

    def __remove_client_desktop(self, client_ip):
        if client_ip in self.mac_binding.keys():
            self.mac_binding.pop(client_ip)
        if client_ip in self.clients.keys():
            index = self.ui.desktop_layout.row(self.clients[client_ip])
            self.ui.desktop_layout.removeItemWidget(self.ui.desktop_layout.takeItem(index))
            self.clients.pop(client_ip)

    def __update_client_desktop(self, client_ip, client_desktop):
        if client_ip in self.clients.keys():
            self.clients[client_ip].setIcon(QIcon(client_desktop))

    def get_client_label_by_ip(self, ip):
        label = self.client_config.get('ClientLabel').get(self.mac_binding.get(ip))
        if not label:
            return ip
        return label

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
        send_message_group_dialog = SendMessageGroupForm(self)
        result = send_message_group_dialog.exec_()
        if result:
            message = send_message_group_dialog.ui.send_message_input.toPlainText()
            if send_message_group_dialog.ui.send_to_all.isChecked():
                self.class_broadcast_object.send_public_text(message)
                self.__log_append(f'广播消息：{message}')
            elif send_message_group_dialog.ui.send_to_selected.isChecked():
                targets = send_message_group_dialog.ui.target_list.selectedItems()
                if len(targets) == 0:
                    QMessageBox.critical(self, '错误', '选择目标为空')
                    return
                target_labels = list(map(lambda x: x.text(), targets))
                target_ips = list(map(lambda x: x.data(Qt.UserRole), targets))
                self.class_broadcast_object.send_private_text(target_ips, message)
                self.__log_append(f'私人消息({",".join(target_labels)})：{message}')

    def remote_command(self):
        remote_command_group_dialog = RemoteCommandGroupForm(self)
        result = remote_command_group_dialog.exec_()
        if result:
            command = remote_command_group_dialog.ui.command_select.selectedItems()
            if len(command) == 0:
                QMessageBox.critical(self, '错误', '选择命令为空')
                return
            selected_label = command[0].text()
            selected_command = command[0].data(Qt.UserRole)
            confirm = QMessageBox.question(self, '确认', f'是否确认发送 {selected_label} 命令？', QMessageBox.Yes | QMessageBox.No)
            if confirm != QMessageBox.Yes:
                return
            if remote_command_group_dialog.ui.send_to_all.isChecked():
                self.class_broadcast_object.send_public_command(selected_command)
            elif remote_command_group_dialog.ui.send_to_selected.isChecked():
                targets = remote_command_group_dialog.ui.target_list.selectedItems()
                if len(targets) == 0:
                    QMessageBox.critical(self, '错误', '选择目标为空')
                    return
                target_ips = list(map(lambda x: x.data(Qt.UserRole), targets))
                self.class_broadcast_object.send_private_command(target_ips, selected_command)
            QMessageBox.information(self, '提示', '发送成功')

    def toggle_broadcast(self, working):
        if working:
            self.screen_broadcast_thread.start()
            self.class_broadcast_object.screen_broadcast_nodity(True)
        else:
            self.screen_broadcast_thread.safe_stop()
            self.class_broadcast_object.screen_broadcast_nodity(False)

    def closeEvent(self, event):
        self.toggle_broadcast(False)
        self.class_broadcast_object.console_quit_notify()
        event.accept()
