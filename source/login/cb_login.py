import os, sys, base64
from dotenv import load_dotenv
from multiprocessing import Pool
from typing import List
from PySide2.QtWidgets import QWidget
from source.design import ui_login
from PySide2 import QtCore
from source.utils import cb_splashscreen, cb_initialize
from source.window import cb_window
from source.login import login_utils
from ... import cb_utils

extDataDir = os.getcwd()
if getattr(sys, 'frozen', False):
    extDataDir = sys._MEIPASS
load_dotenv(dotenv_path=os.path.join(extDataDir, '.env'))

movie: str = ':/games/loading'

class LoginPage(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = ui_login.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.label.setText("<a href='https://cbauth.herokuapp.com/registration'>Create an account</a>")
        self.ui.label.setOpenExternalLinks(True)
        self.ui.login.setShortcut("Return")
        self.ui.login.clicked.connect(self.login)
        self.ui.skip.clicked.connect(self.skiplogin)

    def encodepassword(self, password: str) -> bytes:
        """Return encoded password"""
        encoded_password: bytes = base64.b64encode(password.encode('utf-8'))
        return encoded_password

    def login_details(self) -> str:
        """Returns username and password from text box"""
        global username
        username: str = self.ui.username_text.text()
        password: str = self.ui.password_text.text()
        return username, password

    def save_details(self, password: str) -> None:
        """Create a binary file to save username and password"""
        if self.ui.checkBox.isChecked() and username != 'CB Launcher':
            details: List[str, bytes] = [username, self.encodepassword(password)]
            cb_utils.writebinary(os.getcwd() + '\\config\\settings.dat', details)

    def login(self):
        """Tests if login details are right. Displays invalid details if wrong"""
        username, password = self.login_details()
        if login_utils.login(username, password):
            self.save_details(password)
            self.close()
            self.showMainWindow()
        else:
            self.ui.invalid_text.setPlainText("Invalid Username or Password")

    def skiplogin(self):
        """Sets username to CB Launcher (bot) and opens main window"""
        global username
        username: str = 'CB Launcher'
        self.close()
        self.showMainWindow()

    def startSplashscreen(self):
        """Starts GIF to show loading status"""
        self.splashscreen = cb_splashscreen.MovieSplashScreen(movie)
        self.splashscreen.show()

    def eventLoop(self):
        """Starts an event loop to avoid lag while doing background checks"""
        initLoop = QtCore.QEventLoop()
        pool = Pool(processes=2)
        pool.apply_async(cb_initialize.longInitialization, [2], callback=lambda exitCode: initLoop.exit(exitCode))
        initLoop.exec_()

    def showMainWindow(self):
        """Starts splashscreen, and runs background checks 
        and shows main window after"""
        self.startSplashscreen()
        self.eventLoop()
        window = cb_window.MainWindow()
        window.show()
        self.splashscreen.close()
        self.close()