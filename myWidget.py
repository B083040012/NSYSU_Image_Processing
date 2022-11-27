from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

class glsFunctionWidget(QWidget):
    def __init__(self, type, parent):
        QWidget.__init__(self, parent)
        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)

        self.canvas.axes.set_xlim([0, 255])
        self.canvas.axes.set_ylim([0, 255])
        
        self.type = type
        self.slope = 1 if type == "preserve_gls" else 0
        # if type == "diminish_gls":
        #     self.origin1 = [0, 0]; self.origin2 = [0, 0]
        # elif type == "preserve_gls":
        #     self.origin1 = [0, 0]; self.origin2 = [255,255]
        self.r1 = 85; self.r2 = 170
        self.mod_level = 180
        self.draw_line()

        # 0 for not point, 1 for (r1, s1), 2 for (r1, s2)
        self.get_point_flag = 0

    def draw_line(self):
        line1 = [[0, self.r1], [0, (self.r1 * self.slope)]]
        line2 = [[self.r1, self.r1], [(self.r1 * self.slope), self.mod_level]]
        line3 = [[self.r1, self.r2], [self.mod_level, self.mod_level]]
        line4 = [[self.r2, self.r2], [self.mod_level, (self.r2 * self.slope)]]
        line5 = [[self.r2, 255], [(self.r2 * self.slope), (255 * self.slope)]]
        self.canvas.axes.clear()
        self.canvas.axes.set_xlim([0, 255])
        self.canvas.axes.set_ylim([0, 255])
        self.canvas.axes.scatter([self.r1, self.r2], [self.mod_level, self.mod_level])
        self.canvas.axes.plot(line1[0], line1[1])
        self.canvas.axes.plot(line2[0], line2[1])
        self.canvas.axes.plot(line3[0], line3[1])
        self.canvas.axes.plot(line4[0], line4[1])
        self.canvas.axes.plot(line5[0], line5[1])
        self.canvas.draw()

    def get_point(self, xdata, ydata):
        if abs(xdata - self.r1) < 3 and abs(ydata - self.mod_level) < 3:
            self.get_point_flag = 1
            return 1
        elif abs(xdata - self.r2) < 3 and abs(ydata - self.mod_level) < 3:
            self.get_point_flag = 2
            return 2
        else:
            self.get_point_flag = 0
            return 0

    def update_line(self, xdata, ydata):
        if self.get_point_flag == 0:
            return
        if self.get_point_flag == 1:
            # if ydata <= (self.r2 * self.slope): return
            self.r1 = xdata
        elif self.get_point_flag == 2:
            # if ydata <= (xdata * self.slope): return
            self.r2 =  xdata
        self.mod_level = ydata
        self.draw_line()


class csFunctionWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)

        self.canvas.axes.set_xlim([0, 255])
        self.canvas.axes.set_ylim([0, 255])

        self.origin1 = [0, 0]; self.origin2 = [255,255]
        self.r1 = 85; self.s1 = 85
        self.r2 = 170; self.s2 = 170
        self.draw_line()

        # 0 for not point, 1 for (r1, s1), 2 for (r1, s2)
        self.get_point_flag = 0

    def draw_line(self):
        line1 = [[self.origin1[0], self.r1], [self.origin1[1], self.s1]]
        line2 = [[self.r1, self.r2], [self.s1, self.s2]]
        line3 = [[self.r2, self.origin2[0]], [self.s2, self.origin2[1]]]
        self.canvas.axes.clear()
        self.canvas.axes.set_xlim([0, 255])
        self.canvas.axes.set_ylim([0, 255])
        self.canvas.axes.scatter([self.r1, self.r2], [self.s1, self.s2])
        self.canvas.axes.plot(line1[0], line1[1])
        self.canvas.axes.plot(line2[0], line2[1])
        self.canvas.axes.plot(line3[0], line3[1])
        self.canvas.draw()

    def get_point(self, xdata, ydata):
        if abs(xdata - self.r1) < 3 and abs(ydata - self.s1) < 3:
            self.get_point_flag = 1
            return 1
        elif abs(xdata - self.r2) < 3 and abs(ydata - self.s2) < 3:
            self.get_point_flag = 2
            return 2
        else:
            self.get_point_flag = 0
            return 0

    def update_line(self, xdata, ydata):
        """
        Draw line dynamically depend on the mouse movement and 
        get the update point coordinate
        """
        if self.get_point_flag == 1:
            self.r1 = xdata; self.s1 = ydata
            self.draw_line()
        elif self.get_point_flag == 2:
            self.r2 =  xdata; self.s2 = ydata
            self.draw_line()