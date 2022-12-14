from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

class histogramWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.canvas = FigureCanvas(Figure())

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.canvas)

        self.canvas.axes = None

    def initial_subplot(self):
        self.setLayout(self.vertical_layout)
        self.canvas.axes = self.canvas.figure.add_subplot(111)

    def draw_gray_histogram(self, img, threshold = None):
        if self.canvas.axes is None:
            self.initial_subplot()
        self.canvas.figure.subplots_adjust(left=0.15, right=0.95,
            bottom=0.15, top=0.95, hspace=0, wspace=0)
        y = img.flatten()
        self.canvas.axes.clear()
        self.canvas.axes.hist(y, 255, range = (0, 254), color = 'black')
        self.canvas.axes.plot([threshold, threshold], [0, 2000], color = 'red')
        self.canvas.axes.set_xlim([0, 255])
        self.canvas.axes.autoscale()
        self.canvas.draw()
        
    def draw_color_histogram(self, img):
        if self.canvas.axes is None:
            self.initial_subplot()
        self.canvas.figure.subplots_adjust(left=0.15, right=0.95,
            bottom=0.15, top=0.95, hspace=0, wspace=0)
        r_y = img[:, :, 0].flatten()
        g_y = img[:, :, 1].flatten()
        b_y = img[:, :, 2].flatten()
        self.canvas.axes.clear()
        self.canvas.axes.hist(r_y, 255, range = (0, 254), color = 'red')
        self.canvas.axes.hist(g_y, 255, range = (0, 254), color = 'green')
        self.canvas.axes.hist(b_y, 255, range = (0, 254), color = 'blue')
        self.canvas.axes.set_xlim([0, 255])
        self.canvas.axes.autoscale()
        self.canvas.draw()

    def draw_single_color_histogram(self, img, type):
        if self.canvas.axes is None:
            self.initial_subplot()
        self.canvas.figure.subplots_adjust(left=0.15, right=0.95,
            bottom=0.15, top=0.95, hspace=0, wspace=0)
        if type == "red":
            r_y = img[:, :, 0].flatten()
        elif type == "green":
            g_y = img[:, :, 1].flatten()
        elif type == "blue":
            b_y = img[:, :, 2].flatten()
        self.canvas.axes.clear()
        if type == "red":
            self.canvas.axes.hist(r_y, 255, range = (0, 254), color = 'red')
        elif type == "green":
            self.canvas.axes.hist(g_y, 255, range = (0, 254), color = 'green')
        elif type == "blue":
            self.canvas.axes.hist(b_y, 255, range = (0, 254), color = 'blue')
        self.canvas.axes.set_xlim([0, 255])
        self.canvas.axes.autoscale()
        self.canvas.draw()