import os.path

from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QDialog, QListWidgetItem, QLabel, QMessageBox, \
    QInputDialog, QLineEdit, QSystemTrayIcon, QAction, QMenu
from PyQt5.QtCore import Qt, QSize, QEvent, QUrl
from PyQt5.QtGui import QIcon
import time
from functools import partial
from .DashboardUI import Ui_DashboardForm
from .SendMessageGroup import SendMessageGroupForm
from .RemoteCommandGroup import RemoteCommandGroupForm
from .RemoteSpy import RemoteSpyForm
from .FileReceive import FileReceiveForm
from .About import AboutDialog


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
        self.tray_icon_menu = QMenu(self)
        self.tray_icon = QSystemTrayIcon(self)
        self.remote_spy_window = RemoteSpyForm(self)
        self.file_receive_window = FileReceiveForm(self)

    def init_connections(self):
        self.private_message_thread.client_login_logout.connect(self.__logger)
        self.private_message_thread.client_notify_recieved.connect(partial(self.__logger, 'client_notify'))
        self.private_message_thread.client_desktop_recieved.connect(self.__update_client_desktop)
        self.private_message_thread.client_file_recieved.connect(partial(self.__logger, 'file_recieved'))
        self.remote_spy_thread.frame_recieved.connect(self.remote_spy_window.update_frame)

    def init_network_device(self, device):
        self.config.save('Network/Local/IP', device['IP'])
        self.config.save('Network/Local/MAC', device['MAC'])

    # noinspection PyArgumentList
    def init_tray(self):
        self.tray_icon_menu.addAction(QAction('Show Dashboard', self, triggered=lambda: self.show_window()))
        self.tray_icon_menu.addAction(QAction('About', self, triggered=lambda: self.show_about()))
        self.tray_icon_menu.addAction(QAction('Exit', self, triggered=self.close))
        self.tray_icon.setIcon(QIcon(':/Core/Resources/Logo.png'))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.activated[QSystemTrayIcon.ActivationReason].connect(lambda x: self.show_window(x))
        self.__update_tray_tooltip()
        self.tray_icon.show()

    def __mark_status(self, name, status):
        self.threadings[name] = status

    def __logger(self, type_, ip, mac=None):
        if type_ == 'online':
            self.mac_binding[ip] = mac
            self.__log_append(f'{self.get_client_label_by_ip(ip)} logged on')
            self.__add_client_desktop(ip)
            self.__update_tray_tooltip()
        elif type_ == 'offline':
            self.__log_append(f'{self.get_client_label_by_ip(ip)} logged off')
            self.__remove_client_desktop(ip)
            self.__update_tray_tooltip()
        elif type_ == 'file_recieved':
            client = self.get_client_label_by_ip(ip)
            self.__log_append(f'File received: {client}, <a href="{mac}">Detail</a>')
            self.file_receive_window.add_received_file(mac, client)
            self.class_broadcast_object.client_file_recieved_notify(ip)
        elif type_ == 'client_notify':
            self.__log_append(f'Hands up: {self.get_client_label_by_ip(ip)}')

    def __log_append(self, message):
        self.ui.log_area.append(f'[{time.strftime("%H:%M", time.localtime(time.time()))}] <b>{message}</b>')

    def __add_client_desktop(self, client_ip):
        if client_ip in self.clients.keys():
            return
        desktop = QListWidgetItem(self.get_client_label_by_ip(client_ip))
        desktop.setIcon(QIcon(':/Core/Resources/ClientBlank.png'))
        desktop.setTextAlignment(Qt.AlignHCenter)
        desktop.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
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

    def __update_tray_tooltip(self):
        local_ip = self.config.get_item('Network/Local/IP')
        self.tray_icon.setToolTip('PYCM Console\n' +
                                  f'Local IP: {local_ip}\n' +
                                  f'Online: {len(self.clients)} Clients')

    def client_rename(self):
        target = self.get_all_selected_clients()
        if not target:
            return
        if len(target) > 1:
            QMessageBox.warning(self, 'Warning', 'Only support to rename one client each time')
            return
        target = target[0]
        client = self.clients[target['ip']]
        new_label, confirm = QInputDialog.getText(self, 'Rename client',
                                                  'Please input the new name, leave blank for restoring to default',
                                                  QLineEdit.Normal, target['label'])
        if confirm:
            if new_label != target['label']:
                if new_label == '':
                    self.config.remove(f'Client/ClientLabel/{target["mac"]}')
                else:
                    self.config.save(f'Client/ClientLabel/{target["mac"]}', new_label)
                client.setText(self.get_client_label_by_ip(target['ip']))

    def client_quit(self):
        targets = self.get_all_selected_clients()
        if not targets:
            return
        selected_label = [client['label'] for client in targets]
        confirm = QMessageBox.warning(self, 'Confirm',
                                      f'Are you sure to quit these clients: {" ".join(selected_label)}?\n' +
                                      'This action is irreversible!', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm != QMessageBox.Yes:
            return
        targets = [client['ip'] for client in targets]
        self.class_broadcast_object.remote_quit_notify(targets)
        QMessageBox.information(self, 'Info', 'Quit client command send successfully')

    def get_client_label_by_ip(self, ip):
        label = self.config.get_item(f'Client/ClientLabel/{self.mac_binding.get(ip)}')
        if not label:
            return ip
        return label

    def get_all_selected_clients(self, ip_only=False):
        clients = self.ui.desktop_layout.selectedItems()
        if len(clients) == 0:
            QMessageBox.warning(self, 'Warning', 'No targets selected')
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
        if result == send_message_group_dialog.Accepted:
            message = send_message_group_dialog.ui.send_message_input.toPlainText()
            self.class_broadcast_object.send_text(targets, message)
            self.__log_append(f'Message send: {message}')

    def remote_command(self):
        targets = self.get_all_selected_clients(ip_only=True)
        if not targets:
            return
        remote_command_group_dialog = RemoteCommandGroupForm(self)
        result = remote_command_group_dialog.exec_()
        if result == remote_command_group_dialog.Accepted:
            command = remote_command_group_dialog.ui.command_select.selectedItems()
            if len(command) == 0:
                QMessageBox.critical(self, 'Warning', 'No command selected')
                return
            command = command[0]
            selected_label = command.text()
            selected_command = command.data(Qt.UserRole)
            confirm = QMessageBox.question(self, 'Confirm', f'Confirm to send command: {selected_label} ?',
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm != QMessageBox.Yes:
                return
            self.class_broadcast_object.send_command(targets, selected_command)
            QMessageBox.information(self, 'Info', 'Command send successfully')

    def toggle_remote_spy(self, working):
        if working:
            targets = self.get_all_selected_clients(ip_only=True)
            if not targets:
                self.ui.remote_spy.setChecked(False)
                return
            if len(targets) > 1:
                QMessageBox.warning(self, 'Warning', 'Only support to control one client each time')
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
            self.screen_broadcast_thread.start()
            self.class_broadcast_object.screen_broadcast_nodity(True)
        else:
            self.screen_broadcast_thread.safe_stop()
            self.class_broadcast_object.screen_broadcast_nodity(False)

    def show_file_receive(self, file_url: QUrl = None):
        if file_url is not None and type(file_url) != bool:
            item = self.file_receive_window.ui.received_files.findItems(file_url.url(), Qt.MatchExactly)
            if len(item) > 0:
                item_row = item[0].row()
                self.file_receive_window.ui.received_files.selectRow(item_row)
        self.file_receive_window.activateWindow()
        self.file_receive_window.showNormal()

    def show_about(self):
        AboutDialog(self).exec_()

    def show_window(self, reason=None):
        if reason is not None and reason != QSystemTrayIcon.Trigger:
            return
        self.activateWindow()
        self.showNormal()

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() == Qt.WindowMinimized:
                event.ignore()
                self.hide()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Warning', 'Are you sure to exit?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply != QMessageBox.Yes:
            event.ignore()
            return
        self.toggle_broadcast(False)
        self.remote_spy_thread.safe_stop()
        self.class_broadcast_object.console_quit_notify()
        if self.tray_icon.isVisible():
            self.tray_icon.hide()
        self.tray_icon = None
        QApplication.instance().quit()
