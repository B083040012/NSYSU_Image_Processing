import numpy as np
from time import sleep
from PIL import Image, ImageQt
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QLabel, QMainWindow, QApplication
from PyQt5.QtCore import QEvent, QThread

from myQLabel import imgLabel
from myPcxImage import PcxImage
from histogramwidget import histogramWidget
from myWidget import csFunctionWidget, glsFunctionWidget
from myVideo import mpegVideo
from myWidget import PSNR_Widget

class videoWindow(QMainWindow):
    def __init__(self, parent = None):
        super(videoWindow, self).__init__(parent)

        self.setObjectName("video_mainwindow")
        self.setGeometry(300, 100, 1000, 800)
        # self.resize(1500, 800)
        self.setWindowTitle("video MainWindow")

        """
        Menubar initialize
        """
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1500, 26))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Setting = QtWidgets.QMenu(self.menubar)
        self.menu_Setting.setObjectName("menu_Setting")
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Setting.menuAction())
        self.actionOpen = QtWidgets.QAction(self.menubar)
        self.actionOpen.setObjectName("actionOpen")
        self.actionMotionCompensation = QtWidgets.QAction(self.menubar)
        self.actionMotionCompensation.setObjectName("actionMotionCompensation")
        self.menu_File.addAction(self.actionOpen)
        self.menu_Setting.addAction(self.actionMotionCompensation)
        _translate = QtCore.QCoreApplication.translate
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.menu_Setting.setTitle(_translate("MainWindow", "Setting"))
        self.actionMotionCompensation.setText(_translate("MainWindow", "Motion Compensation"))

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        """
        Action trigger definition
        """
        self.actionOpen.triggered.connect(lambda: self.open_file())
        self.actionMotionCompensation.triggered.connect(lambda: self.set_mc_component())

        """
        Window components initialization
        """
        self.img_label_dict = dict()
        self.create_img_label(100, 100, 256, 256, "ori_display")
        self.create_img_label(500, 100, 256, 256, "new_display")
        self.create_img_label(100, 500, 256, 256, "motion_vector_display")
        self.psnr_widget = PSNR_Widget(self)
        self.psnr_widget.setGeometry(QtCore.QRect(500, 500, 256, 256))

    def open_file(self):
        try:
            filenames, filetype = QFileDialog.getOpenFileNames(self, "Open File", "./sequence/")
        except:
            return -1

        self.my_mpeg = mpegVideo()
        self.my_mpeg.read_from_filename(filenames)
        self.display(self.img_label_dict["ori_display"], self.my_mpeg.frame_list[self.my_mpeg.current_frame_index], 256, 256, -1, -1)

        """
        Show the button group
        """
        self.button_dict = dict()
        self.create_button(80, 400, 35, 20, "slow", "slow")
        self.create_button(130, 400, 35, 20, "prev", "prev")
        self.create_button(180, 400, 35, 20, "play", "play")
        self.create_button(230, 400, 35, 20, "pause", "paus")
        self.create_button(280, 400, 35, 20, "next", "next")
        self.create_button(330, 400, 35, 20, "acc", "acc")

        self.button_dict["slow"].clicked.connect(lambda: self.slow())
        self.button_dict["prev"].clicked.connect(lambda: self.prev())
        self.button_dict["play"].clicked.connect(lambda: self.play())
        self.button_dict["pause"].clicked.connect(lambda: self.pause())
        self.button_dict["next"].clicked.connect(lambda: self.next())
        self.button_dict["acc"].clicked.connect(lambda: self.acc())

        return

    def difference_coding(self):
        """
        Create label for block
        """
        self.create_img_label(400, 100, 64, 64, "matching_block")
        self.create_img_label(400, 200, 64, 64, "prev_matching_block")
        self.create_img_label(400, 300, 64, 64, "sub_motion_map")
        self.create_img_label(800, 100, 64, 64, "target_block")
        self.create_img_label(800, 200, 64, 64, "prev_target_block")
        block_size = 8
        
        return

    def set_mc_component(self):
        self.create_button(900, 300, 93, 28, "mc_process_button", "Start")
        self.button_dict["mc_process_button"].clicked.connect(lambda: self.motion_compensation())
        self.radio_button_list = dict()
        self.block_size_btn_group = QtWidgets.QButtonGroup(self)
        self.block_size_btn_group.setObjectName("button_group")
        for size in range(8, 9, 8):
            name = "block_size_radio_btn_{0}".format(size) 
            self.radio_button_list[name] = self.create_radio_button(900, 100 + (int(size / 8 - 1) * 20), 98, 19, \
                name, "{0} * {0}".format(size))
            self.block_size_btn_group.addButton(self.radio_button_list[name], size)

    def motion_compensation(self):
        """
        Create label for block
        """
        self.create_img_label(400, 100, 64, 64, "matching_block")
        self.create_img_label(400, 200, 64, 64, "prev_matching_block")
        self.create_img_label(400, 300, 64, 64, "sub_motion_map")
        self.create_img_label(800, 100, 64, 64, "target_block")
        self.create_img_label(800, 200, 64, 64, "prev_target_block")
        block_size = self.block_size_btn_group.checkedId()
        print("block_size: {0}".format(block_size))
        self.motion_vector_list = list()
        for current_frame_index in range(1, self.my_mpeg.total_frame_num):
            reference_frame  = self.my_mpeg.compress_frame_list[current_frame_index - 1]
            current_frame = self.my_mpeg.frame_list[current_frame_index]
            self.display(self.img_label_dict["ori_display"], reference_frame, 256, 256, -1, -1)
            self.display(self.img_label_dict["new_display"], current_frame, 256, 256, -1, -1)
            QApplication.processEvents()
            """
            Comparing matching and target block
            """
            width, height = current_frame.shape[0], current_frame.shape[1]
            # print("width: {0}, height: {1}".format(width, height))
            for target_x in range(0, width, block_size):
                for target_y in range(0, height, block_size):
                    print("target_x: {0}, target_y: {1}".format(target_x, target_y))
                    motion_vector_tmp = [0, 0]
                    difference = 999
                    target_block = current_frame[target_x:(target_x + block_size), target_y:(target_y + block_size)]
                    self.display(self.img_label_dict["target_block"], target_block, 64, 64, -1, -1)
                    QApplication.processEvents()
                    """
                    Paint target block
                    """
                    self.img_label_dict["new_display"].block_flag = True
                    self.img_label_dict["new_display"].block_x = target_y
                    self.img_label_dict["new_display"].block_y = target_x
                    self.update()
                    QApplication.processEvents()
                    for match_x in range(0, width - block_size):
                        for match_y in range(0, height - block_size):
                    # for match_x in range(0, 30):
                    #     for match_y in range(0, 30):
                            # print("matching_x: {0}, matching_y: {1}".format(match_x, match_y))
                            matching_block = reference_frame[match_x:(match_x + block_size), match_y:(match_y + block_size)]
                            self.display(self.img_label_dict["matching_block"], matching_block, 64, 64, -1, -1)
                            QApplication.processEvents()
                            """
                            Paint matching block
                            """
                            self.img_label_dict["ori_display"].block_flag = True
                            self.img_label_dict["ori_display"].block_x = match_y
                            self.img_label_dict["ori_display"].block_y = match_x
                            self.update()
                            QApplication.processEvents()
                            diff_tmp = abs(int(target_block.sum()) - int(matching_block.sum()))
                            if diff_tmp < difference:
                                difference = diff_tmp
                                motion_vector_tmp = [-(target_x - match_x), -(target_y - match_y)]
                                prev_matching_block = matching_block
                    # print("motion vector: {0}".format(motion_vector_tmp))
                    sub_map = self.my_mpeg.update_motion_vector_map(target_y, target_x, motion_vector_tmp)
                    self.motion_vector_list.append(motion_vector_tmp)
                    self.display(self.img_label_dict["sub_motion_map"], sub_map, 64, 64, -1, -1)
                    self.display(self.img_label_dict["motion_vector_display"], self.my_mpeg.motion_vector_map, 256, 256, -1, -1)
                    self.display(self.img_label_dict["prev_target_block"], target_block, 64, 64, -1, -1)
                    self.display(self.img_label_dict["prev_matching_block"], prev_matching_block, 64, 64, -1, -1)
                    QApplication.processEvents()   
        return

    def next_frame(self):
        self.my_mpeg.update_index("next")
        self.display(self.img_label_dict["ori_display"], self.my_mpeg.frame_list[self.my_mpeg.current_frame_index], 256, 256, -1, -1)
        self.statusbar.showMessage("frame no.{0}, fps: {1}".format(self.my_mpeg.current_frame_index, self.my_mpeg.fps))

    def prev_frame(self):
        self.my_mpeg.update_index("prev")
        self.display(self.img_label_dict["ori_display"], self.my_mpeg.frame_list[self.my_mpeg.current_frame_index], 256, 256, -1, -1)
        self.statusbar.showMessage("(*reverse) frame no.{0}, fps: {1}".format(self.my_mpeg.current_frame_index, abs(self.my_mpeg.fps)))

    def slow(self):
        self.my_mpeg.fps -= 5
        self.timer = QtCore.QTimer()
        self.timer.setInterval(int(1000 / abs(self.my_mpeg.fps)))
        if self.my_mpeg.fps >= 0:
            self.timer.timeout.connect(self.next_frame)
        else:
            self.timer.timeout.connect(self.prev_frame)
        self.timer.start()
        return

    def prev(self):
        self.prev_frame()

    def play(self):
        """
        Timer to play the video
        """
        self.timer = QtCore.QTimer()
        self.timer.setInterval(int(1000 / abs(self.my_mpeg.fps)))
        if self.my_mpeg.fps >= 0:
            self.timer.timeout.connect(self.next_frame)
        else:
            self.timer.timeout.connect(self.prev_frame)
        self.timer.start()

    def pause(self):
        self.timer.stop()

    def next(self):
        self.next_frame()

    def acc(self):
        self.my_mpeg.fps += 5
        self.timer = QtCore.QTimer()
        self.timer.setInterval(int(1000 / abs(self.my_mpeg.fps)))
        if self.my_mpeg.fps >= 0:
            self.timer.timeout.connect(self.next_frame)
        else:
            self.timer.timeout.connect(self.prev_frame)
        self.timer.start()
        return

    def display(self, label, image_array, width, height, posx, posy):

        """
        Display image on the qt label
            posx, posy: -1 for default position (defined in DIP_GUI)
        """
        # try:
        # print("size of image_array: {0}".format(image_array.shape))
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
        # except:
        #     err_msgbox("cannot diaplay the image on label", self.display.__name__)
        #     return -1
        return

    def create_img_label(self, posx, posy, width, height, name):

        """
        Create the image label
        """
        if name in self.img_label_dict:
            self.img_label_dict[name].hide()
        label = imgLabel(self)
        label.setGeometry(QtCore.QRect(posx, posy, width, height))
        label.setText("")
        label.setObjectName(name)
        label.installEventFilter(self)

        self.img_label_dict[name] = label
        return

    def create_button(self, posx, posy, width, height, name, text):

        """
        Create button
        """
        btn = QtWidgets.QPushButton(self)
        btn.setGeometry(QtCore.QRect(posx, posy, width, height))
        btn.setObjectName("pushButton")
        _translate = QtCore.QCoreApplication.translate
        btn.setText(_translate("MainWindow", text))
        btn.show()

        self.button_dict[name] = btn
        return

    def create_radio_button(self, posx, posy, width, height, name, text):
        radio_btn = QtWidgets.QRadioButton(self)
        radio_btn.setGeometry(QtCore.QRect(posx, posy, width, height))
        radio_btn.setObjectName(name)
        _translate = QtCore.QCoreApplication.translate
        radio_btn.setText(_translate("MainWindow", text))
        radio_btn.show()

        return radio_btn