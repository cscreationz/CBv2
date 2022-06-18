# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'appdwenloadPmYJWB.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(442, 210)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"background-color: rgb(33, 33, 33);\n"
"border-radius: 10px;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.pushButton_8 = QPushButton(self.frame)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setGeometry(QRect(130, 50, 161, 35))
        self.pushButton_8.setMinimumSize(QSize(111, 31))
        self.pushButton_8.setMaximumSize(QSize(9999, 9999))
        font = QFont()
        font.setFamily(u"Ubuntu")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setStyleSheet(u"QPushButton{\n"
"	background-color: rgb(12, 100, 203);\n"
"	color: rgb(255, 255, 255);\n"
"	border-radius: 10px;\n"
"	font: 12px \"Ubuntu\";\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(12, 117, 225);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(12, 117, 203);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"")
        self.pushButton_9 = QPushButton(self.frame)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setGeometry(QRect(130, 100, 161, 35))
        self.pushButton_9.setMinimumSize(QSize(111, 31))
        self.pushButton_9.setMaximumSize(QSize(9999, 9999))
        self.pushButton_9.setFont(font)
        self.pushButton_9.setStyleSheet(u"QPushButton{\n"
"	background-color: rgb(12, 100, 203);\n"
"	color: rgb(255, 255, 255);\n"
"	border-radius: 10px;\n"
"	font: 12px \"Ubuntu\";\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(12, 117, 225);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(12, 117, 203);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"")

        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton_8.setText(QCoreApplication.translate("Form", u"Installer (.exe)", None))
        self.pushButton_9.setText(QCoreApplication.translate("Form", u"7zip (.zip) - extracted", None))
    # retranslateUi

