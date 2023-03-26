from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class testDraw(FigureCanvas):
    def __init__(self):
        self.fig = Figure(figsize=(4, 5), dpi=100)
        self.ax1 = self.fig.add_subplot(1,1,1)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, 300, 400)
        FigureCanvas.updateGeometry(self)