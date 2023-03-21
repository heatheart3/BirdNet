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
   audioOutput->setVolume(0.5);
   player->play();

    //控制台按键构造
   playBtn = new QPushButton("Play");
   nextBtn = new QPushButton("Next");
   backBtn = new QPushButton("Back");
   QHBoxLayout *ctlBox = new QHBoxLayout();
   ctlBox->addWidget(nextBtn);
   ctlBox->addWidget(playBtn);
   ctlBox->addWidget(backBtn);

   //进度条和时长
   timeSlider = new QSlider(Qt::Horizontal);
   curPlayTime = new QLabel("00:00");
   totalPlayTime = new QLabel("00:00");
   QHBoxLayout *timeLabels = new QHBoxLayout();
   timeLabels->addWidget(curPlayTime);
   timeLabels->addWidget(totalPlayTime);
   QVBoxLayout *mainLayout = new QVBoxLayout();
   mainLayout->addLayout(timeLabels);
   mainLayout->addWidget(timeSlider);
   mainLayout->addLayout(ctlBox);
   setLayout(mainLayout);


   //播放按钮
   connect(playBtn, SIGNAL(clicked()), this, SLOT(changerStatus()));
   //总时长显示
   connect(player, &QMediaPlayer::durationChanged, this, [=](qint64 duration)
   {
      totalPlayTime->setText(QString("%1:%2").arg(duration/1000/60,2,10,QChar('0')).arg(duration/1000%60,2,10,QChar('0')));
      timeSlider->setRange(0,duration);
   });
   //已播放时长显示
   connect(player, &QMediaPlayer::positionChanged, curPlayTime, [=](qint64 position)
   {
        curPlayTime->setText(QString("%1:%2").arg(position/1000/60,2,10,QChar('0')).arg(position/1000%60,2,10,QChar('0')));
        timeSlider->setValue(position);
   });
   //拖动进度条调整播放位置
   connect(timeSlider,&QSlider::sliderMoved, player, &QMediaPlayer::setPosition);
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
        player->pause();
    }
}

