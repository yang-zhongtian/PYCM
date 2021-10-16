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
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.freeze_frame.setFont(font)
        self.freeze_frame.setCheckable(True)
        self.freeze_frame.setObjectName("freeze_frame")
        self.control_box_layout.addWidget(self.freeze_frame)
        self.full_screen = QtWidgets.QPushButton(ScreenBroadcast)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.full_screen.setFont(font)
        self.full_screen.setCheckable(True)
        self.full_screen.setObjectName("full_screen")
        self.control_box_layout.addWidget(self.full_screen)
        self.screen_shot = QtWidgets.QPushButton(ScreenBroadcast)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.screen_shot.setFont(font)
        self.screen_shot.setObjectName("screen_shot")
        self.control_box_layout.addWidget(self.screen_shot)
        self.verticalLayout.addLayout(self.control_box_layout)
        self.screen_widget = QtWidgets.QWidget(ScreenBroadcast)
        self.screen_widget.setStyleSheet("background-color: rgb(3, 118, 108);")
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
        QtCore.QMetaObject.connectSlotsByName(ScreenBroadcast)

    def retranslateUi(self, ScreenBroadcast):
        _translate = QtCore.QCoreApplication.translate
        ScreenBroadcast.setWindowTitle(_translate("ScreenBroadcast", "屏幕广播"))
        self.freeze_frame.setText(_translate("ScreenBroadcast", "冻结屏幕"))
        self.full_screen.setText(_translate("ScreenBroadcast", "全屏"))
        self.screen_shot.setText(_translate("ScreenBroadcast", "截图"))
import Resources_rc
