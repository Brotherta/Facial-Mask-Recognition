import sys

from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

from src.controller.MainController import MainController
from src.data.DataContainer import DataContainer
from src.view.window.MainWindow import MainWindow
from src.view.window.ProjectWindow import ProjectWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_purple.xml')
    data = DataContainer()
    mainWindow = MainWindow()
    projectWindow = ProjectWindow()
    controller = MainController(mainWindow, projectWindow, data)
    projectWindow.show()
    app.exec_()
