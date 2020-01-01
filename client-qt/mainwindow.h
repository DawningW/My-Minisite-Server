#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QVBoxLayout>
#include <QWebEngineView>

class MainWindow : public QMainWindow
{
    Q_OBJECT

    // TitleBar *titleBar;
    QWebEngineView *webView;

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
};
#endif // MAINWINDOW_H
