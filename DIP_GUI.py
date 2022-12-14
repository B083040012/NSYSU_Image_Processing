# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DIP_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QKeySequence


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 1030)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.header_label = QtWidgets.QLabel(self.centralwidget)
        self.header_label.setGeometry(QtCore.QRect(800, 40, 421, 441))
        self.header_label.setText("")
        self.header_label.setObjectName("header_label")
        self.palette_label = QtWidgets.QLabel(self.centralwidget)
        self.palette_label.setGeometry(QtCore.QRect(800, 500, 96, 96))
        self.palette_label.setText("")
        self.palette_label.setObjectName("palette_label")
        self.color_widget = histogramWidget(self.centralwidget)
        self.color_widget.setGeometry(QtCore.QRect(800, 630, 421, 171))
        self.color_widget.setObjectName("color_widget")
        self.gray_widget = histogramWidget(self.centralwidget)
        self.gray_widget.setGeometry(QtCore.QRect(800, 810, 421, 161))
        self.gray_widget.setObjectName("gray_widget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1300, 26))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuFunc = QtWidgets.QMenu(self.menubar)
        self.menuFunc.setObjectName("menuFunc")
        self.menuEnlarge = QtWidgets.QMenu(self.menuFunc)
        self.menuEnlarge.setEnabled(False)
        self.menuEnlarge.setObjectName("menuEnlarge")
        self.menuEnlarge.setIcon(QIcon("./icon/process.png"))
        self.menuRotate = QtWidgets.QMenu(self.menuFunc)
        self.menuRotate.setEnabled(False)
        self.menuRotate.setObjectName("menuRotate")
        self.menuRotate.setIcon(QIcon("./icon/process.png"))
        self.menuCut = QtWidgets.QMenu(self.menuFunc)
        self.menuCut.setEnabled(False)
        self.menuCut.setObjectName("menuCut")
        self.menuCut.setIcon(QIcon("./icon/process.png"))
        self.menuThreshold = QtWidgets.QMenu(self.menuFunc)
        self.menuThreshold.setEnabled(False)
        self.menuThreshold.setObjectName("menuThreshold")
        self.menuThreshold.setIcon(QIcon("./icon/process.png"))
        self.menuLocal_Thresholding = QtWidgets.QMenu(self.menuThreshold)
        self.menuLocal_Thresholding.setEnabled(False)
        self.menuLocal_Thresholding.setObjectName("menuLocal_Thresholding")
        self.menuLocal_Thresholding.setIcon(QIcon("./icon/process.png"))
        self.menuBit_Plane = QtWidgets.QMenu(self.menuFunc)
        self.menuBit_Plane.setEnabled(False)
        self.menuBit_Plane.setObjectName("menuBit_Plane")
        self.menuBit_Plane.setIcon(QIcon("./icon/process.png"))
        self.menuContrast_Stretching = QtWidgets.QMenu(self.menuFunc)
        self.menuContrast_Stretching.setEnabled(False)
        self.menuContrast_Stretching.setObjectName("menuContrast_Stretching")
        self.menuContrast_Stretching.setIcon(QIcon("./icon/process.png"))
        self.menuChannel = QtWidgets.QMenu(self.menuFunc)
        self.menuChannel.setEnabled(False)
        self.menuChannel.setObjectName("menuChannel")
        self.menuChannel.setIcon(QIcon("./icon/process.png"))
        self.menuGray_Level_Slicing = QtWidgets.QMenu(self.menuFunc)
        self.menuGray_Level_Slicing.setEnabled(False)
        self.menuGray_Level_Slicing.setObjectName("menuGray_Level_Slicing")
        self.menuGray_Level_Slicing.setIcon(QIcon("./icon/process.png"))
        self.menuFilter = QtWidgets.QMenu(self.menuFunc)
        self.menuFilter.setEnabled(False)
        self.menuFilter.setObjectName("menuFilter")
        self.menuFilter.setIcon(QIcon("./icon/process.png"))
        self.menuAnimation = QtWidgets.QMenu(self.menubar)
        self.menuAnimation.setEnabled(True)
        self.menuAnimation.setObjectName("menuAnimation")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(QIcon("./icon/open_file.png"), "open", MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.setShortcut(QKeySequence("Ctrl+o"))
        self.actionReset = QtWidgets.QAction(QIcon("./icon/setting"), "reset", MainWindow)
        self.actionReset.setObjectName("actionReset")
        self.actionReset.setShortcut(QKeySequence("Ctrl+r"))
        self.actionSimple_Dup = QtWidgets.QAction(MainWindow)
        self.actionSimple_Dup.setCheckable(False)
        self.actionSimple_Dup.setEnabled(True)
        self.actionSimple_Dup.setObjectName("actionSimple_Dup")
        self.actionSimple_Dup.setShortcut(QKeySequence("Ctrl+Shift+s"))
        self.actionBi_Linear = QtWidgets.QAction(MainWindow)
        self.actionBi_Linear.setObjectName("actionBi_Linear")
        self.actionBi_Linear.setShortcut(QKeySequence("Ctrl+Shift+b"))
        self.actionNormal_Rotate = QtWidgets.QAction(MainWindow)
        self.actionNormal_Rotate.setObjectName("actionNormal_Rotate")
        self.actionNormal_Rotate.setShortcut("Ctrl+Shift+n")
        self.actionReverse_Rotate = QtWidgets.QAction(MainWindow)
        self.actionReverse_Rotate.setObjectName("actionReverse_Rotate")
        self.actionReverse_Rotate.setShortcut("Ctrl+Shift+r")
        self.actionShear = QtWidgets.QAction(QIcon("./icon/process.png"), "shear", MainWindow)
        self.actionShear.setEnabled(False)
        self.actionShear.setObjectName("actionShear")
        self.actionShear.setShortcut("Ctrl+s")
        self.actionRect_Cut = QtWidgets.QAction(MainWindow)
        self.actionRect_Cut.setObjectName("actionRect_Cut")
        self.actionCircle_Cut = QtWidgets.QAction(MainWindow)
        self.actionCircle_Cut.setObjectName("actionCircle_Cut")
        self.actionMagic_Wand = QtWidgets.QAction(QIcon("./icon/process.png"), "magic_wand", MainWindow)
        self.actionMagic_Wand.setEnabled(False)
        self.actionMagic_Wand.setObjectName("actionMagic_Wand")
        self.actionMagic_Wand.setShortcut("Ctrl+m")
        self.actionAlpha = QtWidgets.QAction(QIcon("./icon/process.png"), "alpha", MainWindow)
        self.actionAlpha.setEnabled(False)
        self.actionAlpha.setObjectName("actionAlpha")
        self.actionAlpha.setShortcut("Ctrl+a")
        self.actionBall = QtWidgets.QAction(QIcon("./icon/animation.png"), "ball", MainWindow)
        self.actionBall.setObjectName("actionBall")
        self.actionBall.setShortcut("Ctrl+b")
        self.actionMisaligned = QtWidgets.QAction(QIcon("./icon/process.png"), "misaligned", MainWindow)
        self.actionMisaligned.setEnabled(False)
        self.actionMisaligned.setObjectName("actionMisaligned")
        self.actionMisaligned.setShortcut("Ctrl+Shift+m")
        self.actionDithering = QtWidgets.QAction(QIcon("./icon/process.png"), "dithering", MainWindow)
        self.actionDithering.setEnabled(False)
        self.actionDithering.setObjectName("actionDithering")
        self.actionDithering.setShortcut("Ctrl+d")
        self.actionNegative = QtWidgets.QAction(QIcon("./icon/process.png"), "negative", MainWindow)
        self.actionNegative.setEnabled(False)
        self.actionNegative.setObjectName("actionNegative")
        self.actionNegative.setShortcut("Ctrl+n")
        self.actionMirror = QtWidgets.QAction(QIcon("./icon/process.png"), "mirror", MainWindow)
        self.actionMirror.setEnabled(False)
        self.actionMirror.setObjectName("actionMirror")
        self.actionMirror.setShortcut("Ctrl+i")
        self.actionLT_Mean = QtWidgets.QAction(MainWindow)
        self.actionLT_Mean.setObjectName("actionLT_Mean")
        self.actionLT_Median = QtWidgets.QAction(MainWindow)
        self.actionLT_Median.setObjectName("actionLT_Median")
        self.actionLT_Min_Max_Mean = QtWidgets.QAction(MainWindow)
        self.actionLT_Min_Max_Mean.setObjectName("actionLT_Min_Max_Mean")
        self.actionOtsu_Thresholding = QtWidgets.QAction(MainWindow)
        self.actionOtsu_Thresholding.setObjectName("actionOtsu_Thresholding")
        self.actionCustom_Thresholding = QtWidgets.QAction(MainWindow)
        self.actionCustom_Thresholding.setObjectName("actionCustom_Thresholding")
        self.actionBinary_Bit_Plane = QtWidgets.QAction(MainWindow)
        self.actionBinary_Bit_Plane.setObjectName("actionBinary_Bit_Plane")
        self.actionGray_Code_Bit_Plane = QtWidgets.QAction(MainWindow)
        self.actionGray_Code_Bit_Plane.setObjectName("actionGray_Code_Bit_Plane")
        self.actionSimple_Linear_CS = QtWidgets.QAction(MainWindow)
        self.actionSimple_Linear_CS.setObjectName("actionSimple_Linear_CS")
        self.actionPiecewise_Linear_CS = QtWidgets.QAction(MainWindow)
        self.actionPiecewise_Linear_CS.setObjectName("actionPiecewise_Linear_CS")
        self.actionChannelGray_Scale = QtWidgets.QAction(MainWindow)
        self.actionChannelGray_Scale.setObjectName("actionChannelGray_Scale")
        self.actionChannelRed = QtWidgets.QAction(MainWindow)
        self.actionChannelRed.setObjectName("actionChannelRed")
        self.actionChannelGreen = QtWidgets.QAction(MainWindow)
        self.actionChannelGreen.setObjectName("actionChannelGreen")
        self.actionChannelBlue = QtWidgets.QAction(MainWindow)
        self.actionChannelBlue.setObjectName("actionChannelBlue")
        self.actionDiminish_GLS = QtWidgets.QAction(MainWindow)
        self.actionDiminish_GLS.setObjectName("actionDiminish_GLS")
        self.actionDiminish_GLS.setShortcut("Ctrl+Shift+d")
        self.actionPreserve_GLS = QtWidgets.QAction(MainWindow)
        self.actionPreserve_GLS.setObjectName("actionPreserve_GLS")
        self.actionPreserve_GLS.setShortcut("Ctrl+Shift+p")
        self.actionOutlier = QtWidgets.QAction(MainWindow)
        self.actionOutlier.setObjectName("actionOutlier")
        self.actionMedian = QtWidgets.QAction(MainWindow)
        self.actionMedian.setObjectName("actionMedian")
        self.actionPass = QtWidgets.QAction(MainWindow)
        self.actionPass.setObjectName("actionPass")
        self.actionCris = QtWidgets.QAction(MainWindow)
        self.actionCris.setObjectName("actionCris")
        self.actionHighBoost = QtWidgets.QAction("actionHighBoost")
        self.actionHighBoost.setObjectName("actionHighBoost")
        self.actionGradient = QtWidgets.QAction(MainWindow)
        self.actionGradient.setObjectName("actionGradient")
        self.actionVideo = QtWidgets.QAction(QIcon("./icon/video.png"), "video", MainWindow)
        self.actionVideo.setObjectName("actionVideo")
        self.actionVideo.setShortcut(QKeySequence("Ctrl+v"))
        self.menu_File.addAction(self.actionOpen)
        self.menuSettings.addAction(self.actionReset)
        self.menuEnlarge.addAction(self.actionSimple_Dup)
        self.menuEnlarge.addAction(self.actionBi_Linear)
        self.menuRotate.addAction(self.actionNormal_Rotate)
        self.menuRotate.addAction(self.actionReverse_Rotate)
        self.menuCut.addAction(self.actionRect_Cut)
        self.menuCut.addAction(self.actionCircle_Cut)
        self.menuLocal_Thresholding.addAction(self.actionLT_Mean)
        self.menuLocal_Thresholding.addAction(self.actionLT_Median)
        self.menuLocal_Thresholding.addAction(self.actionLT_Min_Max_Mean)
        self.menuThreshold.addAction(self.menuLocal_Thresholding.menuAction())
        self.menuThreshold.addAction(self.actionOtsu_Thresholding)
        self.menuThreshold.addAction(self.actionCustom_Thresholding)
        self.menuBit_Plane.addAction(self.actionBinary_Bit_Plane)
        self.menuBit_Plane.addAction(self.actionGray_Code_Bit_Plane)
        self.menuContrast_Stretching.addAction(self.actionSimple_Linear_CS)
        self.menuContrast_Stretching.addAction(self.actionPiecewise_Linear_CS)
        self.menuChannel.addAction(self.actionChannelGray_Scale)
        self.menuChannel.addAction(self.actionChannelRed)
        self.menuChannel.addAction(self.actionChannelGreen)
        self.menuChannel.addAction(self.actionChannelBlue)
        self.menuGray_Level_Slicing.addAction(self.actionDiminish_GLS)
        self.menuGray_Level_Slicing.addAction(self.actionPreserve_GLS)
        self.menuFilter.addAction(self.actionOutlier)
        self.menuFilter.addAction(self.actionMedian)
        self.menuFilter.addAction(self.actionPass)
        self.menuFilter.addAction(self.actionCris)
        self.menuFilter.addAction(self.actionHighBoost)
        self.menuFilter.addAction(self.actionGradient)
        self.menuFunc.addAction(self.menuChannel.menuAction())
        self.menuFunc.addAction(self.menuEnlarge.menuAction())
        self.menuFunc.addAction(self.menuRotate.menuAction())
        self.menuFunc.addAction(self.actionShear)
        self.menuFunc.addAction(self.menuCut.menuAction())
        self.menuFunc.addAction(self.actionMagic_Wand)
        self.menuFunc.addAction(self.actionAlpha)
        self.menuFunc.addAction(self.actionMisaligned)
        self.menuFunc.addAction(self.actionDithering)
        self.menuFunc.addAction(self.actionNegative)
        self.menuFunc.addAction(self.actionMirror)
        self.menuFunc.addAction(self.menuThreshold.menuAction())
        self.menuFunc.addAction(self.menuBit_Plane.menuAction())
        self.menuFunc.addAction(self.menuContrast_Stretching.menuAction())
        self.menuFunc.addAction(self.menuGray_Level_Slicing.menuAction())
        self.menuFunc.addAction(self.menuFilter.menuAction())
        self.menuFunc.addAction(self.actionVideo)
        self.menuAnimation.addAction(self.actionBall)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuFunc.menuAction())
        self.menubar.addAction(self.menuAnimation.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuFunc.setTitle(_translate("MainWindow", "Func"))
        self.menuEnlarge.setTitle(_translate("MainWindow", "Enlarge"))
        self.menuRotate.setTitle(_translate("MainWindow", "Rotate"))
        self.menuCut.setTitle(_translate("MainWindow", "Cut"))
        self.menuThreshold.setTitle(_translate("MainWindow", "Threshold"))
        self.menuLocal_Thresholding.setTitle(_translate("MainWindow", "Local Thresholding"))
        self.menuBit_Plane.setTitle(_translate("MainWindow", "Bit Plane"))
        self.menuContrast_Stretching.setTitle(_translate("MainWindow", "Contrast Stretching"))
        self.menuChannel.setTitle(_translate("MainWindow", "Channel"))
        self.menuGray_Level_Slicing.setTitle(_translate("MainWindow", "Gray Level Slicing"))
        self.menuFilter.setTitle(_translate("MainWindow", "Filter"))
        self.menuAnimation.setTitle(_translate("MainWindow", "Animation"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionReset.setText(_translate("MainWindow", "Reset"))
        self.actionSimple_Dup.setText(_translate("MainWindow", "Simple_Dup"))
        self.actionBi_Linear.setText(_translate("MainWindow", "Bi-Linear"))
        self.actionNormal_Rotate.setText(_translate("MainWindow", "Normal_Rotate"))
        self.actionReverse_Rotate.setText(_translate("MainWindow", "Reverse_Rotate"))
        self.actionShear.setText(_translate("MainWindow", "Shear"))
        self.actionRect_Cut.setText(_translate("MainWindow", "Rect_Cut"))
        self.actionCircle_Cut.setText(_translate("MainWindow", "Circle_Cut"))
        self.actionMagic_Wand.setText(_translate("MainWindow", "Magic_Wand"))
        self.actionAlpha.setText(_translate("MainWindow", "Alpha"))
        self.actionBall.setText(_translate("MainWindow", "Ball"))
        self.actionMisaligned.setText(_translate("MainWindow", "Misaligned"))
        self.actionDithering.setText(_translate("MainWindow", "Dithering"))
        self.actionNegative.setText(_translate("MainWindow", "Negative"))
        self.actionMirror.setText(_translate("MainWindow", "Mirror"))
        self.actionLT_Mean.setText(_translate("MainWindow", "LT_Mean"))
        self.actionLT_Median.setText(_translate("MainWindow", "LT_Median"))
        self.actionLT_Min_Max_Mean.setText(_translate("MainWindow", "LT_Min_Max_Mean"))
        self.actionOtsu_Thresholding.setText(_translate("MainWindow", "Otsu Thresholding"))
        self.actionCustom_Thresholding.setText(_translate("MainWindow", "Custom Thresholding"))
        self.actionBinary_Bit_Plane.setText(_translate("MainWindow", "Binary_Bit_Plane"))
        self.actionGray_Code_Bit_Plane.setText(_translate("MainWindow", "Gray_Code_Bit_Plane"))
        self.actionSimple_Linear_CS.setText(_translate("MainWindow", "Simple Linear CS"))
        self.actionPiecewise_Linear_CS.setText(_translate("MainWindow", "Piecewise Linear CS"))
        self.actionChannelGray_Scale.setText(_translate("MainWindow", "Gray Scale"))
        self.actionChannelRed.setText(_translate("MainWindow", "Red"))
        self.actionChannelGreen.setText(_translate("MainWindow", "Green"))
        self.actionChannelBlue.setText(_translate("MainWindow", "Blue"))
        self.actionDiminish_GLS.setText(_translate("MainWindow", "Diminish"))
        self.actionPreserve_GLS.setText(_translate("MainWindow", "Preserve"))
        self.actionOutlier.setText(_translate("MainWindow", "Outlier"))
        self.actionMedian.setText(_translate("MainWindow", "Median"))
        self.actionPass.setText(_translate("MainWindow", "Low/High Pass"))
        self.actionCris.setText(_translate("MainWindow", "Edge_Crispening"))
        self.actionHighBoost.setText(_translate("MainWindow", "High_Boost"))
        self.actionGradient.setText(_translate("MainWindow", "Gradient"))
        self.actionVideo.setText(_translate("Mainwindow", "Video"))
from histogramwidget import histogramWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
