from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QCoreApplication
from .AboutUI import Ui_AboutDialog

try:
    from BuildInfo import BUILD_INFO
except ImportError:
    BUILD_INFO = None


class AboutDialog(QDialog):
    _translate = QCoreApplication.translate

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.ui = Ui_AboutDialog()
        self.parent = parent
        self.ui.setupUi(self)
        build_info = BUILD_INFO
        if build_info is None:
            build_info = self._translate('AboutDialog', 'No build info')
        self.ui.buildInfo.setText(self._translate('AboutDialog', 'Build Info: %s') % BUILD_INFO)
