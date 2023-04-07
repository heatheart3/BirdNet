from PyQt5.QtWidgets import (QWidget, QMainWindow, QDialog, QAction, QPushButton,
                             QLineEdit, QHBoxLayout, QVBoxLayout, QLabel)
from PyQt5.QtCore import Qt
from src.BRLPlayer import BRLPlayer
from src.BirdClassifier.predict import BSR


class BRLMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.BRLPlayer = BRLPlayer()
        self.initUI()
        self.mainWindowConfig()

    def initUI(self):
        # 主窗口成员创建：菜单，菜单选项*3
        menubar = self.menuBar()
        aAnalyse = QAction("鸟类分析", self)
        aReset = QAction("数据分析", self)
        aClose = QAction("关闭", self)

        # “操作”菜单设置
        menufile = menubar.addMenu("操作")
        menufile.addAction(aAnalyse)
        menufile.addAction(aReset)
        menufile.addAction(aClose)
        # “操作”菜单选项设置
        aClose.triggered.connect(self.close)
        aAnalyse.triggered.connect(self.analyseDialog)
        # 窗口设置
        self.setWindowTitle("BRL_Classifier")

        # 主部件（BRLPlayer)启动
        self.setCentralWidget(self.BRLPlayer)

    def mainWindowConfig(self):
        self.resize(1500, 600)

    def analyseDialog(self):
        analysisDialog = QDialog()
        getTimeInput = QLineEdit()
        analysisBtn = QPushButton("确认")
        closeBtn = QPushButton("取消")
        btnLayout = QHBoxLayout()
        inputWinLayout = QHBoxLayout()
        mainLayout = QVBoxLayout()
        hintWords = QLabel("请输入要分析的时段：")

        # 信号连接
        # --按键信号连接
        analysisBtn.clicked.connect(self.showResult)
        closeBtn.clicked.connect(analysisDialog.close)

        # widgets配置
        getTimeInput.resize(20, 20)

        # 对话窗口设置
        # --布局设置
        # ---按键布局
        btnLayout.addWidget(analysisBtn)
        btnLayout.addWidget(closeBtn)
        # ---输入框布局
        inputWinLayout.addWidget(hintWords)
        inputWinLayout.addWidget(getTimeInput)
        # ---主体布局
        mainLayout.addLayout(inputWinLayout)
        mainLayout.addLayout(btnLayout)
        analysisDialog.setLayout(mainLayout)
        # --UI设置
        analysisDialog.setWindowTitle("鸟鸣声分析")
        analysisDialog.resize(400, 400)
        analysisDialog.setWindowModality(Qt.ApplicationModal)

        analysisDialog.exec_()
    def showResult(self):
        temp = BSR("./mediaFiles/south.mp3")
        analysisDialog = QDialog()
        resultText = QLabel()
        resultText.setText("识别结果：" + temp)

        resultDialogLayout = QVBoxLayout()
        resultDialogLayout.addWidget(resultText)
        analysisDialog.setLayout(resultDialogLayout)

        analysisDialog.setWindowTitle("鸟鸣声分析")
        analysisDialog.resize(400, 400)
        analysisDialog.setWindowModality(Qt.ApplicationModal)
        analysisDialog.exec_()


