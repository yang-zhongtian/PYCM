# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NetworkDeviceSelectUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NetworkDeviceSelectDialog(object):
    def setupUi(self, NetworkDeviceSelectDialog):
        NetworkDeviceSelectDialog.setObjectName("NetworkDeviceSelectDialog")
        NetworkDeviceSelectDialog.resize(413, 120)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Core/Resources/Logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        NetworkDeviceSelectDialog.setWindowIcon(icon)
        self.buttonBox = QtWidgets.QDialogButtonBox(NetworkDeviceSelectDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 70, 391, 41))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.network_device_list = QtWidgets.QComboBox(NetworkDeviceSelectDialog)
        self.network_device_list.setGeometry(QtCore.QRect(20, 20, 371, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.network_device_list.setFont(font)
        self.network_device_list.setObjectName("network_device_list")

        self.retranslateUi(NetworkDeviceSelectDialog)
        self.buttonBox.accepted.connect(NetworkDeviceSelectDialog.accept)
        self.buttonBox.rejected.connect(NetworkDeviceSelectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NetworkDeviceSelectDialog)

    def retranslateUi(self, NetworkDeviceSelectDialog):
        _translate = QtCore.QCoreApplication.translate
        NetworkDeviceSelectDialog.setWindowTitle(_translate("NetworkDeviceSelectDialog", "Network Settings"))
import Resources_rc
