from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget

from src.view.widget.images_widget import ImagesListWidget
from src.view.widget.labels_widget import LabelsListWidget
from src.view.widget.menu_widget import MenuBar

MENU_CSS = 'style/style_menu.css'
TITLE = 'Image Annotator'


class MainWindow(QMainWindow):

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

