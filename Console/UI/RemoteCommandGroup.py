from PyQt5.QtWidgets import QDialog, QListWidgetItem
from PyQt5.QtCore import Qt
from .RemoteCommandGroupUI import Ui_RemoteCommandGroupDialog


class RemoteCommandGroupForm(QDialog):
    def __init__(self, parent=None):
        super(RemoteCommandGroupForm, self).__init__(parent)
        self.ui = Ui_RemoteCommandGroupDialog()
        self.parent = parent
        self.available_commands = parent.config.get_all('Client/AvailableRemoteCommands')
        self.ui.setupUi(self)
        self.init()

    def init(self):
        for label, command in self.available_commands.items():
            new_item = QListWidgetItem(label)
            new_item.setData(Qt.UserRole, command)
            self.ui.command_select.addItem(new_item)
