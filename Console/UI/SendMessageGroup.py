from PyQt5.QtWidgets import QDialog, QListWidgetItem
from PyQt5.QtCore import Qt
from .SendMessageGroupUI import Ui_SendMessageGroupDialog


class SendMessageGroupForm(QDialog):
    def __init__(self, parent=None):
        super(SendMessageGroupForm, self).__init__(parent)
        self.ui = Ui_SendMessageGroupDialog()
        self.parent = parent
        self.ui.setupUi(self)
