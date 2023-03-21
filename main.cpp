#include "audiomediaplayer.h"
#include<QMediaPlayer>
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    audioMediaPlayer *q = new audioMediaPlayer();
    q->show();
    return a.exec();
}
