import os
import sys
from dotenv import load_dotenv
from PySide2.QtWidgets import QSplashScreen
from PySide2 import QtWidgets, QtGui

extDataDir = os.getcwd()
if getattr(sys, 'frozen', False):
    extDataDir = sys._MEIPASS
load_dotenv(dotenv_path=os.path.join(extDataDir, '.env'))

class MovieSplashScreen(QSplashScreen):

	def __init__(self, pathToGIF):
		self.movie = QtGui.QMovie(pathToGIF)
		self.movie.jumpToFrame(0)
		pixmap = QtGui.QPixmap(self.movie.frameRect().size())
		QtWidgets.QSplashScreen.__init__(self, pixmap)
		self.movie.frameChanged.connect(self.repaint)

	def showEvent(self, event):
		self.movie.start()

	def hideEvent(self, event):
		self.movie.stop()

	def paintEvent(self, event):
		painter = QtGui.QPainter(self)
		pixmap = self.movie.currentPixmap()
		self.setMask(pixmap.mask())
		painter.drawPixmap(0, 0, pixmap)