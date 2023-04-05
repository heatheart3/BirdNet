from matplotlib import pyplot as plt
import matplotlib
import librosa
import numpy as np
from pydub import AudioSegment
from matplotlib.pyplot import MultipleLocator


def analyseAudio(path:str):
    y, sr = librosa.load(path, sr=36000)
    y = y.astype(np.double)
    # 0.025s
    framelength = 0.025
    # NFFT点数=0.025*fs
    framesize = int(framelength * sr)

    # 提取mel特征
    mel_spect = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, hop_length=512, n_fft=1024)
    # 转化为log形式
    mel_spect_dB = librosa.power_to_db(mel_spect)
    return mel_spect_dB, sr

song = AudioSegment.from_mp3("../mediaFiles/南极鸬鹚.mp3")
song = song[0: 20 * 1000]
song.export('../mediaFiles/5sClip')
path = '../mediaFiles/5sClip'
y, sr = analyseAudio(path)
librosa.display.specshow(y, sr=sr, x_axis='time', y_axis='mel')
margin = 0.2 / plt.gcf().get_size_inches()[0]
plt.gcf().subplots_adjust(left=margin, right=1. - margin)
plt.gcf().set_size_inches(30, plt.gcf().get_size_inches()[1])
plt.autoscale(enable=False, axis='x', tight=True)
plt.show()
print(np.shape(y))

