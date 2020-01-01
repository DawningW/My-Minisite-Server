#coding=utf-8

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QAxContainer import QAxWidget
# from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        titleheight = 20

        self.resize(720, titleheight + 448)
        self.setWindowIcon(QIcon('./client/icon.ico'))
        self.setWindowTitle('我的热点新闻客户端')
        self.setWindowFlags(Qt.FramelessWindowHint | self.windowFlags())
        self.setCentralWidget(QWidget(self))

        self.vlayout = QVBoxLayout(self.centralWidget())
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.vlayout.setSpacing(0)

        titlewidget = QWidget(self.centralWidget())
        titlewidget.setFixedWidth(self.width())
        titlewidget.setFixedHeight(titleheight)

        self.hlayout = QHBoxLayout(titlewidget)
        self.hlayout.setContentsMargins(0, 0, 0, 0)
        self.hlayout.setSpacing(0)
        self.vlayout.addWidget(titlewidget)

        self.hlayout.addStretch()

        self.buttonminimize = QPushButton(titlewidget)
        self.buttonminimize.setToolTip("Minimize")
        self.buttonminimize.clicked.connect(self.onClicked)
        self.hlayout.addWidget(self.buttonminimize, 0, Qt.AlignRight | Qt.AlignTop)

        self.buttonclose = QPushButton(titlewidget)
        self.buttonclose.setToolTip("Close");
        self.buttonclose.clicked.connect(self.onClicked)
        self.hlayout.addWidget(self.buttonclose, 0, Qt.AlignRight | Qt.AlignTop)

        self.webview = QAxWidget(self.centralWidget())
        self.webview.setControl("{8856F961-340A-11D0-A96B-00C04FD705A2}")
        self.webview.setProperty("DisplayAlerts", False)
        self.webview.setProperty("DisplayScrollBars", True)
        self.webview.dynamicCall("Navigate(const QString&)", "http://127.0.0.1:80/kingsoft/default")
        self.vlayout.addWidget(self.webview)

        #self.webview = QWebEngineView(self)
        #self.webview.load(QUrl("https://hotnews.duba.com/minisite/1339/"))
        #self.webview.show()
        #self.vlayout.addWidget(self.webview)

    def onClicked(self):
        window = self.window();
        button = self.sender();
        if (button == self.buttonminimize):
            window.showMinimized();
        elif (button == self.buttonclose):
            window.close();

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
