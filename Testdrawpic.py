import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QBrush, QFont, QTransform
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDialog, QLabel,
                             QSlider, QMenuBar, QMenu, QAction,
                             QFormLayout, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem)


class TransDialog(QDialog):
    def __init__(self, view, parent=None):
        super(TransDialog, self).__init__(parent)

        self.view = view

        # 操作窗口标题
        self.setWindowTitle('视口变换操作')

        self.initUi()

    def initUi(self):
        fLayout = QFormLayout()

        # 旋转
        sdrRotate = QSlider(Qt.Horizontal)
        sdrRotate.setRange(-360, 360)
        sdrRotate.setPageStep(5)
        sdrRotate.setValue(0)
        sdrRotate.valueChanged.connect(self.onRotateValueChanged)

        fLayout.addRow('旋转', sdrRotate)

        # 缩放
        sdrScale = QSlider(Qt.Horizontal)
        sdrScale.setRange(0, 100)
        sdrScale.setPageStep(5)
        sdrScale.setValue(50)
        sdrScale.valueChanged.connect(self.onScaleValueChanged)
        fLayout.addRow('缩放', sdrScale)

        self.setLayout(fLayout)

    def onRotateValueChanged(self, value):
        # 是个累积效应，先对变化矩阵进行复位操作
        self.view.setTransform(QTransform())
        self.view.rotate(value)

    def onScaleValueChanged(self, value):
        s = 0.5 + value / 100.0
        # 是个累积效应，先对变化矩阵进行复位操作
        self.view.setTransform(QTransform())
        self.view.scale(s, s)


class DemoGraphicsView(QMainWindow):
    def __init__(self, parent=None):
        super(DemoGraphicsView, self).__init__(parent)

        # 设置窗口标题
        self.setWindowTitle('实战PyQt5: QGraphicsView Demo!')
        # 设置窗口大小
        self.resize(480, 360)

        self.initUi()

    def initUi(self):
        # 菜单条
        menuBar = self.menuBar()
        menuFile = menuBar.addMenu('文件')

        aTrans = QAction('变换操作', self)
        aTrans.triggered.connect(self.onTransDialog)
        aReset = QAction('复位', self)
        aReset.triggered.connect(self.onReset)
        aExit = QAction('退出', self)
        aExit.triggered.connect(self.close)

        menuFile.addAction(aTrans)
        menuFile.addAction(aReset)
        menuFile.addSeparator()
        menuFile.addAction(aExit)

        # 场景部分
        scene = QGraphicsScene()

        scene.addText('Hello Graphics View', QFont(self.font().family(), 24))
        scene.addEllipse(0, 80, 200, 120, QPen(Qt.black), QBrush(Qt.blue))
        scene.addRect(220, 80, 200, 160, QPen(Qt.red))


        self.view = QGraphicsView()
        self.view.setScene(scene)

        self.setCentralWidget(self.view)

    def onTransDialog(self):
        dlg = TransDialog(self.view, self)
        dlg.exec()

    def onReset(self):
        self.view.setTransform(QTransform())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DemoGraphicsView()
    window.show()
    sys.exit(app.exec())