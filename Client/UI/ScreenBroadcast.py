from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
import pathlib
from .ScreenBroadcastUI import Ui_ScreenBroadcast


class ScreenBroadcastForm(QWidget):
    parent = None
    freeze = False
    screen_shot_idx = 1

    def __init__(self, parent=None):
        super(ScreenBroadcastForm, self).__init__()
        self.parent = parent
        self.ui = Ui_ScreenBroadcast()
        self.ui.setupUi(self)
        self.ui.screen_display.move(0, 0)
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint)

    def update_frame(self, frame):
        if not self.freeze:
            screen_display_object = self.ui.screen_display
            screen_display_object.setPixmap(frame)

    def freeze_frame(self, freeze=True):
        self.freeze = freeze

    def show_full_screen(self, fullscreen=True):
        self.showFullScreen() if fullscreen else self.showNormal()

    def screen_shot(self):
        frame = self.ui.screen_display.pixmap()
        frame = frame.toImage()
        desktop_path = pathlib.Path.home() / 'Desktop' / f'屏幕广播截图{self.screen_shot_idx}.jpg'
        self.screen_shot_idx += 1
        frame.save(str(desktop_path), 'JPEG')

    def paintEvent(self, event):
        self.ui.screen_display.resize(self.ui.screen_widget.size())

    def closeEvent(self, event):
        event.ignore()
