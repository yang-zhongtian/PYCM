from PyQt5.QtWidgets import QWidget, QApplication
from qt_material import apply_stylesheet
import sys
import os

from LoadConfig import NetworkConfig

from UI.Main import MainForm
from UI.FileSend import FileSendForm

from Threadings import NetworkDiscoverThread
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
        self.private_message_object = PrivateMessage
        self.init_connections()
        self.net_discover_thread.start()

    @staticmethod
    def show_file_send_window():
        file_send_window.show()


class FileSendWindow(FileSendForm):

    def __init__(self):
        super(FileSendWindow, self).__init__(self)

    @staticmethod
    def get_main_window():
        return main_window


main_window = MainWindow()
file_send_window = FileSendWindow()

if __name__ == '__main__':
    main_window.show()
    sys.exit(app.exec_())
