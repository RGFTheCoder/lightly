from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

import os
import sys

# if str[-1:] == '/':
#     urlcode
# else:
#     searchcode

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MainWindow(QMainWindow):
    def home(self):
        # self.currentview.load(QUrl("https://google.com/"))
        self.loadUrl(QUrl("https://google.com/"))
        
    def update_urlbar(self, q):

        if q.scheme() == "https":
            self.httpsicon.setPixmap(QPixmap(os.path.join("res","icons","Safe_24px.png")))

        else:
            self.httpsicon.setPixmap(QPixmap(os.path.join("res","icons","Unsafe_24px.png")))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)
    def navigate_to_url(self):
        view = self.currentview
        url = self.urlbar.text()
        # if url[-1:] == '/':
        
        if url[0:1] == '/' or url[0:8] == 'https://' or url[0:8] == 'http://':
            if url[0:8] == 'https://' or url[0:8] == 'http://':
                url = url
            else:
                url = "https://" + url

            view.setUrl(QUrl(url))
        else:
            view.setUrl(QUrl("https://www.google.com/search?q="+url))
    def loadUrl(self, url):    
        view = QWebEngineView()
        self.currentview = view
        
        
        view.loadFinished.connect(self.loadFinished)
        self.tabs.setCurrentIndex(self.tabs.addTab(view, 'loading...'))
        view.load(url)

    def loadFinished(self, ok):
        index = self.tabs.indexOf(self.sender())
        self.tabs.setTabText(index, self.sender().url().host())
    def connectTools(self):
        self.currentview = self.tabs.widget(self.tabs.currentIndex())
        # print(self.currentview.reload())
        if hasattr(self, "reload_btn"):
            self.reload_btn.triggered.connect(self.currentview.reload)
            self.back_btn.triggered.connect(self.currentview.back)
            self.forward_btn.triggered.connect(self.currentview.forward)
            self.currentview.urlChanged.connect(self.update_urlbar)
            self.urlbar.setText(self.currentview.url().toString());
            
    def closetab(self, index):
        self.tabs.removeTab(index)

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.currentChanged.connect(self.connectTools)
        self.tabs.tabCloseRequested.connect(self.closetab)

        self.browser = QWebEngineView()
        self.loadUrl(QUrl("https://google.com/"))
        # self.loadUrl(QUrl("https://youtube.com/"))
        

        self.setCentralWidget(self.tabs)
        navtb = QToolBar("Navigation")
        navtb.setMovable(False)
        navtb.setIconSize(QSize(24,24))
        # navtb.setBaseSize(QSize(32,32))
        self.addToolBar(navtb)

        self.back_btn = QAction(QIcon(os.path.join("res","icons","Back_64px.png")), "Back", self)
        self.back_btn.setStatusTip("Back to previous page")
        self.back_btn.triggered.connect(self.currentview.back)
        navtb.addAction(self.back_btn)
        
        self.forward_btn = QAction(QIcon(os.path.join("res","icons","Forward_64px.png")), "Forward", self)
        self.forward_btn.setStatusTip("Forward to next page")
        self.forward_btn.triggered.connect(self.currentview.forward)
        navtb.addAction(self.forward_btn)
        
        self.reload_btn = QAction(QIcon(os.path.join("res","icons","Refresh_64px.png")), "Reload", self)
        self.reload_btn.setStatusTip("Reload the current page")
        self.reload_btn.triggered.connect(self.currentview.reload)
        navtb.addAction(self.reload_btn)
        
        home_btn = QAction(QIcon(os.path.join("res","icons","Home_64px.png")), "Home", self)
        home_btn.setStatusTip("Go to Home")
        home_btn.triggered.connect(self.home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(os.path.join("res","icons","Unsafe_24px.png")))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        self.currentview.urlChanged.connect(self.update_urlbar)

        self.show()
        self.setWindowTitle("Atlas Lightly")
        self.setWindowIcon( QIcon(os.path.join('res',os.path.join('icons','icon.png'))))
    




app = QApplication(sys.argv);
app.setApplicationName("Atlas Lightly")
app.setOrganizationName("Atlas")
app.setOrganizationDomain("atlas.net")


window = MainWindow()

app.exec_()