#include "TitleBar.h"

#ifdef Q_OS_WIN
#pragma comment(lib, "user32.lib")
#include <qt_windows.h>
#endif

TitleBar::TitleBar(QWidget *parent) : QWidget(parent)
{
    setFixedWidth(parent->width());
    setFixedHeight(30);

    QHBoxLayout *layout = new QHBoxLayout(this);
    layout->setMargin(0);
    layout->setSpacing(0);

    layout->addSpacing(5);

    labelIcon = new QLabel(this);
    labelIcon->setObjectName("iconLabel");
    labelIcon->setFixedSize(20, 20);
    labelIcon->setScaledContents(true);
    labelIcon->setPixmap(parent->windowIcon().pixmap(labelIcon->size()));
    layout->addWidget(labelIcon, 0, Qt::AlignLeft);

    layout->addSpacing(5);

    labelTitle = new QLabel(this);
    labelTitle->setObjectName("titleLabel");
    labelTitle->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Fixed);
    labelTitle->setText(parent->windowTitle());
    layout->addWidget(labelTitle, 0, Qt::AlignLeft);

    layout->addStretch();

    buttonMinimize = new QPushButton(this);
    buttonMinimize->setObjectName("minimizeButton");
    buttonMinimize->setToolTip("Minimize");
    connect(buttonMinimize, SIGNAL(clicked(bool)), this, SLOT(onClicked()));
    layout->addWidget(buttonMinimize, 0, Qt::AlignRight | Qt::AlignTop);

    buttonClose = new QPushButton(this);
    buttonClose->setObjectName("closeButton");
    buttonClose->setToolTip("Close");
    connect(buttonClose, SIGNAL(clicked(bool)), this, SLOT(onClicked()));
    layout->addWidget(buttonClose, 0, Qt::AlignRight | Qt::AlignTop);
}

TitleBar::~TitleBar()
{

}

bool TitleBar::eventFilter(QObject *obj, QEvent *event)
{
    QWidget *widget = qobject_cast<QWidget *>(obj);
    if (widget)
    {
        switch (event->type())
        {
        case QEvent::WindowIconChange:
        {
            labelIcon->setPixmap(widget->windowIcon().pixmap(labelIcon->size()));
            return true;
        }
        case QEvent::WindowTitleChange:
        {
            labelTitle->setText(widget->windowTitle());
            return true;
        }
        case QEvent::WindowStateChange:
        case QEvent::Resize:
            return true;
        default: return QWidget::eventFilter(obj, event);
        }
    }
    return QWidget::eventFilter(obj, event);
}

void TitleBar::mousePressEvent(QMouseEvent *event)
{
#ifdef Q_OS_WIN
    if (ReleaseCapture())
    {
        QWidget *window = this->window();
        if (window->isTopLevel())
        {
           SendMessage(HWND(window->winId()), WM_SYSCOMMAND, SC_MOVE + HTCAPTION, 0);
        }
    }
    event->ignore();
#else
#endif
}

void TitleBar::onClicked()
{
    QWidget *window = this->window();
    if (window->isTopLevel())
    {
        QPushButton *button = qobject_cast<QPushButton *>(sender());
        if (button == buttonMinimize)
        {
            window->showMinimized();
        }
        else if (button == buttonClose)
        {
            window->close();
        }
    }
}
