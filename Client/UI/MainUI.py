# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(322, 95)
        MainForm.setMinimumSize(QtCore.QSize(322, 95))
        MainForm.setMaximumSize(QtCore.QSize(397, 95))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/logo/UI/Resources/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainForm.setWindowIcon(icon)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(MainForm)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.title_label = QtWidgets.QLabel(MainForm)
        font = QtGui.QFont()
        font.setFamily("Roboto Medium")
        font.setPointSize(11)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("background-color: rgb(0, 0, 255);\n"
"color: rgb(255, 255, 255);")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.verticalLayout_2.addWidget(self.title_label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.status_label = QtWidgets.QLabel(MainForm)
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(9)
        self.status_label.setFont(font)
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setObjectName("status_label")
        self.horizontalLayout.addWidget(self.status_label)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.notify_button = QtWidgets.QPushButton(MainForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.notify_button.sizePolicy().hasHeightForWidth())
        self.notify_button.setSizePolicy(sizePolicy)
        self.notify_button.setObjectName("notify_button")
        self.horizontalLayout_2.addWidget(self.notify_button)
        self.send_file_button = QtWidgets.QPushButton(MainForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.send_file_button.sizePolicy().hasHeightForWidth())
        self.send_file_button.setSizePolicy(sizePolicy)
        self.send_file_button.setObjectName("send_file_button")
        self.horizontalLayout_2.addWidget(self.send_file_button)
        self.private_message_button = QtWidgets.QPushButton(MainForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.private_message_button.sizePolicy().hasHeightForWidth())
        self.private_message_button.setSizePolicy(sizePolicy)
        self.private_message_button.setObjectName("private_message_button")
        self.horizontalLayout_2.addWidget(self.private_message_button)
        self.hide_button = QtWidgets.QPushButton(MainForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hide_button.sizePolicy().hasHeightForWidth())
        self.hide_button.setSizePolicy(sizePolicy)
        self.hide_button.setObjectName("hide_button")
        self.horizontalLayout_2.addWidget(self.hide_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 4)

        self.retranslateUi(MainForm)
        self.hide_button.clicked.connect(MainForm.hide)
        self.send_file_button.clicked.connect(MainForm.show_file_send_window)
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "客户端"))
        self.title_label.setText(_translate("MainForm", "PYCM Client"))
        self.status_label.setText(_translate("MainForm", "服务端未连接"))
        self.notify_button.setText(_translate("MainForm", "举手"))
        self.send_file_button.setText(_translate("MainForm", "发送文件"))
        self.private_message_button.setText(_translate("MainForm", "私信"))
        self.hide_button.setText(_translate("MainForm", "隐藏"))
import Resources_rc
