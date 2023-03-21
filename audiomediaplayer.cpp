#include "audiomediaplayer.h"
#include<QLayout>
#include<QDebug>
audioMediaPlayer::audioMediaPlayer(QWidget *parent)
    : QWidget(parent)
{
   player = new QMediaPlayer();
   QAudioOutput *audioOutput = new QAudioOutput;
   player->setSource(QUrl::fromLocalFile("E:/download/Music/complexity.mp3"));
   player-> setAudioOutput(audioOutput);
   audioOutput->setVolume(50);
   player->stop();

    //控制台按键构造
   playBtn = new QPushButton("Play");
   nextBtn = new QPushButton("Next");
   backBtn = new QPushButton("Back");
   QHBoxLayout *ctlBox = new QHBoxLayout();
   ctlBox->addWidget(nextBtn);
   ctlBox->addWidget(playBtn);
   ctlBox->addWidget(backBtn);
   setLayout(ctlBox);

   connect(playBtn, SIGNAL(clicked()), this, SLOT(changerStatus()));
}

audioMediaPlayer::~audioMediaPlayer()
{

}

void audioMediaPlayer::changerStatus()
{
    playerStatus = !playerStatus;
    if(playerStatus)
    {
        player->play();
    }
    else
    {
        player->stop();
    }
}

