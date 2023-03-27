import BRLPlayer
import sys
from PyQt5.QtWidgets import QApplication, QWidget
import librosa
import numpy as np


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QWidget()
    p = BRLPlayer.BRLPlayer()
    p.show()
    sys.exit(app.exec_())
