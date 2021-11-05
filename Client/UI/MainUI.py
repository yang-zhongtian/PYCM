# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(322, 70)
        MainForm.setMinimumSize(QtCore.QSize(322, 70))
        MainForm.setMaximumSize(QtCore.QSize(397, 75))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Core/Resources/Logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainForm.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(MainForm)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Container = QtWidgets.QWidget(MainForm)
        self.Container.setStyleSheet("#Container{\n"
"    background-color: rgb(255, 255, 255);\n"
"}")
        self.Container.setObjectName("Container")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.Container)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.title_label = QtWidgets.QLabel(self.Container)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(82, 229, 231, 255), stop:1 rgba(19, 12, 183, 255));\n"
"color: rgb(255, 255, 255);")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.verticalLayout_2.addWidget(self.title_label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(5, 3, 5, 5)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.notify_button = QtWidgets.QPushButton(self.Container)
        self.notify_button.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.notify_button.sizePolicy().hasHeightForWidth())
        self.notify_button.setSizePolicy(sizePolicy)
        self.notify_button.setObjectName("notify_button")
        self.horizontalLayout.addWidget(self.notify_button)
        self.file_button = QtWidgets.QPushButton(self.Container)
        self.file_button.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_button.sizePolicy().hasHeightForWidth())
        self.file_button.setSizePolicy(sizePolicy)
        self.file_button.setObjectName("file_button")
        self.horizontalLayout.addWidget(self.file_button)
        self.private_message_button = QtWidgets.QPushButton(self.Container)
        self.private_message_button.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.private_message_button.sizePolicy().hasHeightForWidth())
        self.private_message_button.setSizePolicy(sizePolicy)
        self.private_message_button.setObjectName("private_message_button")
        self.horizontalLayout.addWidget(self.private_message_button)
        self.hide_button = QtWidgets.QPushButton(self.Container)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hide_button.sizePolicy().hasHeightForWidth())
        self.hide_button.setSizePolicy(sizePolicy)
        self.hide_button.setObjectName("hide_button")
        self.horizontalLayout.addWidget(self.hide_button)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.Container)
        self.action_send_file = QtWidgets.QAction(MainForm)
        self.action_send_file.setObjectName("action_send_file")
        self.action_file_client = QtWidgets.QAction(MainForm)
        self.action_file_client.setObjectName("action_file_client")

        self.retranslateUi(MainForm)
        self.notify_button.clicked.connect(MainForm.notify_console)
        self.hide_button.clicked.connect(MainForm.hide)
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "Client"))
        self.title_label.setText(_translate("MainForm", "PYCM Client - Offline"))
        self.notify_button.setText(_translate("MainForm", "Hands Up"))
        self.file_button.setText(_translate("MainForm", "File"))
        self.private_message_button.setText(_translate("MainForm", "Messaging"))
        self.hide_button.setText(_translate("MainForm", "Hide"))
        self.action_send_file.setText(_translate("MainForm", "Send File"))
        self.action_file_client.setText(_translate("MainForm", "File Client"))
import Resources_rc
