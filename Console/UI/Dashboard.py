from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QDialog, QListWidgetItem, QLabel, QMessageBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
import time
import platform
from functools import partial
from .DashboardUI import Ui_DashboardForm
from .SendMessageGroup import SendMessageGroupForm
from .RemoteCommandGroup import RemoteCommandGroupForm
from .RemoteSpy import RemoteSpyForm


class DashboardForm(QMainWindow):
    def __init__(self, parent=None):
        super(DashboardForm, self).__init__(parent)
        self.ui = Ui_DashboardForm()
        self.threadings = {'net_discover_thread': False,
                           'private_message_thread': False,
                           'remote_spy_thread': False}
        self.clients = {}
        self.mac_binding = {}
        self.ui.setupUi(self)
        self.ui.toggle_broadcast.setProperty('class', 'big_button')
        self.ui.remote_spy.setProperty('class', 'big_button')
        self.ui.remote_command.setProperty('class', 'big_button')
        self.ui.file_transfer.setProperty('class', 'big_button')
        self.remote_spy_window = RemoteSpyForm(self)

    def init_connections(self):
        self.private_message_thread.client_login_logout.connect(self.__logger)
        self.private_message_thread.client_notify_recieved.connect(partial(self.__logger, 'client_notify'))
        self.private_message_thread.client_desktop_recieved.connect(self.__update_client_desktop)
        self.private_message_thread.client_file_recieved.connect(partial(self.__logger, 'file_recieved'))
        self.remote_spy_thread.frame_recieved.connect(self.remote_spy_window.update_frame)

    def init_network_device(self, device):
        self.config.save('Network/Local/IP', device['IP'])
        self.config.save('Network/Local/MAC', device['MAC'])

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
        desktop.setIcon(QIcon(':/Core/Resources/ClientBlank.png'))
        desktop.setTextAlignment(Qt.AlignHCenter)
        desktop.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
        desktop.setData(Qt.UserRole, client_ip)
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
        label = self.config.get_item(f'Client/ClientLabel/{self.mac_binding.get(ip)}')
        if not label:
            return ip
        return label

    def get_all_selected_clients(self, ip_only=False):
        clients = self.ui.desktop_layout.selectedItems()
        if len(clients) == 0:
            QMessageBox.warning(self, '提示', '未选择任何目标')
            return []
        client_infos = []
        for client in clients:
            client_ip = client.data(Qt.UserRole)
            client_mac = self.mac_binding.get(client_ip)
            if ip_only:
                client_infos.append(client_ip)
            else:
                client_infos.append({'label': client.text(), 'ip': client_ip, 'mac': client_mac})
        return client_infos

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
        targets = self.get_all_selected_clients(ip_only=True)
        if not targets:
            return
        send_message_group_dialog = SendMessageGroupForm(self)
        result = send_message_group_dialog.exec_()
        if result:
            message = send_message_group_dialog.ui.send_message_input.toPlainText()
            self.class_broadcast_object.send_text(targets, message)
            self.__log_append(f'发送消息：{message}')

    def remote_command(self):
        targets = self.get_all_selected_clients(ip_only=True)
        if not targets:
            return
        remote_command_group_dialog = RemoteCommandGroupForm(self)
        result = remote_command_group_dialog.exec_()
        if result:
            command = remote_command_group_dialog.ui.command_select.selectedItems()
            if len(command) == 0:
                QMessageBox.critical(self, '错误', '选择命令为空')
                return
            command = command[0]
            selected_label = command.text()
            selected_command = command.data(Qt.UserRole)
            confirm = QMessageBox.question(self, '确认', f'是否确认发送 {selected_label} 命令？', QMessageBox.Yes | QMessageBox.No)
            if confirm != QMessageBox.Yes:
                return
            self.class_broadcast_object.send_command(targets, selected_command)
            QMessageBox.information(self, '提示', '发送成功')

    def toggle_remote_spy(self, working):
        if working:
            targets = self.get_all_selected_clients(ip_only=True)
            if not targets:
                self.ui.remote_spy.setChecked(False)
                return
            if len(targets) > 1:
                QMessageBox.warning(self, '提示', '仅支持同时控制一台计算机')
                self.ui.remote_spy.setChecked(False)
                return
            self.class_broadcast_object.remote_spy_start_notify(targets[0])
            self.remote_spy_window.show()
        else:
            self.remote_spy_thread.safe_stop()
            self.remote_spy_window.hide()
            self.ui.remote_spy.setChecked(False)

    def toggle_broadcast(self, working):
        if working:
            if platform.system().lower() not in ('windows', 'darwin'):
                QMessageBox.critical(self, '提示', '屏幕广播当前仅支持 Windows MacOS 系统')
                self.ui.toggle_broadcast.setChecked(False)
                return
            self.screen_broadcast_thread.start()
            self.class_broadcast_object.screen_broadcast_nodity(True)
        else:
            self.screen_broadcast_thread.safe_stop()
            self.class_broadcast_object.screen_broadcast_nodity(False)

    def closeEvent(self, event):
        self.toggle_broadcast(False)
        self.remote_spy_thread.safe_stop()
        self.class_broadcast_object.console_quit_notify()
        event.accept()
