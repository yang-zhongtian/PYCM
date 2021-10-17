# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RemoteCommandGroupUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RemoteCommandGroupDialog(object):
    def setupUi(self, RemoteCommandGroupDialog):
        RemoteCommandGroupDialog.setObjectName("RemoteCommandGroupDialog")
        RemoteCommandGroupDialog.resize(398, 294)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RemoteCommandGroupDialog.sizePolicy().hasHeightForWidth())
        RemoteCommandGroupDialog.setSizePolicy(sizePolicy)
        RemoteCommandGroupDialog.setMinimumSize(QtCore.QSize(0, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Core/Resources/Logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        RemoteCommandGroupDialog.setWindowIcon(icon)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(RemoteCommandGroupDialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.command_group = QtWidgets.QGroupBox(RemoteCommandGroupDialog)
        self.command_group.setObjectName("command_group")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.command_group)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.command_select = QtWidgets.QListWidget(self.command_group)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.command_select.setFont(font)
        self.command_select.setObjectName("command_select")
        self.horizontalLayout_2.addWidget(self.command_select)
        self.verticalLayout_3.addWidget(self.command_group)
        self.buttonBox = QtWidgets.QDialogButtonBox(RemoteCommandGroupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)
        self.verticalLayout_3.setStretch(0, 5)

        self.retranslateUi(RemoteCommandGroupDialog)
        self.buttonBox.accepted.connect(RemoteCommandGroupDialog.accept)
        self.buttonBox.rejected.connect(RemoteCommandGroupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RemoteCommandGroupDialog)

    def retranslateUi(self, RemoteCommandGroupDialog):
        _translate = QtCore.QCoreApplication.translate
        RemoteCommandGroupDialog.setWindowTitle(_translate("RemoteCommandGroupDialog", "Remote Command"))
        self.command_group.setTitle(_translate("RemoteCommandGroupDialog", "Command Select"))
import Resources_rc
