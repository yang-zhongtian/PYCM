from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5.QtCore import QCoreApplication
import os
import hashlib
from .LoginUI import Ui_LoginForm


def encode_password(password):
    return hashlib.md5(str(password).encode()).hexdigest()


class LoginForm(QDialog):
    _translate = QCoreApplication.translate

    def __init__(self, parent=None):
        super(LoginForm, self).__init__(parent)
        self.ui = Ui_LoginForm()
        self.parent = parent
        self.ui.setupUi(self)

    def login(self):
        real_admin_username = self.parent.config.get_item('Login/Username')
        real_admin_password = self.parent.config.get_item('Login/Password')
        username = self.ui.username.text()
        password = self.ui.password.text()
        if not all([username, password]):
            QMessageBox.critical(self, self._translate('LoginForm', 'Warning'),
                                 self._translate('LoginForm', "Username and password can't be blank"))
            return
        if self.ui.username.text() == real_admin_username:
            if encode_password(self.ui.password.text()) == real_admin_password:
                self.accept()
                self.close()
            else:
                QMessageBox.critical(self, self._translate('LoginForm', 'Warning'),
                                     self._translate('LoginForm', 'Password incorrect'))
        else:
            QMessageBox.critical(self, self._translate('LoginForm', 'Warning'),
                                 self._translate('LoginForm', 'Username incorrect'))
