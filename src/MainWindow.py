from PyQt5.QtWidgets import (QWidget, QMainWindow, QAction,QVBoxLayout)
from src.BRLPlayer import BRLPlayer


class BRLMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.BRLPlayer = BRLPlayer()
        self.initUI()
        self.mainWindowConfig()

    def initUI(self):
        # 菜单栏设置
        menubar = self.menuBar()
        menufile = menubar.addMenu("操作")
        aTrans = QAction("变换操作", self)
        aReset = QAction("复原", self)
        aClose = QAction("关闭", self)
        aClose.triggered.connect(self.close)
        menufile.addAction(aTrans)
        menufile.addAction(aReset)
        menufile.addAction(aClose)

        # 主部件（BRLPlayer)启动
        self.setCentralWidget(self.BRLPlayer)

    def mainWindowConfig(self):
        self.resize(1500, 600)
