# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AboutUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(545, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AboutDialog.sizePolicy().hasHeightForWidth())
        AboutDialog.setSizePolicy(sizePolicy)
        AboutDialog.setMinimumSize(QtCore.QSize(0, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Core/Resources/Logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AboutDialog.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(AboutDialog)
        self.verticalLayout.setContentsMargins(30, 25, 30, 25)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.productName = QtWidgets.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setFamily("阿里巴巴普惠体")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.productName.setFont(font)
        self.productName.setAlignment(QtCore.Qt.AlignCenter)
        self.productName.setObjectName("productName")
        self.verticalLayout_2.addWidget(self.productName)
        self.buildInfo = QtWidgets.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setFamily("阿里巴巴普惠体")
        self.buildInfo.setFont(font)
        self.buildInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.buildInfo.setObjectName("buildInfo")
        self.verticalLayout_2.addWidget(self.buildInfo)
        self.label = QtWidgets.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setFamily("阿里巴巴普惠体")
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setOpenExternalLinks(True)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.groupBox = QtWidgets.QGroupBox(AboutDialog)
        font = QtGui.QFont()
        font.setFamily("阿里巴巴普惠体")
        self.groupBox.setFont(font)
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("阿里巴巴普惠体")
        font.setBold(True)
        font.setWeight(75)
        self.textBrowser.setFont(font)
        self.textBrowser.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'阿里巴巴普惠体\',\'阿里巴巴普惠体\'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\'; font-weight:400;\">This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or at your option any later version.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimSun\'; font-weight:400;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\'; font-weight:400;\">This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimSun\'; font-weight:400;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\'; font-weight:400;\">You should have received a copy of the GNU General Public License along with this program. If not, see &lt;</span><a href=\"https://www.gnu.org/licenses/\"><span style=\" font-family:\'SimSun\'; font-weight:400; text-decoration: underline; color:#0000ff;\">https://www.gnu.org/licenses/</span></a><span style=\" font-family:\'SimSun\'; font-weight:400;\">&gt;.</span></p></body></html>")
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_3.addWidget(self.textBrowser)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(AboutDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AboutDialog)
        self.buttonBox.accepted.connect(AboutDialog.accept)
        self.buttonBox.rejected.connect(AboutDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutDialog.setWindowTitle(_translate("AboutDialog", "About"))
        self.productName.setText(_translate("AboutDialog", "PYCM Console"))
        self.buildInfo.setText(_translate("AboutDialog", "No build info"))
        self.label.setText(_translate("AboutDialog", "<html><head/><body><p>Project Home: <a href=\"https://github.com/yangzhongtian001/PYCM\"><span style=\" text-decoration: underline; color:#0000ff;\">https://github.com/yangzhongtian001/PYCM</span></a></p></body></html>"))
        self.groupBox.setTitle(_translate("AboutDialog", "GNU General Public License"))
import Resources_rc
