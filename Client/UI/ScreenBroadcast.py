from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from .ScreenBroadcastUI import Ui_ScreenBroadcast


class ScreenBroadcastForm(QWidget):
    parent = None

    def __init__(self, parent=None):
        super(ScreenBroadcastForm, self).__init__()
        self.parent = parent
        self.ui = Ui_ScreenBroadcast()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint)
        self.window_title = self.windowTitle()

    def update_frame(self, frame):
        screen_display_object = self.ui.screen_display
        frame = frame.scaled(screen_display_object.width(), screen_display_object.height(), Qt.KeepAspectRatio,
                             Qt.SmoothTransformation)
        self.ui.screen_display.setPixmap(frame)

    def update_fps(self, fps):
        self.setWindowTitle(f'{self.window_title} fps: {fps}')

    def resizeEvent(self, event):
        frame = self.ui.screen_display.pixmap()
        if frame:
            frame = frame.scaled(self.ui.screen_display.width(), self.ui.screen_display.height(), Qt.KeepAspectRatio,
                                 Qt.SmoothTransformation)
            self.ui.screen_display.setPixmap(frame)

        def closeEvent(self, event):
            event.ignore()
