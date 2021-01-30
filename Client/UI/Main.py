from PyQt5.QtWidgets import QWidget, QSystemTrayIcon, QAction, QMenu, QMessageBox
from PyQt5.QtCore import Qt, QPoint, QCoreApplication, QTimer
from PyQt5.QtGui import QMouseEvent, QIcon
from .MainUI import Ui_MainForm


# noinspection PyAttributeOutsideInit
class MainForm(QWidget):
    server_ip = None
    screen_spy_timer = QTimer()
    _start_pos = None
    _end_pos = None
    _is_tracking = False

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(322, 95)
        self.init_tray()

    def init_connections(self):
        self.net_discover_thread.server_info.connect(self.server_found)
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

    def server_found(self, server_ip, config):
        self.server_ip = server_ip
        self.private_message_object = self.private_message_object(config.get('Local').get('IP'), server_ip,
                                                                  config.get('PrivateMessage').get('Port'),
                                                                  config.get('PrivateMessage').get('Buffer'))
        self.private_message_object.online_notify()
        self.ui.status_label.setText('服务端已连接')
        self.screen_spy_timer.start(3000)

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
            event.accept()
        else:
            event.ignore()
            self.hide()
