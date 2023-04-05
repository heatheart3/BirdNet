from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSlider, QLabel, QListWidget, QFileDialog, QMessageBox, QStyleFactory
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt, QTimer
from src.AuditoFeaturePicture import Drawpic
import librosa
import numpy as np
from librosa import feature
import os
import time


class BRLPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.songs_list = []
        self.player = QMediaPlayer()
        self.cur_playing_song = ''
        self.is_pause = True
        self.is_switching = False
        self.timer = QTimer(self)
        self.timer.start(100)
        self.timer.timeout.connect(self.flush)
        self.fig = Drawpic()
        self.piclab = None

        self.initUI()
        # self.setFixedSize(1000,1000)

    def initUI(self):
        # 创建组件成员：三个按键, 播放器，播放列表，进度条，matplotlib组件，图片
        # self.piclab = QLabel(self)

        # 各部件细节设置
        # --按键配置
        self.btnPrev = QPushButton('Prev', self)
        self.btnNext = QPushButton('Next', self)
        self.btnPlay = QPushButton('Play', self)
        self.btnOpen = QPushButton('Open', self)
        self.btnPlay.clicked.connect(self.playMusic)
        self.btnOpen.clicked.connect(self.openMusic)
        self.btnPrev.clicked.connect(self.prevMusic)
        self.btnNext.clicked.connect(self.nextMusic)
        # --播放时间
        self.startTimeLabel = QLabel('00:00')
        self.endTimeLabel = QLabel('00:00')
        # --进度条
        self.playSlider = QSlider(Qt.Horizontal, self)
        self.playSlider.sliderMoved[int].connect(lambda: self.player.setPosition(self.playSlider.value()))
        self.playSlider.setStyle(QStyleFactory.create('Fusion'))
        # --播放列表
        self.musicList = QListWidget()
        self.musicList.itemDoubleClicked.connect(self.doubleCicked)


        # matplotlib绘图设置
        mel_feature, sr = self.extract_melspec()
        librosa.display.specshow(mel_feature, sr=sr, x_axis='time', y_axis='mel', ax=self.fig.ax1)
        figure0 = self.fig.get_fig()
        figure0.savefig("./mediaFiles/melSpectrogram.png")
        # 图片显示设置
        # self.piclab.setPixmap(QPixmap("./mediaFiles/melSpectrogram.png"))
        # self.piclab.setScaledContents(True)


        # 布局设置
        lh1 = QHBoxLayout()
        lh1.addWidget(self.btnPrev)
        lh1.addWidget(self.btnPlay)
        lh1.addWidget(self.btnNext)
        lh1.addWidget(self.btnOpen)
        hBoxSlider = QHBoxLayout()
        hBoxSlider.addWidget(self.startTimeLabel)
        hBoxSlider.addWidget(self.playSlider)
        hBoxSlider.addWidget(self.endTimeLabel)
        lmain = QVBoxLayout()
        # lmain.addWidget(self.piclab)
        # lmain.addWidget(self.fig)
        lmain.addWidget(self.musicList)
        lmain.addLayout(hBoxSlider)
        lmain.addLayout(lh1)
        self.setLayout(lmain)

    def extract_melspec(self):
        path = "./mediaFiles/南极鸬鹚.mp3"
        y, sr = librosa.load(path, sr=16000)
        y = y.astype(np.double)

        # 提取mel特征
        mel_spect = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, hop_length=512, n_fft=1024)
        # 转化为log形式
        mel_spect_dB = librosa.power_to_db(mel_spect)
        return mel_spect_dB, sr


    def flush(self):
        if (not self.is_pause) and (not self.is_switching):
            self.playSlider.setMinimum(0)
            self.playSlider.setMaximum(self.player.duration())
            self.playSlider.setValue(self.playSlider.value() + 100)
        self.startTimeLabel.setText(time.strftime('%M:%S', time.localtime(self.player.position() / 1000)))
        self.endTimeLabel.setText(time.strftime('%M:%S', time.localtime(self.player.duration() / 1000)))


    # 将文件加入播放列表
    def openMusic(self):
        path = QFileDialog.getOpenFileName(self, "选择音乐", './')
        song_formats = ['wav', 'mp3']
        song = path[0]
        if not song.split('.')[-1] in song_formats:
            QMessageBox.critical(self, '打开文件失败', '不支持的文件格式')
            return
        filename = os.path.basename(song)
        self.songs_list.append([filename, song])
        self.musicList.addItem(filename)


    # 播放/暂停
    def playMusic(self):
        if self.musicList.count() == 0:
            QMessageBox.critical(self, '播放失败', '当前播放列表中无音乐')
            return
        if not self.player.isAudioAvailable():
            self.setCurrentlyPlaying()
        if self.is_pause or self.is_switching:
            self.player.play()
            self.is_pause = False
            self.btnPlay.setText('Pause')
        elif (not self.is_pause) and (not self.is_switching):
            self.player.pause()
            self.is_pause = True
            self.btnPlay.setText('Play')


    def prevMusic(self):
        self.playSlider.setValue(0)
        if self.musicList.count() == 0:
            QMessageBox.critical(self, '播放失败', '当前播放列表中无音乐')
            return
        pre_row = self.musicList.currentRow() - 1 if self.musicList.currentRow() != 0 else self.musicList.count() - 1
        self.musicList.setCurrentRow(pre_row)
        self.is_switching = True
        self.setCurrentlyPlaying()
        self.playMusic()
        self.is_switching = False


    def nextMusic(self):
        self.playSlider.setValue(0)
        if self.musicList.count() == 0:
            QMessageBox.critical(self, '播放失败', '当前播放列表中无音乐')
            return
        next_row = self.musicList.currentRow()+1 if self.musicList.currentRow() != self.musicList.count()-1 else 0
        self.musicList.setCurrentRow(next_row)
        self.is_switching = True
        self.setCurrentlyPlaying()
        self.playMusic()
        self.is_switching = False


    def setCurrentlyPlaying(self):
        self.cur_playing_song = self.songs_list[self.musicList.currentRow()][-1]
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.cur_playing_song)))


    def doubleCicked(self):
        self.is_switching = True
        self.playSlider.setValue(0)
        self.setCurrentlyPlaying()
        self.playMusic()
        self.is_switching = False
