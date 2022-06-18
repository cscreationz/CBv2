import os, pickle, getpass, sys, time, json, urllib.request, requests
from typing import Dict
from multiprocessing import Pool, Process
from dotenv import load_dotenv
from PySide2.QtGui import QImage, QBrush, QPainter, QWindow, QPixmap, QIcon, QColor, QCursor 
from PySide2.QtCore import QRect, Qt, Slot, QUrl
from PySide2.QtWidgets import QLabel, QGraphicsDropShadowEffect
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from source.utils import cb_videoplayer, cb_notification, cb_discordrpc, cb_profile, cb_widgets
from source.login import cb_login, login_utils
from source.download import cb_rclone, cb_downloadpage
from source.design import ui_window, py_toggle
from ... import cb_utils
import cb_gamepage
#from cb_files.apps.download import cb_download
from ..download import cb_rclone
from source.modules import *
from source.widgets import *
from PySide2 import QtCore

extDataDir = os.getcwd()
if getattr(sys, 'frozen', False):
    extDataDir = sys._MEIPASS
load_dotenv(dotenv_path=os.path.join(extDataDir, '.env'))

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = ui_window.Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        Settings.ENABLE_CUSTOM_TITLE_BAR = True
        self.toggle = py_toggle.PyToggle()
        self.ui.horizontalLayout_6.addWidget(self.toggle, Qt.AlignRight, Qt.AlignRight)
        self.ui.horizontalLayout_6.addWidget(self.ui.label100)
        self.toggle.stateChanged.connect(self.change_hentai_game_state)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.label_21.setText("<a href='http://gg.gg/cblgames'>Games Status</a>")
        self.ui.label_21.setOpenExternalLinks(True)
        self.ui.pushButton_6.clicked.connect(self.play_trailer)
        self.ui.pushButton_7.clicked.connect(self.check_if_download_in_progress)
        self.ui.pushButton_10.clicked.connect(self.back_page)
        self.ui.btn_home.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.home_page))
        self.ui.btn_games.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.games_page))
        #self.ui.btn_emulators.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.emulators_page))
        self.ui.btn_downloads.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.downloads_page))
        self.ui.settings.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.settings_page))
        self.ui.rclone_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page))
        self.ui.closeAppBtn.clicked.connect(lambda: self.close())
        self.ui.minimizeAppBtn.clicked.connect(lambda: self.showMinimized())
        self.ui.detroit_become_human_download.clicked.connect(self.game_page)
        self.ui.cyberpunk_2077_download.clicked.connect(self.game_page)
        self.ui.red_dead_redemption_2_download.clicked.connect(self.game_page)
        self.ui.forza_horizon_5_download.clicked.connect(self.game_page)
        self.ui.control_download.clicked.connect(self.game_page)
        self.ui.assassins_creed_valhalla_download.clicked.connect(self.game_page)
        self.ui.the_medium_download.clicked.connect(self.game_page)
        self.ui.pushButton_4.clicked.connect(self.change_pfp_window)
        self.ui.pushButton_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))
        self.ui.lineEdit.textChanged.connect(self.update_display)
        self.ui.lineEdit_2.textChanged.connect(self.search_apps)

        self.textbin_requests()
        self.discord_RPC()
        self.get_username_and_pcusername()
        self.initialize_arrays()
        self.paint_PFP()
        self.stretch_layouts()
        self.parse_downloaded_games_json()
        self.parse_games_database()
        self.download_PFP()
        self.completer()

        self.ui.titleRightInfo.setText(self.username)
        QTimer.singleShot(1000, self.aftersingleshot)

    def textbin_requests(self):
        """Retrieves data from request response"""
        self.changelog = requests.get(os.getenv('CHANGELOG')).text
        self.start_error_games = requests.get(os.getenv('GAEGAMES')).text
        self.save_error_games = requests.get(os.getenv('SAVEGAE')).text
        self.flagged_file_games = requests.get(os.getenv('FIXGAMES')).text
        gfn_request = requests.get(os.getenv('GFNSPECIFIC'))
        self.gfn_games = json.loads(gfn_request.text)
        games = requests.get(os.getenv('GAMES'))
        self.games_list = json.loads(games.text)

    def discord_RPC(self):
        """Starts Discord RPC pipeline. Passes if error"""
        try:
            cb_discordrpc.cblauncher()
        except:
            pass

    def get_username_and_pcusername(self):
        """Retrieves Username and PC Username
        
        Reads binary file and parses string to get username
        and uses getpass module to get pc username"""
        if os.path.exists('config\\settings.dat'):
            self.username, password = login_utils.get_login_details(cb_utils.readbinary('config\\settings.dat'))
            self.pc_user = getpass.getuser()
        else:
            self.username = cb_login.username
            self.pc_user = getpass.getuser()

    def initialize_arrays(self):
        """Create arrays to store buttons and their names"""
        self.indexbrow = 0
        self.game_names, self.app_names, self.hentai_games, self.button_names = []
        self.image_links = []
        self.app_frame = []
        self.dick = {}
        self.nonhen = []

    def paint_PFP(self):
        """Displays profile picture of user
        
        Checks if pfp.png exists. If exists, open image and paint rounded
        image onto app. Paint CB Launcher Icon if it doesn't exist"""
        if self.username != 'CB Launcher':
            pfp_path = os.getcwd() + "\\config\\pfp.png"
            if os.path.exists(pfp_path) == True:
                try:
                    imgdata = open(pfp_path, 'rb').read()
                    pixmap = cb_profile.mask_image(imgdata)
                    self.ui.big_socks.setGeometry(QRect(10, 5, 38, 38))
                    self.ui.normal_socks.setPixmap(QPixmap(pixmap))
                    self.ui.big_socks.setPixmap(QPixmap(pixmap))
                except:
                    self.ui.big_socks.setGeometry(QRect(-20, 0, 101, 81))
                    self.ui.big_socks.setPixmap(QPixmap(u":/games/cb"))
        else:
            self.ui.big_socks.setGeometry(QRect(-20, 0, 101, 81))
            self.ui.big_socks.setPixmap(QPixmap(u":/games/cb"))

    def stretch_layouts(self):
        """Configure X and Y axis for layouts depending on number of games"""
        for i in self.games_list.keys():
            for j in self.games_list[i]:
                if j["type"] == 'normal' or j["type"] == 'wow':
                    self.game_names.append(j["game_name"])
                    self.image_links.append(j["image_url"])
                    self.ui.comboBox.addItem(j["game_name"])
                elif j["type"] == 'app':
                    self.app_names.append(j["game_name"])
        self.ui.gridLayout_6.setColumnStretch(5, len(self.game_names))
        self.ui.gridLayout_6.setAlignment(Qt.AlignTop)
        self.ui.gridLayout_5.setColumnStretch(3, len(self.app_names))

    def parse_downloaded_games_json(self):
        """Parse Json data of downloaded games"""
        if os.path.exists('config\\downloads.json'):
            with open('config\\downloads.json') as f:
                games_data = json.load(f)
                for game in games_data.keys():
                    self.add_downloaded_games(games_data, game)

    def add_downloaded_games(self, game_json: Dict, game: Dict) -> None:
        """Add buttons and images for downloaded games"""
        for j in game_json[game]:
            button = cb_widgets.create_button(width=177, 
                                        height=265, 
                                        iconw=177, 
                                        iconh=260, 
                                        button_name=j["game_name"].replace(' ', '_').lower() + "_download", )
            icon = QPixmap(j["image"])
            button.setIcon(icon)
            button.clicked.connect(self.game_page)
            self.ui.gridLayout_6.addWidget(button)

    def parse_games_database(self):
        """Parse json data of games database"""
        for game in self.games_list.keys():
            self.configure_button_placement(game)

    def add_game_buttons(self, game: Dict) -> None:
        """Add buttons for all pc games"""
        button = cb_widgets.create_button(width=177,
                                            height=265,
                                            iconw=177,
                                            iconh=260,
                                            button_name=game["button_name"])
        self.button_names.append(button)
        if game["type"] == 'wow':
            self.hentai_games.append(button)
            button.setVisible(False)
        self.ui.gridLayout.addWidget(button, self.xaxis, self.yaxis)

    def add_app_buttons(self, app: Dict) -> None:
        """Add buttons for portable apps - no setup apps"""
        frame = cb_widgets.create_frame(width=150, height=150, frame_name=app["button_name"])
        button = cb_widgets.create_button(sub=frame, 
                                            width=150,
                                            height=150,
                                            iconw=140,
                                            iconh=140,
                                            button_name=app["button_name"])
        button.clicked.connect(self.apps)
        self.app_frame.append(frame)
        icon = QPixmap(app["image"])
        button.setIcon(icon)
        self.ui.gridLayout_5.addWidget(frame)

    def configure_button_placement(self, game: Dict) -> None:
        """Place buttons depending on X and Y axis"""
        self.xaxis = 0
        self.yaxis = 0
        for j in self.games_list[game]:
            if j["type"] == 'normal' or j["type"] == 'wow':
                self.add_game_buttons(j)
                self.yaxis += 1
                if self.yaxis % 6 == 0:
                    self.yaxis = 0
                    self.xaxis += 1
            elif j["type"] == 'app':
                self.add_app_buttons(j)
                self.app_names.append(j["game_name"])

    def download_PFP(self):
        """Start Rclone process to download profile picture of user"""
        command = f'CBDownloader copy -P --stats-one-line "saves:{self.username}/pfp.png" "{os.getcwd()}/config"'
        self.rclone = cb_rclone.RcloneDownloader()
        self.rclone.rclone(command)

    def completer(self):
        """Add auto-complete to text boxes to be able to search for games"""
        self.game_completer = QCompleter(self.game_names)
        self.game_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.lineEdit.setCompleter(self.game_completer)
        self.app_completer = QCompleter(self.app_names)
        self.app_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.lineEdit_2.setCompleter(self.app_completer)

    def play_trailer(self):
        """Parse json and get trailer link to play it"""
        pressed_button_name = self.sender()
        for game in self.games_list[pressed_button_name.objectName()]:
            cb_videoplayer.video(game["trailer"])

    def change_hentai_game_state(self):
        """Hides hentai games if NSFW is not checked. Display hentai games when NSFW toggle is checked"""
        if self.toggle.isChecked():
            for i in self.hentai_games:
                i.setVisible(True)
        else:
            for j in self.hentai_games:
                j.setVisible(False)

    def back_page(self):
        """Goes back a page by setting current page index to desired page index"""
        self.ui.stackedWidget.setCurrentIndex(self.page_index)

    def game_detail_images(self, pressed_button):
        """Grab images of selected game"""
        if self.checker == 4:
            self.checker = 0
            if pressed_button.objectName() in self.gfn_games.keys():
                self.game_details_page.feckme(self.gfn_games, pressed_button.objectName())
            else:
                self.game_details_page.feckme(self.games_list, pressed_button.objectName())
        else:
            self.betton6 = self.labels[self.checker]
            self.start_image6(self.imagelinks[self.checker])

    def game_page(self):
        """Set all labels and text on game details page"""
        self.page_index = self.ui.stackedWidget.currentIndex()
        self.pressed_button = self.sender()
        self.game_details_page = cb_gamepage.GamePage(self.ui, self.gfn_games, self.games_list, self.pressed_button)
        self.imagelinks, self.labels = self.game_details_page.setgamepage(self.pressed_button)
        self.game_detail_images(self.pressed_button)

    def adjust_stacked_widget(self):
        """Accomadate download window on stacked widget in main window"""
        try:
            self.stackedwidget_count = self.ui.stackedWidget_2.count()
            if self.stackedwidget_count > 1:
                self.ui.stackedWidget_2.removeWidget(self.stackedwidget_count - 1)
        except:
            pass

    def download_window(self):
        """Check if game is specific for GFN or not and open download window with those details"""
        parallel_transfers = self.ui.parallel_text.text()
        if self.sender().objectName() in self.gfn_games.keys() and self.pc_user == 'kiosk':
            games_list = self.gfn_games            
        else:
            games_list = self.games_list
        for i in games_list[self.sender().objectName()]:
            download_window = cb_downloadpage.DownloadPage(i["game_size"], i["game_name"], i["game_download"], i["exepath"], i["save_path"], parallel_transfers, self.ui.gridLayout_6, self.ui.rclone_button, self.game_page)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)
        self.adjust_stacked_widget()
        self.ui.stackedWidget_2.addWidget(download_window)
        self.ui.stackedWidget_2.setCurrentIndex(self.stackedwidget_count)

    def check_if_download_in_progress(self):
        """Check if progress.txt exists. If it does notify download in progress, if not open download window"""
        if os.path.exists('config\\progress.txt'): #Message if a game is downloading
            parent = self
            desktop = False
            pixmap = QPixmap(":/games/window2")
            cb_notification.QToaster.showMessage(
                parent, 'Another download is in progress', icon=pixmap, corner='TopRight', desktop=desktop)
        else:
            self.download_window()

    def set_temporary_pfp(self):
        """Open File Dialog to choose a temporary .png file as profile"""
        filelocation = QFileDialog.getOpenFileName(self, None, None, "Images (*.png)")
        imgpath = filelocation[0]
        imgdata = open(imgpath, 'rb').read()
        pixmap = cb_profile.mask_image(imgdata)
        self.ui.label.setGeometry(QRect(10, 5, 38, 38))
        self.ui.logo.setPixmap(QPixmap(pixmap))
        self.ui.label.setPixmap(QPixmap(pixmap))

    def change_pfp_window(self):
        """Open PFP window to allow user to change PFP permanantly"""
        if self.username != 'CB Launcher':
            self.main = cb_profile.ProfileWindow(self.ui.normal_socks, self.ui.big_socks)
            self.main.show()
        else:
            self.set_temporary_pfp()

    def determine_hentai_status(self):
        """Hide hentai games when searching for any game if NSFW toggle is OFF. Display hentai games when searching and NSFW toggle is ON"""
        for j in self.hentai_games:
                if self.toggle.isChecked():
                    j.setVisible(True)
                else:
                    j.setVisible(False)

    def update_display(self, text):
        """Displays game being searched for and hides others"""
        for i in self.button_names:
            if text.lower() in i.objectName().replace('_', ' '):
                i.setVisible(True)
            else:
                i.setVisible(False)
            self.determine_hentai_status()

    def search_apps(self, text):
        """Display app being searched for and hide others"""
        for j in self.app_frame:
            if text.lower() in j.objectName().replace('_', ' '):
                j.setVisible(True)
            else:
                j.setVisible(False)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos() 
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor)) 
            
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:  
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()
            
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
        
    def aftersingleshot(self):
        version = '2.35'
        response = requests.get(os.getenv('UPDATE'))
        if response.text == version:
            pass
        else:
            parent = self
            desktop = False
            pixmap = QPixmap(":/games/window2")
            cb_notification.QToaster.showMessage(
                parent, "You're running an outdated version of CB Launcher, run CB Updater to update the program", icon=pixmap, corner='TopRight', desktop=desktop)

        self.checker = 0
        self.get_image6 = QNetworkAccessManager()
        self.get_image6.finished.connect(self.image_final6)
        '''self.get_image = QNetworkAccessManager()
        self.get_image.finished.connect(self.image_final)
        self.get_image2 = QNetworkAccessManager()
        self.get_image2.finished.connect(self.image_final2)
        self.get_image3 = QNetworkAccessManager()
        self.get_image3.finished.connect(self.image_final3)
        self.get_image4 = QNetworkAccessManager()
        self.get_image4.finished.connect(self.image_final4)
        self.get_image5 = QNetworkAccessManager()
        self.get_image5.finished.connect(self.image_final5)
        self.lan = len(self.nonhen)
        num, div = self.lan, 5
        self.nig = [num // div + (1 if x < num % div else 0) for x in range(div)]
        print(self.nig)
        self.first_counter = 0
        self.second_counter = 0
        self.third_counter = 0
        self.fourth_counter = 0
        self.fifth_counter = 0
        self.first_batch = self.nonhen[0:self.nig[0] + 1]
        self.second_batch = self.nonhen[self.nig[0] + 1:(self.nig[0] + self.nig[1]) + 1]
        self.third_batch = self.nonhen[(self.nig[0] + self.nig[1]) + 1:(self.nig[0] + self.nig[1] + self.nig[2]) + 1]
        self.fourth_batch = self.nonhen[(self.nig[0] + self.nig[1] + self.nig[2]) + 1:(self.nig[0] + self.nig[1] + self.nig[2] + self.nig[3]) + 1]
        self.fifth_batch = self.nonhen[(self.nig[0] + self.nig[1] + self.nig[2] + self.nig[3]) + 1:(self.nig[0] + self.nig[1] + self.nig[2] + self.nig[3] + self.nig[4]) + 1]
        self.bich()
        self.bich2()
        self.bich3()
        self.bich4()
        self.bich5()

    def bich(self):
        try:
            if self.first_counter == self.nig[0]:
                pass
            else:
                self.betton = self.first_batch[self.first_counter]
                url = self.dick.get(self.betton)
                self.start_image(url)
        except:
            pass

    def bich2(self):
            if self.second_counter == self.nig[1]:
                pass
            else:
                self.betton2 = self.second_batch[self.second_counter]
                url = self.dick.get(self.betton2)
                self.start_image2(url)

    def bich3(self):
        try:
            if self.third_counter == self.nig[2]:
                pass
            else:
                self.betton3 = self.third_batch[self.third_counter]
                url = self.dick.get(self.betton3)
                self.start_image3(url)
        except:
            pass

    def bich4(self):
        try:
            if self.fourth_counter == self.nig[3]:
                pass
            else:
                self.betton4 = self.fourth_batch[self.fourth_counter]
                url = self.dick.get(self.betton4)
                self.start_image4(url)
        except:
            pass

    def bich5(self):
        try:
            if self.fifth_counter == self.nig[4]:
                pass
            else:
                self.betton5 = self.fifth_batch[self.fifth_counter]
                url = self.dick.get(self.betton5)
                self.start_image5(url)
        except:
            pass

    def networkaccess(self, image):
        self.get_image.finished.connect(self.image_final)
        self.start_image(image)'''





    def pagesave(self):
        parent = self
        desktop = False
        pixmap = QPixmap(":/games/window2")
        cb_notification.QToaster.showMessage(
            parent, 'Save Game Uploaded', icon=pixmap, corner='TopRight', desktop=desktop)
        self.ui.plainTextEdit.setPlainText("Save game uploaded")
        self.p = None







    '''def downloadedappcheck(self):
        if os.path.exists('config\\progress.txt'): #Message if a game is downloading
            parent = self
            desktop = False
            pixmap = QPixmap(":/games/window2")
            cb_notification.QToaster.showMessage(
                parent, 'Another download is in progress', icon=pixmap, corner='TopRight', desktop=desktop)
        else:
            if os.path.exists("apps") == True:
                pass
            else:
                os.mkdir('apps')

    def openexistingapp(self):
        parent = self
        desktop = False
        pixmap = QPixmap(":/games/window2")
        cb_notification.QToaster.showMessage(
            parent, f'Starting - {self.name}', icon=pixmap, corner='TopRight', desktop=desktop)
        pattii = QProcess()
        pattii.startDetached(f'"{self.exepath}"')

    def downloadapp(self, game_download):
        parent = self
        desktop = False
        pixmap = QPixmap(":/games/window2")
        cb_notification.QToaster.showMessage(
            parent, f'Downloading - {self.name}', icon=pixmap, corner='TopRight', desktop=desktop)

        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setVisible(True)
        initLoop = QEventLoop()
        pool = Pool(processes=1)
        pool.apply_async(self.apptest(game_download), [2], callback=lambda exitCode: initLoop.exit(exitCode))
        initLoop.exec_()

    def apps(self):
        app_name = self.sender()
        for i in self.games_list[app_name.objectName()]:
            self.name = i["game_name"]
            game_download = i["game_download"]
            self.exepath = i["exepath"]
            #self.exepath = exebefore.replace('/', '\\')
            self.link = i["link"]

        if os.path.exists(self.exepath):
            self.openexistingapp()
        else:
            self.downloadapp(game_download)


    def startappdownload(self, game_download):
        with open('config\\progress.txt', 'w') as f:
            f.write('1')

        wow = os.getcwd()
        self.rclone_process = QProcess()
        self.rclone_process.readyReadStandardOutput.connect(self.downloadaepp)
        self.rclone_process.start(f'CBDownloader copy -v --progress "{game_download}" "{wow}\\apps\\{self.name}"')

        return 0

    def downloadappremaining(self):
        if self.link != ' ':
            r = requests.get(self.link, allow_redirects=True) #Download Updater
            open(os.getcwd() + f"\\apps\\{self.name}\\{self.name}.exe", 'wb').write(r.content)

    def startdownloadedapp(self):
        parent = self
        desktop = False
        pixmap = QPixmap(":/games/window2")
        cb_notification.QToaster.showMessage(
            parent, f'Starting - {self.name}', icon=pixmap, corner='TopRight', desktop=desktop)

        pattii = QProcess()
        pattii.startDetached(f'"{self.exepath}"')

    def opendownloadedapp(self):
        try:
            os.remove('config\\progress.txt')
        except:
            pass

        self.downloadappremaining()
        self.startdownloadedapp()'''

    def save_brow(self): #Display Results
        self.ui.plainTextEdit.setPlainText("Save Game Uploaded")
        self.p = None

    @Slot(str)
    def start_image(self, url):
        request = QNetworkRequest(QUrl(url))
        self.get_image.get(request)

    @Slot(QNetworkReply)
    def image_final(self, reply):
        try:
            target = reply.attribute(QNetworkRequest.RedirectionTargetAttribute)
            if reply.error():
                print("error: {}".format(reply.errorString()))
                return
            elif target:
                newUrl = reply.url().resolved(target)
                self.start_image(newUrl)
                return
            pixmap = QPixmap()
            pixmap.loadFromData(bytes(reply.readAll()))
            icon = QIcon(pixmap)
            self.betton.setIcon(icon)
            self.first_counter += 1
            #print(self.counter)
            self.bich()
        except:
            pass
        #butten.setIcon(icon)
        '''try:
            botton = self.button_woo[self.button_counter + 1]
            botton.setIcon(icon)
            self.button_counter += 1
        except Exception as e:
            pass'''

    @Slot(str)
    def start_image2(self, url):
        request = QNetworkRequest(QUrl(url))
        self.get_image2.get(request)

    @Slot(QNetworkReply)
    def image_final2(self, reply):
        try:
            target = reply.attribute(QNetworkRequest.RedirectionTargetAttribute)
            if reply.error():
                print("error: {}".format(reply.errorString()))
                return
            elif target:
                newUrl = reply.url().resolved(target)
                self.start_image(newUrl)
                return
            pixmap = QPixmap()
            pixmap.loadFromData(bytes(reply.readAll()))
            icon = QIcon(pixmap)
            self.betton2.setIcon(icon)
            self.second_counter += 1
            #print(self.counter)
            self.bich2()
        except:
            pass
        #butten.setIcon(icon)
        '''try:
            botton = self.button_woo[self.button_counter + 1]
            botton.setIcon(icon)
            self.button_counter += 1
        except Exception as e:
            pass'''

    @Slot(str)
    def start_image3(self, url):
        request = QNetworkRequest(QUrl(url))
        self.get_image3.get(request)

    @Slot(QNetworkReply)
    def image_final3(self, reply):
        try:
            target = reply.attribute(QNetworkRequest.RedirectionTargetAttribute)
            if reply.error():
                print("error: {}".format(reply.errorString()))
                return
            elif target:
                newUrl = reply.url().resolved(target)
                self.start_image(newUrl)
                return
            pixmap = QPixmap()
            pixmap.loadFromData(bytes(reply.readAll()))
            icon = QIcon(pixmap)
            self.betton3.setIcon(icon)
            self.third_counter += 1
            #print(self.counter)
            self.bich3()
        except:
            pass
        #butten.setIcon(icon)
        '''try:
            botton = self.button_woo[self.button_counter + 1]
            botton.setIcon(icon)
            self.button_counter += 1
        except Exception as e:
            pass'''

    @Slot(str)
    def start_image4(self, url):
        request = QNetworkRequest(QUrl(url))
        self.get_image4.get(request)

    @Slot(QNetworkReply)
    def image_final4(self, reply):
        try:
            target = reply.attribute(QNetworkRequest.RedirectionTargetAttribute)
            if reply.error():
                print("error: {}".format(reply.errorString()))
                return
            elif target:
                newUrl = reply.url().resolved(target)
                self.start_image(newUrl)
                return
            pixmap = QPixmap()
            pixmap.loadFromData(bytes(reply.readAll()))
            icon = QIcon(pixmap)
            self.betton4.setIcon(icon)
            self.fourth_counter += 1
            #print(self.counter)
            self.bich4()
        except:
            pass
        #butten.setIcon(icon)
        '''try:
            botton = self.button_woo[self.button_counter + 1]
            botton.setIcon(icon)
            self.button_counter += 1
        except Exception as e:
            pass'''

    @Slot(str)
    def start_image5(self, url):
        request = QNetworkRequest(QUrl(url))
        self.get_image5.get(request)

    @Slot(QNetworkReply)
    def image_final5(self, reply):
        try:
            target = reply.attribute(QNetworkRequest.RedirectionTargetAttribute)
            if reply.error():
                print("error: {}".format(reply.errorString()))
                return
            elif target:
                newUrl = reply.url().resolved(target)
                self.start_image(newUrl)
                return
            pixmap = QPixmap()
            pixmap.loadFromData(bytes(reply.readAll()))
            icon = QIcon(pixmap)
            self.betton5.setIcon(icon)
            self.fifth_counter += 1
            #print(self.counter)
            self.bich5()
        except:
            pass
        #butten.setIcon(icon)
        '''try:
            botton = self.button_woo[self.button_counter + 1]
            botton.setIcon(icon)
            self.button_counter += 1
        except Exception as e:
            pass'''

    @Slot(str)
    def start_image6(self, url):
        request = QNetworkRequest(QUrl(url))
        self.get_image6.get(request)

    @Slot(QNetworkReply)
    def image_final6(self, reply):
        try:
            target = reply.attribute(QNetworkRequest.RedirectionTargetAttribute)
            if reply.error():
                print("error: {}".format(reply.errorString()))
                return
            elif target:
                newUrl = reply.url().resolved(target)
                self.start_image6(newUrl)
                return
            pixmap = QPixmap()
            pixmap.loadFromData(bytes(reply.readAll()))
            self.betton6.setPixmap(pixmap)
            if self.checker == 0:
                self.ui.label_25.setPixmap(pixmap)
            self.checker += 1
            print(self.checker)
            self.gamedetailimages(self.pressed_button)
        except:
            pass
        #butten.setIcon(icon)
        '''try:
            botton = self.button_woo[self.button_counter + 1]
            botton.setIcon(icon)
            self.button_counter += 1
        except Exception as e:
            pass'''