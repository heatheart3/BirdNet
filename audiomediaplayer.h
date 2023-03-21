#ifndef AUDIOMEDIAPLAYER_H
#define AUDIOMEDIAPLAYER_H

#include <QWidget>
#include<QMediaPlayer>
#include<QPushButton>
#include<QBoxLayout>
#include<QUrl>
#include<QAudioOutput>
#include<QFileDialog>
#include<QSlider>
#include<QLabel>
class audioMediaPlayer : public QWidget
{
    Q_OBJECT

public:
    audioMediaPlayer(QWidget *parent = nullptr);
    ~audioMediaPlayer();
private:
    bool playerStatus = false;
    QMediaPlayer *player;
    QPushButton *playBtn;
    QPushButton *nextBtn;
    QPushButton *backBtn;
    QSlider *timeSlider;
    QLabel *curPlayTime;
    QLabel *totalPlayTime;

private slots:
    void changerStatus();

};
#endif // AUDIOMEDIAPLAYER_H
