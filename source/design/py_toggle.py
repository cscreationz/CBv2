from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class PyToggle(QCheckBox):
    def __init__(
        self,
        width = 30,
        bg_color = "#777",
        circle_color = "#000",
        active_color = "#008Cff",
        animation_curve = QEasingCurve.OutQuint
    ):

        QCheckBox.__init__(self)

        self.setFixedSize(width, 10)
        self.setText("NSFW")
        self.setStyleSheet("color: rgb(255, 255, 255);")
        self.setCursor(Qt.PointingHandCursor)
        
        self._bg_color = bg_color      
        self._circle_color = circle_color 
        self._active_color = active_color

        self._circle_position = 3
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(500)

        self.stateChanged.connect(self.start_transition)              

    @Property(float)
    def circle_position(self):
        return self._circle_position

    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos                      
        self.update()

    def start_transition(self, value):
        self.animation.stop()
        if value:
            self.animation.setEndValue(self.width() - 10)
        else:
            self.animation.setEndValue(3)

        self.animation.start()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(Qt.NoPen)        

        rect = QRect(0, 0, self.width(), self.height())

        if not self.isChecked():
            p.setBrush(QColor(self._bg_color))     
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)

            p.setBrush(QColor(self._circle_color))    
            p.drawEllipse(self._circle_position, 3, 5, 5)
        else:
            p.setBrush(QColor(self._active_color))     
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() /2 , self.height() / 2)

            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._circle_position, 3, 5, 5)

        p.end()