#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent): QMainWindow(parent)
{
    resize(720, 20 + 448);
    //setWindowIcon(QIcon(":/icon"));
    setWindowTitle(QString("我的热点新闻客户端"));
    setWindowFlags(Qt::FramelessWindowHint | windowFlags());
    setCentralWidget(new QWidget(parent));

    QVBoxLayout *layout = new QVBoxLayout(centralWidget());
    layout->setMargin(0);
    layout->setSpacing(0);

    webView = new QWebEngineView(this);
    webView->load(QUrl("https://hotnews.duba.com/minisite/1339/"));
    webView->show();
    layout->addWidget(webView);
}

MainWindow::~MainWindow()
{
    delete webView;
}

