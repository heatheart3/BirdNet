import matplotlib.pyplot as plt

import BRLPlayer
import sys
from PyQt5.QtWidgets import QApplication, QWidget
import librosa
import numpy as np
import pyworld


if __name__ == '__main__':


    app = QApplication(sys.argv)
    w = QWidget()
    p = BRLPlayer.BRLPlayer()
    p.show()
    sys.exit(app.exec_())
