# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RemoteCommandGroupUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RemoteCommandGroupDialog(object):
    def setupUi(self, RemoteCommandGroupDialog):
        RemoteCommandGroupDialog.setObjectName("RemoteCommandGroupDialog")
        RemoteCommandGroupDialog.resize(398, 528)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RemoteCommandGroupDialog.sizePolicy().hasHeightForWidth())
        RemoteCommandGroupDialog.setSizePolicy(sizePolicy)
        RemoteCommandGroupDialog.setMinimumSize(QtCore.QSize(0, 0))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(RemoteCommandGroupDialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.command_group = QtWidgets.QGroupBox(RemoteCommandGroupDialog)
        self.command_group.setObjectName("command_group")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.command_group)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.command_select = QtWidgets.QListWidget(self.command_group)
        self.command_select.setObjectName("command_select")
        self.horizontalLayout_2.addWidget(self.command_select)
        self.verticalLayout_3.addWidget(self.command_group)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.user_group = QtWidgets.QGroupBox(RemoteCommandGroupDialog)
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
        self.target_select = QtWidgets.QGroupBox(RemoteCommandGroupDialog)
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
        self.buttonBox = QtWidgets.QDialogButtonBox(RemoteCommandGroupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)
        self.verticalLayout_3.setStretch(0, 5)
        self.verticalLayout_3.setStretch(1, 6)

        self.retranslateUi(RemoteCommandGroupDialog)
        self.buttonBox.accepted.connect(RemoteCommandGroupDialog.accept)
        self.buttonBox.rejected.connect(RemoteCommandGroupDialog.reject)
        self.send_to_selected.clicked.connect(self.target_select.show)
        self.send_to_all.clicked.connect(self.target_select.hide)
        QtCore.QMetaObject.connectSlotsByName(RemoteCommandGroupDialog)

    def retranslateUi(self, RemoteCommandGroupDialog):
        _translate = QtCore.QCoreApplication.translate
        RemoteCommandGroupDialog.setWindowTitle(_translate("RemoteCommandGroupDialog", "远程命令"))
        self.command_group.setTitle(_translate("RemoteCommandGroupDialog", "命令选择"))
        self.user_group.setTitle(_translate("RemoteCommandGroupDialog", "用户组"))
        self.send_to_selected.setText(_translate("RemoteCommandGroupDialog", "指定"))
        self.send_to_all.setText(_translate("RemoteCommandGroupDialog", "全体"))
        self.target_select.setTitle(_translate("RemoteCommandGroupDialog", "发送目标"))
