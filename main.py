import sys, os, multiprocessing, cb_utils
from typing import List
from PySide2.QtGui import QFontDatabase, QIcon, QPixmap
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication
from source.login import cb_login, login_utils
from source.window import cb_window
from source.utils import cb_messagebox, cb_splashscreen, cb_notification

list_of_folders_needed: List[str] = ['config', 'resources']
files_to_delete: List[str] = ['config\\progress.txt', 'CB Updater.exe']
movie: str = ':/games/loading'

if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont(':/font/ubuntu')
    app.setWindowIcon(QIcon(":/games/window2"))
    try:
        cb_utils.check_if_files_exist(list_of_folders_needed)
        cb_utils.delete_files(files_to_delete)
        if os.path.exists('config\\settings.dat'):
            username, password = login_utils.get_login_details(cb_utils.readbinary('config\\settings.dat'))
            if login_utils.login(username, password):
                splashscreen = cb_splashscreen.MovieSplashScreen(movie)
                splashscreen.show()
                main_window = cb_window.MainWindow()
                main_window.show()
                splashscreen.close()
            else:
                cb_notification.QToaster.showMessage(
                    None, 'Auth Failed', icon=QPixmap(":/games/window2"), corner='TopRight', desktop=True)
                login_window = cb_login.LoginPage()
                login_window.show()
                cb_utils.delete_files(['config\\settings.dat'])
        else:
            login_window = cb_login.LoginPage()
            login_window.show()
    except Exception as error_string:
        message_box = cb_messagebox.MessageBox()
        message_box.displayMessageBox(window_title="CB Launcher", error=str(error_string))
        splashscreen.close()
    sys.exit(app.exec_())