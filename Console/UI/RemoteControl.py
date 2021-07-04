from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from Module.QtKeyMap import Qt2Code
from .RemoteControlUI import Ui_RemoteControl


class RemoteControlForm(QWidget):
    parent = None

    def __init__(self, parent=None):
        super(RemoteControlForm, self).__init__()
        self.parent = parent
        self.frame_proportion = 9 / 16
        self.ui = Ui_RemoteControl()
        self.ui.setupUi(self)
        self.ui.screen_display.move(0, 0)
        self.setMouseTracking(True)

    def update_frame(self, frame):
        screen_display_object = self.ui.screen_display
        screen_display_object.setPixmap(frame)

    @staticmethod
    def mouse_click_handler(button):
        if button == Qt.LeftButton:
            return 0  # 左键
        elif button == Qt.RightButton:
            return 1  # 右键
        elif button == Qt.MiddleButton:
            return 2  # 中键
        return None

    def paintEvent(self, event):
        container_size = self.size()
        container_height = container_size.height()
        container_width = container_size.width()
        container_proportion = container_height / container_width
        screen_height = container_height
        screen_width = container_width
        if container_proportion > self.frame_proportion:
            container_height = int(screen_width * self.frame_proportion)
        elif container_proportion < self.frame_proportion:
            container_width = int(screen_height / self.frame_proportion)
        self.ui.screen_display.resize(container_width, container_height)
        self.resize(container_width, container_height)

    def mouseMoveEvent(self, event):
        pixmap = self.ui.screen_display.pixmap()
        if not pixmap:
            return
        rate = (pixmap.width() / self.width() + pixmap.height() / self.height()) / 2
        x = int(event.x() * rate)
        y = int(event.y() * rate)
        self.parent.remote_control_thread.add_command(0, 0, x, y)

    def mousePressEvent(self, event):
        button = self.mouse_click_handler(event.button())
        if button is not None:
            self.parent.remote_control_thread.add_command(1, button, 0, 0)

    def mouseReleaseEvent(self, event):
        button = self.mouse_click_handler(event.button())
        if button is not None:
            self.parent.remote_control_thread.add_command(1, button, 1, 0)

    def keyPressEvent(self, event):
        key = Qt2Code.get(event.key())
        if key is not None:
            self.parent.remote_control_thread.add_command(2, key, 0, 0)

    def keyReleaseEvent(self, event):
        key = Qt2Code.get(event.key())
        if key is not None:
            self.parent.remote_control_thread.add_command(2, key, 1, 0)

    def wheelEvent(self, event):
        delta = event.angleDelta() / 16
        if delta is not None:
            self.parent.remote_control_thread.add_command(3, 0, delta.x(), delta.y())

    def closeEvent(self, event):
        self.parent.toggle_remote_control(False)
