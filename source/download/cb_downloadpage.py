from PySide2.QtWidgets import QWidget, QGraphicsDropShadowEffect, QFileDialog, QPushButton
import download_utils, cb_rclone
from source.design import ui_download
from PySide2.QtGui import QIcon, QColor, QCursor, QPixmap
from PySide2.QtCore import Qt, QCoreApplication, QProcess, QTimer, QSize
from PySide2 import QtCore
from source.login import cb_login, login_utils
from source.utils import cb_notification, cb_widgets
from ... import cb_utils
import cb_rclone
import os
import getpass
import json

DESKTOP_DIRECTORY = "C:\\Users\\{}\\Desktop"
STARTMENU_DIRECTORY = "C:\\Users\\{}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs"

class DownloadPage(QWidget):

    def __init__(self, ui, game_size, game_name, game_download, exepath, save_path, transfers):
        QWidget.__init__(self)
        self.downloadpageui = ui_download.Download_Widget()
        self.downloadpageui.setupUi(self)
        self.rclone = cb_rclone.RcloneDownloader(self.downloadpageui)
        self.ui = ui
        icon = QIcon(':/icons/images/icons/cil-media-pause')
        self.downloadpageui.close_download_5.setIcon(icon)
        #Assigning variables
        self.game_size, self.game_name, self.game_download, self.exepath, self.save_path, self.parallel_transfers = game_size, game_name, game_download, exepath, save_path, transfers
        self.downloadpageui.loadsave.setVisible(False)
        self.downloadpageui.nosave.setVisible(False)
        self.downloadpageui.download_progress_2.setVisible(False)
        self.downloadpageui.pushButton.setVisible(False)
        #Remove Title Bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.hundredcount = 0
        #Drop Shadow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.downloadpageui.frame.setGraphicsEffect(self.shadow)
        self.downloadpageui.filedialog.setCursor(QCursor(Qt.PointingHandCursor))
        self.downloadpageui.start.setCursor(QCursor(Qt.PointingHandCursor))
        self.downloadpageui.loadsave.setCursor(QCursor(Qt.PointingHandCursor))
        self.downloadpageui.nosave.setCursor(QCursor(Qt.PointingHandCursor))
        self.downloadpageui.filedialog.clicked.connect(self.browse_drive)
        self.downloadpageui.start.clicked.connect(self.downloadChecks)
        self.downloadpageui.loadsave.clicked.connect(self.load_save)
        self.downloadpageui.nosave.clicked.connect(self.download_final)
        self.downloadpageui.close_download_2.clicked.connect(self.close_window)
        self.downloadpageui.minimizeAppBtn_2.clicked.connect(lambda: self.showMinimized())
        self.downloadpageui.close_download_3.clicked.connect(self.shutit)
        self.downloadpageui.minimizeAppBtn_3.clicked.connect(lambda: self.showMinimized())
        self.downloadpageui.close_download_4.clicked.connect(self.shutit)
        self.downloadpageui.minimizeAppBtn_4.clicked.connect(lambda: self.showMinimized())
        self.downloadpageui.pushButton.clicked.connect(self.startgame)
        self.downloadpageui.close_download_5.clicked.connect(self.pauseresume)
        self.downloadpageui.minimizeAppBtn_2.setVisible(False)
        self.downloadpageui.minimizeAppBtn_3.setVisible(False)
        self.downloadpageui.minimizeAppBtn_4.setVisible(False)
        self.downloadpageui.game_name.setText(QCoreApplication.translate("Form", u"{}".format(self.game_name), None))
        self.downloadpageui.label_2.setText(self.game_size)
        self.downloadpageui.download_location.textChanged.connect(self.disk_free)

        self.checks()
        space = psutil.disk_usage("C:").free #Display amount of free space
        proper_socks = self.convert_size(space)
        self.downloadpageui.available_space.setText(f'Available Disk Space: {proper_socks}')

    def checks(self):
        if os.path.exists('config\\settings.dat'):
            self.username, password = login_utils.get_login_details(cb_utils.readbinary('config\\settings.dat'))
            self.pc_user = getpass.getuser()
        else:
            self.username = cb_login.username
            self.pc_user = getpass.getuser()

    def browse_drive(self): #Change line edit text according to file dialog
        #filelocation = QFileDialog.getExistingDirectory()
        self.downloadpageui.download_location.setText(download_utils.browseFile)

    def disk_free(self, text): #Display free disk space
        try:
            #free_space = psutil.disk_usage(text[0:2]).free
            #free_space_readable = cb_modules.convert_size(free_space)

            self.downloadpageui.available_space.setText(f'Available Disk Space: {download_utils.freeDiskSpace(text)}')
        except:
            self.downloadpageui.available_space.setText('Unknown')

    def close_window(self): #closing windows gymnastics
        self.close()
        self.ui.rclone_button.setVisible(False)
        if self.rclone_process != None:
            self.rclone_process.kill()
        try:
            os.remove('config\\progress.txt')
        except:
            pass

    '''def verifydownloadlocation(self):
        if not verifyLocation(self.download_location):
            self.downloadpageui.label_8.setText('Remove backslash from the end to continue')
            return False
        else:
            return True

        if self.download_location.endswith("\\"):
            return False
        elif self.download_location.isalpha == False:
            self.downloadpageui.label_8.setText('Input download location')
            return False
        else:
            return True'''

    '''def rclone(self, command, func_err='', func_out=''):
        self.rclone_process = QProcess()
        self.rclone_process.readyReadStandardOutput.connect(self.handle_stderr(func_err))
        self.rclone_process.readyReadStandardOutput.connect(self.handle_stdout(func_out))
        self.rclone_process.start(command)'''

    def verifyDownloadLocation(self):
        self.downloadpageui.download_progress_2.setVisible(False)
        self.download_location = self.downloadpageui.download_location.text()
        if download_utils.verifyLocation(self.download_location) and self.username != 'CB Launcher':
            self.checkForSaves()
        elif download_utils.verifyLocation(self.download_location) and self.username == 'CB Launcher':
            self.download_final()
        else:
            self.downloadpageui.label_8.setText('Remove backslash from the end to continue')

    def checkForSaves(self): #Start rclone checks
        self.downloadpageui.stackedWidget.setCurrentWidget(self.downloadpageui.page_5)
        self.downloadpageui.label_5.setText("Checking for saves...")
        command = f'CBDownloader lsf "saves:{self.username}"'
        if self.rclone.checkSavesRclone(command):
            self.loadSaveOption()
        else:
            self.download_final()
                #rcloneProcess = rclone(command)
                #rcloneProcess.readyReadStandardOutput.connect(self.download_final)
                #rcloneProcess.readyReadStandardOutput.connect(self.test)
                #self.rclone(command, func_err=self.dowload_final, func_out=self.check_save_exists)

    def loadSaveOption(self):
        self.downloadpageui.stackedWidget.setCurrentWidget(self.downloadpageui.page_5)
        self.downloadpageui.label_5.setText("Cloud Save Found, would you like to load your save?")
        self.downloadpageui.loadsave.setVisible(True)
        self.downloadpageui.nosave.setVisible(True)

    '''def check_save_exists(self):
        try:
            fucksake = 0
            brow = self.stdout.replace('/', '')
            gae = brow.split('\n')
            for i in gae:
                if self.game_name == i:
                    fucksake += 1
                    
            if fucksake > 0:
                    self.downloadpageui.stackedWidget.setCurrentWidget(self.downloadpageui.page_5)
                    self.downloadpageui.label_5.setText("Cloud Save Found, would you like to load your save?")
                    self.downloadpageui.loadsave.setVisible(True)
                    self.downloadpageui.nosave.setVisible(True)
            else:
                self.download_final()
        except:
            try:
                self.download_final()
            except:
                pass'''

    def checkIfHasSaveProblem(self):
        self.fucksake = 0
        for i in cb_requests.save_gae:
            if self.game_name == i:
                self.fucksake += 1

    def load_save(self): #Check if save already exists on target pc
        self.downloadpageui.loadsave.setVisible(False)
        self.downloadpageui.nosave.setVisible(False)
        self.downloadpageui.label_5.setText("Loading Save...")
        self.downloadpageui.download_progress_2.setVisible(True)
        if self.checkIfHasSaveProblem():
            command = f'CBDownloader copy -P --stats-one-line "saves:{self.username}/{self.game_name}" "{self.download_location}{self.save_path}"'
            #downloadSaveRclone(command)
            #downloadSaveProgress(rclone(command))
            self.rclone.rclone(command, func_err=self.download_final, func_out=self.download_progress)
        else:
            command = f'CBDownloader copy -P --stats-one-line "saves:{self.username}/{self.game_name}" "{self.save_path}"'
            self.rclone(command, func_err=self.dowload_final, func_out=self.download_progress)

    def download_final(self): #Start game download
        self.downloadpageui.stackedWidget.setCurrentWidget(self.okaynow.page_6)
        try:
            download_location = self.downloadpageui.download_location.text()
            with open('config/progress.txt', 'w') as f:
                f.write('1')
            command = f'CBDownloader copy -P --stats-one-line --fast-list --transfers={self.parallel_transfers} "{self.game_download}" "{download_location}\\{self.game_name}"'
            self.rclone(command, func_err=self.dowload_final, func_out=self.download_progress)
            self.somepid = self.rclone_process.pid()
            self.counter = 0
        except:
            pass

    def downloadfinish(self):
        self.downloadpageui.close_download_5.setVisible(False)
        try:
            os.remove('config\\progress.txt')
        except:
            pass
        self.downloadpageui.status.setText("Finalizing...")
        self.okakaka()

    def desktopshortcut(self):
        if self.downloadpageui.create_shortcut.isChecked():
            download_utils.createShortcut(DESKTOP_DIRECTORY.format(self.pc_user), self.download_location, self.game_name, self.exepath)
            #destination = f"C:\\Users\\{self.pc_user}\\Desktop"
            #cb_modules.createshortcut(DESKTOP_DIRECTORY.format(self.pc_user), self.download_location, self.game_name, self.exepath)
        if self.downloadpageui.create_shortcut_2.isChecked():
            download_utils.createShortcut(STARTMENU_DIRECTORY.format(self.pc_user), self.download_location, self.game_name, self.exepath)
            #destination = f"C:\\Users\\{self.pc_user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs"
            #cb_modules.createshortcut(destination, self.download_location, self.pc_user, self.game_name, self.exepath)

    def updatejsonexists(self, x):
        x[self.game_name.replace(' ', '_').lower() + "_download"] = [
            {
                "game_name":f"{self.game_name}",
                "image":f"{self.image}",
                "exepath":f"{self.download_location + '/' + self.game_name + self.exepath}",
                "download_location":f"{self.download_location + '/' + self.game_name}"
            }
        ]
        return x

    def updatejsonnew(self):
        x = {self.game_name.replace(' ', '_').lower() + "_download":[
                        {
                            "game_name":f"{self.game_name}",
                            "image":f"{self.image}",
                            "exepath":f"{self.download_location + '/' + self.game_name + self.exepath}",
                            "download_location":f"{self.download_location + '/' + self.game_name}"
                        }
                    ]
                }
        return x

    def downloadsjson(self):
        try:
            self.download_location = self.download_location.replace('\\', '/')
        except:
            self.download_location = self.download_location
        if os.path.exists('config\\downloads.json'):
            with open('config\\downloads.json', 'r+') as f:
                x = json.load(f)
                jsonString = download_utils.updateJson(x, self.game_name, self.image, self.download_location, self.exepath)
                #x = self.updatejsonexists(x)
                f.seek(0)
                f.write(json.dumps(jsonString, indent=4))
                f.truncate()
        else:
            with open('config\\downloads.json', 'w') as f:
                jsonString = download_utils.updateJson({}, self.game_name, self.image, self.download_location, self.exepath)
                #x = self.updatejsonnew()
                f.write(json.dumps(jsonString, indent=4))

    def downloaded_game_button(self):
        button = cb_widgets.create_button(width=177, 
                                            height=265, 
                                            iconw=177, 
                                            iconh=260, 
                                            button_name=self.game_name.replace(' ', '_').lower() + "_download", 
                                            connectfunc=self.function)
        icon = QIcon(self.image)
        button.setIcon(icon)
        button.clicked.connect(self.function)
        self.ui.gridLayout_6.addWidget(button)

    def download_progress(self):
        if self.hundredcount == 10:
                self.rclone_process = None
                self.hundredcount = 0
                QTimer.singleShot(3000, self.download_final)
        else:
                stats = self.stdout.split(',')
                transferred = stats[0]
                percentage = stats[1]
                if int(percentage[0:percentage.index('%')]) == 100:
                    self.hundredcount += 1
                slash = transferred.index('/')
                before = transferred[:slash - 1]
                after = transferred[slash + 2:]
                self.downloadpageui.download_progress_2.setValue(int(percentage[0:percentage.index('%')]))
                if before == after and int(percentage[0:percentage.index('%')]) == 100:
                    self.hundredcount = 0
                    QTimer.singleShot(3000, self.download_final)

    def handle_stderr(self, func_err):
        try:
            data = self.rclone_process.readAllStandardError()
            stderr = bytes(data).decode("utf8")
            if 'ERROR' in stderr:
                self.rclone_process = None
                func_err
        except:
            pass

    def handle_stdout(self, func_out): #Check if save exists
        data = self.rclone_process.readAllStandardOutput()
        self.stdout = bytes(data).decode("utf8")
        self.rclone_process = None
        func_out
