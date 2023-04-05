from PyQt5.QtWidgets import QMainWindow, QAction
from src.BRLPlayer import BRLPlayer


class BRLMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.BRLPlayer = BRLPlayer()
        self.initUI()
        # self.setFixedSize(1200, 1200)

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

        self.setCentralWidget(self.BRLPlayer)
