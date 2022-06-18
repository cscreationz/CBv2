from PySide2.QtWidgets import QMessageBox
from PySide2.QtCore import Qt

import sys

class MessageBox:

    def popup_button(self, i):
        if i.text() == 'OK':
            sys.exit() #Close login window

    def displayMessageBox(self, window_title, error):
        dialog = QMessageBox()
        dialog.setWindowTitle(window_title)
        dialog.setText(str(error))
        dialog.setIcon(QMessageBox.Information)
        dialog.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        dialog.buttonClicked.connect(self.popup_button)
        x = dialog.exec_()