import sys
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PySide2.QtGui import QDesktopServices
from PySide2.QtCore import QUrl

def video(trailer: str) -> None:
    """HTML View to display game trailer taking link as parameter"""
    class WebEnginePage(QWebEnginePage):
        def acceptNavigationRequest(self, url,  _type, isMainFrame):
            if _type == QWebEnginePage.NavigationTypeLinkClicked:
                QDesktopServices.openUrl(url)
                return False
            return True

    class HtmlView(QWebEngineView):
        def __init__(self, *args, **kwargs):
            QWebEngineView.__init__(self, *args, **kwargs)
            self.setPage(WebEnginePage(self))

    w = HtmlView()
    w.setWindowTitle('Trailer')
    w.setFixedWidth(854)
    w.setFixedHeight(465)
    w.setStyleSheet('border-radius: 10px;')
    w.load(QUrl(trailer))
    w.show()
    sys.exit(w.exec_())