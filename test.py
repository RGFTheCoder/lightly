import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

class MainForm(QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.tabWidget = QTabWidget(self)        
        self.setCentralWidget(self.tabWidget)        
        self.loadUrl(QUrl('https://www.google.com/'))

    def loadUrl(self, url):    
        view = QWebEngineView()  
        view.loadFinished.connect(self.loadFinished)
        self.tabWidget.setCurrentIndex(self.tabWidget.addTab(view, 'loading...'))
        view.load(url)

    def loadFinished(self, ok):
        index = self.tabWidget.indexOf(self.sender())
        self.tabWidget.setTabText(index, self.sender().url().host())


def main():
    app = QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()