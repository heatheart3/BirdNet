from PyQt5.QtWidgets import (QGraphicsPixmapItem, QApplication, QGraphicsScene, QGraphicsView,
                             QWidget)
from PyQt5.QtGui import (QPixmap)
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPen, QPainter


class GraphicView(QGraphicsView):

    def __init__(self, graphic_scene, parent=None):
        super().__init__(parent)

        self.gr_scene = graphic_scene  # 将scene传入此处托管，方便在view中维护
        self.parent = parent
        self.init_ui()
        self.scale(0.5, 0.5)
        self.setFixedSize(1000, 1000)

    def init_ui(self):
        self.setScene(self.gr_scene)
        # 设置渲染属性
        self.setRenderHints(QPainter.Antialiasing |  # 抗锯齿
                            QPainter.HighQualityAntialiasing |  # 高品质抗锯齿
                            QPainter.TextAntialiasing |  # 文字抗锯齿
                            QPainter.SmoothPixmapTransform |  # 使图元变换更加平滑
                            QPainter.LosslessImageRendering)  # 不失真的图片渲染
        # 视窗更新模式
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        # 设置水平和竖直方向的滚动条不显示
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setTransformationAnchor(self.AnchorUnderMouse)
        # 设置拖拽模式
        self.setDragMode(self.RubberBandDrag)


class PixItem(QGraphicsPixmapItem):
    def __init__(self, path: str):
        super().__init__()
        # 读取图片
        self.pic = QPixmap(path)
        # 设置图源
        self.setPixmap(self.pic)


app = QApplication(sys.argv)
w = QWidget()
pic = PixItem("../mediaFiles/melSpectrogram.png")
scene = QGraphicsScene()
scene.addItem(pic)
graphic = GraphicView(scene, parent=w)
w.show()
sys.exit(app.exec_())
