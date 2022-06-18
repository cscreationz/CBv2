from PySide2.QtGui import QPixmap, QMovie

import os
import json

class GamePage():

    def __init__(self, ui, gfn_games, games_list, secks_button):
        self.ui = ui
        self.gfn_games, self.games_list, self.checker = gfn_games, games_list, 0
        self.secks_button = secks_button

    def start_loading(self):
        movie = QMovie('C:\\Users\\cotton\\Desktop\\to transfer\\skskksksks\\CB.gif')
        self.ui.label_23.setMovie(movie)
        movie.start()

    def downloadedgamecheck(self, secks_button):
        if os.path.exists('config\\downloads.json'):
            with open('config\\downloads.json', 'r') as f:
                x = json.load(f)
                if secks_button.objectName() in x.keys():
                    self.ui.pushButton_7.setVisible(False)
                    self.ui.pushButton_8.setVisible(True)
                    self.ui.pushButton_9.setVisible(True)
                    self.ui.pushButton_8.setObjectName(secks_button.objectName())
                    self.ui.pushButton_9.setObjectName(secks_button.objectName())
                    return True
        else:
            self.ui.pushButton_7.setVisible(True)
            self.ui.pushButton_8.setVisible(False)  
            self.ui.pushButton_9.setVisible(False)
            return False

    def retrievedetails(self, games_list, button_name):
        for i in games_list[button_name]:
            self.location_load = i["image_widget"]
            self.screenshot_1 = i["screenshot_1"]
            self.screenshot_2 = i["screenshot_2"]
            self.mature = i["maturity"]
            if '17' in self.mature:
                self.maturity_link = "https://store-images.microsoft.com/image/global.53975.image.32437939-2f27-4e79-8431-5f5866f32908.3dc74b18-4153-423c-b367-bdcfd34ac658"
            elif 'EVERYONE' in self.mature:
                self.maturity_link = "https://store-images.microsoft.com/image/global.23456.image.87f616db-3cfc-4611-b3b8-c57bbb87de71.7e7baf95-3edb-4b7c-a960-75e7537b07c9"
            elif 'TEEN' in self.mature:
                self.maturity_link = "https://store-images.microsoft.com/image/global.17268.image.4cc004ee-a56d-4f11-ae99-67a89379b743.13d51d69-d3ba-4760-8fdf-f996abafa50a"

    def retreive(self, secks_button):
        if secks_button.objectName() in self.gfn_games.keys() and self.pc_user == 'kiosk':
            self.retrievedetails(self.gfn_games, secks_button.objectName())
        else:
            self.retrievedetails(self.games_list, secks_button.objectName())

    def setgamepage(self, secks_button):
        print(secks_button.objectName())
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_5)
        self.ui.rclone_button.setVisible(True)
        self.ui.pushButton_6.setObjectName(secks_button.objectName())
        self.ui.pushButton_7.setObjectName(secks_button.objectName())
        self.start_loading()
        self.downloadedgamecheck(secks_button)
        self.retreive(secks_button)

        if os.path.exists('config\\progress.txt'):
            self.image_links = [self.location_load, self.screenshot_1, self.screenshot_2, self.maturity_link]
            self.labels = [self.ui.label_11, self.ui.label_17, self.ui.label_20, self.ui.label_22]
            return self.image_links, self.labels
        else:
            self.image_links = [self.location_load, self.screenshot_1, self.screenshot_2, self.maturity_link]
            self.labels = [self.ui.label_11, self.ui.label_17, self.ui.label_20, self.ui.label_22]
            #self.gamedetailimages(secks_button)
            return self.image_links, self.labels

    def feckme(self, games_list, button_name):
        print('no results')
        for i in games_list[button_name]:
            #icon = QPixmap(self.image)
            self.ui.label.setScaledContents(True)
            self.ui.label.setFixedSize(177, 265)
            #self.ui.label.setPixmap(icon)
            self.ui.label_5.setText(i["game_name"])
            self.ui.textEdit_2.setText(i["description"])
            #self.ui.textEdit_4.setText(mature)
            self.ui.textEdit_3.setText(f'{i["developer"]}   �    {i["genre"]}   �    {i["release_date"]}   �    {i["game_size"]}    �    {i["rating"]}')
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_4)