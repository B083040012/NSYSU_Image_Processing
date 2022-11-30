from PyQt5 import QtWidgets, QtGui, QtCore

class imgLabel(QtWidgets.QLabel):
    def __init__(self, widget):
        super(imgLabel, self).__init__(widget)
        self.setMouseTracking(True)

        self.begin = None
        self.end = None
        self.centroid = None
        self.radius = None
        self.cut_circle = False
        self.cut_rect = False
        self.block_flag = False
        self.block_x = None
        self.block_y = None

    def reset_cut_flags(self):
        self.begin = None
        self.end = None
        self.centroid = None
        self.radius = None
        self.cut_circle = False
        self.cut_rect = False

    def paintEvent(self, QPaintEvent):
        super(imgLabel, self).paintEvent(QPaintEvent)
        painter = QtGui.QPainter(self)
        br = QtGui.QBrush(QtGui.QColor(255, 10, 10, 100))  
        painter.setBrush(br)
        if self.cut_rect == True:
            painter.drawRect(QtCore.QRect(self.begin, self.end))
        elif self.cut_circle == True:
            painter.drawEllipse(QtCore.QPoint(self.centroid.x(), self.centroid.y()), self.radius, self.radius)
        elif self.block_flag == True:
            painter.drawRect(QtCore.QRect(self.block_x, self.block_y, 8, 8))
        return  

    # def set_status_bar(self, status_bar):
    #     self.status_bar = status_bar

    # def mouseMoveEvent(self, QMouseEvent):
    #     pos = QMouseEvent.pos()
    #     self.status_bar.showMessage("x = {0}, y= {1}".format(pos.x(), pos.y()))

    # def mousePressEvent(self, QMouseEvent):
    #     print("the mouse clicked!!")

