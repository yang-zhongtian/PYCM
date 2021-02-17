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
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_3 = QtWidgets.QPushButton(ScreenBroadcast)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_2 = QtWidgets.QPushButton(ScreenBroadcast)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(ScreenBroadcast)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.widget = QtWidgets.QWidget(ScreenBroadcast)
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.screen_display = QtWidgets.QLabel(self.widget)
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
        self.horizontalLayout_2.addWidget(self.screen_display)
        self.verticalLayout.addWidget(self.widget)
        self.verticalLayout.setStretch(1, 50)

        self.retranslateUi(ScreenBroadcast)
        QtCore.QMetaObject.connectSlotsByName(ScreenBroadcast)

    def retranslateUi(self, ScreenBroadcast):
        _translate = QtCore.QCoreApplication.translate
        ScreenBroadcast.setWindowTitle(_translate("ScreenBroadcast", "屏幕广播"))
        self.pushButton_3.setText(_translate("ScreenBroadcast", "PushButton"))
        self.pushButton_2.setText(_translate("ScreenBroadcast", "PushButton"))
        self.pushButton.setText(_translate("ScreenBroadcast", "PushButton"))
import Resources_rc
