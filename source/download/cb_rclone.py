from PySide2.QtCore import QProcess, QTimer
from PySide2.QtGui import QPixmap
from source.utils import cb_notification
from ... import cb_utils
import download_utils
import threading, os

class RcloneDownloader():

    def __init__(self, ui):
        self.ui = ui

    def rclone(self, command):
        self.rclone_process = QProcess()
        self.rclone_process.start(command)

    def handleStderr(self):
        try:
            data = self.rclone_process.readAllStandardError()
            stderr = bytes(data).decode("utf8")
            if 'ERROR' in stderr:
                self.rclone_process = None
        except:
            pass

    def handleStdout(self):
        data = self.rclone_process.readAllStandardOutput()
        self.stdout = bytes(data).decode("utf8")
        self.rclone_process = None

    def checkSavesRclone(self, command):
        self.rclone(command)
        self.rclone_process.readyReadStandardOutput.connect(self.handleStderr)
        self.rclone_process.readyReadStandardOutput.connect(self.parseSaveProgress)

    def parseSaveProgress(self):
        stdout = bytes(self.rclone_process.readAllStandardOutput()).decode("utf8")
        saveCounter = download_utils.countMatchedSaves(stdout)
        if saveCounter > 0:
            self.loadSaveOption()

    def loadSaveOption(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_5)
        self.ui.label_5.setText("Cloud Save Found, would you like to load your save?")
        self.ui.loadsave.setVisible(True)
        self.ui.nosave.setVisible(True)

    def saveDownloadProgress(self, command):
        self.rclone(command)
        self.rclone_process.readyReadStandardOutput.connect(self.checkIfSaveDownloadComplete)

    def checkIfSaveDownloadComplete(self):
        if self.hundredcount == 10:
            self.rclone_process = None
            self.hundredcount = 0
        else:
            stdout = bytes(self.rclone_process.readAllStandardOutput()).decode("utf8")
            self.parseSaveDownloadProgress(stdout)

    def completeDownload(self, progress):
        if progress == 100:
            self.hundredcount += 1

    def compareCurrentAndTotal(self, before, after, progress):
        if before == after and progress == 100:
            self.hundredcount = 0
            QTimer.singleShot(3000, self.download_final)

    def parseSaveDownloadProgress(self, stdout):
        stats = stdout.split(',')
        transferred = stats[0]
        percentage = stats[1]
        progress = int(percentage[0:percentage.index('%')])
        self.completeDownload(progress)
        slash = transferred.index('/')
        before = transferred[:slash - 1]
        after = transferred[slash + 2:]
        self.ui.download_progress_2.setValue(progress)
        self.compareCurrentAndTotal(before, after, progress)

    def finalDownloadCommand(self, command):
        self.rclone(command)
        self.rclone_process.readyReadStandardOutput.connect(self.checkIfGameDownloadComplete)

    def checkIfGameDownloadComplete(self):
        if self.hundredcount == 10:
            self.rclone_process = None
            self.hundredcount = 0
        else:
            stdout = bytes(self.rclone_process.readAllStandardOutput()).decode("utf8")
            self.parseGameDownloadProgress(stdout)

    def compareCurrentAndTotalFinal(self, before, after, progress):
        if before == after and progress == 100:
            QTimer.singleShot(3000, self.endprocess)
            self.ui.close_download_5.setVisible(False)
            self.process_finished()

    def parseGameDownloadProgress(self, stdout):
        stats = stdout.split(',')
        transferred = stats[0]
        percentage = stats[1]
        speed = stats[2]
        eta = stats[3]
        progress = int(percentage[0:percentage.index('%')])
        self.completeDownload(progress)
        self.ui.download_progress.setValue(progress)
        self.ui.ETA_2.setText(transferred)
        self.ui.label_3.setText(speed)
        self.ui.ETA.setText(eta)
        slash = transferred.index('/')
        before = transferred[:slash - 1]
        after = transferred[slash + 2:]
        self.compareCurrentAndTotalFinal(before, after, progress)

    def parseJson(self):
        try:
            self.download_location = self.download_location.replace('\\', '/')
        except:
            self.download_location = self.download_location
        if os.path.exists('config\\downloads.json'):
            fileObject, jsonContent = cb_utils.readjson('config\\downloads.json')
            download_utils.updateExistingJson(jsonContent)
            download_utils.rewriteJsonFile(fileObject, jsonContent)
        else:
            fileObject = cb_utils.writejson('config\\downloads.json')
            jsonObject = download_utils.createNewJson()
            download_utils.writeJsonFile(fileObject, jsonObject)

    def downloadQuarantinedFiles(self):
        if download_utils.checkIfMissingFiles() > 0:
            link, file_name, type_of_file = download_utils.retrieveMissingFileDetail()
            if type_of_file == 'file':
                download_utils.downloadMissingFiles(link, file_name)
            else:
                download_utils.downloadMissingZip(link, file_name)

    def parseShortcut(self):
        if self.ui.create_shortcut.isChecked():
            download_utils.createShortcut()
        if self.ui.create_shortcut_2.isChecked():
            download_utils.createShortcut()

    def finalizeDownload(self):
        threading.Thread(target=self.parseShortcut).start()
        threading.Thread(target=self.parseJson).start()
        threading.Thread(target=self.downloadQuarantinedFiles).start()

    def notifyDownloadComplete(self):
        self.finalizeDownload()
        self.ui.status.setText("Downloaded")
        self.ui.pushButton.setVisible(True)
        self.ui.label_2.setText(" ")
        self.ui.ETA.setText(" ")
        self.ui.ETA_2.setText(" ")
        parent = self
        desktop = False
        pixmap = QPixmap(":/games/window2")
        cb_notification.QToaster.showMessage(
            parent, f'{self.game_name} - Download Complete', icon=pixmap, corner='TopRight', desktop=desktop)

    def startGame(self, command):
        self.rclone(command)
        self.rclone_process.stateChanged.connect(self.gameState)

    def gameState(self, state):
        states = {QProcess.NotRunning: 'Not running',
                QProcess.Starting: 'Starting',
                QProcess.Running: 'Running',
            }
        state_name = states[state]
        if state_name == 'Not running':
            self.autoSave()

    def autoSave(self, command):
        self.rclone(command)
        self.rclone_process.readyReadStandardOutput.connect(self.handle_stdoutsaveup)

    def checkIfSaveUploaded(self):
        if 'There was nothing to transfer' in stdout:
                self.rclone_process = None
        else:
            stdout = bytes(self.rclone_process.readAllStandardOutput()).decode("utf8")
            self.parseSaveDownload(stdout)

    def parseSaveDownload(self, stdout):
        stats = stdout.split(',')
        transferred = stats[0]
        percentage = stats[1]
        progress = int(percentage[0:percentage.index('%')])
        slash = transferred.index('/')
        before = transferred[:slash - 1]
        after = transferred[slash + 2:]
        if before == after and progress == 100:                
            QTimer.singleShot(3000, self.endprocess)
            self.saveuploaded()

    