# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FileSendUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FileSendForm(object):
    def setupUi(self, FileSendForm):
        FileSendForm.setObjectName("FileSendForm")
        FileSendForm.setWindowModality(QtCore.Qt.ApplicationModal)
        FileSendForm.resize(499, 338)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Core/Core/Logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FileSendForm.setWindowIcon(icon)
        self.main_layout = QtWidgets.QVBoxLayout(FileSendForm)
        self.main_layout.setObjectName("main_layout")
        self.header_layout = QtWidgets.QHBoxLayout()
        self.header_layout.setContentsMargins(2, 2, 2, 2)
        self.header_layout.setSpacing(0)
        self.header_layout.setObjectName("header_layout")
        self.add_file_button = QtWidgets.QPushButton(FileSendForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_file_button.sizePolicy().hasHeightForWidth())
        self.add_file_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.add_file_button.setFont(font)
        self.add_file_button.setObjectName("add_file_button")
        self.header_layout.addWidget(self.add_file_button)
        self.delete_file_button = QtWidgets.QPushButton(FileSendForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delete_file_button.sizePolicy().hasHeightForWidth())
        self.delete_file_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.delete_file_button.setFont(font)
        self.delete_file_button.setObjectName("delete_file_button")
        self.header_layout.addWidget(self.delete_file_button)
        self.submit_file_button = QtWidgets.QPushButton(FileSendForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.submit_file_button.sizePolicy().hasHeightForWidth())
        self.submit_file_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.submit_file_button.setFont(font)
        self.submit_file_button.setObjectName("submit_file_button")
        self.header_layout.addWidget(self.submit_file_button)
        self.main_layout.addLayout(self.header_layout)
        self.file_list_container_widget = QtWidgets.QWidget(FileSendForm)
        self.file_list_container_widget.setObjectName("file_list_container_widget")
        self.file_list_container = QtWidgets.QVBoxLayout(self.file_list_container_widget)
        self.file_list_container.setContentsMargins(0, 0, 0, 0)
        self.file_list_container.setObjectName("file_list_container")
        self.main_layout.addWidget(self.file_list_container_widget)
        self.progress_layout = QtWidgets.QHBoxLayout()
        self.progress_layout.setObjectName("progress_layout")
        self.file_send_progress_label = QtWidgets.QLabel(FileSendForm)
        self.file_send_progress_label.setObjectName("file_send_progress_label")
        self.progress_layout.addWidget(self.file_send_progress_label)
        self.file_send_progress_bar = QtWidgets.QProgressBar(FileSendForm)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.file_send_progress_bar.setFont(font)
        self.file_send_progress_bar.setProperty("value", 0)
        self.file_send_progress_bar.setTextVisible(True)
        self.file_send_progress_bar.setOrientation(QtCore.Qt.Horizontal)
        self.file_send_progress_bar.setObjectName("file_send_progress_bar")
        self.progress_layout.addWidget(self.file_send_progress_bar)
        self.main_layout.addLayout(self.progress_layout)
        self.main_layout.setStretch(1, 1)

        self.retranslateUi(FileSendForm)
        self.delete_file_button.clicked.connect(FileSendForm.delete_selected_files) # type: ignore
        self.add_file_button.clicked.connect(FileSendForm.show_add_file_dialog) # type: ignore
        self.submit_file_button.clicked.connect(FileSendForm.send_all) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(FileSendForm)

    def retranslateUi(self, FileSendForm):
        _translate = QtCore.QCoreApplication.translate
        FileSendForm.setWindowTitle(_translate("FileSendForm", "Submit Files"))
        self.add_file_button.setText(_translate("FileSendForm", "Add Files"))
        self.delete_file_button.setText(_translate("FileSendForm", "Remove Selected Files"))
        self.submit_file_button.setText(_translate("FileSendForm", "Submit All Files"))
        self.file_send_progress_label.setText(_translate("FileSendForm", "Ready"))
from Resources import Resources
