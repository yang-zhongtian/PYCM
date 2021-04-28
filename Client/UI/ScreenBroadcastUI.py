# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ScreenBroadcastUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
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
        icon.addPixmap(QtGui.QPixmap(":/logo/UI/Resources/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ScreenBroadcast.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(ScreenBroadcast)
        self.verticalLayout.setContentsMargins(22, -1, 22, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.control_box_layout = QtWidgets.QHBoxLayout()
        self.control_box_layout.setObjectName("control_box_layout")
        self.freeze_frame = QtWidgets.QPushButton(ScreenBroadcast)
        self.freeze_frame.setCheckable(True)
        self.freeze_frame.setObjectName("freeze_frame")
        self.control_box_layout.addWidget(self.freeze_frame)
        self.full_screen = QtWidgets.QPushButton(ScreenBroadcast)
        self.full_screen.setCheckable(True)
        self.full_screen.setObjectName("full_screen")
        self.control_box_layout.addWidget(self.full_screen)
        self.pushButton = QtWidgets.QPushButton(ScreenBroadcast)
        self.pushButton.setObjectName("pushButton")
        self.control_box_layout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.control_box_layout)
        self.screen_widget = QtWidgets.QWidget(ScreenBroadcast)
        self.screen_widget.setObjectName("screen_widget")
        self.screen_display = QtWidgets.QLabel(self.screen_widget)
        self.screen_display.setGeometry(QtCore.QRect(0, 0, 320, 180))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.screen_display.sizePolicy().hasHeightForWidth())
        self.screen_display.setSizePolicy(sizePolicy)
        self.screen_display.setStyleSheet("background-color: rgb(0, 162, 119);")
        self.screen_display.setText("")
        self.screen_display.setScaledContents(True)
        self.screen_display.setAlignment(QtCore.Qt.AlignCenter)
        self.screen_display.setObjectName("screen_display")
        self.verticalLayout.addWidget(self.screen_widget)
        self.verticalLayout.setStretch(1, 50)

        self.retranslateUi(ScreenBroadcast)
        self.freeze_frame.clicked['bool'].connect(ScreenBroadcast.freeze_frame)
        self.full_screen.clicked['bool'].connect(ScreenBroadcast.show_full_screen)
        QtCore.QMetaObject.connectSlotsByName(ScreenBroadcast)

    def retranslateUi(self, ScreenBroadcast):
        _translate = QtCore.QCoreApplication.translate
        ScreenBroadcast.setWindowTitle(_translate("ScreenBroadcast", "屏幕广播"))
        self.freeze_frame.setText(_translate("ScreenBroadcast", "冻结屏幕"))
        self.full_screen.setText(_translate("ScreenBroadcast", "全屏"))
        self.pushButton.setText(_translate("ScreenBroadcast", "PushButton"))
import Resources_rc
