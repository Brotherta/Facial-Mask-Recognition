from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from src.view.widget.ImagesWidget import ImagesListWidget
from src.view.widget.LabelsWidget import LabelsListWidget
from src.view.widget.MenuWidget import MenuBar

MENU_CSS = 'style/style_menu.css'
TITLE = 'Image Annotator'


class MainWindow(QMainWindow):
    closeEventSignal = QtCore.pyqtSignal(QtGui.QCloseEvent)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.widget = QWidget()
        self.layout = QHBoxLayout()
        self.menuBar = MenuBar()
        self.imagesWidget = ImagesListWidget()
        self.labelsWidget = LabelsListWidget()

        self.setMinimumSize(QSize(1280, 720))

        self.layout.addWidget(self.labelsWidget)
        self.layout.addWidget(self.imagesWidget)
        self.widget.setLayout(self.layout)
        self.setMenuBar(self.menuBar)
        self.setCentralWidget(self.widget)
        self.setWindowTitle(TITLE)
        self.setWindowIcon(QIcon("assets/icon.png"))

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.closeEventSignal.emit(a0)

