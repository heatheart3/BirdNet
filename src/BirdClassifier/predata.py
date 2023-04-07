#!/user/bin/python3
# -*-coding:utf-8 -*-

"""
# File       : data.py
# Time       ：2023/1/1 17:02
# Author     ：Kermit Li
# version    ：python 3.9
# Description：
"""
import os
import torch
import numpy as np
from .utils import AudioUtil

DURATION = 4
SR = 48_000
CHANNEL = 2
N_MELS = 64
N_FFT = 512
F_MIN = 150
F_MAX = 15_000
HOP_LEN = int(0.5 * N_FFT)

def load_data(file):
    aud = AudioUtil.open(file)
    aud = AudioUtil.resample(aud, SR)  # 标准化采样
    aud = AudioUtil.rechannel(aud, CHANNEL)  # 转换为 通道
    aud = AudioUtil.pad_trunc(aud, DURATION)  # 统一为 秒
    sgram = AudioUtil.spectro_gram(aud, n_mels=N_MELS, n_fft=N_FFT, f_min=F_MIN, f_max=F_MAX, hop_len=HOP_LEN)

    if len(sgram) == 1:
        sgram = torch.stack([sgram, sgram, sgram])
    elif len(sgram) == 2:
        sgram = torch.stack([sgram[0], sgram[1], sgram[np.random.choice(len(sgram))]])
    return sgram