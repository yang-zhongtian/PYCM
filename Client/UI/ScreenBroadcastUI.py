# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ScreenBroadcastUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ScreenBroadcast(object):
    def setupUi(self, ScreenBroadcast):
        ScreenBroadcast.setObjectName("ScreenBroadcast")
        ScreenBroadcast.resize(967, 702)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ScreenBroadcast.sizePolicy().hasHeightForWidth())
        ScreenBroadcast.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Core/Resources/Logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ScreenBroadcast.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(ScreenBroadcast)
        self.verticalLayout.setContentsMargins(22, -1, 22, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.control_box_layout = QtWidgets.QHBoxLayout()
        self.control_box_layout.setObjectName("control_box_layout")
        self.freeze_frame = QtWidgets.QPushButton(ScreenBroadcast)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.freeze_frame.sizePolicy().hasHeightForWidth())
        self.freeze_frame.setSizePolicy(sizePolicy)
        self.freeze_frame.setCheckable(True)
        self.freeze_frame.setObjectName("freeze_frame")
        self.control_box_layout.addWidget(self.freeze_frame)
        self.full_screen = QtWidgets.QPushButton(ScreenBroadcast)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.full_screen.sizePolicy().hasHeightForWidth())
        self.full_screen.setSizePolicy(sizePolicy)
        self.full_screen.setCheckable(True)
        self.full_screen.setObjectName("full_screen")
        self.control_box_layout.addWidget(self.full_screen)
        self.screen_shot = QtWidgets.QPushButton(ScreenBroadcast)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.screen_shot.sizePolicy().hasHeightForWidth())
        self.screen_shot.setSizePolicy(sizePolicy)
        self.screen_shot.setObjectName("screen_shot")
        self.control_box_layout.addWidget(self.screen_shot)
        self.always_on_top = QtWidgets.QPushButton(ScreenBroadcast)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.always_on_top.sizePolicy().hasHeightForWidth())
        self.always_on_top.setSizePolicy(sizePolicy)
        self.always_on_top.setCheckable(True)
        self.always_on_top.setChecked(True)
        self.always_on_top.setObjectName("always_on_top")
        self.control_box_layout.addWidget(self.always_on_top)
        self.verticalLayout.addLayout(self.control_box_layout)
        self.screen_widget = QtWidgets.QWidget(ScreenBroadcast)
        self.screen_widget.setStyleSheet("#screen_widget {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(82, 229, 231, 255), stop:1 rgba(19, 12, 183, 255));\n"
"}")
        self.screen_widget.setObjectName("screen_widget")
        self.screen_display = QtWidgets.QLabel(self.screen_widget)
        self.screen_display.setGeometry(QtCore.QRect(0, 0, 421, 341))
        self.screen_display.setText("")
        self.screen_display.setScaledContents(True)
        self.screen_display.setObjectName("screen_display")
        self.verticalLayout.addWidget(self.screen_widget)
        self.verticalLayout.setStretch(1, 50)

        self.retranslateUi(ScreenBroadcast)
        self.freeze_frame.clicked['bool'].connect(ScreenBroadcast.freeze_frame)
        self.full_screen.clicked['bool'].connect(ScreenBroadcast.show_full_screen)
        self.screen_shot.clicked.connect(ScreenBroadcast.screen_shot)
        self.always_on_top.clicked['bool'].connect(ScreenBroadcast.toggle_always_on_top)
        QtCore.QMetaObject.connectSlotsByName(ScreenBroadcast)

    def retranslateUi(self, ScreenBroadcast):
        _translate = QtCore.QCoreApplication.translate
        ScreenBroadcast.setWindowTitle(_translate("ScreenBroadcast", "Screen Broadcast"))
        self.freeze_frame.setText(_translate("ScreenBroadcast", "Freeze Screen"))
        self.full_screen.setText(_translate("ScreenBroadcast", "Full Screen"))
        self.screen_shot.setText(_translate("ScreenBroadcast", "Screen Shot"))
        self.always_on_top.setText(_translate("ScreenBroadcast", "Always On Top"))
import Resources_rc
