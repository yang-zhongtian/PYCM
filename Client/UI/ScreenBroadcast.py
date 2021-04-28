from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from .ScreenBroadcastUI import Ui_ScreenBroadcast


class ScreenBroadcastForm(QWidget):
    parent = None
    freeze = False

    def __init__(self, parent=None):
        super(ScreenBroadcastForm, self).__init__()
        self.parent = parent
        self.ui = Ui_ScreenBroadcast()
        self.ui.setupUi(self)
        self.ui.screen_display.move(0, 0)
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint)
        self.window_title = self.windowTitle()

    def update_frame(self, frame):
        if not self.freeze:
            screen_display_object = self.ui.screen_display
            screen_display_object.setPixmap(frame)

    def freeze_frame(self, freeze=True):
        self.freeze = freeze

    def show_full_screen(self, fullscreen=True):
        self.showFullScreen() if fullscreen else self.showNormal()

    def update_fps(self, fps):
        self.setWindowTitle(f'{self.window_title} fps: {fps}')

    def paintEvent(self, event):
        self.ui.screen_display.resize(self.ui.screen_widget.size())

    def closeEvent(self, event):
        event.ignore()
