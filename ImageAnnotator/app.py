import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

from src.controller.MainController import MainController
from src.data.DataContainer import DataContainer
from src.view.window.MainWindow import MainWindow
from src.view.window.ProjectWindow import ProjectWindow

import ctypes

if __name__ == "__main__":

    # On windows, we have to register our process id in order to display or icon on the windows task bar
    if os.name == 'nt':
        myappid = 'broscant11.fmr.annotator.1'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Creating the Qt App
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/icon.png"))
    apply_stylesheet(app, theme='light_purple.xml') # Apply our custom CSS stylesheet

    # Initializing our datas
    data = DataContainer() # Will contain images, labels, boxes...
    mainWindow = MainWindow()
    projectWindow = ProjectWindow()
    controller = MainController(app, mainWindow, projectWindow, data) # MVC Pattern
    projectWindow.show()
    app.exec_()


