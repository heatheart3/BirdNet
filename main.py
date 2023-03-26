import matplotlib.pyplot as plt

import BRLPlayer
import sys
from PyQt5.QtWidgets import QApplication, QWidget
import librosa
import numpy as np
import pyworld


if __name__ == '__main__':
    path = "E:/download/Music/XC769195 - 南极鸬鹚 - Leucocarbo bransfieldensis.mp3"
    y,sr = librosa.load(path, sr=16000)
    y = y.astype(np.double)
    # 0.025s
    framelength = 0.025
    # NFFT点数=0.025*fs
    framesize = int(framelength * sr)

    # 提取mel特征
    mel_spect = librosa.feature.melspectrogram(y = y, sr=sr, n_mels = 128,hop_length = 512, n_fft=1024)
    # 转化为log形式
    mel_spect_dB = librosa.power_to_db(mel_spect)
    #
    # 画mel谱图
    plt.figure(figsize=(80, 10))
    librosa.display.specshow(mel_spect_dB, sr=sr, x_axis='time', y_axis='mel')
    plt.savefig('./example.png')
    plt.show()
    # app = QApplication(sys.argv)
    # w = QWidget()
    # p = BRLPlayer.BRLPlayer()
    # p.show()
    # sys.exit(app.exec_())
