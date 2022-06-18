from PySide2.QtGui import QCursor
from PySide2.QtWidgets import QPushButton, QFrame
from PySide2.QtCore import QSize
from PySide2.QtCore import Qt

def create_button(sub='', width=0, height=0, iconw=0, iconh=0, button_name='name'):
    button = QPushButton(sub)
    button.setObjectName(u"{}".format(button_name))
    button.setMinimumSize(QSize(width, height))
    button.setMaximumSize(QSize(width, height))
    button.setIconSize(QSize(iconw, iconh))
    button.setStyleSheet("QPushButton"
    "{"
    "border: 0px;"
    "}"
    "QPushButton::hover"
    "{"
    "background-color: rgb(12, 100, 203);"
    "}")
    button.setCursor(QCursor(Qt.PointingHandCursor))

    return button

def create_frame(width=0, height=0, frame_name='name'):
    frame = QFrame()
    frame.setObjectName(frame_name)
    frame.setStyleSheet("""background-color: rgba(255, 255, 255, 30);
                                border-radius: 10px;""")
    frame.setMinimumSize(QSize(width, height))
    frame.setMaximumSize(QSize(width, height))

    return frame