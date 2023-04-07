from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import axes, figure


class Drawpic(FigureCanvas):
    def __init__(self):
        self.fig = Figure(constrained_layout = True) #type:figure.Figure
        # 设置背景颜色与窗口颜色相同，消除白边
        self.fig.patch.set_facecolor("#F0F0F0")
        self.fig.set_size_inches(30, self.fig.get_size_inches()[1])
        self.canvas = FigureCanvas(self.fig)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, 300, 400)
        FigureCanvas.updateGeometry(self)
