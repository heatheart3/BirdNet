from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout,
                             QVBoxLayout, QSlider, QLabel, QStyleFactory, QListWidget
                             , QFileDialog, QMessageBox, QDialog)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from PyQt5.QtCore import QUrl, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap
from src.AuditoFeaturePicture import Drawpic
import librosa
import numpy as np
from matplotlib import figure, axes
import os
import time


class BRLPlayer(QWidget):
    def __init__(self):
        super().__init__()
        # 要使用的widgets
        self.playSlider = None
        self.musicList = None
        self.timer = None
        self.playerList = None
        self.btnOpen = None
        self.btnPrev = None
        self.btnNext = None
        self.btnPlay = None
        self.endTimeLabel = None
        self.startTimeLabel = None
        self.player = None

        self.songs_list = []
        self.cur_playing_song = ''
        self.is_pause = True
        self.is_switching = False
        # 自定义信号
        self._signal = pyqtSignal()
        # matplotlib后端
        self.matpltBackend = Drawpic()

        self.initUI()

    def initUI(self):
        # 创建组件成员：三个按键, 播放器，播放列表，进度条，matplotlib组件，图片
        self.btnPlay = QPushButton(self)
        self.btnNext = QPushButton(self)
        self.btnPrev = QPushButton(self)
        self.btnOpen = QPushButton(self)
        self.playerList = QMediaPlaylist(self)
        self.matpltBackend = Drawpic()
        self.player = QMediaPlayer()
        self.timer = QTimer(self)
        self.playSlider = QSlider(Qt.Horizontal, self)
        self.musicList = QListWidget()


        # 各部件细节设置
        # 按键配置
        self.btnPlay.setText("Play")
        self.btnPrev.setText("Prev")
        self.btnNext.setText("Next")
        self.btnOpen.setText("Open")
        self.btnPlay.clicked.connect(self.playMusic)
        self.btnOpen.clicked.connect(self.openMusic)
        self.btnPrev.clicked.connect(self.prevMusic)
        self.btnNext.clicked.connect(self.nextMusic)
        # --播放时间
        self.startTimeLabel = QLabel('00:00')
        self.endTimeLabel = QLabel('00:00')
        # --进度条
        self.playSlider.sliderMoved[int].connect(lambda: self.player.setPosition(self.playSlider.value()))
        self.playSlider.setStyle(QStyleFactory.create('Fusion'))
        # --播放列表
        self.musicList.itemDoubleClicked.connect(self.doubleCicked)
        # --计时器
        self.timer.start(100)
        self.timer.timeout.connect(self.flush)
        # -- 图片显示设置

        # 播放器设置
        self.player.setVolume(100)

        # 布局设置
        # 播放器按键布局
        lh1 = QHBoxLayout()
        lh1.addWidget(self.btnPrev)
        lh1.addWidget(self.btnPlay)
        lh1.addWidget(self.btnNext)
        lh1.addWidget(self.btnOpen)
        # 播放器进度条布局
        hBoxSlider = QHBoxLayout()
        hBoxSlider.addWidget(self.startTimeLabel)
        hBoxSlider.addWidget(self.playSlider)
        hBoxSlider.addWidget(self.endTimeLabel)
        # 语谱图，播放器布局
        lv1 = QVBoxLayout()
        lv1.addWidget(self.matpltBackend)
        lv1.addLayout(hBoxSlider)
        lv1.addLayout(lh1)
        # 主体布局
        lMain = QHBoxLayout()
        lMain.addWidget(self.musicList)
        lMain.addLayout(lv1)
        self.setLayout(lMain)

    def extract_melspec(self, path):
        y, sr = librosa.load(path, sr=16000)
        y = y.astype(np.double)
        # 0.025s
        framelength = 0.025
        # NFFT点数=0.025*fs
        framesize = int(framelength * sr)
        # 提取mel特征
        mel_spect = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, hop_length=512, n_fft=1024)
        # 转化为log形式
        mel_spect_dB = librosa.power_to_db(mel_spect)
        self.drawConfig()
        librosa.display.specshow(mel_spect_dB, sr=sr, x_axis='time', y_axis='mel', ax=self.matpltBackend.fig.gca())
        self.matpltBackend.draw()

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
        next_row = self.musicList.currentRow() + 1 if self.musicList.currentRow() != self.musicList.count() - 1 else 0
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
        self.extract_melspec(self.cur_playing_song)
        self.playMusic()
        self.is_switching = False

    def drawConfig(self):
        ax1 = self.matpltBackend.fig.add_subplot(1, 1, 1)  # type:axes.Axes
        ax1.cla()
        # 关闭坐标轴
        ax1.axis("off")

    def showWaitingDialog(self):
        waitingDialog = QDialog()
        waitingDialog.setWindowModality(Qt.ApplicationModal)
        promptWord = QLabel("音频分析中，请稍等")
        tempLayout = QVBoxLayout()
        tempLayout.addWidget(promptWord)
        waitingDialog.setLayout(tempLayout)
        self._signal.connect(waitingDialog.close)










