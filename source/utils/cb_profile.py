from cb_files.design import ui_profile
from cb_files.apps import cb_login
from cb_files.resources import games

from PySide2 import QtCore, QtGui, QtWidgets, QtUiTools
from PySide2.QtCore import (QCoreApplication, QEventLoop, QMetaObject, QObject, QPoint, QRect, QSize, QThread, Signal, Qt, QEvent, QProcess, QTimer)
from PySide2.QtGui import (QColor, QCursor, QFont, QFontDatabase, QGuiApplication, QIcon, QPixmap, QImage, QPainter, QBrush, QWindow, QMovie)
from PySide2.QtWidgets import *

import os
from os import path
import pickle

def mask_image(imgdata, imgtype ='png', size = 64):
  
    image = QImage.fromData(imgdata, imgtype)
  
    image.convertToFormat(QImage.Format_ARGB32)
  
    imgsize = min(image.width(), image.height())
    rect = QRect(
        (image.width() - imgsize) / 2,
        (image.height() - imgsize) / 2,
        imgsize,
        imgsize,
     )
       
    image = image.copy(rect)
  
    out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
    out_img.fill(Qt.transparent)
  
    brush = QBrush(image)
  
    painter = QPainter(out_img)
    painter.setBrush(brush)
  
    painter.setPen(Qt.NoPen)
  
    painter.drawEllipse(0, 0, imgsize, imgsize)
  
    painter.end()
  
    pr = QWindow().devicePixelRatio()
    pm = QPixmap.fromImage(out_img)
    pm.setDevicePixelRatio(pr)
    size *= pr
    pm = pm.scaled(size, size, Qt.KeepAspectRatio, 
                               Qt.SmoothTransformation)
  
    return pm 

class ProfileWindow(QWidget):
    def __init__(self, logo, label):
        QWidget.__init__(self)
        self.ui = ui_profile.Ui_profilep()
        self.ui.setupUi(self)

        self.ui.closeAppBtn.setVisible(True)
        self.ui.filedialog.setVisible(True)

        global username

        if path.exists('config\\settings.dat'):
            with open(os.getcwd() + '\\config\\settings.dat', 'rb') as f:
                stored_details = pickle.load(f)
                username = stored_details[1]
        else:
            username = cb_login.username

        self.ui.logo = logo
        self.ui.label = label

        self.setWindowModality(Qt.ApplicationModal)

        #self.ui.closeAppBtn.setVisible(False)

        appIcon = QIcon(":/games/window2")
        self.setWindowIcon(appIcon)

        #Remove Title Bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        #Drop Shadow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.frame.setGraphicsEffect(self.shadow)

        self.ui.filedialog.clicked.connect(self.seefiles)
        self.ui.closeAppBtn.clicked.connect(self.phew)

        self.ui.label_2.setText(' ')

    def seefiles(self): #Image location gymnastics
        global pixmap

        self.ui.closeAppBtn.setVisible(False)

        self.ui.label_2.setText('Configuring Image')
        self.ui.filedialog.setVisible(False)

        filelocation = QFileDialog.getOpenFileName(self, None, None, "Images (*.png)")

        try:
            imgpath = filelocation[0]
            imgdata = open(imgpath, 'rb').read()
            pixmap = mask_image(imgdata)
            if username != 'CB Launcher': #Send gymnastic image file to cloud
                direct = os.path.dirname(imgpath)
                name_ting = os.path.basename(imgpath)

                os.rename(direct + '\\' + name_ting, direct + '\\pfp.png')

                simplified = direct + '\\pfp.png'

                self.p = QProcess()
                self.p.start(f'CBDownloader copy "{simplified}" "saves:{username}"')
                self.p.waitForFinished()

                self.ui.label.setGeometry(QRect(10, 5, 38, 38))

                self.ui.logo.setPixmap(QPixmap(pixmap))
                self.ui.label.setPixmap(QPixmap(pixmap))

                self.ui.label_2.setText('Complete')

                os.rename(direct + '\\pfp.png', direct + '\\' + name_ting)

                self.ui.closeAppBtn.setVisible(True)
            else:
                pass
        except:
            self.close()


    def phew(self):
        self.close()