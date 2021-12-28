from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from src.view.widget.ImagesWidget import ImagesListWidget
from src.view.widget.LabelsWidget import LabelsListWidget
from src.view.widget.MenuWidget import MenuBar

MENU_CSS = 'style/style_menu.css'
TITLE = 'Image Annotator'


# The main window, displaying a project
class MainWindow(QMainWindow):
    closeEventSignal = QtCore.pyqtSignal(QtGui.QCloseEvent)  # This signal is connected to the main controller

    def __init__(self):
        super(MainWindow, self).__init__()
        self.widget = QWidget()  # Main widget
        self.layout = QHBoxLayout()  # Horizontal layout
        self.menuBar = MenuBar()  # The menu bar, which will contain the import, saves and other buttons
        self.imagesWidget = ImagesListWidget()  # The images list of the project
        self.labelsWidget = LabelsListWidget()  # The labels list of the project

        self.setMinimumSize(QSize(1280, 720))

        # Adding to the layout
        self.layout.addWidget(self.labelsWidget)
        self.layout.addWidget(self.imagesWidget)
        self.widget.setLayout(self.layout)

        self.setMenuBar(self.menuBar)
        self.setCentralWidget(self.widget)
        self.setWindowTitle(TITLE)
        self.setWindowIcon(QIcon("assets/icon.png"))  # Setting the window icon

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        """ When the window is close, we catch the event and emit a signal.
            It allows use to prompt the user to save if he forgot to save some data. """
        self.closeEventSignal.emit(a0)
