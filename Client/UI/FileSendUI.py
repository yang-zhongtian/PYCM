# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FileSendUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FileSendForm(object):
    def setupUi(self, FileSendForm):
        FileSendForm.setObjectName("FileSendForm")
        FileSendForm.resize(619, 436)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/logo/UI/Resources/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FileSendForm.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(FileSendForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_file_button = QtWidgets.QPushButton(FileSendForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_file_button.sizePolicy().hasHeightForWidth())
        self.add_file_button.setSizePolicy(sizePolicy)
        self.add_file_button.setObjectName("add_file_button")
        self.horizontalLayout.addWidget(self.add_file_button)
        self.add_folder_button = QtWidgets.QPushButton(FileSendForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_folder_button.sizePolicy().hasHeightForWidth())
        self.add_folder_button.setSizePolicy(sizePolicy)
        self.add_folder_button.setObjectName("add_folder_button")
        self.horizontalLayout.addWidget(self.add_folder_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.widget = QtWidgets.QWidget(FileSendForm)
        self.widget.setObjectName("widget")
        self.file_list_container = QtWidgets.QVBoxLayout(self.widget)
        self.file_list_container.setContentsMargins(0, 0, 0, 0)
        self.file_list_container.setObjectName("file_list_container")
        self.file_list = QtWidgets.QTableWidget(self.widget)
        self.file_list.setAcceptDrops(True)
        self.file_list.setObjectName("file_list")
        self.file_list.setColumnCount(0)
        self.file_list.setRowCount(0)
        self.file_list_container.addWidget(self.file_list)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(FileSendForm)
        QtCore.QMetaObject.connectSlotsByName(FileSendForm)

    def retranslateUi(self, FileSendForm):
        _translate = QtCore.QCoreApplication.translate
        FileSendForm.setWindowTitle(_translate("FileSendForm", "发送文件"))
        self.add_file_button.setText(_translate("FileSendForm", "添加文件"))
        self.add_folder_button.setText(_translate("FileSendForm", "添加目录"))
import Resources_rc
