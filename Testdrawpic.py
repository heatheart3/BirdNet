import matplotlib
from matplotlib import figure, axes
import matplotlib.pyplot as plt
import librosa
import numpy as np

fig, ax1 = plt.subplots(figsize=(5, 2.7), constrained_layout = True)# type:figure.Figure, axes.Axes
ax1.axis('off')


# 音频处理
path = "./南极鸬鹚.mp3"
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

librosa.display.specshow(mel_spect_dB, sr=sr, x_axis='time', y_axis='mel', ax=ax1)

fig.show()