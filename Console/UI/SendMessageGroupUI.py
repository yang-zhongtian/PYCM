# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SendMessageGroupUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SendMessageGroupDialog(object):
    def setupUi(self, SendMessageGroupDialog):
        SendMessageGroupDialog.setObjectName("SendMessageGroupDialog")
        SendMessageGroupDialog.resize(395, 282)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SendMessageGroupDialog.sizePolicy().hasHeightForWidth())
        SendMessageGroupDialog.setSizePolicy(sizePolicy)
        SendMessageGroupDialog.setMinimumSize(QtCore.QSize(0, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Core/Resources/Logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SendMessageGroupDialog.setWindowIcon(icon)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(SendMessageGroupDialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.send_message_group = QtWidgets.QGroupBox(SendMessageGroupDialog)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.send_message_group.setFont(font)
        self.send_message_group.setObjectName("send_message_group")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.send_message_group)
        self.horizontalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.send_message_input = QtWidgets.QPlainTextEdit(self.send_message_group)
        self.send_message_input.setObjectName("send_message_input")
        self.horizontalLayout_2.addWidget(self.send_message_input)
        self.verticalLayout_3.addWidget(self.send_message_group)
        self.buttonBox = QtWidgets.QDialogButtonBox(SendMessageGroupDialog)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)
        self.verticalLayout_3.setStretch(0, 3)

        self.retranslateUi(SendMessageGroupDialog)
        self.buttonBox.accepted.connect(SendMessageGroupDialog.accept)
        self.buttonBox.rejected.connect(SendMessageGroupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SendMessageGroupDialog)

    def retranslateUi(self, SendMessageGroupDialog):
        _translate = QtCore.QCoreApplication.translate
        SendMessageGroupDialog.setWindowTitle(_translate("SendMessageGroupDialog", "消息发送"))
        self.send_message_group.setTitle(_translate("SendMessageGroupDialog", "消息编辑"))
import Resources_rc
