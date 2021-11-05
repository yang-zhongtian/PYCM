# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FileClientUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FileClient(object):
    def setupUi(self, FileClient):
        FileClient.setObjectName("FileClient")
        FileClient.setWindowModality(QtCore.Qt.ApplicationModal)
        FileClient.resize(619, 436)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Core/Resources/Logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FileClient.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(FileClient)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_back = QtWidgets.QPushButton(FileClient)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_back.sizePolicy().hasHeightForWidth())
        self.button_back.setSizePolicy(sizePolicy)
        self.button_back.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Theme/Resources/arrow_left_focus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_back.setIcon(icon1)
        self.button_back.setObjectName("button_back")
        self.horizontalLayout.addWidget(self.button_back)
        self.button_forward = QtWidgets.QPushButton(FileClient)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_forward.sizePolicy().hasHeightForWidth())
        self.button_forward.setSizePolicy(sizePolicy)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Theme/Resources/arrow_right_focus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_forward.setIcon(icon2)
        self.button_forward.setObjectName("button_forward")
        self.horizontalLayout.addWidget(self.button_forward)
        self.location = QtWidgets.QLineEdit(FileClient)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.location.sizePolicy().hasHeightForWidth())
        self.location.setSizePolicy(sizePolicy)
        self.location.setObjectName("location")
        self.horizontalLayout.addWidget(self.location)
        self.button_go = QtWidgets.QPushButton(FileClient)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_go.sizePolicy().hasHeightForWidth())
        self.button_go.setSizePolicy(sizePolicy)
        self.button_go.setObjectName("button_go")
        self.horizontalLayout.addWidget(self.button_go)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.file_area_container = QtWidgets.QVBoxLayout()
        self.file_area_container.setObjectName("file_area_container")
        self.file_area = QtWidgets.QListWidget(FileClient)
        self.file_area.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.file_area.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.file_area.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.file_area.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)
        self.file_area.setMovement(QtWidgets.QListView.Static)
        self.file_area.setViewMode(QtWidgets.QListView.IconMode)
        self.file_area.setWordWrap(True)
        self.file_area.setObjectName("file_area")
        self.file_area_container.addWidget(self.file_area)
        self.download_button = QtWidgets.QPushButton(FileClient)
        self.download_button.setEnabled(False)
        self.download_button.setObjectName("download_button")
        self.file_area_container.addWidget(self.download_button)
        self.verticalLayout.addLayout(self.file_area_container)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(FileClient)
        self.download_button.clicked.connect(FileClient.download)
        self.file_area.itemSelectionChanged.connect(FileClient.update_selection)
        QtCore.QMetaObject.connectSlotsByName(FileClient)

    def retranslateUi(self, FileClient):
        _translate = QtCore.QCoreApplication.translate
        FileClient.setWindowTitle(_translate("FileClient", "File Client"))
        self.location.setText(_translate("FileClient", "/"))
        self.button_go.setText(_translate("FileClient", "Go"))
        self.download_button.setText(_translate("FileClient", "Download"))
import Resources_rc
