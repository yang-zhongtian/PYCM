from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
import ujson
import os
import hashlib
from .LoginUI import Ui_LoginForm


def encode_password(password):
    return hashlib.md5(str(password).encode()).hexdigest()


class LoginForm(QWidget):
    def __init__(self, parent=None):
        super(LoginForm, self).__init__(parent)
        self.ui = Ui_LoginForm()
        self.ui.setupUi(self)

    def login(self):
        real_admin_user = ujson.loads(open(os.path.join(self.base_dir, 'Admin.json'), 'r', encoding='utf8').read())
        username = self.ui.username.text()
        password = self.ui.password.text()
        if not all([username, password]):
            QMessageBox.critical(self, '提示', '用户名或密码不能为空')
            return
        if self.ui.username.text() == real_admin_user['username']:
            if encode_password(self.ui.password.text()) == real_admin_user['password']:
                self.show_dashboard_window()
            else:
                QMessageBox.critical(self, '提示', '密码错误')
        else:
            QMessageBox.critical(self, '提示', '用户名错误')
