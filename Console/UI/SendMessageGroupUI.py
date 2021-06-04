# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SendMessageGroupUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SendMessageGroupDialog(object):
    def setupUi(self, SendMessageGroupDialog):
        SendMessageGroupDialog.setObjectName("SendMessageGroupDialog")
        SendMessageGroupDialog.resize(398, 522)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SendMessageGroupDialog.sizePolicy().hasHeightForWidth())
        SendMessageGroupDialog.setSizePolicy(sizePolicy)
        SendMessageGroupDialog.setMinimumSize(QtCore.QSize(0, 0))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(SendMessageGroupDialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.send_message_group = QtWidgets.QGroupBox(SendMessageGroupDialog)
        self.send_message_group.setObjectName("send_message_group")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.send_message_group)
        self.horizontalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.send_message_input = QtWidgets.QPlainTextEdit(self.send_message_group)
        self.send_message_input.setObjectName("send_message_input")
        self.horizontalLayout_2.addWidget(self.send_message_input)
        self.verticalLayout_3.addWidget(self.send_message_group)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.user_group = QtWidgets.QGroupBox(SendMessageGroupDialog)
        self.user_group.setObjectName("user_group")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.user_group)
        self.verticalLayout.setObjectName("verticalLayout")
        self.send_to_selected = QtWidgets.QRadioButton(self.user_group)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        self.send_to_selected.setFont(font)
        self.send_to_selected.setChecked(True)
        self.send_to_selected.setObjectName("send_to_selected")
        self.verticalLayout.addWidget(self.send_to_selected)
        self.send_to_all = QtWidgets.QRadioButton(self.user_group)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        self.send_to_all.setFont(font)
        self.send_to_all.setObjectName("send_to_all")
        self.verticalLayout.addWidget(self.send_to_all)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.user_group)
        self.target_select = QtWidgets.QGroupBox(SendMessageGroupDialog)
        self.target_select.setObjectName("target_select")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.target_select)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.target_list = QtWidgets.QListWidget(self.target_select)
        self.target_list.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.target_list.setObjectName("target_list")
        self.verticalLayout_2.addWidget(self.target_list)
        self.horizontalLayout.addWidget(self.target_select)
        self.horizontalLayout.setStretch(0, 4)
        self.horizontalLayout.setStretch(1, 6)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(SendMessageGroupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)
        self.verticalLayout_3.setStretch(0, 3)
        self.verticalLayout_3.setStretch(1, 6)

        self.retranslateUi(SendMessageGroupDialog)
        self.buttonBox.accepted.connect(SendMessageGroupDialog.accept)
        self.buttonBox.rejected.connect(SendMessageGroupDialog.reject)
        self.send_to_selected.clicked.connect(self.target_select.show)
        self.send_to_all.clicked.connect(self.target_select.hide)
        QtCore.QMetaObject.connectSlotsByName(SendMessageGroupDialog)

    def retranslateUi(self, SendMessageGroupDialog):
        _translate = QtCore.QCoreApplication.translate
        SendMessageGroupDialog.setWindowTitle(_translate("SendMessageGroupDialog", "消息发送"))
        self.send_message_group.setTitle(_translate("SendMessageGroupDialog", "消息编辑"))
        self.user_group.setTitle(_translate("SendMessageGroupDialog", "用户组"))
        self.send_to_selected.setText(_translate("SendMessageGroupDialog", "指定"))
        self.send_to_all.setText(_translate("SendMessageGroupDialog", "全体"))
        self.target_select.setTitle(_translate("SendMessageGroupDialog", "发送目标"))
