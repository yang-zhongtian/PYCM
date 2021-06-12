from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
import platform
from .ScreenBroadcastUI import Ui_ScreenBroadcast
import Module.VLC as VLC


class ScreenBroadcastForm(QWidget):
    parent = None
    freeze = False

    def __init__(self, parent=None):
        super(ScreenBroadcastForm, self).__init__()
        self.parent = parent
        self.socket_ip = parent.config.get('ScreenBroadcast').get('IP')
        self.socket_port = parent.config.get('ScreenBroadcast').get('Port')
        self.socket_buffer = parent.config.get('ScreenBroadcast').get('Buffer')
        self.vlc_instance = VLC.Instance('-q')
        self.vlc_media_player = self.vlc_instance.media_player_new()
        self.vlc_media = None
        self.ui = Ui_ScreenBroadcast()
        self.ui.setupUi(self)
        self.ui.screen_display.move(0, 0)
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint)

    def showEvent(self, event):
        self.vlc_media = self.vlc_instance.media_new(
            f'udp/h264://@{self.socket_ip}:{self.socket_port}?pkt_size={self.socket_buffer}')
        self.vlc_media_player.set_media(self.vlc_media)
        if platform.system() == 'Linux':
            self.vlc_media_player.set_xwindow(int(self.ui.screen_display.winId()))
        elif platform.system() == 'Windows':
            self.vlc_media_player.set_hwnd(int(self.ui.screen_display.winId()))
        elif platform.system() == 'Darwin':
            self.vlc_media_player.set_nsobject(int(self.ui.screen_display.winId()))
        self.vlc_media_player.play()

    def hideEvent(self, event):
        if self.vlc_media_player.is_playing():
            self.vlc_media_player.stop()

    def freeze_frame(self, freeze=True):
        self.freeze = freeze

    def show_full_screen(self, fullscreen=True):
        self.showFullScreen() if fullscreen else self.showNormal()

    def paintEvent(self, event):
        self.ui.screen_display.resize(self.ui.screen_widget.size())

    def closeEvent(self, event):
        event.ignore()
