from PyQt5.QtWidgets import QWidget, QSystemTrayIcon, QAction, QMenu, QMessageBox, QApplication
from PyQt5.QtCore import Qt, QPoint, QTimer, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QIcon
import psutil
import socket
from .MainUI import Ui_MainForm
from .FileSend import FileSendForm
from .ScreenBroadcast import ScreenBroadcastForm


# noinspection PyAttributeOutsideInit
class MainForm(QWidget):
    server_ip = None
    screen_spy_timer = QTimer()
    _start_pos = None
    _end_pos = None
    _is_tracking = False

    def __init__(self, parent=None):
        super(MainForm, self).__init__()
        self.ui = Ui_MainForm()
        self.parent = parent
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setFixedSize(322, 70)
        desktop = QApplication.desktop()
        self.move(int(desktop.width() - 422), 65)
        self.file_send_window = FileSendForm(parent)
        self.screen_broadcast_window = ScreenBroadcastForm(parent)
        self.init_tray()

    def load_network_device(self):
        network_devices = psutil.net_if_addrs()
        devices = {}
        for device in network_devices.keys():
            af_inet4 = []
            af_link = []
            for item in network_devices[device]:
                if item.family == socket.AF_INET:
                    af_inet4.append(item.address)
                elif item.family == psutil.AF_LINK:
                    af_link.append(item.address)
            if len(af_inet4) == 1 and len(af_link) == 1:
                devices[device] = {'IP': af_inet4[0], 'MAC': af_link[0]}
        return devices.get(self.parent.config.get('Local').get('Device'))

    def init_connections(self):
        self.net_discover_thread.server_info.connect(self.server_found)
        self.class_broadcast_thread.message_recieved.connect(self.message_recieved)
        self.class_broadcast_thread.reset_all.connect(lambda: self.reset_all_threadings())
        self.class_broadcast_thread.toggle_screen_broadcats.connect(self.__toggle_screen_broadcast)
        self.screen_broadcast_thread.frame_recieved.connect(self.screen_broadcast_window.update_frame)
        self.screen_spy_timer.timeout.connect(lambda: self.private_message_object.screen_spy_send())

    def init_tray(self):
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(QAction('显示工具栏', self, triggered=self.show))
        self.tray_icon_menu.addAction(QAction('退出程序', self, triggered=self.close))
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(':/logo/UI/Resources/logo.png'))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.activated[QSystemTrayIcon.ActivationReason].connect(self.iconActivated)
        self.tray_icon.show()

    def show_file_send_window(self):
        self.file_send_window.show()

    def message_recieved(self, type_, message):
        icon = QSystemTrayIcon.MessageIcon()
        if type_ == 'public':
            self.tray_icon.showMessage('广播消息', message, icon, 1000)
        elif type_ == 'private':
            self.tray_icon.showMessage('私人消息', message, icon, 1000)

    def notify_console(self):
        self.private_message_object.notify_console()

    def server_found(self, server_ip, config):
        self.server_ip = server_ip
        local_ip = config.get('Local').get('IP')
        local_mac = config.get('Local').get('MAC')
        private_message_port = config.get('PrivateMessage').get('Port')
        private_message_buffer = config.get('PrivateMessage').get('Buffer')
        self.private_message_object = self.private_message_object(local_ip, local_mac, self.server_ip,
                                                                  private_message_port, private_message_buffer)
        self.private_message_object.online_notify()
        self.class_broadcast_thread.start()
        self.ui.title_label.setText('PYCM Client - Online')
        self.ui.notify_button.setEnabled(True)
        self.ui.send_file_button.setEnabled(True)
        self.ui.private_message_button.setEnabled(True)
        self.screen_spy_timer.start(3000)

    def __toggle_screen_broadcast(self, work):
        self.screen_broadcast_thread.socket.working = work
        if work:
            self.screen_broadcast_thread.start()
            self.screen_broadcast_window.show()
        else:
            self.screen_broadcast_thread.quit()
            self.screen_broadcast_window.hide()

    def mouseMoveEvent(self, e: QMouseEvent):
        if self._start_pos and self._is_tracking:
            self._end_pos = e.pos() - self._start_pos
            self.move(self.pos() + self._end_pos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._is_tracking = True
            self._start_pos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._is_tracking = False
            self._start_pos = None
            self._end_pos = None

    def iconActivated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

    def closeEvent(self, event):
        self.show()
        reply = QMessageBox.question(self, '提示', '是否退出？', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.server_ip is not None:
                self.private_message_object.offline_notify()
            if self.tray_icon.isVisible():
                self.tray_icon.hide()
            self.tray_icon = None
            QApplication.instance().quit()
        else:
            event.ignore()
