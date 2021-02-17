from PyQt5.QtWidgets import QWidget, QApplication
from qt_material import apply_stylesheet
import sys
import os

from LoadConfig import NetworkConfig

from UI.Main import MainForm

from Threadings import NetworkDiscoverThread, ClassBroadcastThread, ScreenBroadcastThread
from PrivateMessage import PrivateMessage

base_dir = os.path.dirname(os.path.abspath(__file__))
config = NetworkConfig(base_dir)
app = QApplication(sys.argv)

apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True)


class MainWindow(MainForm):
    base_dir = base_dir

    def __init__(self):
        super(MainWindow, self).__init__(self)
        self.net_discover_thread = NetworkDiscoverThread(config)
        self.class_broadcast_thread = ClassBroadcastThread(config)
        self.screen_broadcast_thread = ScreenBroadcastThread(config)
        self.private_message_object = PrivateMessage
        self.init_connections()
        self.net_discover_thread.start()

    def reset_all_threadings(self):
        self.screen_spy_timer.stop()
        self.class_broadcast_thread.quit()
        self.class_broadcast_thread.wait()
        self.net_discover_thread = NetworkDiscoverThread(config)
        self.class_broadcast_thread = ClassBroadcastThread(config)
        self.private_message_object = PrivateMessage
        self.init_connections()
        self.ui.title_label.setText('PYCM Client - Offline')
        self.ui.notify_button.setEnabled(False)
        self.ui.send_file_button.setEnabled(False)
        self.ui.private_message_button.setEnabled(False)
        self.server_ip = None
        self.net_discover_thread.start()


main_window = MainWindow()

if __name__ == '__main__':
    main_window.show()
    sys.exit(app.exec_())
