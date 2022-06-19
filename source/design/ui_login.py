# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loginTiNPuu.ui'
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
from PySide2 import QtCore
from PySide2 import QtWidgets

from source.resources import font

class Ui_Form(object):
    def setupUi(self, Form):
        if Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(650, 222)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        '''appIcon = QIcon(":/games/cb")
        self.setWindowIcon(appIcon)'''
        self.shadow = QGraphicsDropShadowEffect(Form)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"background-color: rgb(33, 33, 33);\n"
"border-radius: 10px;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setGraphicsEffect(self.shadow)
        self.logo = QLabel(self.frame)
        self.logo.setObjectName(u"logo")
        self.logo.setGeometry(QRect(0, 20, 221, 171))
        self.logo.setPixmap(QPixmap(u":/games/cb"))
        self.logo.setScaledContents(True)
        self.invalid_text = QPlainTextEdit(self.frame)
        self.invalid_text.setObjectName(u"invalid_text")
        self.invalid_text.setGeometry(QRect(20, 110, 201, 21))
        font = QFont()
        font.setFamily(u"Ubuntu")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.invalid_text.setFont(font)
        self.invalid_text.setLayoutDirection(Qt.LeftToRight)
        self.invalid_text.setStyleSheet(u"background-color: rgba(225, 225, 225, 0);\n"
"color: rgb(255, 0, 4);\n"
"font: 12px;")
        self.invalid_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.invalid_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.invalid_text.setReadOnly(True)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(480, 115, 121, 20))
        self.label.setFont(font)
        self.label.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 13px \"Ubuntu\";")
        self.username_text = QLineEdit(self.frame)
        self.username_text.setObjectName(u"username_text")
        self.username_text.setGeometry(QRect(260, 30, 341, 31))
        self.username_text.setFont(font)
        self.username_text.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgba(225, 225, 225, 20);\n"
"font: 13px \"Ubuntu\";")
        self.password_text = QLineEdit(self.frame)
        self.password_text.setObjectName(u"password_text")
        self.password_text.setGeometry(QRect(260, 70, 341, 31))
        self.password_text.setFont(font)
        self.password_text.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgba(225, 225, 225, 20);\n"
"font: 13px \"Ubuntu\";")
        self.password_text.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login = QPushButton(self.frame)
        self.login.setObjectName(u"login")
        self.login.setGeometry(QRect(330, 160, 91, 21))
        self.login.setFont(font)
        self.login.setStyleSheet(u"QPushButton{\n"
"	background-color: rgb(12, 100, 203);\n"
"	color: rgb(255, 255, 255);\n"
"	font: 12px \"Ubuntu\";\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(12, 117, 225);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(12, 117, 203);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"")
        self.login.setCursor(QCursor(Qt.PointingHandCursor))
        self.skip = QPushButton(self.frame)
        self.skip.setObjectName(u"skip")
        self.skip.setGeometry(QRect(450, 160, 91, 21))
        self.skip.setFont(font)
        self.skip.setCursor(QCursor(Qt.PointingHandCursor))
        self.skip.setStyleSheet(u"QPushButton{\n"
"	background-color: rgb(12, 100, 203);\n"
"	color: rgb(255, 255, 255);\n"
"	font: 12px \"Ubuntu\";\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(12, 117, 225);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(12, 117, 203);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"")
        self.checkBox = QCheckBox(self.frame)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(260, 120, 171, 17))
        self.checkBox.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 12px \"Ubuntu\";")

        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.logo.setText("")
        self.invalid_text.setPlainText("")
        self.label.setText(QCoreApplication.translate("Form", u"Create an account", None))
        self.username_text.setText("")
        self.username_text.setPlaceholderText(QCoreApplication.translate("Form", u"Username", None))
        self.password_text.setPlaceholderText(QCoreApplication.translate("Form", u"Password", None))
        self.login.setText(QCoreApplication.translate("Form", u"Login", None))
        self.skip.setText(QCoreApplication.translate("Form", u"Skip", None))
        self.checkBox.setText(QCoreApplication.translate("Form", u"Keep me logged in", None))
    # retranslateUi