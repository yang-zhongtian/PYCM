from PyQt5.QtWidgets import QDialog
from .SendMessageGroupUI import Ui_SendMessageGroupDialog


class SendMessageGroupForm(QDialog):
    def __init__(self, parent=None):
        super(SendMessageGroupForm, self).__init__(parent)
        self.ui = Ui_SendMessageGroupDialog()
        self.ui.setupUi(self)
