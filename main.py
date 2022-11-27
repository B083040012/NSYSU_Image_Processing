from PyQt5 import QtWidgets, QtGui, QtCore
import time

from controller import MainWindowController

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    """
    Splash Screen and Progressbar
    """
    splash_img = QtGui.QPixmap('./splash_screen_img.png').scaled(900, 500)
    splash = QtWidgets.QSplashScreen(splash_img, QtCore.Qt.WindowStaysOnTopHint)
    progressBar = QtWidgets.QProgressBar(splash)
    progressBar.move(splash.pos() + QtCore.QPoint(-510, 190))
    progressBar.resize(splash.width() - 5, 20)
    # splash.setMask(splash_pix.mask())
    # add fade to splashscreen 
    # opaqueness = 0.0
    # step = 0.1
    # splash.setWindowOpacity(opaqueness)
    # while opaqueness < 1:
    #     splash.setWindowOpacity(opaqueness)
    #     time.sleep(step)
    #     opaqueness+=step
    
    
    # splash.show()
    # for i in range(0, 100):
    #     progressBar.setValue(i)
    #     t = time.time()
    #     while time.time() < t + 0.01:
    #        app.processEvents()
    # time.sleep(1)
    # splash.close()

    # show the main window
    window = MainWindowController()
    window.show()
    sys.exit(app.exec_())