# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoginUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoginForm(object):
    def setupUi(self, LoginForm):
        LoginForm.setObjectName("LoginForm")
        LoginForm.setWindowModality(QtCore.Qt.ApplicationModal)
        LoginForm.resize(341, 232)
        LoginForm.setMinimumSize(QtCore.QSize(341, 232))
        LoginForm.setMaximumSize(QtCore.QSize(341, 232))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Core/Resources/Logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        LoginForm.setWindowIcon(icon)
        self.username = QtWidgets.QLineEdit(LoginForm)
        self.username.setGeometry(QtCore.QRect(133, 70, 181, 31))
        self.username.setObjectName("username")
        self.password = QtWidgets.QLineEdit(LoginForm)
        self.password.setGeometry(QtCore.QRect(133, 120, 181, 31))
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.title = QtWidgets.QLabel(LoginForm)
        self.title.setGeometry(QtCore.QRect(30, 20, 291, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setWordWrap(False)
        self.title.setObjectName("title")
        self.label_username = QtWidgets.QLabel(LoginForm)
        self.label_username.setGeometry(QtCore.QRect(30, 70, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_username.setFont(font)
        self.label_username.setObjectName("label_username")
        self.label_password = QtWidgets.QLabel(LoginForm)
        self.label_password.setGeometry(QtCore.QRect(30, 120, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_password.setFont(font)
        self.label_password.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_password.setObjectName("label_password")
        self.login_button = QtWidgets.QPushButton(LoginForm)
        self.login_button.setGeometry(QtCore.QRect(30, 170, 284, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.login_button.setFont(font)
        self.login_button.setObjectName("login_button")

        self.retranslateUi(LoginForm)
        self.login_button.clicked.connect(LoginForm.login)
        QtCore.QMetaObject.connectSlotsByName(LoginForm)

    def retranslateUi(self, LoginForm):
        _translate = QtCore.QCoreApplication.translate
        LoginForm.setWindowTitle(_translate("LoginForm", "PYCM Login"))
        self.username.setPlaceholderText(_translate("LoginForm", "Default: admin"))
        self.password.setPlaceholderText(_translate("LoginForm", "Default: 123456"))
        self.title.setText(_translate("LoginForm", "PYCM Login"))
        self.label_username.setText(_translate("LoginForm", "Username:"))
        self.label_password.setText(_translate("LoginForm", "Password:"))
        self.login_button.setText(_translate("LoginForm", "Login"))
        self.login_button.setShortcut(_translate("LoginForm", "Return"))
import Resources_rc
