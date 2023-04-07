#!/user/bin/python3
# -*-coding:utf-8 -*-

"""
# File       : predict.py
# Time       ：2023/1/1 17:07
# Author     ：Kermit Li
# version    ：python 3.9
# Description：
"""
import os
import json
import random
import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from .predata import load_data
from .model import resnet50, GMv3

MODEL_PATH = "/model/resnet50_3_64_751.pt"
CLASS_PATH = '/class_indices.json'

def BSR(file):
    #device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    device = torch.device("cpu")
    # read class_indict
    current_path = os.path.dirname(__file__)
    assert os.path.exists(current_path + CLASS_PATH), "file: '{}' dose not exist.".format(CLASS_PATH)
    with open(current_path+ CLASS_PATH, "r") as f:
        class_indict = json.load(f)

    # load audio to mel-spectrogram
    sgram = load_data(file)

    # expand batch dimension shape：[1,3,64,751]
    sgram = torch.unsqueeze(sgram, dim=0)

    # load model
    assert os.path.exists(current_path + MODEL_PATH), "file: '{}' dose not exist.".format(MODEL_PATH)
    model = torch.load(current_path + MODEL_PATH, map_location='cpu').to(device)

    # predict
    model.eval()
    with torch.no_grad():
        # predict class
        output = torch.squeeze(model(sgram.to(device))).cpu()
        predict = torch.softmax(output, dim=0)
        predict_cla = torch.argmax(predict).numpy()
    

    print_res = "class: {}   prob: {:.3}".format(class_indict[str(predict_cla)],
                                                 predict[predict_cla].numpy())
    print(print_res)
    return print_res

