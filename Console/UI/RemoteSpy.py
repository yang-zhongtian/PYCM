from PyQt5.QtWidgets import QWidget
from .RemoteSpyUI import Ui_RemoteSpy


class RemoteSpyForm(QWidget):
    parent = None

    def __init__(self, parent=None):
        super(RemoteSpyForm, self).__init__()
        self.parent = parent
        self.frame_proportion = 9 / 16
        self.ui = Ui_RemoteSpy()
        self.ui.setupUi(self)
        self.ui.screen_display.move(0, 0)

    def update_frame(self, frame):
        screen_display_object = self.ui.screen_display
        screen_display_object.setPixmap(frame)

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

    def closeEvent(self, event):
        self.parent.toggle_remote_spy(False)
