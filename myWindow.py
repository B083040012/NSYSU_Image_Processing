import numpy as np
from time import sleep
from PIL import Image, ImageQt
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QLabel, QMainWindow
from PyQt5.QtCore import QEvent, QThread

from myQLabel import imgLabel
from myPcxImage import PcxImage
from histogramwidget import histogramWidget
from myWidget import csFunctionWidget, glsFunctionWidget

class ballWindow(QMainWindow):
    def __init__(self, parent = None):
        super(ballWindow, self).__init__(parent)

        self.setObjectName("ball_window")
        self.resize(256, 256)
        self.setWindowTitle("Bouncing Ball")

        # create label for ball image
        self.label = imgLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 0, 256, 256))
        self.label.setObjectName("ball_label")
        self.label.installEventFilter(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.show()
        self.ball(button = False)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.bouncing_ball)
        self.timer.start()

    def display(self, label, image_array, width, height, posx, posy):

        """
        Display image on the qt label
            posx, posy: -1 for default position (defined in DIP_GUI)
        """
        img = np.array(image_array, dtype=np.uint8)
        img = Image.fromarray(img)
        qt_img = ImageQt.ImageQt(img)
        pixmap_img = QtGui.QPixmap.fromImage(qt_img).scaled(width, height)
        pixmap_img.detach()

        if posx == -1 or posy == -1:
            label.resize(width, height)
        else:
            label.setGeometry(QtCore.QRect(posx, posy, width, height))
        label.setPixmap(pixmap_img)
        label.show()
        return

    def ball(self, button = True):
        if button == False:
            self.ball_flag = True
            self.ball_vector = np.array([1, 0.5])
            self.ball_speed = 10
            self.ball_pcx = PcxImage()
            self.ball_img, width, height, self.ball_center, self.vector = self.ball_pcx.ball("create")
            self.display(self.label, self.ball_img, width, height, -1, -1)
        return

    def bouncing_ball(self):
        self.ball_img, width, height, self.ball_center, self.ball_vector = \
            self.ball_pcx.ball("bouncing", center = self.ball_center, vector = self.ball_vector, speed = self.ball_speed)
        self.display(self.label, self.ball_img, width, height, -1, -1)

class bitPlaneWindow(QMainWindow):
    def __init__(self, pcx_obj, type, parent = None):
        super(bitPlaneWindow, self).__init__(parent)

        self.setObjectName("bit_plane_mainwindow")
        self.resize(1500, 800)
        self.setWindowTitle("Bit Plane " + "(" + type + ")")

        # create the label image
        self.label_list = list()
        for i in range(0, 8):
            if i < 4:
                pos_x, pos_y = (0 + 300 * i), 30
            else:
                pos_x, pos_y = (0 + 300 * (i - 4)), 350
            label = self.create_label(pos_x, pos_y, 256, 256, "{0}-bit_plane_label".format(i), "")
            self.label_list.append(label)

        self.ori_label = self.create_label(1200, 30, 256, 256, "ori_img_label", "")
        ori_text_label = self.create_label(1200, 260, 200, 100, "ori_text_label", "original image")
        self.after_label = self.create_label(1200, 350, 256, 256, "after_img_label", "")

        # create label for SNR value
        self.snr_label = self.create_label(1200, 650, 250, 150, "snr_label", "", font = 15)

        # create label for text
        self.text_label_list = list()
        for i in range(0, 8):
            if i < 4:
                x_pos, y_pos = (0 + 300 * i), 260
            else:
                x_pos, y_pos = (0 + 300 * (i - 4)), 590
            label = self.create_label(x_pos, y_pos, 200, 100, \
                "{0} bit plane text label".format(i), "{0}-bit plane".format(i))

        # create the button for opening image for hiding
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1900, 26))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menubar.addAction(self.menu_File.menuAction())
        self.actionOpen = QtWidgets.QAction(self.menubar)
        self.actionOpen.setObjectName("actionOpen")
        self.menu_File.addAction(self.actionOpen)
        _translate = QtCore.QCoreApplication.translate
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.actionOpen.setText(_translate("MainWindow", "Open Hidden Image"))
        self.actionOpen.triggered.connect(lambda: self.open_hidden_img(type))

        # get the img from main process
        self.draw_bit_plane(pcx_obj, type)
    
    def display(self, label, image_array, width, height, posx, posy):

        """
        Display image on the qt label
            posx, posy: -1 for default position (defined in DIP_GUI)
        """
        img = np.array(image_array, dtype=np.uint8)
        if img.shape[2] < 3:
            img = np.reshape(img, (img.shape[0], img.shape[1]))
            img = Image.fromarray(img, 'L')
        else:
            if label is not self.ui.palette_label:
                self.ui.color_widget.draw_color_histogram(img)
            img = Image.fromarray(img)
        qt_img = ImageQt.ImageQt(img)
        pixmap_img = QtGui.QPixmap.fromImage(qt_img).scaled(width, height)
        pixmap_img.detach()

        if posx == -1 or posy == -1:
            label.resize(width, height)
        else:
            label.setGeometry(QtCore.QRect(posx, posy, width, height))
        label.setPixmap(pixmap_img)
        label.show()
        return

    def create_label(self, posx, posy, width, height, name, text, font = 10):
        """
        Create the text label
        """
        label = imgLabel(self)
        label.setGeometry(QtCore.QRect(posx, posy, width, height))
        label.setText(text)
        label.setObjectName(name)
        label.installEventFilter(self)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setFont(QtGui.QFont('Times', font))
        label.show()

        return label

    def draw_bit_plane(self, pcx_obj, type):
        self.ori_pcx = pcx_obj
        self.mod_img_list = pcx_obj.bit_plane(type)
        self.display(self.ori_label, self.ori_pcx.gray_image, 256, 256, -1, -1)
        for i in range(0, 8):
            tmp_img = self.mod_img_list[i] * 255
            self.display(self.label_list[i], tmp_img, 256, 256, -1, -1)
        return

    def open_hidden_img(self, type):
        
        """
        Open the hidden image and replace the original image's LSB with hidden image 's LSB
            * Improved: let user choose what bit plane to replace by hidden image
        """
        filename, filepath = QFileDialog.getOpenFileName(self, 'Open Hidden Image', "./ImagePCX")

        self.hidden_pcx = PcxImage()
        self.hidden_pcx.read_from_filename(filename)
        self.hidden_pcx.decode_image()
        hidden_img_list = self.hidden_pcx.bit_plane(type)
        hidden_LSB = hidden_img_list[7] * 255
        self.display(self.label_list[0], hidden_LSB, 256, 256, -1, -1)
        self.mod_img_list[0] = hidden_img_list[7]
        merge_image, width, height = self.ori_pcx.merge_bit_plane(type, self.mod_img_list)
        self.display(self.after_label, merge_image, width, height, -1, -1)
        after_text_label = self.create_label(1200, 590, 200, 100, "after_text_label", "Merged Image")
        snr_value = self.ori_pcx.cal_snr(merge_image)
        self.snr_label.setText("SNR Value: {0} db".format(round(snr_value, 2)))
        return

class filterWindow(QMainWindow):
    def __init__(self, pcx_obj, type, parent = None):
        super(filterWindow, self).__init__(parent)

        self.setObjectName("{0}_mainwindow".format(type))
        self.setGeometry(100, 100, 1500, 800)
        self.setWindowTitle("{0}".format(type))

        self.ori_pcx = pcx_obj
        self.type = type
        self.noise_img = self.ori_pcx.gray_image

        # create label for image
        self.ori_img_label = self.create_label(100, 100, 256, 256, "ori_img_label", "")
        self.display(self.ori_img_label, self.ori_pcx.gray_image, \
            self.ori_pcx.gray_image.shape[0], self.ori_pcx.gray_image.shape[1], -1, -1)
        self.noise_img_label = self.create_label(500, 100, 256, 256, "noise_img_label", "")
        self.after_img_label = self.create_label(900, 100, 256, 256, "after_img_label", "")
        

        # create button for showing noise image and processing filter
        noise_btn = QtWidgets.QPushButton(self)
        noise_btn.setGeometry(QtCore.QRect(600, 400, 93, 28))
        noise_btn.setObjectName("noise button")
        _translate = QtCore.QCoreApplication.translate
        noise_btn.setText(_translate("MainWindow", "noise_image"))
        noise_btn.show()
        noise_btn.clicked.connect(lambda: self.show_noise())

        self.process_btn = QtWidgets.QPushButton(self)
        self.process_btn.setGeometry(QtCore.QRect(1300, 600, 93, 28))
        self.process_btn.setObjectName("process button")
        _translate = QtCore.QCoreApplication.translate
        self.process_btn.setText(_translate("MainWindow", "Process"))
        self.process_btn.show()
        self.process_btn.clicked.connect(lambda: self.process())

        # create slider label
        name = "threshold"
        slider_num = "\n0                                             255"
        thre_slider_label = self.create_label(1260, 450, 240, 100, name, name + slider_num)

        # create slider for threshold
        self.thre_slider = QtWidgets.QSlider(self)
        self.thre_slider.setGeometry(QtCore.QRect(1300, 500, 160, 22))
        self.thre_slider.setOrientation(QtCore.Qt.Horizontal)
        self.thre_slider.setObjectName("threshold_slider")
        self.thre_slider.setValue(0)
        self.thre_slider.setMinimum(0)
        self.thre_slider.setMaximum(255)
        self.thre_slider.setSingleStep(1)
        self.thre_slider.show()

        # create radio button for select the size of filter
        self.radio_button_list = dict()
        self.filter_size_btn_group = QtWidgets.QButtonGroup(self)
        self.filter_size_btn_group.setObjectName("button_group")
        for size in range(3, 8, 2):
            name = "filter_size_radio_btn_{0}".format(size) 
            self.radio_button_list[name] = self.create_radio_button(1300, 100 + (size * 20), 98, 19, \
                name, "{0} * {0}".format(size))
            self.filter_size_btn_group.addButton(self.radio_button_list[name], size)

    def show_noise(self):
        self.noise_img, width, height = self.ori_pcx.noise(self.noise_img)
        self.display(self.noise_img_label, self.noise_img, width, height, -1, -1)

        return

    def process(self):

        """
        Process the filter depend on the filter size and type
        """
        filter_size = self.filter_size_btn_group.checkedId()
        if filter_size == -1: return
        if self.type == "outlier":
            threshold = self.thre_slider.value()
            mod_img, width, height = self.ori_pcx.outlier(self.noise_img, filter_size, threshold)
            self.display(self.after_img_label, mod_img, width, height, -1, -1)
            return

    def create_label(self, posx, posy, width, height, name, text, font = 10):
        """
        Create the text label
        """
        label = imgLabel(self)
        label.setGeometry(QtCore.QRect(posx, posy, width, height))
        label.setText(text)
        label.setObjectName(name)
        label.installEventFilter(self)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setFont(QtGui.QFont('Times', font))
        label.show()

        return label

    def create_radio_button(self, posx, posy, width, height, name, text):
        radio_btn = QtWidgets.QRadioButton(self)
        radio_btn.setGeometry(QtCore.QRect(posx, posy, width, height))
        radio_btn.setObjectName(name)
        _translate = QtCore.QCoreApplication.translate
        radio_btn.setText(_translate("MainWindow", text))
        radio_btn.show()

        return radio_btn

    def display(self, label, image_array, width, height, posx, posy):

        """
        Display image on the qt label
            posx, posy: -1 for default position (defined in DIP_GUI)
        """
        img = np.array(image_array, dtype=np.uint8)
        if img.shape[2] < 3:
            img = np.reshape(img, (img.shape[0], img.shape[1]))
            img = Image.fromarray(img, 'L')
        else:
            if label is not self.ui.palette_label:
                self.ui.color_widget.draw_color_histogram(img)
            img = Image.fromarray(img)
        qt_img = ImageQt.ImageQt(img)
        pixmap_img = QtGui.QPixmap.fromImage(qt_img).scaled(width, height)
        pixmap_img.detach()

        if posx == -1 or posy == -1:
            label.resize(width, height)
        else:
            label.setGeometry(QtCore.QRect(posx, posy, width, height))
        label.setPixmap(pixmap_img)
        label.show()
        return

class functionWidgetWindow(QMainWindow):
    def __init__(self, pcx_obj, type, parent = None):
        super(functionWidgetWindow, self).__init__(parent)
        
        self.setObjectName("{0}_mainwindow".format(type))
        self.resize(1500, 800)
        self.setWindowTitle("{0}".format(type))

        self.ori_pcx = pcx_obj
        self.type = type

        # create label for ori and after image
        self.ori_img_label = self.create_label(100, 100, 256, 256, "ori_img_label", "")
        self.display(self.ori_img_label, self.ori_pcx.gray_image, \
            self.ori_pcx.gray_image.shape[0], self.ori_pcx.gray_image.shape[1], -1, -1)
        self.after_img_label = self.create_label(500, 100, 256, 256, "after_img_label", "")
        self.display(self.after_img_label, self.ori_pcx.gray_image, \
            self.ori_pcx.gray_image.shape[0], self.ori_pcx.gray_image.shape[1], -1, -1)

        # create histogram widget
        self.gray_widget = histogramWidget(self)
        self.gray_widget.setGeometry(QtCore.QRect(100, 400, 656, 400))
        self.gray_widget.setObjectName("gray_widget")
        self.gray_widget.draw_gray_histogram(self.ori_pcx.gray_image)

        # create matplotlib canvas
        if type == "contrast_stretching":
            self.function_widget = csFunctionWidget(self)
        elif type == "diminish_gls" or type == "preserve_gls":
            self.function_widget = glsFunctionWidget(type, self)
        self.function_mod_flag = False

        self.function_widget.setGeometry(QtCore.QRect(800, 100, 600, 600))
        self.function_widget.setObjectName("function_widget")
        self.function_widget.canvas.mpl_connect("button_press_event", self.func_widget_press)
        self.function_widget.canvas.mpl_connect("motion_notify_event", self.func_widget_move)

    def create_label(self, posx, posy, width, height, name, text, font = 10):
        """
        Create the text label
        """
        label = imgLabel(self)
        label.setGeometry(QtCore.QRect(posx, posy, width, height))
        label.setText(text)
        label.setObjectName(name)
        label.installEventFilter(self)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setFont(QtGui.QFont('Times', font))
        label.show()

        return label

    def display(self, label, image_array, width, height, posx, posy):

        """
        Display image on the qt label
            posx, posy: -1 for default position (defined in DIP_GUI)
        """
        img = np.array(image_array, dtype=np.uint8)
        if img.shape[2] < 3:
            img = np.reshape(img, (img.shape[0], img.shape[1]))
            img = Image.fromarray(img, 'L')
        else:
            if label is not self.ui.palette_label:
                self.ui.color_widget.draw_color_histogram(img)
            img = Image.fromarray(img)
        qt_img = ImageQt.ImageQt(img)
        pixmap_img = QtGui.QPixmap.fromImage(qt_img).scaled(width, height)
        pixmap_img.detach()

        if posx == -1 or posy == -1:
            label.resize(width, height)
        else:
            label.setGeometry(QtCore.QRect(posx, posy, width, height))
        label.setPixmap(pixmap_img)
        label.show()
        return

    def func_widget_press(self, event):
        x = int(event.xdata) if event.xdata != None else None
        y = int(event.ydata) if event.ydata != None else None
        if x is None or y is None:
            print("invalid coordinate!!")
        else:
            if self.function_mod_flag == True:
                self.function_mod_flag = False
                if self.type == "contrast_stretching":
                    mod_img, width, height = self.ori_pcx.contrast_stretching("piecewise_linear", r1 = self.function_widget.r1, \
                        s1 = self.function_widget.s1, r2 = self.function_widget.r2, s2 = self.function_widget.s2)
                elif self.type == "diminish_gls" or self.type == "preserve_gls":
                    mod_img, width, height = self.ori_pcx.gray_level_slicing(self.type, self.function_widget.r1, \
                        self.function_widget.r2, self.function_widget.mod_level)
                self.gray_widget.draw_gray_histogram(mod_img)
                self.display(self.after_img_label, mod_img, width, height, -1, -1)
                self.function_widget.get_point_flag = False
            else:
                p = self.function_widget.get_point(x, y)
                if p != 0: 
                    self.function_mod_flag = True

    def func_widget_move(self, event):
        x = int(event.xdata) if event.xdata != None else None
        y = int(event.ydata) if event.ydata != None else None
        if x is None or y is None:
            pass
        else:
            if self.function_mod_flag == True:
                # print("x = {0}, y = {1}".format(x, y))
                self.function_widget.update_line(x, y)