# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FileServerUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FileServerForm(object):
    def setupUi(self, FileServerForm):
        FileServerForm.setObjectName("FileServerForm")
        FileServerForm.resize(522, 133)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FileServerForm.sizePolicy().hasHeightForWidth())
        FileServerForm.setSizePolicy(sizePolicy)
        FileServerForm.setMinimumSize(QtCore.QSize(0, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Core/Resources/Logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FileServerForm.setWindowIcon(icon)
        self.verticalLayout_1 = QtWidgets.QVBoxLayout(FileServerForm)
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.working_folder_label = QtWidgets.QLabel(FileServerForm)
        self.working_folder_label.setObjectName("working_folder_label")
        self.horizontalLayout.addWidget(self.working_folder_label)
        self.working_folder = QtWidgets.QLineEdit(FileServerForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.working_folder.sizePolicy().hasHeightForWidth())
        self.working_folder.setSizePolicy(sizePolicy)
        self.working_folder.setText("")
        self.working_folder.setReadOnly(True)
        self.working_folder.setObjectName("working_folder")
        self.horizontalLayout.addWidget(self.working_folder)
        self.working_folder_change = QtWidgets.QPushButton(FileServerForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.working_folder_change.sizePolicy().hasHeightForWidth())
        self.working_folder_change.setSizePolicy(sizePolicy)
        self.working_folder_change.setObjectName("working_folder_change")
        self.horizontalLayout.addWidget(self.working_folder_change)
        self.verticalLayout_1.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.server_info = QtWidgets.QLabel(FileServerForm)
        self.server_info.setObjectName("server_info")
        self.horizontalLayout_2.addWidget(self.server_info)
        self.toggle_working = QtWidgets.QPushButton(FileServerForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggle_working.sizePolicy().hasHeightForWidth())
        self.toggle_working.setSizePolicy(sizePolicy)
        self.toggle_working.setObjectName("toggle_working")
        self.horizontalLayout_2.addWidget(self.toggle_working)
        self.verticalLayout_1.addLayout(self.horizontalLayout_2)
        self.no_folder_notice = QtWidgets.QLabel(FileServerForm)
        self.no_folder_notice.setAlignment(QtCore.Qt.AlignCenter)
        self.no_folder_notice.setWordWrap(True)
        self.no_folder_notice.setObjectName("no_folder_notice")
        self.verticalLayout_1.addWidget(self.no_folder_notice)

        self.retranslateUi(FileServerForm)
        self.working_folder_change.clicked.connect(FileServerForm.change_working_folder)
        self.toggle_working.clicked.connect(FileServerForm.toggle_server)
        QtCore.QMetaObject.connectSlotsByName(FileServerForm)

    def retranslateUi(self, FileServerForm):
        _translate = QtCore.QCoreApplication.translate
        FileServerForm.setWindowTitle(_translate("FileServerForm", "File Server"))
        self.working_folder_label.setText(_translate("FileServerForm", "Target Folder: "))
        self.working_folder_change.setText(_translate("FileServerForm", "Change"))
        self.server_info.setText(_translate("FileServerForm", "Server Status: Stopped"))
        self.toggle_working.setText(_translate("FileServerForm", "Start"))
        self.no_folder_notice.setText(_translate("FileServerForm", "<html><head/><body><p>Folder download is not supported,please consider compressing folders to zipped files.</p></body></html>"))
import Resources_rc
