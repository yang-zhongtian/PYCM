from PyQt5.QtWidgets import QDialog
from .AboutUI import Ui_AboutDialog
try:
    from BuildInfo import BUILD_INFO
except ImportError:
    BUILD_INFO = 'No build info'


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.ui = Ui_AboutDialog()
        self.parent = parent
        self.ui.setupUi(self)
        self.ui.buildInfo.setText(f'Build Info: {BUILD_INFO}')
